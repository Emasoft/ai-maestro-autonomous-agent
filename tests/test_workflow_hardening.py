"""Guard tests for CI workflow hardening (TRDD-TVM7Q4XK + the CPV canonical merge).

These assert against the REAL workflow files on disk — no mocks, no fixtures.
They exist because the hardening is invisible at runtime until a release actually
runs: a dropped `permissions:` block or an unpinned action reintroduces the gap
silently and nothing fails until it matters.

The invariants are asserted over EVERY workflow via a glob rather than a hardcoded
list, so a workflow added later (or swapped in by `cpv standardize`, which replaced
validate.yml with ci.yml) is covered automatically instead of slipping through.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

WORKFLOWS = Path(__file__).resolve().parents[1] / ".github" / "workflows"
RELEASE = WORKFLOWS / "release.yml"
NOTIFY = WORKFLOWS / "notify-marketplace.yml"
ALL_WORKFLOWS = sorted(WORKFLOWS.glob("*.yml"))

# A pinned action reference looks like `owner/repo@<40-hex>`; a floating one ends
# in a tag such as `@v4`. Only the former survives a tag being rewritten.
SHA_PINNED = re.compile(r"^[^@\s]+@[0-9a-f]{40}$")
USES_LINE = re.compile(r"^\s*(?:-\s*)?uses:\s*(\S+)", re.MULTILINE)


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _uses_refs(path: Path) -> list[str]:
    return USES_LINE.findall(path.read_text(encoding="utf-8"))


def test_workflows_exist() -> None:
    """The workflow directory is non-empty, so the globbed guards below cannot vacuously pass."""
    assert ALL_WORKFLOWS, f"no workflows found under {WORKFLOWS}"


def test_release_workflow_declares_least_privilege_permissions() -> None:
    """release.yml pins an explicit read-only token instead of inheriting repo defaults."""
    data = _load(RELEASE)
    assert "permissions" in data, "release.yml must declare an explicit permissions block"
    assert data["permissions"] == {"contents": "read"}, (
        "the post-hoc validate gate creates nothing, so it must be contents: read only; "
        f"got {data['permissions']!r}"
    )


@pytest.mark.parametrize("path", ALL_WORKFLOWS, ids=lambda p: p.name)
def test_every_workflow_declares_top_level_permissions(path: Path) -> None:
    """Each workflow sets an explicit top-level permissions block rather than inheriting defaults."""
    data = _load(path)
    assert "permissions" in data, (
        f"{path.name} must declare top-level permissions; without it the job inherits "
        "the repository default token scope, which may be read/write"
    )


@pytest.mark.parametrize("path", ALL_WORKFLOWS, ids=lambda p: p.name)
def test_all_actions_are_sha_pinned(path: Path) -> None:
    """Every `uses:` is pinned to a full 40-hex commit SHA, so a rewritten tag cannot change it."""
    refs = _uses_refs(path)
    unpinned = [r for r in refs if not SHA_PINNED.match(r)]
    assert not unpinned, f"{path.name} has unpinned action(s): {unpinned}"


@pytest.mark.parametrize("path", ALL_WORKFLOWS, ids=lambda p: p.name)
def test_every_job_is_time_bounded(path: Path) -> None:
    """Every job sets timeout-minutes, so a hung step cannot burn the 6-hour default."""
    data = _load(path)
    missing = [name for name, job in data["jobs"].items() if "timeout-minutes" not in job]
    assert not missing, f"{path.name} job(s) without timeout-minutes: {missing}"


# The real injection vector is interpolating an ATTACKER-INFLUENCED value into a run:
# script: the expansion is textual, so a crafted PR title or branch name can close the
# surrounding quote and execute. Workflow-internal expressions (matrix.*, needs.*.result,
# runner.*) are produced by GitHub or by the workflow itself and cannot carry attacker
# text, so flagging them would be a false positive — which is exactly what a blanket
# "no ${{ }} in run" rule produced against the canonical ci.yml.
UNTRUSTED_EXPR = re.compile(
    r"\$\{\{[^}]*?\b(github\.event\b|github\.head_ref\b|inputs\.|client_payload\b)",
    re.IGNORECASE,
)

# Workflows this repo authors and controls. We hold these to the strictest form of the
# rule — zero interpolation of any kind inside run: — because there is no canon churn
# to fight here and it removes the judgement call entirely.
OWN_WORKFLOWS = [p for p in (RELEASE, NOTIFY) if p.exists()]


def _run_steps(path: Path):
    data = _load(path)
    for job_name, job in data["jobs"].items():
        for step in job.get("steps", []):
            if step.get("run"):
                yield job_name, step


@pytest.mark.parametrize("path", ALL_WORKFLOWS, ids=lambda p: p.name)
def test_no_untrusted_interpolation_inside_run_blocks(path: Path) -> None:
    """No attacker-influenced expression (github.event, head_ref, inputs) is expanded in a run: script."""
    offenders = [
        f"{path.name}:{job}:{step.get('name', '<unnamed>')}"
        for job, step in _run_steps(path)
        if UNTRUSTED_EXPR.search(step["run"])
    ]
    assert not offenders, (
        "an attacker-influenced ${{ }} value is expanded inside a run: block — this is "
        f"the Actions expression-injection vector; pass it via env instead: {offenders}"
    )


@pytest.mark.parametrize("path", OWN_WORKFLOWS, ids=lambda p: p.name)
def test_own_workflows_use_no_interpolation_in_run_blocks(path: Path) -> None:
    """The workflows this repo authors expand no `${{ }}` at all inside run: scripts."""
    offenders = [
        f"{path.name}:{job}:{step.get('name', '<unnamed>')}"
        for job, step in _run_steps(path)
        if "${{" in step["run"]
    ]
    assert not offenders, (
        f"pass values through env instead of expanding them in the script: {offenders}"
    )


def test_notify_job_is_time_bounded() -> None:
    """notify-marketplace.yml bounds its job so a hung dispatch cannot run for hours."""
    job = _load(NOTIFY)["jobs"]["notify"]
    assert 0 < int(job["timeout-minutes"]) <= 30


def test_notify_has_marketplace_pat_no_op_guard() -> None:
    """A missing optional MARKETPLACE_PAT skips the dispatch instead of failing the workflow."""
    steps = _load(NOTIFY)["jobs"]["notify"]["steps"]

    probe = [s for s in steps if s.get("id") == "pat"]
    assert probe, "expected a step with id 'pat' probing the MARKETPLACE_PAT secret"
    assert "MARKETPLACE_PAT" in (probe[0].get("env") or {}), (
        "the probe must read the secret via env, not by interpolating it into the script"
    )

    dispatch = [s for s in steps if "repository-dispatch" in str(s.get("uses", ""))]
    assert dispatch, "expected a repository-dispatch step"
    assert dispatch[0].get("if") == "steps.pat.outputs.present == 'true'", (
        "the dispatch step must be gated on the PAT probe, otherwise a missing "
        f"optional secret turns every push red; got if={dispatch[0].get('if')!r}"
    )


# ---------------------------------------------------------------------------
# Parity between the two callsites that run the SAME remote-CPV strict gate.
#
# ci.yml's `validate` job and release.yml's `validate-tag` job invoke the very
# same `uvx --from git+…@<pin> cpv-remote-validate plugin . --strict`. They had
# silently diverged: the release gate carried none of the cold-build
# affordances ci.yml documents (30-min ceiling, uv cache, integrity skip,
# repo-lint phase cap) and treated a failed uvx BUILD as a validation verdict.
# The divergence is invisible until a real tag is pushed onto a cold runner,
# which is the worst possible moment to discover it — hence these guards.
# ---------------------------------------------------------------------------

CI = WORKFLOWS / "ci.yml"


def _step_named(path: Path, job: str, needle: str) -> dict:
    for step in _load(path)["jobs"][job]["steps"]:
        if needle in str(step.get("name", "")) or needle in str(step.get("uses", "")):
            return step
    raise AssertionError(f"no step matching {needle!r} in {path.name}:{job}")


def test_release_gate_honours_the_cold_build_ceiling() -> None:
    """The release gate allows at least as long as ci.yml for the cold `uvx --from git+…` CPV build.

    That build is empirically 12-20 min on a cold runner. A ceiling inside that
    window cancels a healthy build mid-flight and reports a phantom failure on a
    tag that is actually fine.
    """
    release_cap = int(_load(RELEASE)["jobs"]["validate-tag"]["timeout-minutes"])
    ci_cap = int(_load(CI)["jobs"]["validate"]["timeout-minutes"])
    assert release_cap >= 25, (
        f"release gate timeout-minutes={release_cap} is inside the documented 12-20 min "
        "cold-build window; the documented floor is 25"
    )
    assert release_cap >= ci_cap, (
        f"the release gate ({release_cap}m) must not be tighter than ci.yml's Validate "
        f"job ({ci_cap}m) — they run the identical command"
    )


def test_release_gate_reuses_the_uv_cache() -> None:
    """The release gate enables the uv cache, so the cold CPV build is not repaid on every tag."""
    step = _step_named(RELEASE, "validate-tag", "astral-sh/setup-uv")
    assert (step.get("with") or {}).get("enable-cache") is True, (
        "without enable-cache the release gate rebuilds CPV from source on EVERY "
        "release — the exact worst case for the job's own timeout"
    )


@pytest.mark.parametrize("path", ALL_WORKFLOWS, ids=lambda p: p.name)
def test_every_checkout_disables_credential_persistence(path: Path) -> None:
    """No checkout leaves the token in .git/config (zizmor `artipacked`, issue #151)."""
    offenders = [
        f"{path.name}:{job}:{step.get('name') or step.get('uses')}"
        for job, job_body in _load(path)["jobs"].items()
        for step in job_body.get("steps", [])
        if "actions/checkout" in str(step.get("uses", ""))
        and (step.get("with") or {}).get("persist-credentials") is not False
    ]
    assert not offenders, f"checkout without persist-credentials: false: {offenders}"


def test_release_gate_carries_the_same_validator_env_as_ci() -> None:
    """The release gate sets the integrity-skip and repo-lint caps ci.yml documents."""
    env = _step_named(RELEASE, "validate-tag", "CPV strict validation gate").get("env") or {}
    assert env.get("PLUGIN_SKIP_GITHUB_INTEGRITY") == "1", (
        "a fresh-checkout runner already matches its own manifest; the live "
        "raw.githubusercontent.com fetch adds only latency and hang risk"
    )
    assert int(env.get("PLUGIN_REPO_LINT_PHASE_TIMEOUT", 0)) > 0, (
        "issue #162: without an aggregate REPO LINT cap the linter fan-out can "
        "march past the job's own timeout with orphaned children"
    )


def test_release_gate_separates_infra_failure_from_a_validation_verdict() -> None:
    """A failed uvx BUILD is reported as infra failure, not as 'someone bypassed publish.py'.

    A cold `uvx --from git+…` build that dies on a transient GitHub fetch exits 1
    or 2 — indistinguishable from a findings verdict by exit code alone. Only the
    SUMMARY line proves the validator actually ran and produced a verdict.
    """
    script = _step_named(RELEASE, "validate-tag", "CPV strict validation gate")["run"]
    assert "SUMMARY: CRITICAL=" in script, (
        "the gate must confirm a real verdict was produced before blaming the tag"
    )
    assert "FAILED TO RUN" in script, (
        "the gate must have a distinct branch for an infra/network/install failure"
    )


@pytest.mark.parametrize("path", ALL_WORKFLOWS, ids=lambda p: p.name)
def test_no_workflow_seeds_the_private_username_allowlist(path: Path) -> None:
    """No workflow sets CLAUDE_PRIVATE_USERNAMES — it is the list CPV FLAGS, not an allowlist.

    Seeding it with the PUBLIC repo owner makes CPV report every github.com/<owner>/
    URL and the owner's no-reply email as a CRITICAL private-path leak, red-lighting
    --strict CI on a repo with nothing wrong with it (claude-plugins-validation#141).
    """
    data = _load(path)
    scopes = [data.get("env") or {}]
    for job in data["jobs"].values():
        scopes.append(job.get("env") or {})
        scopes.extend((step.get("env") or {}) for step in job.get("steps", []))
    # Parsed env mappings only — a comment SAYING "do not set this" is the
    # documentation of the trap, not the trap itself.
    assert not [s for s in scopes if "CLAUDE_PRIVATE_USERNAMES" in s], (
        f"{path.name} sets CLAUDE_PRIVATE_USERNAMES; in CI there is no developer "
        "local username to protect and the public owner is public"
    )


def test_publish_emits_dependency_resolution_tag() -> None:
    """publish.py emits the `<plugin>--v<version>` tag Claude Code resolves dependencies against.

    Without it every dependent plugin installs with `no-matching-tag` and is DISABLED —
    a breakage invisible from the depending side (CPV RC-DEP-TAG-PIPELINE).
    """
    src = (Path(__file__).resolve().parents[1] / "scripts" / "publish.py").read_text(
        encoding="utf-8"
    )
    assert "_cpv_dependency_tag_name" in src, "publish.py lost the dependency-tag helper"
    assert '--v' in src and 'f"{name}--v{new_ver}"' in src, (
        "the dependency tag must use the DOUBLE-hyphen `--v` separator; the single-hyphen "
        "form does not match Claude Code's resolver prefix filter and is silently useless"
    )


def test_publish_pushes_branch_and_tags_atomically() -> None:
    """The release push is ONE `--atomic` push carrying the branch and both tags.

    Splitting it (push HEAD, then push the tags) is not all-or-nothing: run()
    sys.exit()s on failure, so a tag-push failure after a successful branch push
    leaves origin with the release COMMIT and no `vX.Y.Z` / `<plugin>--vX.Y.Z`.
    Nothing then resolves that version, and the next run bumps PAST it — so the
    skipped version is never tagged at all.
    """
    src = (Path(__file__).resolve().parents[1] / "scripts" / "publish.py").read_text(
        encoding="utf-8"
    )
    push_lines = [
        line.strip()
        for line in src.splitlines()
        if '"git", "push"' in line and "origin" in line
    ]
    assert len(push_lines) == 1, (
        "expected exactly ONE release push; a second `git push origin ...` re-splits "
        f"the atomic push and reintroduces the half-published state. Got: {push_lines}"
    )
    assert '"--atomic"' in push_lines[0], (
        f"the release push must pass --atomic so the remote takes all refs or none; got {push_lines[0]}"
    )
    for ref in ('"HEAD"', 'f"v{new_version}"', "*dep_refs"):
        assert ref in push_lines[0], f"the atomic push lost {ref}; got {push_lines[0]}"

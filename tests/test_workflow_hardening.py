"""Guard tests for the CI workflow hardening ported from canon (TRDD-TVM7Q4XK).

These assert against the REAL workflow files on disk — no mocks, no fixtures.
They exist because the hardening is invisible at runtime until a release actually
runs: a dropped `permissions:` block or an unpinned action reintroduces the gap
silently and nothing fails until it matters.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

WORKFLOWS = Path(__file__).resolve().parents[1] / ".github" / "workflows"
RELEASE = WORKFLOWS / "release.yml"
NOTIFY = WORKFLOWS / "notify-marketplace.yml"

# A pinned action reference looks like `owner/repo@<40-hex>`; a floating one ends
# in a tag such as `@v4`. Only the former survives a tag being rewritten.
SHA_PINNED = re.compile(r"^[^@\s]+@[0-9a-f]{40}$")
USES_LINE = re.compile(r"^\s*(?:-\s*)?uses:\s*(\S+)", re.MULTILINE)


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _uses_refs(path: Path) -> list[str]:
    return USES_LINE.findall(path.read_text(encoding="utf-8"))


def test_release_workflow_declares_least_privilege_permissions() -> None:
    """release.yml pins an explicit read-only token instead of inheriting repo defaults."""
    data = _load(RELEASE)
    assert "permissions" in data, "release.yml must declare an explicit permissions block"
    assert data["permissions"] == {"contents": "read"}, (
        "the post-hoc validate gate creates nothing, so it must be contents: read only; "
        f"got {data['permissions']!r}"
    )


def test_all_actions_are_sha_pinned() -> None:
    """Every `uses:` in both workflows is pinned to a full 40-hex commit SHA, not a tag."""
    for path in (RELEASE, NOTIFY):
        refs = _uses_refs(path)
        assert refs, f"expected at least one `uses:` in {path.name}"
        unpinned = [r for r in refs if not SHA_PINNED.match(r)]
        assert not unpinned, f"{path.name} has unpinned action(s): {unpinned}"


def test_notify_job_is_time_bounded() -> None:
    """notify-marketplace.yml bounds its job so a hung dispatch cannot run for hours."""
    data = _load(NOTIFY)
    job = data["jobs"]["notify"]
    assert "timeout-minutes" in job, "notify job must set timeout-minutes"
    assert 0 < int(job["timeout-minutes"]) <= 30


def test_notify_has_marketplace_pat_no_op_guard() -> None:
    """A missing optional MARKETPLACE_PAT skips the dispatch instead of failing the workflow."""
    data = _load(NOTIFY)
    steps = data["jobs"]["notify"]["steps"]

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


def test_no_expression_interpolation_inside_run_blocks() -> None:
    """No `${{ }}` expansion appears inside any `run:` script (expression-injection vector)."""
    offenders: list[str] = []
    for path in (RELEASE, NOTIFY):
        data = _load(path)
        for job_name, job in data["jobs"].items():
            for step in job.get("steps", []):
                script = step.get("run")
                if script and "${{" in script:
                    offenders.append(f"{path.name}:{job_name}:{step.get('name', '<unnamed>')}")
    assert not offenders, (
        "`${{ }}` inside a run: block is textual substitution and is the standard "
        f"Actions injection vector — pass values through env instead: {offenders}"
    )

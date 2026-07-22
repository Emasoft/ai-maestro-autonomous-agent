"""Guard tests for interrupted-publish recovery in scripts/publish.py (pipeline-migration §4).

A publish performs four irreversible acts — bump, commit, tag, push — and only the
push is atomic. When the push fails, the working copy is already AT the new version,
committed and tagged, while origin is one release behind. publish.py used to read the
LOCAL version as its bump baseline, so the next run produced N+2 and the
tagged-but-unpushed N+1 was skipped forever. Nothing resolves that version for any
dependent plugin, and no error is ever printed. CPV's own pipeline hit this shipping
v2.64.0.

The helper tests below drive REAL git repositories (real init, real commits, real
tags, a real bare remote) — no mocks, because the whole point is what git actually
reports. The wiring tests assert the three skips are actually called from the release
path, since a helper nothing calls fixes nothing.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import publish  # noqa: E402  (path insert above must run first)

PUBLISH_SRC = (SCRIPTS / "publish.py").read_text(encoding="utf-8")


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, timeout=30)


def _write_version(repo: Path, version: str) -> None:
    manifest = repo / ".claude-plugin" / "plugin.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps({"name": "demo", "version": version}), encoding="utf-8")


@pytest.fixture
def published_repo(tmp_path: Path) -> Path:
    """A real repo at v1.0.0 with that version already pushed to a real bare origin/main."""
    remote = tmp_path / "origin.git"
    subprocess.run(["git", "init", "--bare", "-b", "main", str(remote)], check=True,
                   capture_output=True, timeout=30)

    repo = tmp_path / "work"
    repo.mkdir()
    _git(repo, "init", "-b", "main")
    _git(repo, "config", "user.name", "Test")
    _git(repo, "config", "user.email", "test@example.invalid")
    _write_version(repo, "1.0.0")
    _git(repo, "add", ".claude-plugin/plugin.json")
    _git(repo, "commit", "-m", "chore(release): v1.0.0")
    _git(repo, "remote", "add", "origin", str(remote))
    _git(repo, "push", "origin", "main")
    return repo


def _interrupt(repo: Path, version: str) -> None:
    """Reproduce the exact interrupted state: bumped + committed + tagged, never pushed."""
    _write_version(repo, version)
    _git(repo, "add", ".claude-plugin/plugin.json")
    _git(repo, "commit", "-m", f"chore(release): v{version}")
    _git(repo, "tag", "-a", f"v{version}", "-m", f"v{version}")


# ── the baseline: origin, never the working copy ─────────────────────────────


def test_remote_version_ignores_the_bumped_working_copy(published_repo: Path) -> None:
    """After an interrupted publish the baseline is origin's 1.0.0, not the local 1.0.1."""
    _interrupt(published_repo, "1.0.1")
    assert publish._read_remote_version(published_repo, "main") == "1.0.0"


def test_resume_is_detected_instead_of_double_bumping(published_repo: Path) -> None:
    """The interrupted state resolves to a RESUME of 1.0.1 — never a bump to 1.0.2."""
    _interrupt(published_repo, "1.0.1")
    remote = publish._read_remote_version(published_repo, "main")
    local = json.loads((published_repo / ".claude-plugin" / "plugin.json").read_text())["version"]

    assert remote is not None and remote != local, "expected a diverged working copy"
    assert publish.bump_semver(remote, "patch") == local, (
        "local must be exactly one patch ahead of origin, which is what marks a resume"
    )
    assert publish.bump_semver(local, "patch") == "1.0.2", (
        "bumping from the LOCAL value is the bug: it skips 1.0.1 permanently"
    )


def test_clean_state_is_not_mistaken_for_a_resume(published_repo: Path) -> None:
    """On the happy path local == origin, so the normal bump still applies."""
    remote = publish._read_remote_version(published_repo, "main")
    assert remote == "1.0.0"
    assert publish.bump_semver(remote, "minor") == "1.1.0"


def test_remote_version_is_none_without_an_origin(tmp_path: Path) -> None:
    """No origin (first publish / offline / shallow clone) falls back to the local value."""
    repo = tmp_path / "solo"
    repo.mkdir()
    _git(repo, "init", "-b", "main")
    _git(repo, "config", "user.name", "Test")
    _git(repo, "config", "user.email", "test@example.invalid")
    _write_version(repo, "1.0.0")
    _git(repo, "add", ".claude-plugin/plugin.json")
    _git(repo, "commit", "-m", "init")
    assert publish._read_remote_version(repo, "main") is None


def test_remote_version_is_none_when_the_manifest_is_unparseable(published_repo: Path) -> None:
    """A corrupt manifest on origin fails CLOSED rather than yielding a junk baseline."""
    (published_repo / ".claude-plugin" / "plugin.json").write_text("{not json", encoding="utf-8")
    _git(published_repo, "add", ".claude-plugin/plugin.json")
    _git(published_repo, "commit", "-m", "break it")
    _git(published_repo, "push", "origin", "main")
    assert publish._read_remote_version(published_repo, "main") is None


# ── the three "already done" probes ───────────────────────────────────────────


def test_local_tag_exists_sees_the_interrupted_runs_tag(published_repo: Path) -> None:
    """`git tag -a` is a hard error on an existing tag, so a resume must detect it first."""
    assert publish._local_tag_exists(published_repo, "v1.0.1") is False
    _interrupt(published_repo, "1.0.1")
    assert publish._local_tag_exists(published_repo, "v1.0.1") is True


def test_head_commit_message_returns_the_subject(published_repo: Path) -> None:
    """The commit skip keys off HEAD's subject, so it must be read exactly."""
    assert publish._head_commit_message(published_repo) == "chore(release): v1.0.0"


def test_porcelain_clean_tracks_the_working_tree(published_repo: Path) -> None:
    """A dirty tree must never read as clean — the commit skip depends on it."""
    assert publish._git_porcelain_clean(published_repo) is True
    (published_repo / "scratch.txt").write_text("x", encoding="utf-8")
    assert publish._git_porcelain_clean(published_repo) is False


def test_helpers_fail_closed_outside_a_repository(tmp_path: Path) -> None:
    """Every probe degrades to 'not done yet', so a git failure can never fake a skip."""
    assert publish._read_remote_version(tmp_path, "main") is None
    assert publish._local_tag_exists(tmp_path, "v1.0.0") is False
    assert publish._head_commit_message(tmp_path) == ""
    assert publish._git_porcelain_clean(tmp_path) is False


# ── wiring: a helper nothing calls fixes nothing ─────────────────────────────


def test_release_path_takes_its_baseline_from_origin() -> None:
    """main() reads origin's version before computing the bump."""
    assert "_read_remote_version(plugin_root, default_branch)" in PUBLISH_SRC, (
        "the bump baseline must come from origin; reading only the local "
        "plugin.json is what double-bumps after an interrupted publish"
    )


def test_release_path_skips_an_already_made_release_commit() -> None:
    """The commit step is guarded by HEAD-subject + clean-tree probes."""
    assert "_head_commit_message(git_root) == release_subject" in PUBLISH_SRC
    assert "_git_porcelain_clean(git_root)" in PUBLISH_SRC


def test_release_path_skips_an_already_created_tag() -> None:
    """The tag step is guarded, otherwise a resumed run dies on `git tag -a`."""
    assert '_local_tag_exists(git_root, f"v{new_version}")' in PUBLISH_SRC


def test_push_is_never_skipped() -> None:
    """The push always runs — it is the one act the interruption left undone."""
    push_lines = [
        line for line in PUBLISH_SRC.splitlines()
        if '"git", "push"' in line and "origin" in line
    ]
    assert len(push_lines) == 1, f"expected exactly one release push, got {push_lines}"
    indent = len(push_lines[0]) - len(push_lines[0].lstrip())
    assert indent == 4, (
        "the push sits at the release path's top level; indenting it under an "
        f"`if` would make the one non-idempotent act skippable (indent={indent})"
    )


def test_release_baseline_is_refreshed_before_it_is_read() -> None:
    """The origin baseline is fetched before use, so the resume guard cannot read a stale ref.

    `_read_remote_version` resolves `origin/<branch>` — a LOCAL tracking ref, only as
    fresh as the last fetch (this clone's was 36 days stale when the guard landed).
    Without a refresh the guard silently bumps onto an already-published version, and
    the push fails only AFTER bump+commit+tag — the exact dirty state it exists to
    prevent. The fetch must therefore precede the read at the call site.
    """
    src = (Path(__file__).resolve().parents[1] / "scripts" / "publish.py").read_text(
        encoding="utf-8"
    )
    assert "def _refresh_remote_ref(" in src, "the baseline refresh helper went missing"
    assert '"fetch"' in src, "_refresh_remote_ref must actually fetch"

    refresh_at = src.index("_refresh_remote_ref(plugin_root")
    read_at = src.index("_read_remote_version(plugin_root")
    assert refresh_at < read_at, (
        "the refresh must run BEFORE the baseline is read; reading first makes the "
        "fetch pointless for this release"
    )

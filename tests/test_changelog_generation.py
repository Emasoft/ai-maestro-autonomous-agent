"""Guard tests for CHANGELOG generation (TRDD-R3JRZURT).

Two real defects lived here for 18 releases and neither failed anything:

B1 — `run_git_cliff`'s CHANGELOG call passed `--unreleased` alongside `-o`, so the
     overwrite regenerated the file latest-version-only. 17 of 18 releases were absent
     while the function's own docstring claimed full tag history.
B2 — the git-cliff `body` template indented `## [x.y.z]` by 4 spaces, so CommonMark
     rendered the version heading as an indented CODE BLOCK rather than a heading.

Both are invisible to a normal test run — the pipeline exits 0 either way — so these
assert on the generator source and on the produced artifact directly. No mocks.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PUBLISH = ROOT / "scripts" / "publish.py"
CLIFF_TOML = ROOT / "cliff.toml"
CHANGELOG = ROOT / "CHANGELOG.md"

# A markdown heading or bullet emitted with leading spaces renders as an indented
# code block instead of a heading/list — this is exactly defect B2.
INDENTED_MD = re.compile(r"^ +(#{2,3} |- )", re.MULTILINE)


def _cliff_argv_blocks(src: str) -> list[str]:
    """Every argv list literal in publish.py that invokes git-cliff."""
    return re.findall(r'\[\s*\n\s*"git-cliff",(.*?)\]', src, re.DOTALL)


def test_changelog_call_walks_full_history_not_unreleased_only() -> None:
    """The CHANGELOG-generating git-cliff call omits --unreleased (B1), so it walks all tags."""
    blocks = _cliff_argv_blocks(PUBLISH.read_text(encoding="utf-8"))
    generation = [b for b in blocks if "CHANGELOG.md" in b]
    assert len(generation) == 1, f"expected exactly one CHANGELOG-writing git-cliff call, got {len(generation)}"
    assert "--unreleased" not in generation[0], (
        "--unreleased combined with -o overwrites CHANGELOG.md with only the newest "
        "section, silently dropping every earlier release (TRDD-R3JRZURT B1)"
    )


def test_release_notes_call_keeps_unreleased() -> None:
    """The release-notes git-cliff call still passes --unreleased — it is meant to be latest-only."""
    blocks = _cliff_argv_blocks(PUBLISH.read_text(encoding="utf-8"))
    notes = [b for b in blocks if "--strip" in b]
    assert len(notes) == 1, f"expected exactly one release-notes git-cliff call, got {len(notes)}"
    assert "--unreleased" in notes[0], (
        "GitHub release notes are intentionally latest-only; removing --unreleased here "
        "would dump the entire changelog into every release"
    )


@pytest.mark.parametrize(
    "path", [CLIFF_TOML, PUBLISH], ids=["cliff.toml", "publish.py-embedded-default"]
)
def test_body_template_emits_unindented_markdown(path: Path) -> None:
    """Neither copy of the git-cliff body template indents a heading or bullet (B2).

    The template lives in TWO places that must stay in sync: the committed cliff.toml
    and the default embedded in publish.py::ensure_cliff_config, which a fresh checkout
    regenerates from. Fixing only one leaves the bug latent.
    """
    text = path.read_text(encoding="utf-8")
    body = re.search(r'body = """(.*?)"""', text, re.DOTALL)
    assert body, f"could not locate the git-cliff body template in {path.name}"
    offenders = INDENTED_MD.findall(body.group(1))
    assert not offenders, (
        f"{path.name}'s body template emits indented markdown {offenders} — a leading-space "
        "'## [x.y.z]' renders as an indented code block, not a version heading"
    )


def test_changelog_artifact_documents_full_history() -> None:
    """The committed CHANGELOG.md contains every release, not just the newest one."""
    text = CHANGELOG.read_text(encoding="utf-8")
    sections = re.findall(r"^## \[", text, re.MULTILINE)
    assert len(sections) > 1, (
        f"CHANGELOG.md has {len(sections)} version section(s); the file's own header "
        "promises 'all notable changes', so a single section means B1 has regressed"
    )


def test_changelog_artifact_has_no_indented_markdown() -> None:
    """The committed CHANGELOG.md renders headings as headings, not as indented code."""
    offenders = INDENTED_MD.findall(CHANGELOG.read_text(encoding="utf-8"))
    assert not offenders, f"CHANGELOG.md contains indented markdown {offenders} — B2 has regressed"

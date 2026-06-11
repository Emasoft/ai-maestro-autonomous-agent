"""Real (no-mock) structural tests for every shipped skill.

A doc-skill's contract is its frontmatter + the files it links. These tests assert
each SKILL.md has a description and that every `references/<file>` link resolves —
the same shape CPV's validate_skill.py enforces, but pinned here so a broken link
fails the plugin's own suite immediately.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

EXPECTED_SKILLS = {
    "ai-maestro-autonomous-governance",
    "ai-maestro-autonomous-workspace-isolation",
    "ai-maestro-autonomous-prrd-trdd-kanban",
    "autonomous-memory-recall",
    "autonomous-memory-write",
}


def _skill_dirs() -> list[Path]:
    return [d for d in SKILLS_DIR.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]


def test_all_expected_skills_present() -> None:
    """The five bundled skills each have a SKILL.md."""
    found = {d.name for d in _skill_dirs()}
    assert EXPECTED_SKILLS <= found, f"missing skills: {EXPECTED_SKILLS - found}"


def test_every_skill_has_nonempty_description() -> None:
    """Every SKILL.md frontmatter declares a non-empty description (CPV triggering surface)."""
    for skill in _skill_dirs():
        text = (skill / "SKILL.md").read_text(encoding="utf-8")
        fm = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        assert fm, f"{skill.name}: no YAML frontmatter block"
        block = fm.group(1)
        m = re.search(r"^description:\s*(.*)$", block, re.MULTILINE)
        assert m, f"{skill.name}: no description: key"
        # description value is on the same line, or folded (`>`) onto indented lines below
        inline = m.group(1).strip().strip(">|").strip().strip('"')
        folded = re.search(r"^description:\s*[>|]\s*\n((?:\s+\S.*\n)+)", block, re.MULTILINE)
        assert inline or folded, f"{skill.name}: description is empty"


def test_every_reference_link_resolves() -> None:
    """Every `references/<file>` link in a SKILL.md points at a file that exists."""
    broken: list[str] = []
    for skill in _skill_dirs():
        text = (skill / "SKILL.md").read_text(encoding="utf-8")
        for rel in re.findall(r"\]\((references/[^)#]+)", text):
            target = skill / rel
            if not target.exists():
                broken.append(f"{skill.name}: {rel}")
    assert not broken, f"broken references: {broken}"


def test_governance_skill_links_amp_templates_and_questions() -> None:
    """The governance skill links both its questions.md and the new amp-templates.md, and both exist."""
    gov = SKILLS_DIR / "ai-maestro-autonomous-governance"
    text = (gov / "SKILL.md").read_text(encoding="utf-8")
    assert "references/questions.md" in text
    assert "references/amp-templates.md" in text
    assert (gov / "references" / "questions.md").exists()
    assert (gov / "references" / "amp-templates.md").exists()

"""Real (no-mock) tests for scripts/memory_note_write.py — schema, index line, overwrite guard."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "memory_note_write.py"

VALID_TYPES = {"user", "feedback", "project", "reference"}


def run_write(memdir: Path, *extra: str, body: str = "The one durable fact.") -> subprocess.CompletedProcess[str]:
    """Invoke memory_note_write.py exactly as the skill documents it."""
    args = [
        sys.executable,
        str(SCRIPT),
        "--memdir",
        str(memdir),
        "--name",
        "publish-skips-uv-lock",
        "--description",
        "release commit shipped a stale lockfile — why was uv.lock missing",
        "--type",
        "project",
        "--body",
        body,
        *extra,
    ]
    return subprocess.run(args, capture_output=True, text=True, check=False)


def parse_frontmatter(note: Path) -> dict:
    """Extract and parse the YAML frontmatter of a note file."""
    text = note.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    assert match, f"no frontmatter block in {note}"
    data = yaml.safe_load(match.group(1))
    assert isinstance(data, dict)
    return data


def test_write_creates_schema_valid_note(tmp_path: Path) -> None:
    """A write produces a note whose frontmatter has name/description/metadata per the schema."""
    result = run_write(tmp_path)
    assert result.returncode == 0, result.stderr
    note = tmp_path / "publish-skips-uv-lock.md"
    assert note.exists()
    assert result.stdout.strip() == str(note.resolve()), "script must print exactly the note path"
    data = parse_frontmatter(note)
    assert data["name"] == "publish-skips-uv-lock"
    assert "stale lockfile" in data["description"]
    assert data["metadata"]["node_type"] == "memory"
    assert data["metadata"]["type"] in VALID_TYPES
    assert "The one durable fact." in note.read_text(encoding="utf-8")


def test_write_appends_memory_index_line(tmp_path: Path) -> None:
    """A write appends one de-duplicated `- [Title](name.md) — hook` line to MEMORY.md."""
    assert run_write(tmp_path).returncode == 0
    index = (tmp_path / "MEMORY.md").read_text(encoding="utf-8")
    assert index.count("(publish-skips-uv-lock.md)") == 1
    assert re.search(r"^- \[.+\]\(publish-skips-uv-lock\.md\) — .+$", index, re.MULTILINE)
    # A second write with --update must refresh, not duplicate, the index line.
    assert run_write(tmp_path, "--update").returncode == 0
    index2 = (tmp_path / "MEMORY.md").read_text(encoding="utf-8")
    assert index2.count("(publish-skips-uv-lock.md)") == 1


def test_write_refuses_overwrite_without_update(tmp_path: Path) -> None:
    """Writing the same note slug twice without --update fails with exit code 2."""
    assert run_write(tmp_path).returncode == 0
    result = run_write(tmp_path, body="A different fact that must NOT overwrite silently.")
    assert result.returncode == 2
    assert "already exists" in result.stderr
    assert "The one durable fact." in (tmp_path / "publish-skips-uv-lock.md").read_text(encoding="utf-8")


def test_write_update_flag_overwrites(tmp_path: Path) -> None:
    """With --update, the note body is replaced and the note still verifies against the schema."""
    assert run_write(tmp_path).returncode == 0
    result = run_write(tmp_path, "--update", body="Corrected fact, second revision.")
    assert result.returncode == 0, result.stderr
    text = (tmp_path / "publish-skips-uv-lock.md").read_text(encoding="utf-8")
    assert "Corrected fact, second revision." in text
    assert "The one durable fact." not in text


def test_write_rejects_bad_slug_and_empty_body(tmp_path: Path) -> None:
    """Non-kebab slugs and empty bodies are rejected before anything is written (fail-fast)."""
    bad_slug = subprocess.run(
        [sys.executable, str(SCRIPT), "--memdir", str(tmp_path), "--name", "Not_Kebab", "--description", "d", "--type", "project", "--body", "x"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert bad_slug.returncode != 0
    assert "kebab-case" in bad_slug.stderr
    empty_body = run_write(tmp_path / "sub", body="   ")
    assert empty_body.returncode != 0
    assert "body is empty" in empty_body.stderr
    assert not (tmp_path / "sub" / "publish-skips-uv-lock.md").exists()

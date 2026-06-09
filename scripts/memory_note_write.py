#!/usr/bin/env python3
"""memory_note_write.py — write a schema-valid markdown memory note + MEMORY.md index line.

Usage:
    uv run python scripts/memory_note_write.py \
        --memdir DIR --name kebab-slug --description "symptom surface" \
        --type project [--title "Human Title"] [--hook "index hook"] \
        [--body "the fact"] [--update]

Behavior (fail-fast, atomic):
- Validates the note schema BEFORE writing: kebab-case name, non-empty
  symptom description, type in {user, feedback, project, reference}.
- Refuses to overwrite an existing note unless --update is given (exit 2).
- Writes the note atomically (tmp file + os.replace) as:
      ---
      name: <name>
      description: "<description>"
      metadata:
        node_type: memory
        type: <type>
      ---
      <body>
- Appends one index line to MEMORY.md (`- [Title](<name>.md) — <hook>`),
  creating MEMORY.md if missing and de-duplicating by note filename.
- Re-reads the written note and verifies the frontmatter parses back with the
  required keys — the script never reports success on an unverified write.
- Prints exactly one line on success: the absolute note path.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path

import yaml

VALID_TYPES = {"user", "feedback", "project", "reference"}
KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def fail(msg: str, code: int = 1) -> None:
    """Print an error to stderr and exit non-zero (fail-fast, no fallbacks)."""
    print(f"memory_note_write: error: {msg}", file=sys.stderr)
    sys.exit(code)


def build_note(name: str, description: str, note_type: str, body: str) -> str:
    """Render the note file content with schema-valid YAML frontmatter."""
    frontmatter = {
        "name": name,
        "description": description,
        "metadata": {"node_type": "memory", "type": note_type},
    }
    yaml_text = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True, width=100).rstrip("\n")
    return f"---\n{yaml_text}\n---\n\n{body.rstrip()}\n"


def atomic_write(path: Path, content: str) -> None:
    """Write content to path atomically (tmp file in same dir + os.replace)."""
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(content)
        os.replace(tmp, path)
    except BaseException:
        # The tmp file is an incomplete artifact of THIS run — removing it on
        # failure is required so a crashed write never leaves half a note.
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def verify_note(path: Path) -> None:
    """Re-read the written note and assert the frontmatter schema round-trips."""
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail(f"verification failed: no frontmatter block in {path}")
        return
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        fail(f"verification failed: frontmatter is not a mapping in {path}")
        return
    if not data.get("name") or not data.get("description"):
        fail(f"verification failed: missing name/description in {path}")
    metadata = data.get("metadata")
    if not isinstance(metadata, dict) or metadata.get("node_type") != "memory" or metadata.get("type") not in VALID_TYPES:
        fail(f"verification failed: bad metadata block in {path}")


def update_index(memdir: Path, name: str, title: str, hook: str) -> None:
    """Append the note's index line to MEMORY.md, de-duplicated by filename."""
    index = memdir / "MEMORY.md"
    line = f"- [{title}]({name}.md) — {hook}"
    if index.exists():
        existing = index.read_text(encoding="utf-8")
        if f"({name}.md)" in existing:
            # Replace the stale line for this note instead of duplicating it.
            kept = [ln for ln in existing.splitlines() if f"({name}.md)" not in ln]
            content = "\n".join(kept).rstrip("\n")
            content = (content + "\n" if content else "") + line + "\n"
        else:
            content = existing.rstrip("\n") + ("\n" if existing.strip() else "") + line + "\n"
    else:
        content = f"# Memory index\n\n{line}\n"
    atomic_write(index, content)


def main() -> None:
    parser = argparse.ArgumentParser(description="Write a schema-valid markdown memory note.")
    parser.add_argument("--memdir", required=True, help="memory directory (created if missing)")
    parser.add_argument("--name", required=True, help="kebab-case note slug (== filename stem)")
    parser.add_argument("--description", required=True, help="symptom-surface description (the recall field)")
    parser.add_argument("--type", required=True, dest="note_type", choices=sorted(VALID_TYPES), help="note type")
    parser.add_argument("--title", default=None, help="human title for the MEMORY.md index (default: name, humanized)")
    parser.add_argument("--hook", default=None, help="one-line index hook (default: the description)")
    parser.add_argument("--body", default=None, help="note body — the one fact (default: read from stdin)")
    parser.add_argument("--update", action="store_true", help="allow overwriting an existing note")
    args = parser.parse_args()

    if not KEBAB_RE.match(args.name):
        fail(f"--name must be kebab-case (got {args.name!r})")
    if not args.description.strip():
        fail("--description must be a non-empty symptom surface")

    body = args.body if args.body is not None else sys.stdin.read()
    if not body.strip():
        fail("note body is empty (pass --body or pipe it on stdin)")

    memdir = Path(args.memdir).expanduser()
    memdir.mkdir(parents=True, exist_ok=True)

    note_path = memdir / f"{args.name}.md"
    if note_path.exists() and not args.update:
        fail(f"note already exists: {note_path} (pass --update to overwrite)", code=2)

    title = args.title or args.name.replace("-", " ").capitalize()
    hook = args.hook or args.description.strip()

    atomic_write(note_path, build_note(args.name, args.description.strip(), args.note_type, body))
    verify_note(note_path)
    update_index(memdir, args.name, title, hook)
    print(note_path.resolve())


if __name__ == "__main__":
    main()

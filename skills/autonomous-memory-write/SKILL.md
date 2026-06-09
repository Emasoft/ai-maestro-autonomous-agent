---
description: >
  Use when an AUTONOMOUS agent has learned a durable fact worth remembering
  across sessions — an operational gotcha, a solved recurring alert, a
  project decision, user feedback. Trigger with "remember this", "save this
  to memory", "write a memory note", or after solving a problem recall could
  not answer. Writes a schema-valid, symptom-indexed markdown note plus its
  MEMORY.md index line.
allowed-tools: "Bash, Read, Grep, Glob"
---

# Autonomous Memory Write — capture a durable fact

Capture ONE durable fact as a symptom-indexed markdown note, per
`rules/memory-protocol.md`, so the next autonomous cycle recalls it instead
of re-deriving it.

## Overview

Wraps `scripts/memory_note_write.py`: validates the note schema (kebab-case
`name`, symptom-surface `description`, `metadata.node_type: memory`,
`metadata.type` ∈ user|feedback|project|reference), writes the note
atomically, verifies it round-trips, and appends the note's de-duplicated
index line — a markdown link to the note file plus a one-line hook — to
`MEMORY.md`.

## Prerequisites

- The `ai-maestro-autonomous-agent` plugin is installed
  (`$CLAUDE_PLUGIN_ROOT` resolves) and `uv` is available.
- You know the project memory dir:
  `$HOME/.claude/projects/<project-slug>/memory` (slug = absolute project
  path with `/` → `-`).

## Instructions

1. **Index by the QUESTION, not the answer**: put the SYMPTOM vocabulary
   (the user's words, the alert/error text) in `--description`; put the
   answer in the body. A note findable only by its solution's jargon is a
   dead note.
2. Check for an existing note that already covers the fact
   (`autonomous-memory-recall`); prefer updating it (`--update`) over
   creating a near-duplicate.
3. Write the note:

   ```bash
   uv run python "$CLAUDE_PLUGIN_ROOT/scripts/memory_note_write.py" \
     --memdir "$MEMDIR" --name short-kebab-slug \
     --description "symptom words a future session will actually have" \
     --type project --body "the one fact; Why:/How to apply: for feedback"
   ```

4. One fact per note. For `feedback`/`project` notes include **Why:** and
   **How to apply:** lines in the body.

## Output

On success the script prints exactly one line — the absolute note path —
and `MEMORY.md` in the memory dir gains (or refreshes) the note's index
line.

## Error Handling

- Exit 2 = the note already exists: re-run with `--update` only if you mean
  to replace it; otherwise pick a new slug.
- Any other non-zero exit = validation or I/O failure (bad slug, empty
  description/body, unwritable dir) — fix the input; the script never
  leaves a half-written note (atomic write + post-write verification).

## Examples

```text
User: good catch — remember that our publish step must never skip uv.lock.
Agent: writes note publish-skips-uv-lock with description "release commit
shipped a stale lockfile — why was uv.lock missing from the publish commit"
and the rule in the body, then confirms the note path.
```

## Resources

- `scripts/memory_note_write.py` — the validating, atomic note writer.
- `rules/memory-protocol.md` — note schema and the index-by-symptom law.
- `autonomous-memory-recall` — the companion recall skill.

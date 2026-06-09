---
description: >
  Use when an AUTONOMOUS agent should consult the project's markdown memory
  before acting — on a recurring alert in unattended mode, a repeated error,
  a familiar-looking task, or before re-deriving a past decision. Trigger
  with "have we hit this before?", "recall memories about X", "check the
  memory", or before debugging/designing. Ranks symptom-indexed notes with
  memgrep and degrades to plain grep when memgrep is absent.
allowed-tools: "Bash, Read, Grep, Glob"
---

# Autonomous Memory Recall — symptom → top notes

Recall durable, symptom-indexed markdown notes from the project memory
BEFORE acting, per `rules/memory-protocol.md`. Two-hop recall: the symptom
query finds the note; the note's body holds the answer.

## Overview

Wraps `scripts/memory_recall.sh`: builds a SYMPTOM query from the words the
problem presents with (the user's words, the alert text, the error message —
never the answer's jargon), runs ranked recall over the per-project memory
directory, then reads the top notes. Uses `memgrep` when installed; falls
back to `grep -rliE` when absent — recall degrades, never breaks.

## Prerequisites

- The `ai-maestro-autonomous-agent` plugin is installed
  (`$CLAUDE_PLUGIN_ROOT` resolves).
- Optional: `memgrep` on PATH (ranked, best-first output). Without it the
  grep fallback returns an unranked path list.
- A memory directory may or may not exist yet — an empty corpus is normal.

## Instructions

1. Build the SYMPTOM query from the problem's own vocabulary (alert text,
   error message, the user's phrasing). Do NOT use solution jargon — notes
   are indexed by the question, not the answer.
2. Run the recall script (MEMDIR defaults to the per-project memory dir
   derived from `$CLAUDE_PROJECT_DIR`):

   ```bash
   "$CLAUDE_PLUGIN_ROOT/scripts/memory_recall.sh" "<SYMPTOM>" [MEMDIR]
   ```

3. Read the top 1-3 returned notes with the Read tool — the answer is in
   their bodies, not in the match line.
4. If nothing matches, try once more with alternate symptom wording, then
   proceed normally — and after solving the problem, capture the fact with
   the `autonomous-memory-write` skill so the next cycle recalls it.

## Output

- memgrep path: ranked lines, best first — `path — "description"`.
- grep fallback: unranked matching note paths, one per line.
- Empty stdout (exit 0) = no matching notes; a missing memory dir prints a
  one-line notice on stderr and exits 0 (empty corpus is a normal outcome).

## Error Handling

- Non-zero exit = a real error (e.g. a stopword-only memgrep query, I/O
  failure) — fix the query or report it; do not silently retry.
- Never treat empty recall as failure: it just means the note was never
  written. Write it after solving.

## Examples

```text
User: the janitor heartbeat stopped firing again — have we hit this before?
Agent: runs memory_recall.sh "heartbeat stopped firing" → reads the top
note → applies the recorded fix instead of re-deriving it.
```

## Resources

- `scripts/memory_recall.sh` — the gate + fallback recall script.
- `rules/memory-protocol.md` — the full protocol (note schema, the
  index-by-symptom law, AUTONOMOUS workflow wiring).
- `autonomous-memory-write` — the companion capture skill.

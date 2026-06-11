---
trdd-id: d21a83f1-f33e-43d3-96e8-dac7e590c960
title: Adopt the markdown memory system — recall + write skills (issue #5)
column: completed
created: 2026-06-11T11:25:10+0200
updated: 2026-06-11T11:25:10+0200
current-owner: aimaa
assignee: aimaa
priority: 2
severity: MEDIUM
effort: M
labels: [memory, skills, retroactive]
task-type: feature
parent-trdd: null
relevant-rules: [1]
release-via: publish
publish-target: ai-maestro-plugins
publish-channel: stable
test-requirements: [unit, lint, typecheck]
review-requirements: [human-review]
fixtures: [memory-corpus]
last-test-result: pass
implementation-commits: [8eb049f, e151466, e3da481]
published-version: 1.2.0
external-refs: ["github.com/Emasoft/ai-maestro-autonomous-agent/issues/5"]
---

# TRDD-d21a83f1 — Adopt the markdown memory system (issue #5)

> Retroactive record (M3 of issue #6): shipped in v1.2.0 before TRDD tracking
> existed. Archived `completed` for the backtracking trail.

## What shipped

- `rules/memory-protocol.md` — AUTONOMOUS memory recall protocol (index-by-symptom).
- `skills/autonomous-memory-recall/` + `skills/autonomous-memory-write/` — 7-section
  CPV skills; added to the persona frontmatter (`8eb049f`, `e151466`).
- `scripts/memory_recall.sh` — symptom recall, `memgrep`-gated with a `grep`
  fallback so recall never breaks.
- `scripts/memory_note_write.py` — argparse CLI: kebab `name` / symptom
  `description` / type validation, atomic write + round-trip verify,
  de-duplicated `MEMORY.md` index line.
- `tests/test_memory_recall.py`, `tests/test_memory_write.py` — 10 real pytest
  tests (no mocks) + `tests/fixtures/memory/` corpus.
- Devitalized scanner-signature shapes for CPV `--strict` (`e3da481`).

## Outcome

Shipped in v1.2.0. CPV `--strict` exit 0; 10/10 memory tests pass. Issue #5 closed.

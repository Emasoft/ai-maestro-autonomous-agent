---
trdd-id: 81RC6IXC
title: Fix two persona currency defects — status-vs-column field, deprecated MEMORY.md-index instruction
column: complete
created: 2026-07-01T18:19:54+0200
updated: 2026-07-01T18:19:54+0200
current-owner: aimaa-autonomous
assignee: aimaa-autonomous
priority: 4
severity: MINOR
effort: S
task-type: bugfix
parent-trdd: null
npt: []
eht: []
blocked-by: []
relevant-rules: []
release-via: publish
delivery: direct-push
target-branch: main
must-pass-tests-before-merge: true
test-requirements: [unit, lint, typecheck]
audit-requirements: []
review-requirements: []
runtime-targets: [macos, linux]
impacts: []
attempts: 1
test-failures: 0
last-test-result: pass
last-test-at: 2026-07-01T18:19:54+0200
implementation-commits: [4710380]
external-refs: ["reports/go-on-yourself-eval/20260701_181205+0200-skills-agent.md"]
---

# TRDD-81RC6IXC — Fix two persona currency defects (status-vs-column, MEMORY.md-index)

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-07-01

- **DONE this session.** Two VERIFIED persona defects surfaced by the go-on-yourself
  project evaluation (skills-agent fork report, corroborated by direct read) — both fixed
  in `agents/ai-maestro-autonomous-agent-main-agent.md`, guarded in
  `tests/test_content_invariants.py`, suite + ruff + mypy + CPV `--strict` all green.
- **Load-bearing facts:** these are pure factual-correctness fixes (a wrong field name; a
  deprecated instruction), NOT governance-policy changes. Authorized under the USER
  go-on-yourself directive ("identify shortcomings … act"). Publishing a release remains a
  separate Tier-2/Tier-3 gate (surfaced to USER).

## Why

The go-on-yourself evaluation (2026-07-01) found the plugin healthy overall (tests green,
CPV-clean, docs current, no leaks) but surfaced two genuine persona-currency defects. Both
verified against live files + the cited ecosystem rules before fixing.

## The two defects (both VERIFIED, both MINOR)

- **D1 — `status:` used where TRDD v2 requires `column:`.**
  `agents/ai-maestro-autonomous-agent-main-agent.md` L419 (two-folder table header
  `` `status:` ``) and L424 ("the approver sets `status: planned`"). TRDD v2 has **no
  `status:` field** — `proposal`/`planned` are overlay VALUES of `column:`
  (`~/.claude/rules/trdd-approval-tiers.md`). The same table's row already said
  "`column:` flow", so L419 contradicted its own row. Risk: the agent could write/expect a
  nonexistent `status:` frontmatter field, or edit the wrong field on promotion.
  **Fix:** `` `status:` `` → `` `column:` `` (header); "sets `status: planned`" →
  "sets `column: planned`".

- **D2 — deprecated "MEMORY.md index line" instruction.**
  L718-719 told the agent that `/janitor-memory-write` captures "(+ the `MEMORY.md` index
  line)". The global memory system (`~/.claude/rules/markdown-memory-recall.md`) makes
  `MEMORY.md` a DEPRECATED STUB and explicitly forbids appending pointers / hand-trimming
  it (the index is 100% memgrep-managed). The parenthetical instructed the exact
  anti-pattern. **Fix:** removed "(+ the `MEMORY.md` index line)".

## What shipped

- `agents/ai-maestro-autonomous-agent-main-agent.md` — the two D1 edits + the D2 removal.
- `tests/test_content_invariants.py` — two real (no-mock) regression guards
  (`test_persona_two_folder_table_uses_column_not_status`,
  `test_persona_memory_write_has_no_memory_md_index_instruction`) asserting the corrected
  form is present AND the buggy form is gone; module docstring extended.

## Verification (all green)

- `uv run --with pytest pytest tests/ -q` → **30 passed** (was 28).
- `ruff check tests/test_content_invariants.py` clean; `mypy` clean.
- `CLAUDE_PRIVATE_USERNAMES=runner uvx … cpv-remote-validate plugin . --strict` →
  CRITICAL=0 MAJOR=0 MINOR=0 NIT=0, WARNING=7, "✓ All checks passed" — persona edits added
  zero new findings.
- No README/CHANGELOG hand-edit: persona internal-correctness fix, no documented-surface
  change; CHANGELOG is git-cliff-generated at the next `publish.py`.

## Approval log

- 2026-07-01T18:19:54+0200 — Fixed under the USER go-on-yourself standing directive
  (authorizes autonomous action on identified shortcomings; USER > MANAGER). Pure
  factual-correctness persona fixes, not governance-policy changes. A release that ships
  them (v1.5.4) is a separate Tier-2 publish gate surfaced to USER/MANAGER.

---
trdd-id: QJ30E8TD
title: Add content-invariant regression guards for the issue-12 governance fixes
column: dev
created: 2026-07-01T18:11:44+0200
updated: 2026-07-01T18:11:44+0200
current-owner: aimaa-autonomous
assignee: aimaa-autonomous
priority: 4
severity: LOW
effort: S
task-type: feature
parent-trdd: TRDD-7c4f9ea4
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
attempts: 0
test-failures: 0
last-test-result: not-run
implementation-commits: []
external-refs: ["github.com/Emasoft/ai-maestro-autonomous-agent/issues/12"]
---

# TRDD-QJ30E8TD — Add content-invariant regression guards for the issue-12 governance fixes

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-07-01

- **Current state:** the issue-12 governance fixes (commit `cd063ea`, TRDD-7c4f9ea4)
  are LIVE in the source but have NO regression test. `tests/test_content_invariants.py`
  is the project's established home for "regression guards for the governance fixes"
  (its own module docstring says so, for issue #6). The #12 batch was never added.
- **NEXT ACTION:** append three focused invariant tests to `tests/test_content_invariants.py`
  guarding the #12 fixes (see Acceptance criteria), extend its module docstring to cite
  issue #12, run the full suite (must stay green), commit.
- **Load-bearing facts:** tests are REAL (no mocks) — each reads a shipped file and asserts
  a substring/semantic invariant. Assertions must be ROBUST to rewording (assert the
  load-bearing tokens, not a whole sentence), matching the existing test style.
- **Tier:** Tier-0 (a regression test for already-shipped, already-approved governance
  work; no governance mutation, no release, no cross-project reach; reversible + local).
  Authored directly in `design/tasks/` per the approval-tiers rule; no MANAGER approval
  needed to WRITE/commit. PUBLISHING a release remains a separate Tier-2 gate.
- **This TRDD is an EHT of TRDD-7c4f9ea4** (it handles the consequence of the #12 fixes —
  locking them in). 7c4f9ea4 is terminal (`complete`); its body is NOT edited (one-way
  parent link only, per the "don't edit terminal TRDD bodies" rule).

## Why

The #12 governance audit shipped three prose fixes to the persona + kanban skill
(commit `cd063ea`). Governance prose has no compiler; a future edit can silently
regress it (the exact "catch regressions six months later" failure the
`test_content_invariants.py` file was created to prevent for the issue-#6 fixes).
The project already has the convention — the #12 batch is simply missing its guards.
This is the one strictly-necessary, in-lane improvement surfaced by the
`go-on-yourself` project evaluation (2026-07-01); everything else on the plugin
(tests 25/25, CPV-clean, README/docs current, no memory leak, no stale/broken refs)
verified healthy.

## Acceptance criteria (the invariants to guard)

Append to `tests/test_content_invariants.py` (real, no-mock; robust token asserts):

1. **`test_kanban_silver_prrd_is_tier2_not_self_auth`** — the kanban skill
   (`skills/ai-maestro-autonomous-prrd-trdd-kanban/SKILL.md`) documents that a SILVER
   PRRD change is **Tier-2 when a MANAGER is reachable** AND that `prrd-edit.py --user`
   is the **TRUE-SOLO fallback ONLY**. Guards Fix C — catches a revert to
   "use --user by default / no MANAGER check".

2. **`test_persona_status_report_is_not_a_work_order`** — the persona
   (`agents/ai-maestro-autonomous-agent-main-agent.md`) documents that a status-report
   request is **NOT a work order**. Guards Fix E — catches a revert of the RULE-1 carve-out.

3. **`test_persona_documents_recall_before_acting`** — the persona documents the
   **recall-before-acting** startup step tied to `/janitor-memory-recall`. Guards Fix F4 —
   catches removal of the proactive-recall step.

Plus: extend the module docstring to note it now also guards the issue-#12 fixes.

## Verification

- `uv run --with pytest pytest tests/ -q` → all tests pass (was 25; becomes 28).
- Each new test would FAIL if its guarded invariant string were removed (reasoned by
  construction — the assert keys on the load-bearing tokens of the fix).
- `uv run --with ruff ruff check tests/test_content_invariants.py` clean; mypy clean
  (test file is already in the checked set).
- No README/CHANGELOG hand-edit: test-only internal change, no user-facing surface
  change; CHANGELOG is git-cliff-generated at the next `publish.py`.

## Approval log

- 2026-07-01T18:11:44+0200 — Authored directly in `design/tasks/` as a Tier-0 task
  (regression test for already-shipped governance work). No approval required to write
  or commit. A release that ships it (v1.5.4) is a separate Tier-2 publish gate to be
  surfaced to USER/MANAGER.

---
trdd-id: a08b839d-dfd8-4b5e-b89c-e41a999ad001
title: Persona approval tiers, proposal lifecycle & baseline governance (issue #4)
column: completed
created: 2026-06-11T11:25:10+0200
updated: 2026-08-11T22:24:00+0200
current-owner: aimaa
assignee: aimaa
priority: 2
severity: MEDIUM
effort: M
labels: [governance, persona, retroactive]
task-type: docs
parent-trdd: null
relevant-rules: [1]
release-via: publish
publish-target: ai-maestro-plugins
publish-channel: stable
test-requirements: [lint, typecheck]
review-requirements: [human-review]
last-test-result: pass
implementation-commits: [42ab63e, 25952ce, 89fa5e0, 449af1a, b2ca5f3, e151466]
published-version: 1.2.0
external-refs: ["github.com/Emasoft/ai-maestro-autonomous-agent/issues/4"]
---

# TRDD-a08b839d — Persona approval tiers, lifecycle & baseline governance (issue #4)

> Retroactive record (M3 of issue #6): the work shipped in v1.2.0 before the
> project adopted TRDD tracking. Authored as a `completed` archive entry so the
> shipped work has a real backtracking trail (`implementation-commits:`).

## What shipped

- Added the AUTONOMOUS PRRD/TRDD/Kanban skill layer and its Approval-discipline
  section (`42ab63e`, `25952ce`), restructured to CPV 7-section format
  (`89fa5e0`), fixed a broken `references/` link (`449af1a`).
- Inserted the **Approval Tiers, proposal→planned Lifecycle, and Baseline
  Governance** section into the persona; reconciled the error-handling
  escalation ladder; wired the memory protocol (`e151466`).
- Removed a ghost `deployer/releaser` subagent dispatch from the kanban skill
  (`b2ca5f3`, RC-GHOST-DISPATCH-001 CRITICAL).

## Outcome

Shipped in v1.2.0. CPV `--strict` exit 0. Issue #4 closed.

## Approval log

- 2026-08-11T22:24:00+0200 — **AUDIT FINDING appended by ai-maestro-autonomous-agent; the body
  above is terminal and was NOT modified.** One of this card's six `implementation-commits` does
  not exist in the repository: **`449af1a` is not a valid object** (`git cat-file -t` fails; it
  appears in no branch or tag). The other five all resolve —

      42ab63e ✓   25952ce ✓   89fa5e0 ✓   449af1a ✗ UNRESOLVABLE   b2ca5f3 ✓   e151466 ✓

  The body attributes a specific change to it ("fixed a broken `references/` link"), so the record
  asserts evidence that cannot be followed. Most likely the sha was captured before an amend or
  rebase rewrote it. **Why this is recorded rather than removed:** `implementation-commits` is the
  backtracking trace a future bug hunt follows from code to the TRDD that introduced it, and a
  dangling entry fails SILENTLY — the reader gets "unknown revision" with nothing saying the sha
  was always bad. Deleting it would hide that the trail was ever broken; leaving it unannotated
  would let the next reader assume their tooling is at fault. Found by a systematic audit of all
  52 archived cards, which is also how the only other defect of this class (`CPVPINGD`) surfaced.
  No fix is available — an absent commit cannot be recovered — so this stands as a known gap.

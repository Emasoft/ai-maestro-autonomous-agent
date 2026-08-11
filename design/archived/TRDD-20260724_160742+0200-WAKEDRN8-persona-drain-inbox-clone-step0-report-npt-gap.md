---
trdd-id: WAKEDRN8
title: Persona worker-side duties — drain AMP inbox on wake, clone assigned repo as step 0, report the NPT gap
column: completed
created: 2026-07-24T16:07:42+0200
updated: 2026-08-11T21:12:12+0200
current-owner: ai-maestro-autonomous-agent
task-type: docs
approval-tier: 2
relevant-rules: [1]
external-refs: [Emasoft/ai-maestro-autonomous-agent#17]
implementation-commits: [2dcf7fa]
---

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-07-24

- S: Persona `agents/ai-maestro-autonomous-agent-main-agent.md` did not enforce three
  worker-side operational duties that SCEN-031 (2026-07-23) proved missing: a fresh
  AUTONOMOUS dev received a well-formed AMP build mandate and never acted (0 tokens, 6+ min idle).
- D: Two surgical persona edits + three no-mock content-invariant guards, one commit.
  1. Startup-checklist step 2 → affirmative "drain inbox FIRST; a mandate IS a work order"
     (status-report request stays the sole exception).
  2. After the "A clear mandate is authorization to begin" block → "clone repo as step 0"
     and "hold the NPT gate honestly but REPORT the gap to the sender (receiver's duty)".
  3. `tests/test_content_invariants.py` → 3 asserts guarding the load-bearing tokens.
- P: `pytest tests/test_content_invariants.py -q` green; the existing
  `test_persona_clear_mandate_is_authorization_to_begin` and
  `test_persona_status_report_is_not_a_work_order` still pass (fix is additive).
- N: FIX only. `complete → publish` is Tier-2/3 release; the commit stays LOCAL and rides
  the next USER-approved publish. Do NOT ship as a side effect.
- NEXT ACTION: none — implemented; flip to `complete` after tests pass and commit lands.

## Why

Issue #17 (filed by the ai-maestro server Claude, 2026-07-24) reports the SCEN-031 worker-side
stall: the MANAGER delegated a build to a fresh AUTONOMOUS dev via a well-formed AMP mandate; the
dev sat idle at the prompt. The mandate reached the filesystem inbox but nothing in the persona
made the dev (a) treat an inbound mandate as an actionable work order, (b) clone the named repo as
the first concrete step, or (c) report an unmet prerequisite instead of holding silently.

The persona already carries the *psychological* half — "A clear mandate is authorization to begin"
(TRDD-MND8AUTH). This TRDD adds the *operational* half the SCEN-031 re-run showed was still absent.

## The three worker-side duties (from #17)

1. **On wake, drain the AMP inbox FIRST and act on any mandate.** Every turn's first action is to
   read the inbox and act on an inbound mandate — a mandate is a build order, not a passive banner.
   The single exception is a status-report request, which is answered but is not a work order.
2. **Clone the assigned repo as step 0.** A build mandate names a repo; the dev clones it into its
   isolated workspace before reading requirements or building.
3. **Hold the NPT gate honestly — but REPORT the gap.** If the referenced requirements are not yet
   on the base the dev branches from (e.g. an unmerged PR), holding is CORRECT — but the dev must
   report the unmet prerequisite back to the sender (receiver's duty), never sit silent.

## Scope and non-goals

- IN: `agents/ai-maestro-autonomous-agent-main-agent.md` (persona prose), `tests/test_content_invariants.py`.
- OUT: the server-side turn-trigger that WAKES an idle pane with a pending inbox — that is the
  ai-maestro server's job (ai-maestro TRDD-9DYUI97S / ai-maestro#51), not this persona. The
  dispatch-precondition (not dispatching before prerequisites merge) is the MANAGER's
  (ai-maestro-assistant-manager-agent#32). This TRDD is only the persona's receive-and-act half.
- No tier or gate is weakened; the change is additive prose + guards.

## Approval

Tier 2 (persona/governance file). Authorized under the standing USER go-on-yourself mandate
(the USER is the sole approver in this standalone project) and directly implements the
governance authority's request in #17. FIX is authorized; SHIP (publish) stays USER-gated.

## Verify

`pytest tests/test_content_invariants.py -q` green (new + pre-existing persona guards);
`grep -n "Drain your AMP inbox FIRST" agents/ai-maestro-autonomous-agent-main-agent.md`.

## Approval log

- 2026-07-24T16:07:42+0200 — Authored `dev` under the USER go-on-yourself mandate (Tier-2 change,
  USER is approver in standalone mode). Implements #17. Commit stays local; publish USER-gated.
- 2026-07-24T16:12:30+0200 — COMPLETED. Impl `2dcf7fa` (persona + 3 guards). Full suite 100 passed,
  ruff clean, MD004 clean. Commit local (unpushed); rides the next USER-approved publish.

- 2026-08-11T21:12:12+0200 — COMPLETED by ai-maestro-autonomous-agent. `release-via:` absent, so
  it defaults to `none` and `complete` is this card's terminal column; work landed in `2dcf7fa`
  (verified present). Tier-2 approval confirmed recorded above before archiving. Archived per the
  TRDD archival protocol.

## Notes and lessons learned

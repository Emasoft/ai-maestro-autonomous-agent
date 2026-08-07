---
trdd-id: VFE3YFVS
title: Persona must require re-verifying recorded external state before relying on it
column: complete
created: 2026-08-07T19:22:00+0200
updated: 2026-08-07T19:22:00+0200
current-owner: ai-maestro-autonomous-agent
task-type: docs
scope: project
relevant-rules: [1]
implementation-commits: [fdf57cf]
---

# TRDD-VFE3YFVS — re-verify recorded external state

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-08-07

**DONE.** Persona + README + guard test. 119 tests pass.

## Why (the evidence, not a principle)

On **2026-08-07**, in a single session, **three** facts this agent had recorded were
found to have gone false, with no signal of any kind:

| recorded fact | how it went false | did I act on the stale version? |
|---|---|---|
| `CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION` = a live 200 ceiling | removed upstream in Claude Code 2.1.224 | yes — documented it in 2 shipped surfaces |
| `[janitor-memory-atomize]` on LOCAL is "provably null" | never true; it described a *different chore* | **yes — skipped 2 dispatches on it** |
| iTerm Automation grant is DENIED to the daemon | the owner granted it; 6 rearms fired that day | yes — kept recommending the tmux workaround |

None of these produced an error. None turned a test red. Each was true, or believed
true, when written. **A stale note is byte-identical in appearance to a fresh one**,
which is what makes this a structural problem rather than carelessness.

### Why AUTONOMOUS specifically

Every role accumulates stale notes. AUTONOMOUS is the role that runs **unattended for
days with no human correcting its state** — the correction loop that quietly rescues
other roles is precisely the one this role does not have. So the discipline has to be
written into the persona rather than left to the operator.

### The asymmetry that makes it dangerous

Two of the three cost real decisions, and the worst was a **skip**. An unnecessary
action gets noticed — it shows up as a diff, a cost, a failure. **A decision NOT to act
produces no artifact at all**, so nothing downstream ever re-checks it. The atomize case
is the clean illustration: two dispatches skipped to "save" ~468k tokens, on reasoning
that was wrong, and the actual work took seconds once the right question was asked. The
saving was real; the premise was not; and nothing would ever have surfaced that.

## What changed

`agents/…-main-agent.md` — a third leg in the memory protocol, between *write after
solving* and *propagate to sub-agents*: **re-verify before relying**. It states that a
recorded fact about uncontrolled state is a measurement with a timestamp; requires
re-running the check before acting, and **especially before skipping**; requires
recording the CHECK beside the verdict so re-verification is cheap enough to happen;
and adds two bounds learned the same day — an absence of errors is not evidence of
success (a path that never ran also logs none), and a verification is scoped to the
mechanism actually exercised (proving the daemon drives iTerm said nothing about
whether the R42.8 CLI can read it).

`README.md` — the same rule in the `Running unattended` section, which is where an
operator evaluating this plugin for a long run will look.

## The guard, and why it is shaped this way

`test_persona_requires_reverifying_recorded_external_state` asserts **five claims**, not
five keywords — deliberately. The README guard that preceded it asserted only that
`CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION` was *mentioned*, and it stayed green through the
exact fact-flip it existed to catch. A guard on a changelog-derived claim must assert the
claim in both directions or it cannot fail.

**Falsified before being trusted:** seeded a violation (removed the "a wrong skip is
silent forever" clause) → the test FAILED; restored → PASSED. Verified the probe left no
residue (`git diff`: 16 insertions, **0 deletions**, no trace of the seeded string). A
guard nobody has watched go red is a guess.

## Deliberately NOT done

- **No enforcement mechanism / expiry field / re-check scheduler.** The failure is one of
  discipline at the point of writing and reading a fact; a machine that stamps expiries
  would produce a second thing that goes stale. Revisit only if the discipline demonstrably
  fails again.
- **No retroactive audit of every recorded fact.** Three were found by ordinary work. A
  sweep would be expensive and would itself produce a snapshot that decays.

## Memory

Cross-scope, already captured — this TRDD does not restate them:
`a-doc-guard-that-asserts-a-mention-cannot-see-a-stale-claim` (USER, new today) ·
`agent-rescue-paths-both-assume-tmux` (USER, corrected by supersession today) ·
`ATOM-178N-C7CG` in `ai-maestro-autonomous-agent-local-overview` (LOCAL — the skip lesson).

## Verification

- `uv run pytest -q` → **119 passed**.
- `uv run python scripts/publish.py --gate` → exit 0, CRITICAL=0 MAJOR=0 MINOR=0 NIT=0
  (3 standing `RC-PIPELINE-DRIFT-001` WARNINGs, by-design for the `remote-validation`
  profile, not introduced here).
- New guard proven to fail on a seeded violation, then restored.
- `implementation-commits:` is filled in AFTER the commit exists — a predicted sha reads
  as evidence while pointing at nothing.

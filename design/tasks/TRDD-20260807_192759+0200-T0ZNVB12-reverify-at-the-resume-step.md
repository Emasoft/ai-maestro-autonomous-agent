---
trdd-id: T0ZNVB12
title: Carry the re-verify duty into the startup checklist resume step
column: complete
created: 2026-08-07T19:27:59+0200
updated: 2026-08-07T19:27:59+0200
current-owner: ai-maestro-autonomous-agent
task-type: docs
scope: project
relevant-rules: [1]
derived-from: VFE3YFVS
implementation-commits: [2d5ba56]
---

# TRDD-T0ZNVB12 — re-verify at the resume step

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-08-07

**DONE.** 119 tests pass. Derived from TRDD-VFE3YFVS (terminal, so this is a new card
rather than an edit to it).

## Why this was necessary the moment VFE3YFVS landed

VFE3YFVS put "re-verify before relying" in the **Memory protocol** section. The derived
question — asked because a task's consequences are part of the task — was: *does the rule
reach the place where it actually has to fire?*

It did not. `## Startup checklist` step 4 read:

> If you have a `loop.md` or similar state file in your working directory, read it and
> resume where you left off.

That step **is the failure**. It is the exact moment recorded state becomes action, it
runs on every wake and every resume, and it instructed the agent to act on a file with no
suggestion that any line in it might have expired. A rule stated only in a reference
section three screens earlier fires too late to matter — the agent has already resumed.

All three of the 2026-08-07 stale-fact incidents entered exactly this way: resume from a
handoff → trust it → act. The most expensive one (two skipped `atomize` dispatches) was a
line in a state file saying work was unnecessary, obeyed without re-checking.

## What changed

`agents/…-main-agent.md` step 4 — resuming is still the instruction, but the file is now
framed as **a claim to re-check, not a briefing to act on**, with the skip warning carried
down explicitly (*"above all before you SKIP work because the file says the work is
unnecessary"*) and the concrete case named: a blocker recorded days ago may already be
resolved, and nothing will have updated it.

Deliberately kept as a *framing* change, not a new procedure: adding a mandatory
verification pass at every wake would tax every resume, including the overwhelming
majority where nothing has moved. The duty is to re-check the lines you are about to
*rely on*, not to re-audit the file.

## Guard

Extended `test_persona_requires_reverifying_recorded_external_state` with two assertions
scoped to the checklist section specifically (`text.split("## Startup checklist")`), so
the rule cannot satisfy the test from the Memory-protocol section alone — which is the
precise failure this TRDD fixes.

**Falsified:** blunted the checklist wording only, leaving every Memory-protocol clause
intact → the test FAILED (proving the new assertions are section-scoped and not satisfied
by the older text) → restored → 119 pass. Diff audited: the only deletions are the two
original step-4 lines this change replaces, and the seeded string is absent.

## Verification

- `uv run pytest -q` → **119 passed**.
- `uv run python scripts/publish.py --gate` → exit 0, CRITICAL=0 MAJOR=0 MINOR=0 NIT=0
  (3 standing by-design `RC-PIPELINE-DRIFT-001` WARNINGs).
- `implementation-commits:` filled in after the commit exists.

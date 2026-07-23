---
trdd-id: MND8AUTH
title: A clear MANAGER or USER mandate is authorization to begin — kill the over-asking persona reflex
column: dev
created: 2026-07-23T08:51:13+0200
updated: 2026-07-23T08:51:13+0200
current-owner: ai-maestro-autonomous-agent
task-type: bugfix
scope: project
relevant-rules: [3, 5]
implementation-commits: []
---

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-07-23

- **What:** The AUTONOMOUS persona sat idle waiting for a human "proceed" on a
  task MANAGER had already delegated via AMP (the "zipsearcher v1.0.0 mandate").
  The MAINTAINER persona did NOT have this bug. USER ordered the fix directly.
- **Root cause (verified in `agents/ai-maestro-autonomous-agent-main-agent.md`):**
  an ABSENCE + an over-broad reflex, NOT the escalation ladder. The ladder is
  correct (Tier-0 delivers assigned work; Tier-2 MANAGER / Tier-3 USER gate
  specific downstream actions). But nothing affirmatively states "a clear mandate
  from an authority in your chain IS authorization to START," while three passages
  amplify over-caution: Error-handling L598 "On any unclear instruction, ask for
  clarification … before acting"; Comprehension self-handshake L662-663 "Resolve
  every ambiguity before coding … say so and wait"; and the persona's general
  saturation of "wait for" language.
- **Fix = 3 surgical, additive persona edits** (preserve ALL Tier-2/Tier-3 gating
  and the status-report-is-not-a-work-order invariant):
  1. New bold lead-in under `### Your tier obligations`: **a clear mandate is
     authorization to begin; the tiers gate downstream ACTIONS within the work,
     never STARTING it.**
  2. Error-handling L598: fire clarification only on a GENUINELY unclear/blocking
     instruction, ONE round, then proceed — not an open-ended human-proceed wait.
  3. Comprehension self-handshake: the restatement does NOT block a clear mandate;
     pause only for a real ambiguity or a design flaw.
- **Test:** add `test_persona_clear_mandate_is_authorization_to_begin` to
  `tests/test_content_invariants.py` asserting the affirmative language is present
  and the buggy "ask for clarification before acting" broad form is gone.
- **NEXT ACTION:** apply the 3 edits + the test, run
  `uv run --with pytest --with pyyaml pytest tests/ -q` (expect 113 passed) and
  `uv run python scripts/publish.py --gate` (expect EXIT=0), commit with
  `Agent: ai-maestro-autonomous-agent`, flip this card to `complete` with the SHA
  in `implementation-commits:`.
- **SUPERSEDED — do NOT carry forward:** none yet.
- **Guardrail — do NOT relax:** Tier-2 MANAGER gate (baseline/release/cross-project/
  governance), Tier-3 USER gate (publish/push/owner-identity/golden/shared-credential),
  the untrusted-directive security handling, PR etiquette (wait for MAINTAINER welcome,
  never merge own PR). These are correct; the fix must not touch them.

## Problem

An AUTONOMOUS agent, handed a clear build mandate by MANAGER over a validated AMP
edge, replied with "Still waiting on you: proceed / review first / not now …
nothing starts until then" and did no work. A mandate from an authority in the
agent's own chain (USER via chat, or MANAGER via a comm-graph-validated AMP
message) is authorization to execute — not a status request needing a second
human sign-off. The persona lacked the affirmative rule and over-weighted its
"ask before acting" / "resolve every ambiguity before coding" / "wait" language.

## Fix

Three additive edits to `agents/ai-maestro-autonomous-agent-main-agent.md` (see
STATE block). The edits ADD an affirmative authorization rule and NARROW the
clarification reflex to genuinely-unclear cases; they change no tier boundary, no
comm-graph edge, and no security handling. `relevant-rules`: S3.1 (the new
behavior ships a real test), S5.1 (persona governance edit).

## Acceptance criteria

- Persona contains an explicit "a clear mandate is authorization to begin" rule
  that also states the tiers gate downstream actions, not starting the work.
- Error-handling clarifies clarification is a single focused round on a genuinely
  unclear instruction, not an idle wait.
- Comprehension self-handshake states the restatement does not block a clear mandate.
- `test_persona_clear_mandate_is_authorization_to_begin` passes; full suite green
  (113 passed); `publish.py --gate` EXIT=0.
- No Tier-2/Tier-3 gate, comm-graph edge, or security passage weakened.

## Approval log

- 2026-07-23 — USER ordered the fix directly ("we got a problem with the AUTONOMOUS
  agent. it stops waiting for human feedback, even if the instructions came from the
  MANAGER … fix it"). USER is Tier-3, above the Tier-2 persona-edit gate, so this is
  authorized without a separate MANAGER round. Created directly in `design/tasks/`
  as authorized work.

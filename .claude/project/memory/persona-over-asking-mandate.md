---
name: persona-over-asking-mandate
description: "the AUTONOMOUS agent STALLS / waits for a human 'proceed' even though the task was already delegated by MANAGER (or USER) via AMP — why does it idle on a clear mandate, and how was it fixed? Root cause is an ABSENCE of an affirmative 'mandate=authorization' rule plus over-broad 'ask before acting' language, NOT the escalation ladder"
ocd: 2026-07-23
lmd: 2026-07-23
metadata:
  node_type: memory
  type: project
  tier: component
  functionality: architecture
---
**Symptom:** an AUTONOMOUS agent, handed a clear build mandate by MANAGER over a
comm-graph-validated AMP edge, replied "Still waiting on you: proceed / review
first / not now … nothing starts until then" and did no work. The MAINTAINER
persona did NOT have this bug. USER reported it directly (2026-07-23).

**Root cause (the non-obvious part):** it was NOT the approval-tier ladder — that
is correct and stays (Tier-0 delivers assigned work; Tier-2 MANAGER / Tier-3 USER
gate specific downstream ACTIONS). The bug was an **ABSENCE + an over-broad
reflex**: nothing in the persona affirmatively said "a clear mandate authorizes
STARTING," while Error-handling ("on any unclear instruction, ask before acting")
and the comprehension self-handshake ("resolve every ambiguity before coding / say
so and wait") amplified over-caution into an open-ended human-proceed wait.

**Fix (TRDD-MND8AUTH, commit `3c27ced`):** 3 additive persona edits in
`agents/ai-maestro-autonomous-agent-main-agent.md` — (1) a bold rule under *Your
tier obligations*: a clear USER/MANAGER mandate IS authorization to begin, and the
tiers gate downstream actions *within* the work, never STARTING it; (2)
Error-handling fires clarification only on a genuinely-unclear/blocking
instruction, ONE round, then proceed; (3) the comprehension handshake no longer
blocks a clear mandate. Plus a `tests/test_content_invariants.py` guard
(`test_persona_clear_mandate_is_authorization_to_begin`) that also asserts
Tier-2/Tier-3 and status-report-≠-work-order survived — proving the fix is additive.
Local `publish.py --gate` PARITY-CLEAN; 113 tests pass.

See also [[governance-audit-handling]] (the same fix-in-`test_content_invariants.py`
guard-in-the-same-batch methodology, and why a persona fix stays local until the
USER-gated publish), [[architecture]].

## Notes and lessons learned
[^1]: [id:ATOM-MND8-ABSENCE, status:valid, keywords:"agent_waits_for_proceed stalls_on_mandate over-asking absence_not_ladder affirmative_authorization_rule", ocd:2026-07-23, lmd:2026-07-23]
  DO NOT hunt an over-asking / over-waiting persona bug in the escalation ladder
  first, BECAUSE the ladder is usually correct and the real defect is an ABSENCE —
  no affirmative "a clear mandate authorizes starting" rule — amplified by
  over-broad "ask before acting / resolve every ambiguity / wait" language. DO add
  the affirmative rule AND narrow the clarification reflex to genuinely-unclear
  cases, while explicitly preserving every tier/gate (guard it with a content
  invariant that asserts the gates survived).

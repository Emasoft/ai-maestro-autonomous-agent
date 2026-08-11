---
trdd-id: 4P2RZQFE
title: Skills must instruct the CLI wrappers and forbid direct ai-maestro server API calls
column: completed
created: 2026-08-02T11:58:33+0200
updated: 2026-08-11T21:07:55+0200
current-owner: ai-maestro-autonomous-agent
task-type: security
approval-tier: 2
relevant-rules: [1]
external-refs: []
implementation-commits: [2f3df20]
---

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-08-02

- S: USER directive 2026-08-02 — the janitor reported cases of agents calling the ai-maestro
  server API directly. Direct API calls from agents are FORBIDDEN; only the ai-maestro scripts
  (the frozen CLI) may talk to the server, and **every plugin must instruct this in its SKILLS**.
  Declared an IRON RULE.
- C: Audited this plugin at HEAD before acting. **No violation in code or prose.** The single
  `/api/` occurrence in any shipped surface is the persona's own prohibition
  (`agents/ai-maestro-autonomous-agent-main-agent.md:212`, FORBIDDEN ACTION #2, R23). The
  `curl` hits in `scripts/publish.py` are GitHub's PUBLIC API, already cleared by TRDD-7c4f9ea4.
- C: The GAP is exactly the one the directive names — the rule lives in the PERSONA and in two
  `references/*.md`, but **no `SKILL.md` states it**, and the governance self-audit had no
  question for it. A rule that is not a checklist question is a rule the audit cannot catch.
- D: Add **Q13 — Direct-server-API check** to the governance self-audit (12 → 13 questions),
  state the rule in all three `SKILL.md` files, and guard it with a content-invariant test.
- P: suite **103 passed** (101 + 2 new guards, both falsified); `publish.py --gate` **exit 0**.
- NEXT ACTION: none — implemented in 2f3df20 and shipping in the next release.

## Why the persona alone was not enough

The persona is the always-loaded contract, so an agent that reads it will not call `/api/*`.
But skills are loaded *on demand and in isolation*: an agent that invokes the governance
self-audit to answer "am I allowed to do this?" walks 12 questions, none of which ask about
the transport it is about to use. The audit would return ALLOWED for a raw HTTP mutation that
FORBIDDEN ACTION #2 prohibits — the checklist and the persona disagreed, and the checklist is
what gets consulted at decision time.

This is also the shape the USER's directive asks for: *"all plugins must instruct in their
skills to use the ai-maestro scripts, never the api directly"*. Instructing it in the persona
only is not instructing it in the skills.

## What changed

1. `skills/ai-maestro-autonomous-governance/SKILL.md`
   - 12 → **13** questions (frontmatter description, overview, checklist).
   - Step 1's "every tmux/API call that mutates another agent" reworded: an API call is not a
     neutral thing to enumerate, it is the thing to refuse. Now names the frozen CLI.
2. `skills/ai-maestro-autonomous-governance/references/questions.md` — new **Q13**, with the
   rationale (routes are renameable, the CLI is the frozen interface, and the CLI runs the
   pipeline gates a raw route bypasses).
3. `skills/ai-maestro-autonomous-prrd-trdd-kanban/SKILL.md` and
   `skills/ai-maestro-autonomous-workspace-isolation/SKILL.md` — a one-line standing rule so
   the instruction is present in EVERY skill, not only the governance one.
4. `tests/test_content_invariants.py` — `test_all_skills_forbid_direct_server_api`, which
   asserts each `SKILL.md` carries the rule and that Q13 exists. Without it the rule is prose
   that a future edit can silently drop.

## Why a test and not just prose

TRDD-RULENUM7 already recorded that a prose test can assert a string is present but never that
it still means what it claimed. That limit applies here too — but the failure mode this guard
covers is the cheaper one: **deletion**, not drift. The rule vanishing from a SKILL.md is
exactly what a string assertion does catch, and it is the realistic regression (a skill rewrite
that drops a line nobody re-reads).

## Verify

```
uv run pytest -q                                # expect 101 + 1 = 102 passed
uv run python scripts/publish.py --gate         # expect exit 0
grep -rn "never.*raw.*/api\|frozen CLI" skills/*/SKILL.md
```

## Approval log

- 2026-08-02T11:58:33+0200 — Authored under the USER's explicit 2026-08-02 directive declaring
  this an iron rule (Tier-2; USER is approver in standalone mode). The directive IS the
  approval — no separate sign-off sought.
- 2026-08-11T21:07:55+0200 — COMPLETED by ai-maestro-autonomous-agent. `release-via:` absent, so
  it defaults to `none` and `complete` is this card's terminal column; work landed in `2f3df20`
  (verified present). Tier-2 approval confirmed present above before archiving — a Tier-2 card
  archived without a recorded approval would bury the gap, not close it. Archived per the TRDD
  archival protocol.

## Notes and lessons learned
[^1]: [id:ATOM-API01-SKILLGAP, status:valid, keywords:"rule_is_in_the_persona_but_not_in_the_skills self_audit_checklist_returns_ALLOWED_for_a_forbidden_transport skills_load_in_isolation_persona_is_not_inherited a_rule_that_is_not_a_checklist_question_is_not_enforced", ocd:2026-08-02, lmd:2026-08-02]
  DO NOT treat "the persona already forbids it" as evidence the plugin instructs a rule,
  BECAUSE skills are loaded on demand and IN ISOLATION — the governance self-audit walked 12
  questions, none about the transport, so it would have returned ALLOWED for the very HTTP
  mutation FORBIDDEN ACTION #2 prohibits, and the checklist is what an agent consults at
  decision time. DO put an enforceable rule where the DECISION is made (a checklist question),
  state it in every SKILL.md, and guard it with a content test so a rewrite cannot drop it.

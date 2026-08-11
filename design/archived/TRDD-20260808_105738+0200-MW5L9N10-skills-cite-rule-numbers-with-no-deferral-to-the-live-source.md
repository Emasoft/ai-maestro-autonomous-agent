---
trdd-id: MW5L9N10
title: Skills cite governance rule numbers as fact with no deferral to the live source
column: completed
created: 2026-08-08T10:57:38+0200
updated: 2026-08-11T21:50:24+0200
implementation-commits: [abbfb39]
current-owner: ai-maestro-autonomous-agent
task-type: security
scope: project
relevant-rules: [1]
derived-from: 1R72424K
---

# TRDD-MW5L9N10 — the disclaimer stops at the persona boundary

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-08-08

**DONE** — `abbfb39`. Deferral in all 3 SKILL.md entry points; guard falsified once
**per file** (proving the loop walks all three, not just the first). 122 tests pass;
gate exit 0 PARITY-CLEAN.

## The content is clean — that part was checked first

Every governance claim in the skills was compared against the live text
(v5.3.3, tip `e46764f6`, ✓ 2026-08-08). **All correct**, including the two that
needed the actual R6 graph to settle:

| skill claim | live |
|---|---|
| "the three `Y` edges for AUTONOMOUS: MANAGER, peer AUTONOMOUS, HUMAN" | ✓ AUTONOMOUS row is `HUMAN=Y, MANAGER=Y, AUTONOMOUS=Y`, all else blank |
| persona: "server rejects direct AUTONOMOUS→MAINTAINER" | ✓ that cell is **blank = deny** |
| "identity immutable to me (R26)" | ✓ R26.1 |
| "agents never sudo (R32)" | ✓ R32.1 |
| "install via core skills, CPV-scanned (R27)" | ✓ R27.1/.2/.3 |
| "frozen CLI, routes are renameable (R23)" | ✓ R23.1/.2 |
| "AUTONOMOUS reaches USER directly (R6.6)" | ✓ R6.6 governance-titles clause |

## The gap

**5 skill files cite 8 distinct rules (R6, R6.6, R23, R26, R27, R28, R32, R40).
NOT ONE defers to the live governance source.** The persona does, at length:

> Every rule NUMBER in this persona is as-of-authoring, not a fact you may assert. …
> a renumber or revision drifts this file silently — no test can catch it, because
> prose cannot check a number it cannot resolve. … Never tell another agent
> "rule RNN says X" on this file's authority alone.

That reasoning is not persona-specific. It is a property of **citing a versioned,
revisable source**, and the skills do exactly that with no such caveat.

## Why this is not a manufactured finding — the precedent is USER-established

The identical argument was already accepted for a sibling case, and it is in this repo,
in `test_every_skill_forbids_direct_server_api`:

> The persona already carried this as FORBIDDEN ACTION #2, but **skills load on demand
> and IN ISOLATION — an agent consulting only a skill would never see it.** The USER
> declared the CLI/API separation an iron rule and **required it be instructed in the
> SKILLS.**

Same structure: persona carries it → skills load in isolation → therefore the skills
must carry it too. I am applying a rule the USER already set, not inventing one.

And the drift is not hypothetical. **TRDD-62AO9JXY, today: a governance claim in the
persona was 25 days stale.** In a skill the same drift would be *less* visible, because
no skill carries even the caveat that a number may have moved.

## Steelman, recorded because two candidates already died on it today

*"The persona is this agent's system prompt, so a skill is never read without it."*
True for THIS main agent — and the USER **already rejected that reasoning** for the
`/api/` case, requiring the instruction in the skills anyway. Skills are also readable
standalone, by other agents, and by a human. The precedent governs.

*"It is boilerplate and skills load into context."* Real cost, so the fix is **two
lines**, not the persona's full paragraph, and only in the 3 SKILL.md entry points
(matching the `/api/` test's scope) — never copied into the reference files, which are
always reached through their SKILL.md.

## Fix

1. Two-line deferral in `ai-maestro-autonomous-governance/SKILL.md`,
   `ai-maestro-autonomous-prrd-trdd-kanban/SKILL.md`,
   `ai-maestro-autonomous-workspace-isolation/SKILL.md`.
2. Guard it in the same test that already walks those three files.

## Verification

- [x] `uv run pytest -q` → **122 passed**.
- [x] `uv run python scripts/publish.py --gate` → **exit 0**, `PARITY-CLEAN
      (FAIL=0 WARNING=3 PASS=8)` — baseline unchanged, this added no warning.
- [x] **Guard falsified once PER FILE**, each reddening alone, control green, tree clean:

      | file | broken | result |
      |---|---|---|
      | governance/SKILL.md | `as-of-authoring` | FAIL |
      | prrd-trdd-kanban/SKILL.md | `live governance source governs` | FAIL |
      | workspace-isolation/SKILL.md | `rule RNN says X` | FAIL |

      Breaking a **different** file each time is the point: a loop-over-files guard that
      is only ever falsified on the first element proves the assertion, not the loop.
      A guard that silently checked one file and passed the other two would look
      identical to this one from its green result.

## Approval log

- 2026-08-11T21:50:24+0200 — COMPLETED by ai-maestro-autonomous-agent. `release-via:` absent, so
  it defaults to `none` and `complete` is this card's terminal column; `abbfb39` verified present.
  The closing observation above — that a guard checking one file looks green exactly like a guard
  checking three — later generalised into the corpus-wide 403 guard of `TRDD-KT4MVFHA` and the
  USER-scope lesson `ATOM-JDTP-18YE` ("a guard's SCOPE is part of its claim"). Recorded so the
  lineage of that idea is not lost in the archive. Archived per the TRDD archival protocol.

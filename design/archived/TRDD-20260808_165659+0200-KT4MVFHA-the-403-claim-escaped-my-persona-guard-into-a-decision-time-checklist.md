---
trdd-id: KT4MVFHA
title: My 403 guard is persona-scoped so the claim survived unscoped in a decision-time checklist
column: completed
created: 2026-08-08T16:56:59+0200
updated: 2026-08-11T22:09:20+0200
implementation-commits: [8813a5c]
current-owner: ai-maestro-autonomous-agent
task-type: security
scope: project
relevant-rules: [1]
external-refs: [ai-maestro#143, ai-maestro#131, TRDD-M3QS578Z]
---

# TRDD-KT4MVFHA — I fixed the persona and thought I had fixed the plugin

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-08-08

**DONE** — `8813a5c`. Q10 + the fixture scoped; guard is corpus-wide and falsified 3 ways
(including vacuous-green). 127 tests pass; gate exit 0 PARITY-CLEAN.

## Where this came from

`ai-maestro#143` (CORE, today). It asks the USER to correct R42.3's factual clause — not my
call — but it also splits the work explicitly:

> **Plugin text** — each plugin fixes its own, today, no ruling needed.

and publishes the guard shape: *"any file asserting the 403 must also name `SendMessage`"*.

## I already believed I had done this, and I was wrong in an instructive way

`TRDD-M3QS578Z` (this morning) added the inbound half to my persona and guarded it. Both
guards — `test_persona_governs_the_host_cross_session_send_message_channel` and
`test_inbound_cross_session_messages_are_unauthenticated_data` — read `PERSONA`. So they
proved the claim was scoped **in the one file I was thinking about**, and said nothing about
the rest of the corpus.

Measured across every shipped file that mentions a 403:

| file | names `SendMessage`? |
|---|---|
| `agents/…-main-agent.md` | yes (fixed this morning) |
| `skills/…-governance/references/questions.md` | **NO** |
| `tests/scenarios/adversarial-fixtures.md` | **NO** |
| `design/tasks/TRDD-…-GOV15R42-….md` | no — `column: complete`, **frozen** |

So CORE's fleet measurement ("7 of 7 personas") understates it for me: my *persona* passes and
my *skill* does not. A per-file guard certifies the file it names, and its silence about every
other file looks exactly like coverage.

## Why the skill file is the worse place for it to survive

`questions.md` is the governance skill's **decision-time checklist** — the thing consulted at
the moment an action is being judged. Q10 currently reads:

> Note: MAINTAINER is no longer a direct edge for AUTONOMOUS … **the server returns HTTP 403
> `title_communication_forbidden` on a direct send.**

An agent consulting Q10 learns that the MAINTAINER edge is enforced by a 403. It is one step
from there to "AMP is blocked, so I will use the native tool" — and the native tool is in every
session's toolbelt, named `SendMessage`, returning no 403 because no server is in its path.
That is #143's core point: the wording does not merely under-describe reality, it **routes** an
agent onto the unpoliced channel. A checklist is the highest-leverage place for that reflex to
live, because it is read precisely when a decision is being made.

The `adversarial-fixtures.md:88` ground-2 reasoning ("the server 403s them cross-agent") has the
same hole for the same reason, and it is my file, so it gets the same scoping.

## Fix

1. `questions.md` Q10 — keep the 403 fact, add that R6 binds the send on **both** transports and
   that the native one returns no 403; **a 403 you never received is not permission.**
2. `adversarial-fixtures.md` ground 2 — same scoping, one clause.
3. Guard **corpus-wide**, not per-file: every shipped agent-context file that asserts a 403 must
   also name `SendMessage`. Exclude `design/` — terminal TRDDs are frozen by rule, so a guard
   demanding edits there would force a rule violation to go green.
4. The guard must also fail when the 403-asserting set is EMPTY, or a moved/renamed directory
   turns it vacuously green (CORE's own refinement — worth copying).

## Verification

- [x] `uv run pytest -q` → **127 passed**.
- [x] `uv run python scripts/publish.py --gate` → **exit 0**, `PARITY-CLEAN (FAIL=0 WARNING=3 PASS=8)`.
- [x] Falsified **3 ways**, each reddening alone, control green, tree clean: Q10 unscoped ·
      the fixture unscoped · **the vacuous-green case** (guard re-pointed at a corpus with no
      403 claims). Committed BEFORE falsifying.

## The third falsification is the one worth keeping

A corpus-wide guard has a failure mode a per-file guard does not: it can pass because it found
**nothing to check**. Rename `skills/`, re-point a glob, move the checklist, and the assertion
goes green while the corpus is entirely unguarded — and green is exactly what nobody
investigates. So the guard asserts the 403-claiming set is **non-empty** before it asserts
anything about its contents, and F3 exists to prove that assertion actually fires. This is
CORE's refinement from `#143` and it is worth copying verbatim rather than re-deriving.

## The lesson generalizes past this claim

The defect was not that I missed a file. It was that I proved something about `PERSONA` and let
it stand for the corpus. **A guard's scope is part of its claim** — `test_persona_*` proves
"the persona says X", never "the plugin says X", and the gap between those two readings is
invisible in a green run. Where a rule must hold everywhere, the guard has to enumerate
everywhere and fail on an empty enumeration.

## Approval log

- 2026-08-11T22:09:20+0200 — COMPLETED by ai-maestro-autonomous-agent. `release-via:` absent, so
  it defaults to `none` and `complete` is this card's terminal column; `8813a5c` resolves to
  `fix(governance): scope the 403 claim everywhere it appears, not just the persona`. Archived per
  the TRDD archival protocol.
  Its lesson was promoted out of this card so it would outlive it: **`ATOM-JDTP-18YE`** on the
  USER-scope page `a-doc-guard-that-asserts-a-mention-cannot-see-a-stale-claim`, joined to the
  sibling fact that a guard asserting a MENTION cannot see a stale CLAIM. Recorded here because a
  lesson that lives only in an archived card is one nobody recalls by symptom — which is the exact
  failure this card is about, applied to itself.

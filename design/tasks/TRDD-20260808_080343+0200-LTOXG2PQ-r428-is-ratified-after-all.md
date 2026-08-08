---
trdd-id: LTOXG2PQ
title: R42.8 IS ratified - reverse the 08-07 retraction, publication lagged the grant
column: complete
created: 2026-08-08T08:03:43+0200
updated: 2026-08-08T08:03:43+0200
current-owner: ai-maestro-autonomous-agent
task-type: security
scope: project
relevant-rules: [1]
supersedes-commit: db3a892
implementation-commits: []
external-refs: [ai-maestro#125, ai-maestro#128, ai-maestro#129]
---

# TRDD-LTOXG2PQ — R42.8 is ratified after all

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-08-08

**DONE.** 119 tests pass. Reverses `db3a892`, which had reversed `3cc4bff`. **The original
was right.** If this file ever disagrees with the live governance file, **the file wins** —
re-fetch it (`?ref=governance-rules`) rather than reasoning from this text.

## The fact, verified here before anything was changed

```
gh api repos/Emasoft/ai-maestro/branches/governance-rules
  sha=cdee1dddee33   2026-08-08T05:56:06Z

docs/GOVERNANCE-RULES.md @governance-rules   1952 lines   (was 1929 on 08-07)
  subsections: R42.0 R42.1 … R42.7 R42.8      "R42.8": 7 occurrences
  row 1542 attribution: Explicit (USER — 2026-08-05, ai-maestro#125, TRDD-AODXPI5E)
  changelog 5.3.0: "NEW SUB-RULE R42.8 — BLOCKED-PROMPT UNBLOCK (USER, 2026-08-05,
                    direct first-person grant)"
```

## What went wrong: the measurement was right, the inference was not

| when | what |
|---|---|
| 2026-08-05 | USER grants R42.8 |
| 2026-08-07 ~20:00 | I measure the published file: 1929 lines, R42.1–R42.7, **zero** R42.8 — accurate, reproducible, positively controlled |
| 2026-08-08 05:56Z | the rule text reaches `governance-rules` |

**I measured inside a 3-day publication lag.** My evidence supported *"R42.8 is not
verifiable from any published artifact."* I asserted *"R42.8 is NOT ratified."* Different
claims; I published the stronger one, and it talked four plugins out of a true statement.

**Re-running the measurement could never have caught this** — the measurement was never the
defective part. Every rule I shipped this session (re-verify before relying; falsify the
check) is aimed at stale or vacuous *measurements*, and none of them touches a sound
measurement wrapped in an over-strong *inference*.

## The guard is the worst artifact, and the lesson is not the one I expected

`db3a892` rewrote `test_persona_keystroke_injection_is_absolute_no_manager_exception` to
assert R42.8 **must not** be described as ratified — and I falsified it four ways to prove
it had teeth. It did. So for a day the suite **enforced a false statement about ratified
governance**: the same "a green test pins the defect" failure I had diagnosed hours
earlier, rebuilt in the opposite direction, and made *more durable* by the falsification
work that proved it functioned.

**Proving a guard CAN fail says nothing about whether the fact it encodes is TRUE.**
Falsification tests the mechanism, never the premise. That is now in the test's docstring,
where the next person to trust a well-falsified guard will read it.

## What did NOT change, in any version

The verdict. AUTONOMOUS holds no R42.8 title (constraint (c): *every other title: none*),
and `inject`/`slash`/`queue` are self-only for every title under R42.1 regardless. **Both
refusal grounds survived all three reversals** — which is precisely why nothing caught the
error for three days. A correct answer resting on a false ground passes every test that
checks the answer.

## Not a plain revert — the ratified text is NARROWER than `3cc4bff` claimed

- exception verbs are **`read-prompt` and `answer` ONLY**. **`block-state` is NOT one.**
  (Changelog 5.3.1 records an earlier draft wrongly listing `inject`/`queue`.)
- title scope: MANAGER — any agent on the host except an ASSISTANT; COS — **its own team
  only**, same exclusion; every other title: none.
- eight lettered constraints, incl. blocked-only, unblock-never-drive, never-an-ASSISTANT,
  identity-prompts-escalate, read-before-answer, server-enforced, audited.

A new assertion forbids re-widening the verb list, since that is the direction a
well-meaning restore would drift.

## Guard

Falsified four ways, each independently reddening the test: breaking `R42.8 is RATIFIED`,
`including AUTONOMOUS: none`, `` `read-prompt` and `answer` ONLY ``, or the publication-lag
clause. The lag clause is guarded deliberately — without it, the next reader who measures a
lagging file repeats the identical inference.

## Memory

Corrected by supersession, nothing deleted: `agent-rescue-paths-both-assume-tmux`
(`ATOM-E9LW-C9KA`, 6 preserved bodies) and `verify-cross-repo-cited-sha-before-building`
(`ATOM-35KZ-2FDB`) — the latter because **its worked example inverted**: I had cited the
CLI-vs-spec mismatch as proof a binary cannot be trusted on governance, when the binary was
the only surface telling the truth.

## Verification

- `uv run pytest -q` → **119 passed**.
- `uv run python scripts/publish.py --gate` → exit 0, CRITICAL=0 MAJOR=0 MINOR=0 NIT=0.
- `ai-maestro#129` retitled to state R42.8 IS ratified, with the correction as a comment;
  the earlier `⚠ STOP` comment is explicitly voided there.

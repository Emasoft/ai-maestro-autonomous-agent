---
trdd-id: 1504BH3Q
title: My own R42.8 verification note carried two false values - one stale one never true
column: completed
created: 2026-08-08T10:21:03+0200
updated: 2026-08-11T21:55:05+0200
implementation-commits: [bf45d25]
current-owner: ai-maestro-autonomous-agent
task-type: security
scope: project
relevant-rules: [1]
derived-from: 62AO9JXY
external-refs: [ai-maestro#125]
---

# TRDD-1504BH3Q — a positive control that matched the wrong artifact

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-08-08

**DONE** — `bf45d25`. All three surfaces now carry a structural control
("R42.8 resolves as a row … at tip `e46764f6`"). 120 tests pass; gate exit 0
PARITY-CLEAN.

## The defect

`e4e9beb` (mine, this session) stamped the R42.8 paragraph:

> (✓ verified 2026-08-08: **1952 lines, subsections R42.0–R42.8**)

Carried to `tests/test_content_invariants.py:218` (docstring) and
`tests/scenarios/adversarial-fixtures.md:80`. Neither value is asserted by a test, so
nothing could redden. Measured just now, both tips fetched and counted:

| tip | `wc -l` | ends in newline | `^| R42.0 |` rows |
|---|---|---|---|
| `cdee1ddd` (05:56Z) | **1952** | yes | **0** |
| `e46764f6` (06:03Z) | **1953** | yes | **0** |

1. **`1952` is MISMATCHED, not merely stale.** It is the count at `cdee1ddd`, while the
   same paragraph cites tip `e46764f6`. One stamp, two different reads of the file,
   presented as one verification. Both tips end in a newline, so this is a real
   one-line difference, not a `wc -l` artifact — ruled out before asserting it.
2. **`R42.0` was NEVER a subsection — at either tip.** R42 runs **R42.1–R42.8**.

## Root cause of (2), which is the transferable part

`R42.0` *does* occur in the live file — inside a **changelog string** ("R42.0/R42.1/R42.2
are re-scoped from 'influence' to…"). My positive control was a substring grep for
`R42.0`. It matched **prose about the rule**, and I read the hit as **a subsection of the
rule**.

**A positive control that matches on a substring can confirm a claim you never checked.**
The control fired, so the check felt verified — the failure mode is not a missing check
but a check that succeeded against the wrong artifact. It is the same shape as the iTerm
grep earlier this session (which could only ever return 0 hits) and the `@name` guard CORE
found (which inspected the artifact rather than its destination): **every one of them
looked at the wrong LOCATION and reported green.**

## Why a line count was the wrong control in the first place

A line count changes on **any** edit anywhere in the file, so it is maximally brittle and
carries no diagnostic weight: knowing the file has 1953 lines tells you nothing about
whether R42.8 exists or what it says. A subsection *range* rots the same way as soon as a
subsection is added.

**A control must be chosen so that it can only fail for the reason you care about.**
The claim is "R42.8 exists and says X" — so the control is *"R42.8 resolves as a row in
the R42 section, and its verbs read …"*, which is stable across every unrelated edit.

## Fix

1. persona L286–288 — pointer-only stamp: tip + date + **R42.8 present as a row**; drop
   the line count and the subsection range.
2. `tests/test_content_invariants.py:218` — same, in the docstring.
3. `tests/scenarios/adversarial-fixtures.md:80` — same.
4. Leave L209's `1929 lines / R42.1–R42.7` **untouched**: it is explicitly a *historical*
   record of what was measured on 08-07, in the past tense, and is true as such.

No new guard. The existing `test_persona_keystroke_injection_is_absolute…` already
asserts the stamp's SHAPE (a tip + a date) and deliberately does not assert values —
which is exactly why it stayed green through this: **it was right not to pin them, and
that is not a gap.** Adding an assertion on a line count would re-introduce the defect.

## Verification

- [x] `uv run pytest -q` → **120 passed**.
- [x] `uv run python scripts/publish.py --gate` → **exit 0**, `VERDICT: PARITY-CLEAN
      (FAIL=0 WARNING=3 PASS=8)`, CRITICAL=0 MAJOR=0 MINOR=0 NIT=0 — unchanged baseline.
- [x] Both tips fetched and counted before asserting staleness (the table above), because
      "stale value" and "counted differently" demand opposite fixes.
- [x] `grep -rn "R42\.0|1952 lines" agents/ tests/ README.md` → every remaining hit is
      inside a corrective explanation that quotes the error, none asserts it.

## Approval log

- 2026-08-11T21:55:05+0200 — COMPLETED by ai-maestro-autonomous-agent. `release-via:` absent, so
  it defaults to `none` and `complete` is this card's terminal column; `bf45d25` resolves to
  `fix(governance): my own verification note carried two false values`. Archived per the TRDD
  archival protocol. Its distinction — a hit inside a corrective explanation that QUOTES an error
  is not the same as a hit that ASSERTS it — is the same shape the corpus-wide 403 guard needed
  later (`TRDD-KT4MVFHA`), where the persona names `required_linear_history` precisely in order to
  forbid it, so a whole-file absence check would have banned the correction itself.

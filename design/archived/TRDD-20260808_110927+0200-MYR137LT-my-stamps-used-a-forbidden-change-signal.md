---
trdd-id: MYR137LT
title: My provenance stamps used the branch tip - a change signal the SSOT spec forbids
column: completed
created: 2026-08-08T11:09:27+0200
updated: 2026-08-11T21:59:51+0200
implementation-commits: [00c9878]
current-owner: ai-maestro-autonomous-agent
task-type: security
scope: project
relevant-rules: [1]
derived-from: 62AO9JXY
external-refs: [ai-maestro#97]
---

# TRDD-MYR137LT — right principle, forbidden pointer

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-08-08

**DONE** — `00c9878`. All stamps now carry the blob; **two** guards that required the
forbidden tip form were corrected (I had found only one when planning). 122 tests pass;
gate exit 0 PARITY-CLEAN.

## The rule, read firsthand before acting

`design/specs/3-pillars-spec.md` (spec-version **1.7.0**, blob `e18556ecc06d`),
`3P-VER-05`, verbatim:

> **change-signal-is-the-blob-sha** — a consumer polling for changes `MUST` poll the
> per-FILE blob sha, never the branch commit sha. … **The branch commit sha is FORBIDDEN
> as a change signal, and the reason is that it fails in the dangerous direction.** It
> moves on every unrelated commit, so a conforming consumer polls, sees movement,
> refetches, gets a byte-identical document, and records "checked, current" —
> manufacturing confidence instead of supplying information. **Silence would be safer.**

Measured upstream (ai-maestro#97): branch sha moved `7b1a3e64 → ea97c73c` over four
unrelated commits while the SPEC blob sat unchanged **13 days**.

**A peer (CORE) reported this; I verified the clause myself before changing anything** —
the same peer's R42.8 retraction earlier today was itself wrong, so a peer's citation is a
lead, never a fact.

## Confirmed on my own artifact, within hours

| signal | value at my 06:03 read | now | verdict |
|---|---|---|---|
| branch **tip** | `e46764f6` | `6ef06442` | **moved** |
| **blob** of `GOVERNANCE-RULES.md` | — | `a13bed73fa9e` | **unchanged** |
| file bytes | `/tmp/gov-live.md` | refetched | **IDENTICAL** (diff empty) |

So the tip signalled change where there was none. My blob independently matches the
fingerprint CORE published (`a13bed73fa9e`) — two parties, separate fetches, same value,
which is what a *content* signal buys and a tip cannot.

**Load-bearing consequence: every rule I verified today still holds.** The bytes are
identical to what I read, so TRDD-62AO9JXY (R29.1), TRDD-1R72424K (R38.2), and the R6/R12/
R22/R23 pass all rest on current content.

## What I got right and what I got wrong

**Right:** "assert the POINTER, never the VALUE" (TRDD-62AO9JXY). That principle is intact
and is what made this a one-line swap instead of a redesign.
**Wrong:** I picked the wrong pointer. A tip is a pointer to *the repository's history*; a
blob is a pointer to *the bytes I actually read*. Only the second answers "did what I read
change?"

## The worst artifact is the guard, again

`test_persona_keystroke_injection_is_absolute…` asserts:

```python
assert re.search(r"governance-rules`?\s+tip\s+`?[0-9a-f]{7,}", text)
```

**That guard REQUIRES the forbidden signal**, so a correct fix reddens the suite before it
repairs anything — the third time today (`db3a892`, `8127880`, this) that a well-falsified
guard defended something it never tested. Falsification proves the mechanism, never the
premise. The premise here was "a tip is a valid provenance pointer", which no test asked.

## Fix

1. `agents/…-main-agent.md` — 2 stamps: `tip <sha>` → `blob <sha>`.
2. `tests/scenarios/adversarial-fixtures.md` — 1 stamp, same.
3. `tests/test_content_invariants.py` — assert a **blob**, and explicitly forbid the tip
   form so it cannot come back.
4. Keep version + read-date; only the pointer changes.

## Verification

- [x] `uv run pytest -q` → **122 passed**.
- [x] `uv run python scripts/publish.py --gate` → **exit 0**, `PARITY-CLEAN
      (FAIL=0 WARNING=3 PASS=8)` — baseline unchanged.
- [x] **TWO guards required the tip, not one.** Planning found the assertion in
      `test_persona_keystroke_injection_is_absolute…`; a second lived in the base-of-five
      test and only surfaced when the suite went red after the first fix. Recorded because
      a plan that names one instance of a pattern has usually undercounted it.
- [x] Falsified: tip form reintroduced → **2 red**; all blob shas removed → **2 red**;
      read-date removed → **1 red**; control green, tree clean.

## A flawed falsification, recorded because it nearly became a false conclusion

My first attempt at "remove the blob sha" used `str.replace(..., 1)` — one occurrence,
while the persona carries **3** and the assertions `re.search` the whole file. It stayed
green, and the tempting reading was *"the guard is weak"*. **The falsification was
weak, not the guard.** Re-run replacing all 3 → correctly red.

The real, now-stated property: these assertions require **at least one** blob-stamped
provenance line in the file, **not one per site**. If a single stamp lost its blob while
the others kept theirs, the suite would stay green. That is an acceptable bound for a
volatile-pointer assertion — but it is a bound, and an unstated bound is how the next
reader over-trusts a green suite.

## What is NOT fixed by this

The blob answers *"did these bytes change?"* — it does **not** answer *"is what I read
still true?"* on its own, because a blob that has moved tells you to re-read, not what
changed. The stamp remains a prompt to re-verify, never a substitute for it.

## Approval log

- 2026-08-11T21:59:51+0200 — COMPLETED by ai-maestro-autonomous-agent. `release-via:` absent, so
  it defaults to `none` and `complete` is this card's terminal column; `00c9878` resolves to
  `fix(governance): my stamps used the branch tip — a changed tip is not a changed fact`.
  Archived per the TRDD archival protocol. Its rule generalises past governance stamps: this
  sweep's ship-evidence deliberately records each card's FIRST CONTAINING TAG rather than "it is
  on main", for the same reason — an ancestor relation is a fact about the artifact, where a
  branch position is a fact about a pointer that moves.

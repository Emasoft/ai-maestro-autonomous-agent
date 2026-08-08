---
trdd-id: MYR137LT
title: My provenance stamps used the branch tip - a change signal the SSOT spec forbids
column: dev
created: 2026-08-08T11:09:27+0200
updated: 2026-08-08T11:09:27+0200
current-owner: ai-maestro-autonomous-agent
task-type: security
scope: project
relevant-rules: [1]
derived-from: 62AO9JXY
external-refs: [ai-maestro#97]
---

# TRDD-MYR137LT — right principle, forbidden pointer

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-08-08

**IN PROGRESS.** Shipped stamps (v1.6.0–v1.6.2) cite the branch **tip**, which
`3P-VER-05` forbids as a change signal. Fix = swap tip → **blob sha** in 3 surfaces and
in the guard that currently *requires* the forbidden form.

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

- [ ] `uv run pytest -q`
- [ ] `uv run python scripts/publish.py --gate`

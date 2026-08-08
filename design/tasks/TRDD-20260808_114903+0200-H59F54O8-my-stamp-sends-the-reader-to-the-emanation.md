---
trdd-id: H59F54O8
title: My provenance stamp sends the reader to re-fetch the emanation not the source of truth
column: dev
created: 2026-08-08T11:49:03+0200
updated: 2026-08-08T11:49:03+0200
current-owner: ai-maestro-autonomous-agent
task-type: security
scope: project
relevant-rules: [1]
derived-from: MYR137LT
---

# TRDD-H59F54O8 — the right instrument aimed at the derived artifact

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-08-08

**IN PROGRESS.** The stamp says "re-fetch `docs/GOVERNANCE-RULES.md`" — an artifact the
SSOT declares is authored **after** it. Fix = name the spec as the authority, keep the
catalog as what was actually read.

## The defect

The v4.8.0 **authority inversion** makes `design/specs/governance-spec.md` the SSOT.
From the spec's own frontmatter (spec-version **2.4.3**, blob `b1ffe5998966`):

> `authority:` **"SOURCE OF TRUTH — this SPEC is edited FIRST when a governance rule
> changes; `docs/GOVERNANCE-RULES.md` and the code/personas/DEP-overlays are its
> IMPLEMENTATIONS, authored AFTER it"**
> `implementations:` "`docs/GOVERNANCE-RULES.md` — the **PRIMARY emanation**"

My stamp (`TRDD-62AO9JXY`, hardened in `MYR137LT`) instructs:

> If this stamp is old, **re-fetch before relying on any rule below**

…and names `docs/GOVERNANCE-RULES.md`. **So a reader who obeys my instruction re-fetches
the artifact that lags by construction.** During any window where the spec has been
amended and the catalog has not, they get stale bytes with a fresh blob sha and conclude
"checked, current".

**That is precisely the failure that cost me the R42.8 reversal this morning** — I measured
a published artifact inside a 3-day lag and asserted a fact about ratification. Here I had
built the correct instrument (blob sha, `MYR137LT`) and aimed it at the derived artifact.
**A correct instrument pointed at the wrong target is not a partial fix; it reproduces the
original error with better hygiene.**

## Scope — what is NOT wrong

- The **content** is fine. Both fixes shipped today were re-verified against the SSOT this
  pass: `GOV-R29`/`R29.1` ("creates the other **4**", `@note base-count` = "5 agents
  INCLUDING the COS") and `GOV-R38`/`R38.2` ("a user may message **only** their own
  ASSISTANT, their own-team COS, and the MANAGER"). The SSOT even carries verbatim the
  principle I put in the persona: *"when a rule USES a term, the rule that DEFINES that
  term governs"*.
- The **blob-sha mechanism** is fine and stays.
- Only the **target** of the re-fetch instruction changes.

## A near-miss worth recording

Searching the SSOT for `R38.2` with a line-anchored pattern (`^\`R38\.`) returned nothing,
because the clause sits **mid-paragraph** at line 1571. The tempting conclusion was *"the
SSOT does not carry R38.2"* — which would have made today's security fix look unfounded.
Widening the search found it verbatim.

Third instance today of the same shape: **a search that inspects the wrong SHAPE reports a
confident absence** (R42.0 matched a changelog sentence; the daemon-log `tail -1` read a
rotated file; this). **An absence returned by one search pattern is a fact about the
pattern, not about the corpus.**

## Fix

1. Persona stamp: name **`design/specs/governance-spec.md` (SSOT, spec-version + blob)** as
   the re-fetch target; keep `docs/GOVERNANCE-RULES.md` labelled as the emanation actually
   read, with its own blob.
2. Guard: assert the stamp names the SSOT and labels the catalog an emanation — the
   relationship is stable; versions and blobs are not, so neither is asserted by value.

## Verification

- [ ] `uv run pytest -q`
- [ ] `uv run python scripts/publish.py --gate`

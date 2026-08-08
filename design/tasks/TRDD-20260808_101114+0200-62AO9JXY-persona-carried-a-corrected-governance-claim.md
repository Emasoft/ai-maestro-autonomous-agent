---
trdd-id: 62AO9JXY
title: The persona carried a governance claim upstream corrected 3 weeks earlier - pin was stale and unstamped
column: dev
created: 2026-08-08T10:11:14+0200
updated: 2026-08-08T10:11:14+0200
current-owner: ai-maestro-autonomous-agent
task-type: security
scope: project
relevant-rules: [1]
external-refs: [ai-maestro#125]
---

# TRDD-62AO9JXY — a stale unstamped pin carried a known-false rule for 25 days

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-08-08

**IN PROGRESS.** Two in-repo surfaces carry a governance claim that upstream corrected
on **2026-07-14**. Memory is clean (checked). Fix = correct both surfaces + stamp the
pin + guard. If this file disagrees with the live rule, **the live rule wins** —
re-fetch `docs/GOVERNANCE-RULES.md?ref=governance-rules`.

## The defect, verified here before anything was changed

`agents/…-main-agent.md:114` and `tests/scenarios/governance-scenarios.md:88` both say
the MANAGER creates a team **"auto-creating the CHIEF-OF-STAFF + 5 base members"**.

That is verbatim the text upstream deleted as **wrong twice** (changelog 5.3.3 entry
`4.2.1`, USER-authorized 2026-07-14):

- **MISCOUNT** — "COS + 5" reads as six agents; **R12.1 defines the base as FIVE
  INCLUDING the COS** (1 CHIEF-OF-STAFF, 1 ARCHITECT, 1 ORCHESTRATOR, 1 INTEGRATOR,
  1 MEMBER).
- **WRONG ACTOR** — "auto-creates" says the SYSTEM builds them all; R12.2 and R31.1 put
  that duty on the COS.

Live text now (`governance-rules` tip `e46764f6`, 2026-08-08T06:03:37Z, v5.3.3, L1303):

```
R29.1 | … Creating a team auto-creates **the CHIEF-OF-STAFF, and ONLY the
CHIEF-OF-STAFF**. The **COS** then creates the other **4** basic members
(ARCHITECT, ORCHESTRATOR, INTEGRATOR, MEMBER) — see R12.1 …
```

## Why it survived 25 days: the pin was stale AND unstamped

Persona L79 pins `GOVERNANCE-RULES.md` **v4.0.2**. Live is **v5.3.3**. The correction
landed at **v4.2.1** — *after* the pin. So the persona was internally consistent with
the version it named, and nothing ever asked whether that version was still current.

The pin names a version but records **no date and no tip**, so staleness is invisible:
there is no local artifact whose age anyone could check. **A pin without a stamp cannot
go stale — it can only be wrong.**

## This is the exact shape I had just advised a peer about

Minutes earlier I answered CORE's question about its own three-day-stale mirror,
recommending: assert the **pointer and its provenance**, never the value; enforce
freshness **offline** by the age of the local stamp. I then ran that audit on my own
tree and found this — a **25-day** miss, an order of magnitude worse than the case I
was advising on, in the *foundational* rules block.

The advice was sound and I had not applied it. That is the finding, not a footnote:
**an audit I recommend is one I have not necessarily run.**

## The propagation was already predicted upstream

The same changelog entry records what this error did the first time:

> the miscount **was laundered into the project memory corpus, where it re-read as
> independent corroboration**.

Mine reached a **second in-repo surface** (the scenario file) — the same laundering,
caught one hop earlier. **Memory checked and CLEAN** (LOCAL + PROJECT + USER greps for
the miscount: no hits). Had it landed there, the scenario file and the memory note
would have "confirmed" the persona, all three tracing to one stale copy.

## The general lesson upstream drew, which applies verbatim

> when a rule USES a term ("the 5 basic members"), the rule that DEFINES that term
> governs — a governance corpus is a system of claims, not a list, and an error in one
> rule stays invisible until two are read side by side.

## Fix

1. `agents/…-main-agent.md` L113–120 — correct R29.1 to the live text (MANAGER creates
   the team **and only the COS**; the COS creates the other **4**; base is **5
   including** the COS).
2. `agents/…-main-agent.md` L79 — replace the bare `v4.0.2` pin with a **stamped**
   pointer (version + tip + verified-at), so the next reader can date it offline.
3. `tests/scenarios/governance-scenarios.md` L88 — same correction (the laundered copy).
4. Guard — assert the **known-false form is absent** and the **stamp is present**.
   Split by stability per `ATOM-FEF6-38O0`: the base-of-5 is the *stable* claim
   (R12.1 always governed — upstream states no behavior change was intended), the
   version string is *volatile*, so the guard asserts the stamp EXISTS and never its value.

## Guard rationale — and its limit, stated because I got this wrong twice this week

A negative assertion on a known-false string is right here: "COS + 5" was **never**
correct (R12.1 always governed), so this is not a premise that can flip. But
falsification proves the MECHANISM, never the PREMISE — so the guard also carries the
tip it was read at and sends the reader to the live row.

## Verification

- [ ] `uv run pytest -q`
- [ ] `uv run python scripts/publish.py --gate`

---
trdd-id: 1R72424K
title: A non-MAESTRO user cannot reach AUTONOMOUS at all - the persona treats their order as a weighable request
column: complete
created: 2026-08-08T10:45:27+0200
updated: 2026-08-08T10:49:00+0200
implementation-commits: [7c350a8]
current-owner: ai-maestro-autonomous-agent
task-type: security
scope: project
relevant-rules: [1]
derived-from: 62AO9JXY
external-refs: [ai-maestro#125]
---

# TRDD-1R72424K — an anomalous channel described as a routine one

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-08-08

**DONE** — `7c350a8`. Citation corrected, R38.2 channel fact added, guard falsified
5 ways. 121 tests pass; gate exit 0 PARITY-CLEAN. **Unreleased** — lands in the next
version (v1.6.0 shipped before this).

## What the live rules say (v5.3.3, tip `e46764f6`, ✓ read 2026-08-08)

| rule | text (verbatim, trimmed) |
|---|---|
| R37.1 | *"The **MANAGER** role agent obeys **only the MAESTRO** user, not other users"* |
| R38.2 | *"A user may message **only** their own **ASSISTANT**, their own-team **COS**, and the **MANAGER**"* |
| R38.3 | *"Normal users are **subordinate** to MANAGER + COS"* |
| R39.5 | ASSISTANT *"obeys **no one else — not the MAESTRO user**, no other agent"* |

**Every obedience rule in this corpus is TITLE-SPECIFIC.** R37.1 names MANAGER; R39.5
names ASSISTANT; R38.3 names MANAGER + COS. **None names AUTONOMOUS.**

## What the persona claims

> **R36 / R37 — the MAESTRO and the single DELEGATE.** There is exactly **one MAESTRO
> per host**, and you obey **only the MAESTRO** (every other native or foreign user is
> subordinate to you, like any agent). … **A non-MAESTRO user's instruction is a
> *request* you weigh under normal authority** — it carries no MAESTRO privilege.

Three separate claims, three different verdicts:

1. **"exactly one MAESTRO per host"** — ✓ **CORRECT** (R36.2, verbatim).
2. **"you obey only the MAESTRO"** — **defensible behaviour, wrong citation.** R37.1
   scopes this to the MANAGER. No rule extends it to AUTONOMOUS. The conclusion is
   probably right; the persona asserts it as R36/R37 governance, which is the exact
   thing this same file forbids twelve lines earlier: *"Never tell another agent 'rule
   RNN says X' on this file's authority alone."*
3. **"every other native or foreign user is subordinate to you, like any agent"** —
   **WRONG.** R38.3 makes normal users subordinate to **MANAGER + COS**, two named
   titles. Not "any agent", and AUTONOMOUS is not among them.

## The miss that matters more than the error

**R38.2 is the rule that actually governs this case, and the persona never cites it.**
A normal user may message *only* their own ASSISTANT, their own-team COS, and the
MANAGER. **AUTONOMOUS is not on that list — so a non-MAESTRO user has no channel to me
at all.**

That inverts the correct response. The persona says such an instruction is *"a request
you weigh under normal authority"* — routine handling. But by R38.2 the message
**should not have been able to reach me**, which makes it **anomalous by construction**:
either the principal is misidentified, or something is routing around the graph. The
right response is to **verify the principal, not to weigh the request.**

This is a security weakening, not a wording nit: the persona currently instructs its
agent to engage politely with the one input shape the rules say cannot legitimately
occur. Treating an impossible channel as a normal one is how a laundered instruction
gets served.

**Scope guard:** R38.2's row is explicitly about *"Normal (non-MAESTRO) users"*. The
MAESTRO is NOT restricted by it and may reach any agent — so this changes nothing about
the MAESTRO/DELEGATE relationship or the persona's `Y` edge to HUMAN.

## Fix

1. Re-cite: **R36.2** for one-MAESTRO-per-host, **R38.2/R38.3** for the user model.
   Keep "obey only the MAESTRO" as the behaviour but mark it a **derivation**, since
   R37.1 is scoped to MANAGER — per this file's own rule about citing by substance.
2. Replace *"subordinate to you, like any agent"* with what R38.3 says (MANAGER + COS).
3. Add the operative fact: a non-MAESTRO user **has no channel to AUTONOMOUS**, so such
   a message is **anomalous — verify the principal before acting**, do not merely weigh it.
4. Guard the anomaly instruction (stable) and the citation, not the rule numbers.

## Why the audit found this and the last two did not

TRDD-62AO9JXY checked whether a rule's **content** was current. This one checks whether
the persona's claim is **entailed by the rule it cites** — a different question. A
citation can point at a rule that exists, is current, and simply does not say what the
sentence claims. **"The number resolves" is not "the rule supports the sentence."**

## Verification

- [x] `uv run pytest -q` → **121 passed**.
- [x] `uv run python scripts/publish.py --gate` → **exit 0**, `PARITY-CLEAN
      (FAIL=0 WARNING=3 PASS=8)`, CRITICAL/MAJOR/MINOR/NIT all 0 — baseline unchanged.
- [x] **Guard falsified 5 ways**, each reddening alone, control green, tree clean after:

      | broken | result |
      |---|---|
      | anomaly classification removed | FAIL |
      | "verify the principal" → "weigh it" | FAIL |
      | "You are not on that list" negated | FAIL |
      | derivation marking → "quotation" | FAIL |
      | retracted "subordinate to you, like any agent" reintroduced | FAIL |

## Audit coverage — what has now been checked, and what has NOT

Every rule the persona summarises was compared against the live text this pass:
**R26.1–.3, R27.1–.3, R28.1–.2, R29.1, R30.1, R31.1, R32.1, R33.1, R34.1, R35.1,
R36.1–.2, R37.1–.3, R38.1–.3, R39.1–.5, R40.1** — plus all 35 cited numbers resolved.
Result: **one content error (R29.1, TRDD-62AO9JXY)**, **one entailment error (this)**,
everything else correct, including the teamless-COS scoping in R26 and the
MAESTRO-exempt clause in R39.1.

**NOT checked:** R6 / R6.6 / R22 / R23 / R12.x — the persona defers the comm graph to
the `agent-messaging` skill, and the DEP overlay defining them is reachable only on the
`governance-rules` branch (`ai-maestro#118`, awaiting a ruling). Stated so the next
reader does not mistake this pass for total coverage — **an audit's silence about a
region is not a clean bill for it.**

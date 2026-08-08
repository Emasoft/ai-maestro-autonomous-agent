---
trdd-id: 1R72424K
title: A non-MAESTRO user cannot reach AUTONOMOUS at all - the persona treats their order as a weighable request
column: dev
created: 2026-08-08T10:45:27+0200
updated: 2026-08-08T10:45:27+0200
current-owner: ai-maestro-autonomous-agent
task-type: security
scope: project
relevant-rules: [1]
derived-from: 62AO9JXY
external-refs: [ai-maestro#125]
---

# TRDD-1R72424K — an anomalous channel described as a routine one

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-08-08

**IN PROGRESS.** Persona cites R36/R37 for a claim those rules do not make about
AUTONOMOUS, and misses R38.2 — the rule that actually governs the case. Behaviour is
not wrong; it is weaker than the rule allows. Fix = correct the citation, add the
channel fact, guard it.

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

- [ ] `uv run pytest -q`
- [ ] `uv run python scripts/publish.py --gate`

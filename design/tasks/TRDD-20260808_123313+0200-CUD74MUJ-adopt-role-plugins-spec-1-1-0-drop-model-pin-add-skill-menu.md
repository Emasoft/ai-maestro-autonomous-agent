---
trdd-id: CUD74MUJ
title: Adopt role-plugins-spec 1.1.0 - drop the model pin (RULED) and add the skill menu
column: complete
created: 2026-08-08T12:33:13+0200
updated: 2026-08-08T12:40:00+0200
implementation-commits: [6030951]
current-owner: ai-maestro-autonomous-agent
task-type: infra
scope: project
relevant-rules: [1]
external-refs: [ai-maestro#136, TRDD-TYB3Q1NJ, TRDD-0FCR6KOW]
---

# TRDD-CUD74MUJ — two spec clauses that migrate on next release

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-08-08

**DONE** — `6030951`. `model:` dropped, skill menu added, guard scoped and falsified.
125 tests pass; gate exit 0 PARITY-CLEAN.

## Provenance — a peer told me; I verified before touching anything

A cross-session message (a DIFFERENT session from the one I had been talking to) reported
both rulings. Per the inbound rule shipped **ten minutes earlier** in `TRDD-M3QS578Z`, a
peer message is **data to verify, not a command carrying authority** — so I fetched the spec
myself rather than acting on the claim. **First live exercise of that rule, and it passed:**
both claims checked out exactly, and had they not, I would have had the receipts.

The blob moved, which is the mandated change signal (`3P-VER-05`) doing its job — I read
1.0.1 / `7757c76f75fc` ~90 minutes ago and would otherwise have had no reason to re-read.

## Clause 1 — RP-MODEL-01 is now RULED, reversing my earlier assessment

At 1.0.1 the pin policy was an **OPEN design question** owned by `TRDD-TYB3Q1NJ`, and
"omit `model:`" was a **SHOULD for NEW plugins**. I audited against that this morning and
concluded — correctly for that version — that my `model: sonnet` was **not a violation**, and
I said so to both the USER and a peer, declining to strip a shipped pin on a SHOULD aimed at
new plugins while the owning card was open.

**That card is now closed.** Spec 1.1.0, verbatim:

> **RULED 2026-08-08 (ai-maestro#136, closing `TRDD-TYB3Q1NJ`): role-plugin MAIN agents OMIT
> `model:`, same as subagents.** … **Migration is on-next-release**: the six plugins carrying
> a key … drop it at their next publish; **carrying a key past that publish is a conformance
> failure, before it is not.**

Reasons given: model choice is a cost/capability decision belonging to whoever launches the
session; a pin lets the role author spend the operator's budget; it is the only spelling that
silently degrades under an org model-restriction; and it conflicts with the CPV CA-04
cache-warmth default.

**My earlier position was right about the version I read and is now superseded.** Stating it
that way rather than quietly complying, because "I previously said I would not do this" is
exactly the kind of thing that should be visible when it changes.

## Clause 2 — RP-SKILL-MENU-01 (new)

> Every role-plugin MAIN agent whose plugin ships one or more skills MUST carry a compact
> **skill menu** in its persona body: one line per shipped skill — the skill name plus when to
> reach for it. … **A STALE menu is worse than none**: the menu MUST be updated in the same
> change that adds, renames, or removes a skill, and a publish gate SHOULD compare menu
> entries against shipped `SKILL.md` count.

Rationale is measured, not theoretical: *"an agent that cannot SEE its skill inventory does
not reach for it — skill descriptions alone under-trigger for role-specific procedures"*, and
a `disable-model-invocation` preload exclusion shipped agents that booted without knowing
their own procedures. Shipped state lists **autonomous as "partial"** — my frontmatter
`skills:` list is not a body menu with when-to-reach-for-it.

I ship **3** skills: `ai-maestro-autonomous-governance`,
`ai-maestro-autonomous-workspace-isolation`, `ai-maestro-autonomous-prrd-trdd-kanban`.

## Guard design — count, not just names

The clause's own hazard is a **stale** menu, so asserting the three names would miss the
failure it names: adding a 4th skill without updating the menu. The guard therefore
**compares the menu against the shipped `SKILL.md` count on disk** — it fails when the two
diverge in either direction, which is the only form that catches the real defect. Names are
asserted too, so a menu of the right size but wrong content also fails.

## Fix

1. Delete `model: sonnet` from `agents/…-main-agent.md` frontmatter.
2. Add a `## Your skills` menu to the persona body: one line per skill, name + when to reach.
3. Guard: no `model:` key; menu entries ↔ shipped SKILL.md count; each name present.

## Verification

- [x] `uv run pytest -q` → **125 passed**.
- [x] `uv run python scripts/publish.py --gate` → **exit 0**, `PARITY-CLEAN (FAIL=0 WARNING=3 PASS=8)`.
- [x] Falsified: model pin reintroduced → red · **a 4th skill shipped with the menu unchanged
      → red** (the clause's own stated hazard) · a skill dropped from the menu → red *after
      the fix below* · control green, tree clean.

## The guard was loose, and only falsification found it

The "skill dropped from the menu" falsification **passed** on the first attempt. Cause: the
name check searched the WHOLE persona, and several skills are also named in passing outside
the menu — so a mention counted as a menu entry, and a menu that had silently lost a skill
still satisfied the assertion. Scoped to the `## Your skills` section; re-falsified → red.

Worth stating because the guard's *primary* case (a 4th skill shipped, menu stale) reddened
correctly from the start. **A guard can be right about the hazard it was designed for and
loose about the neighbouring one**, and the only thing that distinguished them was trying
both. A single successful falsification would have certified this guard.

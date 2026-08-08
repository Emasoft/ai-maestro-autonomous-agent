---
trdd-id: CUD74MUJ
title: Adopt role-plugins-spec 1.1.0 - drop the model pin (RULED) and add the skill menu
column: dev
created: 2026-08-08T12:33:13+0200
updated: 2026-08-08T12:33:13+0200
current-owner: ai-maestro-autonomous-agent
task-type: infra
scope: project
relevant-rules: [1]
external-refs: [ai-maestro#136, TRDD-TYB3Q1NJ, TRDD-0FCR6KOW]
---

# TRDD-CUD74MUJ — two spec clauses that migrate on next release

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-08-08

**IN PROGRESS.** `role-plugins-spec` moved 1.0.1 → **1.1.0** (blob `7757c76f75fc` →
`9fb6aa69efc7`). Two clauses bind on next publish. Fix = drop `model:` from the persona
frontmatter, add a body skill menu, guard both.

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

- [ ] `uv run pytest -q`
- [ ] `uv run python scripts/publish.py --gate`

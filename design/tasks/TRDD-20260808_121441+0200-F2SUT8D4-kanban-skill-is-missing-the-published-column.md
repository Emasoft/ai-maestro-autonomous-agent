---
trdd-id: F2SUT8D4
title: The kanban skill carries 16 of the 17 mandated columns - published is absent
column: dev
created: 2026-08-08T12:14:41+0200
updated: 2026-08-08T12:14:41+0200
current-owner: ai-maestro-autonomous-agent
task-type: bugfix
scope: project
relevant-rules: [1]
external-refs: [ai-maestro#14]
---

# TRDD-F2SUT8D4 — a missing column on the path I use every release

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-08-08

**IN PROGRESS.** `published` is absent from the kanban skill. Fix = embed the spec's
authoritative 17-column block verbatim + a guard that compares against all 17.

## The rule

`design/specs/3-pillars-spec.md` (spec-version 1.7.0, blob `e18556ecc06d`):

- `3P-KAN-01` **enum** — `MUST`: a `column:` value is **EXACTLY one of the 17** in the
  block below, **these spellings, no others**.
- `3P-KAN-03` **align-to** — `MUST`: **every consumer** (UI boards, GitHub-Project mirrors,
  `amp-kanban-*.sh`, **role-plugins**, `types/task.ts`, `types/team.ts`) aligns **TO** this
  list, never the reverse.

The spec publishes the list as a machine-extractable block
(`<!-- @spec:kanban-columns v1 — authoritative; the conformance test extracts the block
below verbatim -->`) and names its own lookup: `grep -A20 '@spec:kanban-columns'`.

## The defect

| file | distinct canonical columns | missing |
|---|---|---|
| `skills/…-prrd-trdd-kanban/SKILL.md` | **16 / 17** | **`published`** |
| `agents/…-main-agent.md` | 12 / 17 | (defers mechanics to the skill — see scope) |

No file in the plugin states the count, and none carries the complete enum.

**`published` is not an obscure corner.** `3P-KAN-04` makes it the terminal column of the
publish path: `complete → publish → published` for `release-via: publish`. **That is the
path this plugin takes on every single release — five times today (v1.6.0…v1.6.4).** The
skill describes the publish pipeline in detail at its own §"Claude Code plugin → the CPV
canonical `scripts/publish.py`" and then never names the column that pipeline terminates in.

An agent working from the skill alone can move a card to `publish` and have no vocabulary
for where it goes next — and `3P-KAN-01` forbids inventing one.

## Scope — the persona is NOT part of this fix

The persona carries 12/17, but it **defers kanban mechanics to the skill** by design (the
skill's own opening states it is self-contained precisely so it can be loaded in isolation).
Duplicating the enum into the persona would create the second disagreeing copy that
`3P-META-03` names as the drift mechanism — *"the 17-column vocabulary alone lives
duplicated across five artefacts … with no arbiter"*. **One copy, in the owner.**

## How it was found

Answering the hub's fleet questionnaire (`ai-maestro#14`, question 4: *"the kanban has
exactly 17 columns"*) with `file:line` evidence rather than re-sending my 2026-08-05 reply.
Four of the five answers verified clean; this one did not. **A questionnaire I had already
answered twice contained a question whose answer had never been checked.**

## Fix

1. Embed the spec's authoritative 17-column block **verbatim** in the kanban skill, with
   `3P-KAN-01`/`3P-KAN-03` cited and the spec's own grep recipe for re-derivation.
2. Guard: assert all 17 spellings are present in the skill. The LIST is stable (a change is
   a MAJOR spec bump by `3P-VER-01`), so it is asserted by value.

## Verification

- [ ] `uv run pytest -q`
- [ ] `uv run python scripts/publish.py --gate`

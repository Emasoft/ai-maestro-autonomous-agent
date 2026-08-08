---
trdd-id: F2SUT8D4
title: The kanban skill carries 16 of the 17 mandated columns - published is absent
column: complete
created: 2026-08-08T12:14:41+0200
updated: 2026-08-08T12:22:00+0200
implementation-commits: [859ed3e]
current-owner: ai-maestro-autonomous-agent
task-type: bugfix
scope: project
relevant-rules: [1]
external-refs: [ai-maestro#14]
---

# TRDD-F2SUT8D4 — a missing column on the path I use every release

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-08-08

**DONE** — `859ed3e`. Enum embedded verbatim from the spec block; guard falsified 3 ways.
123 tests pass; gate exit 0 PARITY-CLEAN. Answered + closed `ai-maestro-autonomous-agent#14`.

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

- [x] `uv run pytest -q` → **123 passed**.
- [x] `uv run python scripts/publish.py --gate` → **exit 0**, `PARITY-CLEAN (FAIL=0 WARNING=3 PASS=8)`.
- [x] Falsified 3 ways: every `published` removed → red; `live_auditing` removed → red;
      `3P-KAN-01` citation removed → red; control green, tree clean.

## I destroyed my own work mid-verification — recorded because the rule exists for this

The first falsification ran `git checkout` on the skill while the fix was **uncommitted**,
which reverted it. The result read as *"break → passes, restore → fails"*, i.e. exactly
inverted, and the tempting reading was that the guard was broken. **The guard was fine; I
had deleted the thing it asserts.**

Two failures, not one:
1. **I skipped commit-before-falsify.** Every earlier round today committed first precisely
   so `git checkout` restores the FIX rather than discarding it. I broke my own sequence on
   the one round where the target was a file I had only just edited.
2. **The first break was also incomplete** — it removed the enum line but left the word
   `published` in prose, so the assertion legitimately still passed. Re-run removing every
   occurrence → correctly red.

Nothing was lost (I could restore it verbatim), but that was luck about scope, not process.
**`git checkout <path>` is a destructive command against uncommitted work**, and it does not
feel like one because it is spelled like navigation.

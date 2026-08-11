---
trdd-id: 9NYI3J0X
title: Repair the kanban skill's dangling upstream references after ai-maestro-plugin v3
column: published
created: 2026-08-05T15:35:52+0200
updated: 2026-08-11T21:40:49+0200
current-owner: ai-maestro-autonomous-agent
assignee: ai-maestro-autonomous-agent
priority: 2
severity: HIGH
effort: S
labels: [bugfix, upstream-drift, skills]
task-type: bugfix
parent-trdd: null
relevant-rules: [23]
release-via: publish
test-requirements: [uv run pytest -q]
review-requirements: []
impacts: [skills/ai-maestro-autonomous-prrd-trdd-kanban/SKILL.md]
attempts: 1
last-test-result: pass
implementation-commits: [121ddc1]
external-refs: [https://github.com/Emasoft/ai-maestro/issues/61]
---

# TRDD-9NYI3J0X — the kanban skill pointed at a skill that does not exist

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-08-05

- **NEXT ACTION:** commit, then answer the GitHub threads and file the guidance issue.
- **Do NOT re-verify by memory.** Every claim below was checked against the released tags
  `ai-maestro-plugin--v3.0.3` and `--v2.11.0` via `gh api`, not against a local checkout.

## Origin

USER: "fix all issues … be sure to align with the latest changes." `ai-maestro-plugin` has
moved to **v3.0.3** — a MAJOR bump past the 2.x line this plugin was written against. ai-maestro
issue #61 reports the PROGRAMMER plugin's 3-pillars wiring pointing at a core skill that no
longer exists; the same breakage was present here and had shipped in v1.5.5.

## Findings — verified against released tags, not assumed

| Claim | Check | Result |
|---|---|---|
| `prrd-trdd-kanban` skill exists upstream | `gh api .../contents/skills?ref=ai-maestro-plugin--v3.0.3` and `--v2.11.0` | **GONE at both** — decomposed into task-scoped `ama-*` skills. The only upstream mentions left are in two ARCHIVED TRDDs, i.e. deliberate removal, not an oversight |
| `exempt-operations.md` exists | code search | **survived, MOVED** → `skills/ama-trdd-transition/references/exempt-operations.md` |
| the 5 PRRD/TRDD scripts exist | `contents/scripts?ref=…v3.0.3` | **survived, MOVED** → `scripts/prrd-trdd/`, plus a new `resolve_pillar_scripts.sh` whose whole job is locating them |
| `amama-prrd-trdd-kanban` (MANAGER layer) | `contents/skills` on `ai-maestro-assistant-manager-agent` | **GONE** — that repo ships no kanban skill at all |
| `amaa` / `amoa` / `ampa` / `amia` layers | same, 4 repos | **all 4 exist** — kept |
| our declared dependency range | `plugin.json` | **unconstrained** (`{"name": "ai-maestro-plugin"}`, no version) — see *Open question* |

So the skill declared a hard prerequisite (*"must be loaded"*) on something unloadable, and cited
a reference file at a path that had moved. An agent following it would have gone looking for a
skill that cannot be found and then improvised — the exact failure mode the pillar exists to
prevent.

## Change applied

`skills/ai-maestro-autonomous-prrd-trdd-kanban/SKILL.md`, three sites:

1. **Overview** — replaced the umbrella citation with the task-scoped successor set
   (`ama-trdd-write` / `-update` / `-transition` / `-find`, `ama-prrd-get` / `-find` / `-edit` /
   `-propose`, `ama-kanban-render`, `team-kanban`, `ama-proposal-approvals`), pinned to the tag
   the list was verified against.
2. **Prerequisites** — no umbrella skill to load; scripts are under `scripts/prrd-trdd/` and must
   be located with `resolve_pillar_scripts.sh` rather than a hard-coded path, *because the layout
   already moved once and a hard-coded path fails silently*.
3. **Resources** — exempt-operations repointed at `ama-trdd-transition`; a one-line tombstone so
   the next reader does not go hunting for the deleted skill; `amama-` dropped with its
   replacement named.

Guard: `test_kanban_skill_cites_no_upstream_skill_that_was_deleted` fails if the umbrella
citation, or the dangling MANAGER layer, comes back — and asserts the successors and the moved
paths are present. 116 tests pass.

## Open question — routed to the hub, not guessed

Our `ai-maestro-plugin` dependency carries **no version range**, while ai-maestro#14 Q2 said
"keep the pin". With upstream now at 3.0.3, the correct range is a decision about *upstream's*
compatibility promise, which this plugin cannot make for itself — asked on the ai-maestro
tracker rather than guessed. Leaving it unconstrained is the status quo and is not made worse by
this change.

## Why this class of bug is invisible without a live check

Nothing in the local repo, the test suite, or CPV validates that a skill named in prose exists in
another plugin at the version actually installed. A cross-plugin citation is just text. The only
detector is the one used here: resolve the name against the released tag over the API.

## Approval log

- 2026-08-11T21:40:49+0200 — PUBLISHED by ai-maestro-autonomous-agent. `release-via: publish`, so
  the terminal is `published`. **Evidence:** `121ddc1` is an ancestor of `v1.6.11` and first
  appears in **`ai-maestro-autonomous-agent--v1.6.0`**. Publish gate exercised under the USER's
  standing "implement all, push and publish as you wish" directive. Archived as `published`.

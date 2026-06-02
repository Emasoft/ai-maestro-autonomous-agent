---
name: ai-maestro-autonomous-prrd-trdd-kanban
description: "AUTONOMOUS's role in the PRRD / TRDD / Kanban workflow. AUTONOMOUS works solo (no team, no COS). It owns ALL columns for its own TRDDs — authoring proto-TRDDs, designing them, implementing, testing, deploying / publishing, and auditing. Use when AUTONOMOUS is operating independently of any team."
allowed-tools: "Bash(python3:*), Bash(get-prrd.py:*), Bash(prrd-edit.py:*), Bash(findprrd.py:*), Bash(findtrdd.py:*), Bash(kanban.py:*), Bash(git:*), Bash(gh:*), Bash(amp-send:*), Read, Edit, Write, Grep, Glob"
metadata:
  author: "Emasoft"
  version: "1.0.0"
---

## Overview

The AUTONOMOUS (AIMAA) role-specific layer of the PRRD / TRDD / Kanban
model. AUTONOMOUS works solo — no team, no CHIEF-OF-STAFF. It owns ALL
columns for its own TRDDs, playing MANAGER, ORCHESTRATOR, ARCHITECT,
INTEGRATOR, and MEMBER for its own work. The only role it cannot play
is HUMAN: USER substitutes for MANAGER on every non-exempt approval.
For universal mechanics, see the `prrd-trdd-kanban` skill in
`ai-maestro-plugin`.

## Prerequisites

The universal `prrd-trdd-kanban` skill (in `ai-maestro-plugin`) must be
loaded — it carries the shared mechanics. The project needs a PRRD and a
`design/tasks/` tree of TRDDs. For solo PRRD edits and direct approval,
the session uses `$AID_AUTH` or the `--user` flag rather than a
`--manager` check.

## Instructions

1. Author proto-TRDDs in `backburner` / `todo`, then design them in
   `design` and split or group as ARCHITECT would — all for your own
   TRDDs.
2. Dispatch (`dispatch`), implement (`dev`), and test (`testing`) your
   own TRDDs, then move them through `ai_review`.
3. For EXEMPT operations (per the universal `exempt-operations.md`), act
   directly with no approval request.
4. For NON-EXEMPT operations — `complete → publish`, `complete → deploy`,
   PR merge, force-`failed`, `ai_review → human_review` — request USER
   approval DIRECTLY via `amp-send` to USER (R6.6: AUTONOMOUS reaches
   HUMAN directly, no COS hop). Record USER's reply verbatim in the
   TRDD's `## Approval log`.
5. `human_review` ALWAYS requires USER — never self-approve it.
6. Mutate your own project's silver PRRD rules with the `--user` flag:
   `prrd-edit.py --user add silver "..."`, `prrd-edit.py --user revise N
   "..."`, `prrd-edit.py --user delete N`. Golden-rule promotion/demotion
   needs USER (or a governance AMP from MANAGER if one exists).
7. Spawn DEPLOYER / RELEASER subagents for deploy / publish the same way
   INTEGRATOR does, via the Agent tool (`subagent_type="deployer"` /
   `"releaser"`).
8. Self-broadcast transitions — the AMP recipient is AUTONOMOUS itself,
   or optionally a peer AUTONOMOUS for visibility.

## Output

- TRDD edits moving your own cards across ALL columns (`backburner`
  through `live_auditing`, plus `blocked` / `failed` / `superseded`).
- USER approval-requests via `amp-send`, with replies logged verbatim in
  each TRDD's `## Approval log`.
- PRRD silver-rule edits committed via `prrd-edit.py --user`.
- Subagent dispatch records for DEPLOYER / RELEASER runs.

## Error Handling

- AI Maestro server or a `*.py` helper unreachable → degrade gracefully:
  fall back to the manual git / `gh` path, do not invent state.
- Any golden-rule change, or unilateral promote/demote → STOP and route
  to USER only; AUTONOMOUS may not decide it alone.
- Unsure whether an operation is exempt, or who can unblock a `blocked`
  TRDD → ask USER directly via `amp-send`; never guess.

## Examples

- Ship a feature: design → dev → testing → `ai_review`, then AMP USER
  for `complete → publish`; on approval, spawn the RELEASER subagent and
  log USER's reply in the TRDD.
- Tighten a workflow rule: `prrd-edit.py --user add silver "PRs require
  green CI"` — applied directly, no MANAGER check needed.

## Resources

For the shared mechanics, column transitions, and the authoritative
exempt-operations list, consult the universal `prrd-trdd-kanban` skill
and its `exempt-operations.md` reference, both bundled in
`ai-maestro-plugin`. For the per-column checklists that AUTONOMOUS reuses,
consult the other role layers: `amama-prrd-trdd-kanban` for authoring and
promotion, `amaa-prrd-trdd-kanban` for design and split / group,
`amoa-prrd-trdd-kanban` for dispatch and the red column,
`ampa-prrd-trdd-kanban` for implementation and testing, and
`amia-prrd-trdd-kanban` for ai_review and ship. Each role's checklist
applies, simplified because AUTONOMOUS runs as a single session with no
inter-agent AMP coordination.

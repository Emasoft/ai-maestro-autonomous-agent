---
name: ai-maestro-autonomous-prrd-trdd-kanban
description: "AUTONOMOUS's role in the PRRD / TRDD / Kanban workflow. AUTONOMOUS works solo (no team, no COS). It owns ALL columns for its own TRDDs — authoring proto-TRDDs, designing them, implementing, testing, deploying / publishing, and auditing. Use when AUTONOMOUS is operating independently of any team."
allowed-tools: "Bash(python3:*), Bash(get-prrd.py:*), Bash(prrd-edit.py:*), Bash(findprrd.py:*), Bash(findtrdd.py:*), Bash(kanban.py:*), Bash(git:*), Bash(gh:*), Bash(amp-send:*), Read, Edit, Write, Grep, Glob"
metadata:
  author: "Emasoft"
  version: "1.0.0"
---

## Overview

This is the AUTONOMOUS role-specific layer of the PRRD / TRDD / Kanban
model. For universal mechanics, see `prrd-trdd-kanban` in
`ai-maestro-plugin`.

## Approval discipline — USER substitutes for MANAGER

Check
[references/exempt-operations.md](references/exempt-operations.md)
in the universal skill. AUTONOMOUS owns ALL columns for its own
TRDDs, so the same exempt categories apply. For **non-exempt**
operations, AUTONOMOUS's approval chain short-circuits to USER (per
R6.6 — AUTONOMOUS reaches HUMAN directly, no COS hop). Examples
needing USER approval: `complete → publish` / `complete → deploy`,
PR merge, force-`failed`, `ai_review → human_review`. The
approval-request AMP goes directly to USER; the
`## Approval log` section in the TRDD body records USER's reply
verbatim.

AUTONOMOUS operates without a team and without a CHIEF-OF-STAFF gate.
Per R6 v2/v3, AUTONOMOUS reaches MANAGER + peer AUTONOMOUS + HUMAN
directly (no COS hop). For the PRRD/TRDD/kanban workflow, this means
AUTONOMOUS performs ALL roles itself for its own TRDDs.

AUTONOMOUS is essentially a one-person team where the same agent
plays MANAGER, ORCHESTRATOR, ARCHITECT, INTEGRATOR, and MEMBER for
its own work. The only role it can't play is HUMAN (USER).

## Columns AUTONOMOUS owns

ALL columns, for its own TRDDs:
`backburner`, `todo`, `design`, `dispatch`, `dev`, `testing`,
`ai_review`, `human_review`, `complete`, `publish`, `published`,
`deploy`, `live`, `live_auditing`, `blocked`, `failed`, `superseded`.

There is one exception: `human_review` always requires the USER.
AUTONOMOUS cannot self-approve human review. Use AMP-direct-to-USER
(governance-layer edge per R6.6) when human review is required.

## Transitions AUTONOMOUS triggers

All of them. See `column-transitions.md` for the full list. AUTONOMOUS
self-broadcasts (the AMP recipient is just AUTONOMOUS itself or
optionally peer AUTONOMOUS for visibility).

## PRRD authority

AUTONOMOUS can mutate silver rules of its own project's PRRD
directly:

```bash
prrd-edit.py --user add silver "..."     # use --user, NOT --manager check
prrd-edit.py --user revise N "..."
prrd-edit.py --user delete N
```

Golden rules of an AUTONOMOUS project come from one of:

- The human owner of the project setting them initially
- A peer AUTONOMOUS proposing via AMP (rare)
- The MANAGER reviewing if this project was previously team-managed

AUTONOMOUS cannot promote/demote rules unilaterally — that requires
USER (or an AMP-routed governance decision from MANAGER if applicable).

## Special protocols for solo work

### Subagent dispatch for deploy / publish

AUTONOMOUS can spawn the DEPLOYER and RELEASER subagents the same way
INTEGRATOR does — via Claude Code's Agent tool:

```python
result = Agent(
    subagent_type="deployer",
    description=f"Deploy TRDD-{trdd.uid8}",
    prompt="<deploy instructions>"
)
```

The same subagent definitions ship in the AI Maestro plugin set, so
AUTONOMOUS sessions also have access (if the plugins are installed).

### Communicating with USER

When AUTONOMOUS needs USER input:

- `human_review` column: AMP-send to USER (allowed per R6.6 for
  governance layer)
- Golden-rule decisions: AMP-send to USER directly
- Blocked TRDDs with no other unblocker: AMP-send to USER

### Communicating with MANAGER (if a MANAGER exists)

In some setups AUTONOMOUS coexists with a host-level MANAGER. In that
case, AUTONOMOUS can AMP MANAGER for:

- Cross-project coordination
- Borrowing a team's expertise (MANAGER may delegate)
- Approval for operations spanning the AUTONOMOUS scope

## Per-column checklists (abridged)

AUTONOMOUS uses the same checklists as the relevant role-specific
skills:

- For authoring + promotion: see `amama-prrd-trdd-kanban`
- For design + split/group: see `amaa-prrd-trdd-kanban`
- For dispatch + red column: see `amoa-prrd-trdd-kanban`
- For implementation + testing: see `ampa-prrd-trdd-kanban`
- For ai_review + ship: see `amia-prrd-trdd-kanban`

Each role's checklists apply, with the simplification that AUTONOMOUS
doesn't need AMP coordination (it's a single session).

## Resources

- Universal skill: `prrd-trdd-kanban`
- Existing AUTONOMOUS skills: `ai-maestro-autonomous-governance`,
  `ai-maestro-autonomous-workspace-isolation`
- AUTONOMOUS persona: `agents/ai-maestro-autonomous-agent-main-agent.md`

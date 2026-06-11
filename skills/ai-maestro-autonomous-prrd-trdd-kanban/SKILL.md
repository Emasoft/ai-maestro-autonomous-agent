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
loaded — it carries the shared mechanics. The PRRD/TRDD scripts
(`get-prrd.py`, `prrd-edit.py`, `findprrd.py`, `findtrdd.py`, `kanban.py`)
ship in `ai-maestro-plugin` — this plugin declares that dependency in its
`plugin.json`. The project needs a PRRD and a `design/tasks/` tree of TRDDs.
For solo PRRD edits and direct approval, the session authorizes itself with
`$AID_AUTH` (resolved against the AI Maestro server) or the `--user` flag
rather than a `--manager` check.

**AID_AUTH fallback.** When `$AID_AUTH` is unset or cannot be resolved —
e.g. you are running outside AI Maestro with no server reachable — fall back
to `--user`: for a solo AUTONOMOUS project the local human user IS the
manager, so `prrd-edit.py --user …` is the correct authorization path. Never
fabricate a manager token to satisfy `caller_is_manager()`; use `--user` and
let the human own the decision.

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
7. Run the deploy / publish stage with the pipeline that matches the
   PROJECT TYPE — there is no single universal release path. INTEGRATOR
   normally designs / sets this up per project; solo, you select it from
   the project kind (`publish.py` auto-detects six: claude-plugin, python,
   nodejs, rust, go, bash):
   - **Claude Code plugin** → the CPV canonical `scripts/publish.py`
     (auto-detect → test → lint → CPV `--strict` → consistency → bump →
     changelog → commit → push → GitHub release). This is the ONLY kind
     `publish.py` is authoritative for; for every other kind it is a
     recommendation, not a mandate.
   - **Library / package** (python→PyPI, node→npm, rust→crates.io,
     go→module tag) → build + test + tag + publish to the registry.
   - **Application** → build + sign + package + attach release artifacts.
   - **Service** → containerize + push image + deploy to the target env,
     then soak in `live_auditing` before declaring `live`.
   Dispatch a general-purpose subagent via the Agent tool (or run the steps
   inline) for the DEPLOYER / RELEASER role work — this plugin bundles no
   dedicated deployer/releaser agent. **The USER may mandate ANY custom
   pipeline** (a bespoke CI workflow, a signing flow, a staged rollout);
   when the USER specifies one, follow it exactly and treat the defaults
   above as overridden.
8. Self-broadcast transitions — the AMP recipient is AUTONOMOUS itself,
   or optionally a peer AUTONOMOUS for visibility.

## Solo dialog-loop substitutes (run against the USER, or MANAGER via AMP)

A team's comprehension handshake, in-dev issue dialog, and pre-PR gate have
no ORCH / ARCH / INT to hold them with when you run solo. Substitute:

1. **Comprehension self-handshake (before `dev`).** Restate to the assigner:
   the task in your own words, the files / domains you will touch, any
   ambiguities, the risks you foresee, and the NPT / EHT you anticipate. Wait
   for ambiguities to clear; bounce a design-flawed task back to the
   USER / MANAGER instead of improvising around the flaw.
2. **In-dev issue dialog (during `dev` / `testing`).** Surface any blocker to
   the assigner the moment it appears; resolve CI / merge issues yourself
   (you are your own INTEGRATOR), escalate design issues.
3. **Pre-PR self-check gate (before opening a PR / before `ai_review →
   complete`).** Copy this checklist and track your progress; proceed only
   when every item is YES:
   - [ ] Re-read every file I changed; the diff matches the TRDD's intent.
   - [ ] All `test-requirements:` ran and passed (`last-test-result: pass`).
   - [ ] Lint + typecheck clean; CPV `--strict` exit 0 (for plugin projects).
   - [ ] Every acceptance criterion in the TRDD / issue is met.
   - [ ] No EHT child is still open (EHTs are post-conditions of `complete`).
   - [ ] The self-id line leads every GitHub comment / AMP body I will post.

**The `ai_review → complete` flip is not self-granted on reflex.** In a team
the INTEGRATOR validates the merged work before `completed`; nobody self-marks
completed. Solo, flip your own TRDD to `complete` only after the pre-PR
self-check passes AND — for any NON-EXEMPT transition — the USER confirms
(MANAGER validates when MANAGER assigned the work). Exempt / internal work uses
the checklist alone as the gate.

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

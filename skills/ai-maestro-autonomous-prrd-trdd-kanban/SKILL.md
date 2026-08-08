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

**Rule numbers here are as-of-authoring POINTERS, not facts you may assert.**
The governance source is versioned and revisable, so a renumber or a revision
drifts this file silently — and a number resolving is not the same as the rule
supporting the sentence. Cite a rule by its **substance**; if a number fails to
resolve or contradicts this text, **the live governance source governs** — re-read
it. Never tell another agent "rule RNN says X" on this file's authority alone.

**This skill is self-contained: it carries AUTONOMOUS POLICY, and it does
not defer its mechanics to another skill.** That is deliberate — skills
load on demand and in isolation, so a layer whose content is "the real
rules live over there" resolves to nothing when it is the only thing
loaded, and the agent improvises exactly the governance it was supposed to
follow. Everything binding on you is below; the skills named next are
tools you invoke, not a prerequisite you must read first.

`ai-maestro-plugin` no longer ships one `prrd-trdd-kanban` skill — it was
decomposed into task-scoped skills, so invoke the one that matches the
operation: `ama-trdd-write` (author),
`ama-trdd-update` (edit), `ama-trdd-transition` (move a column — it owns
the transition matrix), `ama-trdd-find` / `ama-prrd-find` / `ama-prrd-get`
(look up), `ama-prrd-edit` / `ama-prrd-propose` (rules),
`ama-kanban-render` / `team-kanban` (render the board), and
`ama-proposal-approvals` (the approval queue). Verified against
`ai-maestro-plugin--v3.0.3`.

**Every board/PRRD operation that reaches the AI Maestro server goes
through the frozen CLI (R23)** — the `*.py` helpers named in
`allowed-tools` above, plus `aimaestro-agent.sh` / `aimaestro-teams.sh`.
**Never call a server HTTP route (`/api/*`) directly**, with any client:
the CLI runs the approval and audit gates a raw route bypasses, so a
direct call can land a column change that no approval log records. Binds hooks and scripts too, and routes that only look read-only.

## Prerequisites

**Nothing here is gated on loading another skill.** Invoke the task-scoped
`ama-*` skill for the operation you are performing (listed in the
Overview) when you need to perform it — that is a tool call, not a
precondition for understanding the policy below. The
PRRD/TRDD scripts (`get-prrd.py`, `prrd-edit.py`, `findprrd.py`,
`findtrdd.py`, `kanban.py`) still ship in `ai-maestro-plugin`, but under
its scripts/prrd-trdd directory; resolve their absolute paths with that
directory's
`resolve_pillar_scripts.sh` rather than hard-coding a location, because the
layout moved once already and a hard-coded path fails silently. This plugin
declares the `ai-maestro-plugin` dependency in its `plugin.json`. The
project needs a PRRD and a `design/tasks/` tree of TRDDs.
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
6. Mutate your own project's silver PRRD rules per the approval tier. A SILVER
   PRRD change is **Tier-2 when a MANAGER is reachable**: file a `proposal` and
   AMP the request straight to MANAGER over your `Y` edge, who approves and
   promotes it — do NOT self-authorize. The `prrd-edit.py --user` path is the
   **TRUE-SOLO fallback ONLY** — use it solely when `$AID_AUTH` is unresolvable
   AND the AI Maestro server is unreachable (the solo/offline case where the
   local human IS the manager, per the Prerequisites "AID_AUTH fallback"):
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
- PRRD silver-rule edits — a Tier-2 proposal to MANAGER when reachable, or
  `prrd-edit.py --user` only in the true-solo fallback (`$AID_AUTH` AND server
  both unreachable).
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
- Tighten a workflow rule (TRUE-SOLO / offline only): `prrd-edit.py --user
  add silver "PRs require green CI"` — applied directly because `$AID_AUTH`
  and the server are both unreachable, so the local human IS the manager. In
  ecosystem mode with a reachable MANAGER, the SAME silver change is Tier-2:
  file a proposal and AMP MANAGER for approval first — do not self-authorize.

## Resources

The column-transition matrix and the authoritative exempt-operations list
both live in the **ama-trdd-transition** skill bundled in
`ai-maestro-plugin` — the list is that skill's own `exempt-operations.md`
reference file. Paths are deliberately not written here: it is another
plugin's tree, so a path would be both unresolvable from this repo and
stale the next time upstream moves it. (The list used to hang off a
`prrd-trdd-kanban` skill; that skill no longer exists at any released
tag, so do not look for it.)

For the per-column checklists that AUTONOMOUS reuses, consult the other
role layers: `amaa-prrd-trdd-kanban` (architect) for design and split /
group, `amoa-prrd-trdd-kanban` (orchestrator) for dispatch and the red
column, `ampa-prrd-trdd-kanban` (programmer) for implementation and
testing, and `amia-prrd-trdd-kanban` (integrator) for ai_review and ship.
Each role's checklist applies, simplified because AUTONOMOUS runs as a
single session with no inter-agent AMP coordination. There is no
MANAGER-side layer to cite: `ai-maestro-assistant-manager-agent` ships no
kanban skill, so authoring and promotion have no sibling checklist —
use the `ama-trdd-write` / `ama-prrd-propose` core skills instead.

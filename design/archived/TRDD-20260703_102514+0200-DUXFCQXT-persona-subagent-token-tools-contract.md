---
trdd-id: DUXFCQXT
title: Persona sub-agent-spawn instructions must inject the token-saving-tools contract not just memory
column: completed
created: 2026-07-03T10:25:14+0200
updated: 2026-08-11T20:34:49+0200
current-owner: ai-maestro-autonomous-agent
assignee: ai-maestro-autonomous-agent
priority: 4
severity: LOW
effort: S
labels: [code-review, persona, token-efficiency]
task-type: docs
parent-trdd: null
relevant-rules: []
release-via: none
test-requirements: []
review-requirements: [code-review]
impacts: []
attempts: 1
last-test-result: not-run
implementation-commits: [a318308]
external-refs: []
---

# TRDD-DUXFCQXT — Persona sub-agent injection: add the token-tools contract

## Origin

`/code-review max --fix` re-run (task `wmgl5kvbs`, the token-efficiency angle
left unfinished by w9dtmt0a2). 13 agents, 1 surviving finding after adversarial
verify (3 test-micro-I/O candidates correctly refuted as negligible).

## Finding (CONFIRMED) + fix

`agents/ai-maestro-autonomous-agent-main-agent.md` told the main agent, at BOTH
the Memory-protocol "Propagate to sub-agents" bullet (line 633) and Startup-
checklist item #5 (line 700), to inject ONLY the memory recall/write contract
into spawned sub-agents — while asserting "sub-agents inherit NOTHING". That is
internally inconsistent: if sub-agents inherit nothing and therefore need the
memory contract injected, they equally need the **token-saving-tools contract**
(lean-ctx `ctx_*` over Read/Grep/Shell, `distill` on non-interactive shell
output, `tldr` for scoped reads) that the repo `CLAUDE.md` + `workflows-rules.md`
mandate. Omitting it means every spawned sub-agent runs context-inflating shell
(whole-file `cat`, un-distilled `git diff`) and returns verbose blobs → inflates
the main agent's context → the token-runaway class this very session hit.

Fix (commit `a318308`): the canonical bullet (633) now enumerates BOTH
inheritance-critical contracts with the concrete token-tool mapping + the WHY;
the checklist (700) cross-references it (single source of truth, no duplication).

## Verification

Doc-only change (no runtime/test surface). The `**Propagate to sub-agents**`
cross-reference target exists. Grep confirmed these are the only two sub-agent-
spawn instruction sites in the persona.

## Note

This was the ONLY actionable survivor of the token-efficiency review — the broad
"token-wasting across the codebase" mandate produced no other verified defect,
which is itself a signal the codebase is largely clean on that axis.

## Approval log

- 2026-08-11T20:34:49+0200 — COMPLETED by ai-maestro-autonomous-agent. `release-via: none`, so
  `complete` is this card's terminal column; work landed in `a318308`. Archived per the TRDD
  archival protocol.

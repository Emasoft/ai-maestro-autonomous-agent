---
trdd-id: e7281b7e-31f6-4740-a7f0-fed48f0ba3be
title: Fleet-readiness deep audit (issue #6) — close governance gaps M1–M12
column: planned
created: 2026-06-11T11:14:46+0200
updated: 2026-06-11T11:14:46+0200
current-owner: aimaa
assignee: aimaa
priority: 1
severity: HIGH
effort: L
labels: [governance, audit-fix, release, r6-v3]
task-type: docs
parent-trdd: null
npt: []
eht: []
blocked-by: []
relevant-rules: [1]
release-via: publish
delivery: direct-push
target-branch: main
must-pass-tests-before-merge: true
publish-target: ai-maestro-plugins
publish-channel: stable
test-requirements: [unit, lint, typecheck]
audit-requirements: []
review-requirements: [human-review]
runtime-targets: [macos, linux]
impacts: [ci-pipeline]
attempts: 0
last-test-result: not-run
implementation-commits: []
external-refs: ["github.com/Emasoft/ai-maestro-autonomous-agent/issues/6"]
---

# TRDD-e7281b7e — Fleet-readiness deep audit (issue #6): close governance gaps M1–M12

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-06-11

**Source of work:** GitHub issue #6 (MANAGER's component-level governance audit of
this repo at v1.2.0). USER authorized implementation ("read the github issues and
implement/fix all pending"). Publishing is pre-authorized by #6's acceptance criteria
("version bumped + published") and the USER's directive — logged in `## Approval log`.

**Current state:** authoring fixes. Working tree was clean at `6ed0999` (v1.2.0).

**NEXT ACTION:** execute Phase 1 (M6: purge all R6 v2 citations → v3).

**Load-bearing facts / gotchas:**
- R6 **v3** model (the delta the docs must encode): COS guards the TEAM BOUNDARY only;
  within-team ORCH↔ARCH/INT/MEMBER are DIRECT edges; **MANAGER reaches team-internal
  agents only via COS** — so "MANAGER has full Y to every node" (persona:265-268) is
  FALSE under v3 and must be corrected. AUTONOMOUS's own edges are UNCHANGED (Y to
  MANAGER / peer-AUTONOMOUS / HUMAN; everything else transits MANAGER).
- `check_version_consistency()` (publish.py:1031) scans plugin.json + pyproject +
  `__version__` in .py — NOT README/persona. It runs at Step 6 **before** the bump, so
  README/persona must equal the CURRENT version (1.2.0) at check time; `do_bump()` must
  ALSO update them so the next bump keeps them in sync. Otherwise the next publish
  self-deadlocks.
- plugin.json `dependencies` must be an **array of strings** (validate_marketplace.py:497).
  → `"dependencies": ["ai-maestro-plugin"]` covers all 3 soft deps (PRRD/TRDD scripts,
  agent-messaging, prrd-trdd-kanban universal skill) with one declaration.
- `prrd-version` is the PRRD rule-doc version (major.minor of the ruleset) — NOT the
  plugin release version. Do not conflate them.

**SUPERSEDED — do NOT carry forward:**
- ✗ Audit M3 claim "all 4 zones exist but 0 files" — INACCURATE. The zones did NOT
  exist at audit time (only `design/requirements/`). Created in this TRDD.

**Durable artifacts to read before acting:**
- Issue #6 body (fetched to /tmp/issue6.json).
- `~/.claude/rules/trdd-approval-tiers.md` (R6 v3, 4-zone lifecycle, tiers).
- `~/.claude/rules/prrd-design-rules.md` (PRRD format, project-id, SILVER).

## Plan (priority order from issue #6)

| # | Item | Files | Status |
|---|------|-------|--------|
| 1 | **M6** purge R6 v2→v3 (6 cites + README) | persona, questions.md, README | pending |
| 2 | **M7** solo-mode loop substitutes (self-handshake, pre-PR self-check, ai_review→complete approver) | persona, kanban SKILL | pending |
| 3 | **M11** version sync (README/persona → 1.2.0) + publish.py enforces it | README, persona, publish.py | pending |
| 4 | **M2** PRRD `project-id: autonomous` + real SILVER rules + bump prrd-version | PRRD | pending |
| 4 | **M3** 4 design zones (done) + author v2 TRDDs for shipped work | design/ | partial |
| 5 | **M8** project-type-specific pipelines + USER override | kanban SKILL, persona | pending |
| 5 | **M9** peer-AUTONOMOUS same-repo claim protocol | persona/governance | pending |
| 5 | **M10** AMP-body self-id + reusable AMP templates | governance SKILL | pending |
| 5 | **M1** plugin.json `dependencies: [ai-maestro-plugin]` | plugin.json | pending |
| 5 | **M4** document AID_AUTH fallback | kanban SKILL | pending |
| 5 | **M12** tests for governance/workspace-isolation/kanban skills; justify bundled validators | tests/ | pending |
| 6 | validate (ruff/mypy/pytest + CPV strict) → publish.py --minor (→1.3.0) → reply on #6 | — | pending |

Verdicts ✓ (no change): M5 (kanban skill keep), M13.

## Approval log

- 2026-06-11T11:14:46+0200 — Authored as `planned` (Tier 0: in-scope governance work on
  THIS project, USER-authorized). `complete → publish` is pre-authorized by USER's
  "implement/fix all pending" directive + issue #6 acceptance criteria ("version bumped +
  published"). No separate MANAGER sign-off needed — the USER (who outranks MANAGER) gave
  the order directly.

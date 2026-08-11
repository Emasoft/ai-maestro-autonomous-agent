---
trdd-id: NHYCSFRZ
title: Add real behavior tests for smart_exec.py + gitignore_filter.py + workspace-isolation content guard
column: published
created: 2026-07-01T18:22:38+0200
updated: 2026-08-11T21:27:00+0200
current-owner: aimaa-autonomous
assignee: aimaa-autonomous
priority: 4
severity: LOW
effort: M
task-type: feature
parent-trdd: null
npt: []
eht: []
blocked-by: []
supersedes: [TRDD-AXI79CXE]
relevant-rules: []
release-via: publish
delivery: direct-push
target-branch: main
must-pass-tests-before-merge: true
test-requirements: [unit, lint, typecheck]
audit-requirements: []
review-requirements: []
runtime-targets: [macos, linux]
impacts: []
attempts: 1
test-failures: 0
last-test-result: pass
implementation-commits: [8b4d200]
external-refs: ["reports/go-on-yourself-eval/20260701_181031+0200-test-coverage.md"]
---

# TRDD-NHYCSFRZ — Behavior tests for the untested helper scripts + workspace-isolation guard

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-07-01

- **Surfaced by** the go-on-yourself test-coverage evaluation (2026-07-01): suite is
  green (25/25 real) but 3 helper scripts are **import-only** (byte-compile + import,
  ZERO behavior asserted) and the workspace-isolation skill's content is unguarded.
- **DONE (2026-07-01):** added test_smart_exec.py (15), test_gitignore_filter.py (6),
  test_workspace_isolation_content.py (3) — all real/no-mock; suite 30→55 pass;
  ruff + mypy clean; CPV `--strict` 0/0/0/0 (WARNING=7, unchanged). Awaiting v1.5.4 ship.
- **Tier-0** — adds tests only; strengthens the quality gate, relaxes nothing.
  Reversible + local.
- **Supersedes TRDD-AXI79CXE** — the fork authored a duplicate test-coverage-gaps
  TRDD the same turn; this one (more actionable) absorbs it. Two of AXI79CXE's items
  are consciously OUT OF SCOPE here: **(4) the 4 orphan `tests/fixtures/memory/*.md`** —
  memory recall is the GLOBAL janitor system, so a recall test here would test the
  janitor's memgrep, violating "plugin tests are the plugin's job"; disposition =
  LEAVE + surface to USER (do NOT wire a foreign-code test, do NOT blind-delete a
  committed fixture). **(5) `cpv_validation_common.py`** — import-smoke suffices
  (78 KB vendored from CPV upstream, which owns its behavior tests).

## Why

`smart_exec.py`'s ~20 pure argv-builder functions decide HOW every external tool is
invoked at publish time — a wrong argv silently mis-invokes a tool with a green
suite. `gitignore_filter.py` decides WHICH files get packaged/published — a
filtering regression ships or drops the wrong files, green suite. Both are
import-only today. The workspace-isolation skill (the plugin's namesake behavior)
has only a generic present/desc/links check, unlike the other two skills which have
content-invariant guards. These are the cheapest, highest-value missing tests.

## Scope — 3 NEW test files (disjoint from all other in-flight work)

Create NEW files (do NOT edit existing test files — avoids collision with parallel
tasks): `tests/test_smart_exec.py`, `tests/test_gitignore_filter.py`,
`tests/test_workspace_isolation_content.py`. All tests REAL (no mocks) — import the
actual modules / read the actual skill file and assert live behavior.

1. **`tests/test_smart_exec.py`** — import `scripts/smart_exec.py`; test the
   DETERMINISTIC, side-effect-free functions (a wrong output = broken publish):
   - the argv builders: `bunx_argv`, `pnpm_dlx_argv`, `yarn_dlx_argv`, `npx_argv`,
     `npm_exec_argv`, `deno_npm_argv`, `uvx_argv`, `pipx_run_argv`,
     `deno_builtin_argv`, `docker_argv` — assert exact argv for a representative
     input incl. the `latest`/version-pin branch where present.
   - `ps_quote` (PowerShell single-quote escaping — assert the doubled-quote rule),
     `powershell_module_argv`.
   - `resolve_tool` (returns a ToolSpec for a known tool name), `choose_best` and
     `build_argv_for_executor` for one representative executor.
   Target ~12-16 focused tests total — cover each function family + the version-pin
   edge; do NOT write 30 tests per function.

2. **`tests/test_gitignore_filter.py`** — build a small fixture tree under
   `tmp_path` with a `.gitignore` (e.g. ignore `*.log`, `build/`, keep `src/`),
   instantiate `GitignoreFilter(tmp_path)`, and assert:
   `is_ignored` (a `*.log` file True, a `src/x.py` False), `is_dir_ignored`
   (`build/` True), and that `walk` / `rglob` / `iterdir` exclude the ignored paths
   and include the kept ones. ~5-7 tests.

3. **`tests/test_workspace_isolation_content.py`** — read
   `skills/ai-maestro-autonomous-workspace-isolation/SKILL.md` (+ `references/layers.md`)
   and assert its load-bearing isolation invariants are present (robust token
   asserts, matching the `test_content_invariants.py` style): e.g. the writable-scope
   rule / no cross-agent state mutation / worktree scoping. ~2-3 tests. FIRST read the
   actual skill text and key the asserts on tokens it really contains — do not invent
   an invariant it does not state.

## Verification (all must pass before `complete`)

- `uv run --with pytest pytest tests/ -q` green; NEW tests counted (30 → ~45+).
- Each new test FAILS if its guarded behavior regresses (verify smart_exec/gitignore
  tests by construction; spot-check one by temporarily breaking an argv locally, then
  reverting — do NOT commit the break).
- `uv run --with ruff ruff check tests/` clean; `mypy` clean (test dir is in the set).
- No source edits to `scripts/` — tests only; CPV `--strict` unaffected.

## Approval log

- 2026-07-01T18:22:38+0200 — Authored directly in `design/tasks/` as Tier-0
  (test-only; strengthens the quality gate). Shipping in a release (v1.5.4) is a
  separate Tier-2 publish gate surfaced to USER/MANAGER.
- 2026-08-11T21:27:00+0200 — PUBLISHED by ai-maestro-autonomous-agent. `release-via: publish`, so
  the terminal is `published`. **Evidence:** `8b4d200` is an ancestor of `v1.6.11` and first
  appears in **`ai-maestro-autonomous-agent--v1.5.4`** — the release anticipated above. Publish
  gate exercised under the USER's standing "implement all, push and publish as you wish"
  directive. Archived as `published` per the TRDD archival protocol.

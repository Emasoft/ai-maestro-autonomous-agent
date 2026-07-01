---
trdd-id: AXI79CXE
title: Close the import-only test-coverage gaps — smart_exec, gitignore_filter, workspace-isolation, orphan fixtures
column: superseded
created: 2026-07-01T18:23:02+0200
updated: 2026-07-01T18:31:27+0200
current-owner: aimaa-autonomous
assignee: null
superseded-by: [TRDD-NHYCSFRZ]
priority: 5
severity: LOW
effort: M
task-type: feature
parent-trdd: null
npt: []
eht: []
blocked-by: []
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
attempts: 0
test-failures: 0
last-test-result: not-run
implementation-commits: []
external-refs: ["reports/go-on-yourself-eval/20260701_181031+0200-test-coverage.md"]
---

# TRDD-AXI79CXE — Close the import-only test-coverage gaps

## ⏵ SUPERSEDED — 2026-07-01

Superseded by **TRDD-NHYCSFRZ** (a near-identical test-coverage-gaps TRDD authored
the same eval turn — this one and NHYCSFRZ were created within seconds of each
other, one by the phantom fork, one by the orchestrator). NHYCSFRZ carries the
active, more-actionable spec (exact new test files + function lists + counts) for
the 3 core gaps and absorbs this TRDD's items 4–5 as explicitly noted out-of-scope.
Archived, not deleted, per the supersede protocol.

## Why

The go-on-yourself evaluation (2026-07-01) found the suite green + 100% real, with strong
coverage of the agent + 2 of 3 skills + publish.py's version logic. It also found genuine
PRE-EXISTING coverage debt: three helper scripts are import-only (byte-compile + import,
no behavior asserted) and one skill + a fixture set are unguarded. These were DEFERRED (not
fixed in the eval turn) to respect scope discipline; this TRDD tracks them so they are not
lost. All are Tier-0 (test-only, no runtime-behavior change).

## Scope (ranked by value; each is cheap + deterministic)

1. **`scripts/smart_exec.py` — ~20 pure argv-builder functions untested (HIGHEST value).**
   `bunx_argv`, `pnpm_dlx_argv`, `yarn_dlx_argv`, `npx_argv`, `npm_exec_argv`,
   `deno_npm_argv`, `uvx_argv`, `pipx_run_argv`, `docker_argv`, `ps_quote`,
   `powershell_module_argv`, `resolve_tool`, `build_argv_for_executor`, `choose_best`,
   `detect_executors`. Side-effect-free, table-driven → the cheapest possible unit tests.
   A wrong argv silently mis-invokes a tool at publish time. Add input→expected-argv tests.
2. **`scripts/gitignore_filter.py` — filtering behavior untested.** `is_ignored` /
   `is_dir_ignored` / `walk` decide WHAT gets packaged/published; a regression ships or
   drops the wrong files with a green suite. Add a fixture-tree + expected-set test.
3. **`workspace-isolation` skill — content-invariant guard missing.** The other two skills
   have content guards in `test_content_invariants.py`; the namesake skill has only the
   generic present/desc/links check. Add a guard for its load-bearing isolation rules
   (no cross-agent state mutation, worktree scoping).
4. **Orphan fixtures `tests/fixtures/memory/*.md` (4 files) consumed by ZERO test.** Staged
   for a memory-recall test never written. PREFER INTEGRATE OVER DELETE: wire a real recall
   test that consumes them; only if that is infeasible, remove them. Do NOT delete blindly.
5. **`scripts/cpv_validation_common.py` — import-only (SOFT).** 78 KB, vendored from CPV
   upstream (upstream owns its behavior tests); locally only import-reachability matters.
   Lowest priority — likely leave as import-smoke.

## Notes
- TDD where the code is new; here it is characterization/regression testing of existing
  pure functions — assert real input→output, no mocks (project convention).
- Consider parallel agents (one per script) once the fork mechanism is reliable again;
  this turn's forks errored `inside a forked worker` on the concurrent batch.

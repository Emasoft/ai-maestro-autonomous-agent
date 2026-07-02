---
trdd-id: V7HJ492I
title: Fix 3 code-review w9dtmt0a2 findings — smart_exec deno dispatch x2 + gitignore anchored-dir leak
column: testing
created: 2026-07-03T01:51:24+0200
updated: 2026-07-03T01:51:24+0200
current-owner: ai-maestro-autonomous-agent
assignee: ai-maestro-autonomous-agent
priority: 3
severity: MEDIUM
effort: S
labels: [code-review, bugfix, smart-exec, gitignore]
task-type: bugfix
parent-trdd: null
npt: []
eht: []
blocked-by: []
supersedes: []
superseded-by: []
relevant-rules: []
release-via: none
delivery: direct-push
target-branch: main
test-requirements: [unit]
audit-requirements: []
review-requirements: [code-review]
runtime-targets: [macos, linux]
impacts: []
attempts: 1
test-failures: 0
last-test-result: partial
last-test-at: 2026-07-03T01:51:24+0200
implementation-commits: [3e55ace, e2706db]
external-refs: []
---

# TRDD-V7HJ492I — Fix 3 code-review w9dtmt0a2 findings

**Filename:** `design/tasks/TRDD-20260703_015124+0200-V7HJ492I-code-review-w9dtmt0a2-fixes.md`
**Tracked in:** this repo (design/tasks/ is git-tracked)

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-07-03

- **Current state:** all 3 findings FIXED + COMMITTED + VERIFIED. Only the
  regression-test EHT remains.
  - #1 smart_exec deno_builtin direct fast-path guard → commit `3e55ace`
  - #2 smart_exec deno_npm `cmd==pkg` stray-positional → commit `3e55ace`
  - #3 gitignore anchored-dir nested-file leak (root cause in
    `is_path_gitignored`) → commit `e2706db`, ad-hoc verified 9/9 cases PASS.
- **NEXT ACTION:** add exactly 3 regression tests (one per finding), extending
  the EXISTING test files — `tests/test_smart_exec.py` (#1, #2) and
  `tests/test_gitignore_filter.py` (#3). Then run the suite; on green →
  `column: complete`.
- **Load-bearing facts:**
  - The fixes intentionally PRESERVE the direct fast-path for python/node/native
    (real PATH binaries); only `deno_builtin` (Deno subcommands like fmt/lint/
    check that collide with coreutils) and `powershell_module` (cmdlets) are
    gated out of it.
  - The gitignore fix is in the PREDICATE `is_path_gitignored`
    (`scripts/cpv_validation_common.py`), NOT in `rglob` — so it fixes rglob,
    iterdir, and is_ignored transitively (single source of truth). `walk()`
    was never affected (it prunes ignored dirs via `is_dir_ignored` before
    descending); `rglob()` enumerates every descendant directly and relied
    solely on the predicate.
- **SUPERSEDED — do NOT carry forward:** the summary's earlier framing that #3
  lived at `gitignore_filter.py:115` — ✗ that is the SYMPTOM site; the ROOT
  CAUSE and the fix are in `cpv_validation_common.py::is_path_gitignored`
  (anchored branch).
- **Durable artifacts:** the fixes' WHY lives in the code comments at each site
  and in the two commit messages (`3e55ace`, `e2706db`).

## Origin

Findings came from the `/code-review max --fix` run, task `w9dtmt0a2`
("scan the whole codebase for token-wasting / cache-inefficiency / bash
commands skipping lean-ctx/distill/tldr-code"). The verifier confirmed 3
distinct code-correctness findings; the token-efficiency angle of the scan
was NOT completed (finders rate/session-limited — see Open items).

## The 3 findings

### #1 — smart_exec `choose_best` direct fast-path had no ecosystem guard
`scripts/smart_exec.py`. The unconditional "direct" fast-path ran the tool's
`command` as a standalone PATH binary. For `deno_builtin` tools whose command
is a Deno SUBCOMMAND (`fmt`/`lint`/`check`), `have("fmt")` matched coreutils
`fmt` → ran text-reflow instead of `deno fmt`. Fix: gate `deno_builtin` and
`powershell_module` out of the fast-path (their `command` is not a real
binary); keep it for python/node/native. Verified against source.

### #2 — smart_exec `deno_npm_argv` appended a stray positional when cmd==pkg
`scripts/smart_exec.py`. `deno run npm:<pkg>` already invokes the default bin;
unconditionally appending `-- <cmd>` passed the bin name as a stray positional
(e.g. eslint treated `eslint` as a lint target). Every sibling builder
(npx/bunx/pnpm/yarn) already had the `cmd==pkg` guard; this one lacked it.
Fix: add the same `cmd==pkg` special-case. Verified against source.

### #3 — gitignore anchored-directory patterns leaked nested files
`scripts/cpv_validation_common.py::is_path_gitignored`. The anchored branch did
ONLY a full-path `fnmatch`, so an anchored directory pattern like `/reports_dev/`
matched only the dir entry `reports_dev`, NOT the nested file
`reports_dev/foo.py`. `walk()` masked this (it prunes ignored dirs before
descending); `rglob()` (which enumerates all descendants and filters each path
individually) yielded gitignored nested files as if tracked. Failure scenario:
a validator/publish path using `rglob` reads a leaked `reports_dev/*.py` and
mis-scans it (false version-mismatch abort, or private report content pulled
into a scan). Fix: the anchored branch now also matches any ancestor-directory
prefix (progressive leading prefixes preserve the anchor — `sub/reports_dev/x`
is still NOT matched by `reports_dev`). Root-cause fix in the predicate fixes
rglob/iterdir/is_ignored at once. Verified 9/9 cases (fixed, dir-entry,
deep-nested, anchor-preserved, no-false-positive, multi-segment, non-anchored
unchanged, glob unchanged, file-pattern unchanged).

## Open items

- **EHT (pending):** 3 regression tests, one per finding, extending the two
  existing test files. Delegated authorization: `/code-review --fix` (Tier-0,
  own-project mechanical work).
- **Token-efficiency review angle INCOMPLETE:** the original w9dtmt0a2 scan's
  broader mandate (token-wasting / cache-inefficiency / lean-ctx-skipping bash)
  was defeated by rate/session limits — only the 3 code-correctness findings
  survived verification. Offer a fresh re-run when limits clear.

---
trdd-id: P8QK3ZTR
title: Update the publish pipeline via CPV — fix the missing dependency-resolution tag
column: complete
created: 2026-07-21T22:35:19+0200
updated: 2026-07-21T22:35:19+0200
current-owner: ai-maestro-autonomous-agent
assignee: ai-maestro-autonomous-agent
priority: 2
severity: HIGH
effort: M
labels: [pipeline, cpv, dependency-resolution, ci]
task-type: infra
parent-trdd: null
npt: []
eht: []
blocked-by: []
relevant-rules: []
release-via: publish
delivery: direct-push
target-branch: main
test-requirements: [unit, lint]
review-requirements: []
runtime-targets: [macos, linux]
impacts: [ci-pipeline, release-pipeline]
attempts: 1
test-failures: 0
last-test-result: pass
last-test-at: 2026-07-21T22:35:19+0200
implementation-commits: [f255127]
external-refs: ["github.com/Emasoft/claude-plugins-validation/issues/171", "TRDD-TVM7Q4XK", "TRDD-5c21e4a0"]
---

# TRDD-P8QK3ZTR — CPV-driven publish-pipeline update

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-07-21

- **DONE.** Commit `f255127`. USER instruction was explicit: *"you must use the cpv
  plugin to update the publish pipeline"* — so this was driven through
  `cpv-remote-validate standardize . --fix`, not hand-edited.
- **NEXT ACTION:** none in-repo. One residual is USER-gated: backfill the
  `ai-maestro-autonomous-agent--v1.5.3` tag (`RC-DEP-TAG-MISSING`), which needs a push.

## The defect this surfaced (the reason the TRDD exists)

`RC-DEP-TAG-PIPELINE` — **`publish.py` tagged releases only as `v{version}`, never as
`ai-maestro-autonomous-agent--v{version}`.**

Since Claude Code 2.1.110 a version-constrained dependency on this plugin is resolved by
listing this repo's tags, keeping ONLY those prefixed `<plugin>--v`, and taking the
highest match. The plain `vX.Y.Z` tag is **ignored by that resolver**. So every plugin
declaring a version-constrained dependency on this one would fail to install with
`no-matching-tag` and be **DISABLED**.

It is invisible from the depending side — an already-installed dependent keeps working —
which is how it survived **18 releases**. Note the separator is a DOUBLE hyphen (`--v`);
the single-hyphen form matches the resolver's prefix filter and is silently useless.

## What was applied

- **publish.py** — the resolver-tag stage, built from the MANIFEST name (never the
  directory name, so renaming the checkout cannot desync it) and pushed in the **same
  atomic push** as the release tag, so a release can never ship one ref without the other.
- **`validate.yml` → `ci.yml`** — canon merged them in v2.12.32. The replacement is
  strictly better: top-level *and* per-job `permissions`, `timeout-minutes` on every job,
  every action SHA-pinned, plus actionlint, MegaLinter, commitlint and zizmor.
- CPV pre-push 4-gate hook (`git-hooks/pre-push` → `publish.py --gate`), and
  commitlint / cspell / jscpd / mega-linter configs.

## What was deliberately NOT done

**No `--force-templates`.** Canon's `publish.py` is 278 lines; ours is 1805 with custom
version-sync logic — a force-template would regress ~1500 lines. CPV's own warning
cautions against exactly this, and TRDD-5c21e4a0 (USER-ratified) forbids it. The surgical
`--fix` was verified purely additive: **1735 → 1805 lines with exactly ONE line removed**
— the old lone `git push origin v{ver}`, superseded by the atomic two-ref push.

## Regression the fixer itself introduced (found and fixed)

`standardize --fix` generated a `.cspell.json` whose `monkeypatch` entry trips CPV's own
`skillaudit TOOL_SHADOW` detector as a tool redefinition — a **blocking MAJOR**, taking a
clean repo from `0/0/0/0` to `MAJOR=1`. The word is genuinely used by
`tests/test_smart_exec.py`, so deleting it would only trade TOOL_SHADOW for a SPELL
failure — the two gates conflict for any such word. Moved it to an inline
`# cspell:ignore` directive: both gates pass, **no security rule suppressed**.
Reported upstream as claude-plugins-validation#171 (CPV bug, not ours — we do not edit
another project's tree).

## Verification

- 83 tests pass; `tests/test_workflow_hardening.py` generalized to glob ALL workflows so
  the new `ci.yml` is covered automatically, plus a guard asserting the dependency-tag
  stage stays in publish.py.
- Corrected an over-strict rule of my own while here: a blanket "no `${{ }}` inside
  `run:`" flagged canon's `${{ matrix.group }}` / `${{ needs.*.result }}`, which are
  GitHub-generated and **not** attacker-controllable. Now an untrusted-source check
  (`github.event` / `head_ref` / `inputs`) across all workflows, plus the strict
  zero-interpolation rule on the two workflows this repo authors.
- `ruff` clean. `cpv-remote-validate --strict` **EXIT=0, CRITICAL=0 MAJOR=0 MINOR=0
  NIT=0** (WARNING=9, all non-blocking).

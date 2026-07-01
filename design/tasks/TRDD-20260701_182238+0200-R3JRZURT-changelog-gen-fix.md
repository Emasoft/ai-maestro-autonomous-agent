---
trdd-id: R3JRZURT
title: Fix CHANGELOG generation — full tag history + correct heading render
column: backburner
created: 2026-07-01T18:22:38+0200
updated: 2026-07-01T18:37:23+0200
current-owner: aimaa-autonomous
assignee: aimaa-autonomous
priority: 4
severity: MINOR
effort: S
task-type: bugfix
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
external-refs: ["reports/go-on-yourself-eval/20260701_181208+0200-docs-governance.md"]
---

# TRDD-R3JRZURT — Fix CHANGELOG generation (full history + heading render)

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-07-01

- **Surfaced by** the go-on-yourself docs-governance evaluation (2026-07-01). A
  three-way inconsistency: `publish.py` docstring says the CHANGELOG walks full
  tag history, but the actual invocation restricts it to `--unreleased`, and the
  file header claims "all notable changes" while only 1 of 18 releases is present.
- **HELD — awaiting approval (2026-07-01).** During the go-on-yourself run an
  unsupervised spark applied the `publish.py` part of this fix; the orchestrator
  **REVERTED it** — editing the release pipeline (under issue #11's USER-ratified
  ahead-of-canon exception, TRDD-5c21e4a0) is *escalate-when-unsure* → treat as
  Tier-2, do NOT auto-apply. The reverted diff is saved at
  `reports/go-on-yourself-eval/publish-py-spark-uncommitted.patch` for reference.
- **NEXT ACTION (after USER/MANAGER approval):** apply the 3 source fixes below,
  regenerate artifacts, add the guard test, run suite + lint + CPV, commit.
- Parked in `backburner` until that approval; the plan below is complete + ready.

## Why

`CHANGELOG.md` documents only `## [1.5.3]` while `git tag` shows 18 releases — 17
released versions are undocumented, contradicting the file's own header AND the
`run_git_cliff` docstring. Root cause is two publish-time generator bugs; fixing
them there prevents recurrence on every future release.

## The defects (both VERIFIED against live source)

- **B1 — `--unreleased` on the CHANGELOG call restricts it to latest-only.**
  `scripts/publish.py::run_git_cliff` (~L841-850) runs
  `git-cliff --bump --unreleased --tag vX.Y.Z -o CHANGELOG.md`. The `--unreleased`
  flag (L845) + `-o` overwrite regenerates the file latest-only. The **docstring
  (L825-832) already describes the correct intent** (full tag history), so the
  code contradicts its own doc.
  **Fix:** remove `--unreleased` (and the now-stale `--bump`/`--tag` combination
  only if a dry-run shows it is needed for the top section — verify empirically)
  from the **line-841 CHANGELOG call** so git-cliff walks full history.
  **KEEP `--unreleased` on the second, release-notes call (~L858-865)** — GitHub
  release notes are intentionally latest-only; that usage is correct. Reconcile
  the docstring L827 wording to match the corrected flag set.

- **B2 — cliff.toml body template indents headings, breaking markdown render.**
  The `body` template prefixes `## [..]`, `### ..` with 4 literal spaces and `- ..`
  with 8, so `CHANGELOG.md` headings render as indented-code / lazy-paragraph, not
  headings. The template lives in TWO places that must stay in sync:
  - the committed **`cliff.toml`** `body` (~L10-19), AND
  - **`scripts/publish.py::ensure_cliff_config`** embedded default `body`
    (~L778-782) — the source a fresh checkout regenerates from.
  **Fix both:** remove the leading indentation so headings render as proper
  markdown. Tera whitespace control is finicky — **dry-run `git-cliff` and inspect
  the rendered output** to confirm clean headings before finalizing the template.

## Derived tasks (consequences of the change)

1. **Regenerate the artifacts** once the generator is fixed: rewrite `cliff.toml`
   to the corrected template, then regenerate `CHANGELOG.md` via the corrected
   full-history invocation. Verify by eye: multiple `## [x.y.z]` version sections,
   all rendering as headings. If a leading `## [Unreleased]` section appears for
   the post-v1.5.3 commits, that is acceptable (Keep-a-Changelog convention) — but
   confirm it renders correctly.
2. **Guard test** (real, no-mock; add to `tests/test_publish_version_sync.py` — the
   established publish-behavior test home, no file-overlap with parallel work):
   assert `run_git_cliff`'s CHANGELOG-generation call does NOT contain
   `--unreleased` while the release-notes call DOES (source-level assert on
   `scripts/publish.py`), and that `cliff.toml`'s `body` has no leading-indented
   `## [` heading line. TDD: write it to fail on current source, then fix.
3. **Docstring** — reconcile `run_git_cliff` docstring to the corrected flags.

## Verification (all must pass before `complete`)

- `uv run --with pytest pytest tests/ -q` green (new guard included).
- `uv run --with ruff ruff check scripts/publish.py tests/` clean; `mypy` clean.
- `git-cliff` dry-run renders a full-history CHANGELOG with proper headings.
- CPV `--strict` still `CRITICAL=0 MAJOR=0 MINOR=0 NIT=0` (WARNING count unchanged).

## Approval log

- 2026-07-01T18:22:38+0200 — Authored directly in `design/tasks/` as Tier-0
  (bugfix to the plugin's own tooling; no governance/ruleset change). Shipping in a
  release (v1.5.4) is a separate Tier-2 publish gate surfaced to USER/MANAGER.

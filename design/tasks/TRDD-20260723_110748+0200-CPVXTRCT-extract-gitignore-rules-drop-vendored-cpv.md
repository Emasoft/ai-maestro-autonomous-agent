---
trdd-id: CPVXTRCT
title: Extract the 2 used gitignore functions to gitignore_rules.py; delete the vendored cpv_validation_common + smart_exec pair
column: complete
created: 2026-07-23T11:07:48+0200
updated: 2026-07-23T11:07:48+0200
current-owner: ai-maestro-autonomous-agent
task-type: refactor
scope: project
relevant-rules: [2, 3]
implementation-commits: []
external-refs: [Emasoft/claude-plugins-validation#172]
---

## Problem

`scripts/cpv_validation_common.py` was an 80 KB / 2320-line file vendored from CPV.
Verified dependency graph: the release pipeline used it ONLY for two pure functions
(`is_path_gitignored`, `parse_gitignore`, imported by `gitignore_filter.py`).
`publish.py` imports NEITHER `cpv_validation_common` NOR `smart_exec` (stdlib-only;
it shells tools directly). `smart_exec.py`'s only importer was
`cpv_validation_common.py:46` (`resolve_tool_command`, which nothing reachable
calls). So the whole vendored pair was dead weight, and it dragged a bandit **B108**
false-positive (hardcoded-tmp in `ALLOWED_DOC_PATH_PREFIXES`) that is CPV#172.

## Fix (decision: EXTRACT — over `depend` or `delete-anyway`)

- **Why not `depend`** (import the 2 funcs from an installed CPV): `publish.py` is the
  sole release path (PRRD S2.1) and must run standalone — a runtime dep on CPV being
  importable is a fragility. Rejected.
- **Why not `delete-anyway`:** needlessly breaks working gitignore logic. Rejected.
- **EXTRACT (done):** new `scripts/gitignore_rules.py` carries the two functions
  byte-for-byte (free names verified: `Path`, `fnmatch`, `re`, and each other — no
  other in-file deps). `gitignore_filter.py` imports from it. `git rm`'d the vendored
  pair + their dead-code tests (`test_doc_path_prefixes.py` guarded the deleted
  B108 constant; `test_smart_exec.py` tested the deleted module). Updated
  `test_validators_invocable.py` (KEEP_SET → {publish, gitignore_filter,
  gitignore_rules}; vestigial guard asserts both deletions stay gone) and
  `test_gitignore_filter.py` (import repoint).

Net: −~2500 LOC of vendored code, B108/CPV#172 removed at root, chain reduced to
publish.py → gitignore_filter → gitignore_rules. `relevant-rules`: S2.1 (standalone
release path), S3.1 (tests updated, no mock).

## Verification (all done)

- Full suite: 94 passed (was 115; −21 = the two deleted dead-code test modules, 0 failures).
- `mypy scripts/`: Success, 3 files. `bandit -r scripts/`: 0 High/Medium; **B108 = 0** (was the CPV#172 root); remaining 43 Low are standard subprocess findings in publish.py.
- All deletions recoverable via git history (git rm, tracked).

## Acceptance criteria

- gitignore_filter imports the 2 funcs from gitignore_rules; behavior unchanged.
- cpv_validation_common.py + smart_exec.py deleted and guarded against reappearance.
- B108 absent; suite green; `publish.py --gate` EXIT=0.

## Approval log

- 2026-07-23 — USER: "delete cpv_validation_common.py" (earlier) + "evaluate the choices
  above and decide yourself. go on". Decided EXTRACT on verified facts (only 2 funcs used;
  publish.py imports neither vendored file). Authorized; done in `design/tasks/`.

## Follow-up note

`smart_exec` was already effectively orphaned before this change (its only importer was the
vendored file); removed here as part of the same no-ghosts cleanup. No further action.

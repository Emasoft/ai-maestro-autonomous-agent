# Changelog

All notable changes to this project will be documented in this file.
## [Unreleased]

### Bug Fixes

- Correct status→column field + drop deprecated MEMORY.md-index line (TRDD-81RC6IXC)
- Clear CPV --strict SHELL_EXEC false-positive in governance note

### Documentation

- Close TRDD-270ef961 published v1.5.3; record CLAUDE_PRIVATE_USERNAMES canon trap
- Record fleet re-ask #11 reconciliation + one-shot canon-clean recipe (publish-pipeline [^4])
- Fix #12 audit — gate silver-PRRD --user, add startup carve-outs (TRDD-7c4f9ea4)
- Record implementation-commit cd063ea on TRDD-7c4f9ea4 (backtracking)
- Add governance-audit-handling note (verify-HEAD-first + fix-vs-publish split)
- Add TRDD-QJ30E8TD — regression guards for issue-12 governance fixes
- Add TRDD-81RC6IXC — persona currency fixes (impl 4710380)
- Add TRDD-AXI79CXE — backburner test-coverage gaps (go-on-yourself eval)
- Record the guard-with-each-governance-fix lesson (go-on-yourself eval)
- Add TRDD-R3JRZURT (changelog-gen fix) + TRDD-NHYCSFRZ (script behavior tests)
- Supersede TRDD-AXI79CXE via TRDD-NHYCSFRZ (duplicate test-coverage TRDD)
- Park R3JRZURT changelog-gen fix -- Tier-2 publish.py change reverted pending approval
- Capture the fork-delegation-under-autonomous-directive lesson
- Correct issue-11 "ahead-of-canon" premise — it is INVERTED (TRDD-TVM7Q4XK)
- Cite CONSOLIDATED eval report from TVM7Q4XK + capture-map (report->TRDD)
- Wire reciprocal back-links to fork-delegation note (LINK LAW)
- Add TRDD-V7HJ492I for 3 code-review w9dtmt0a2 findings and fixes, impl-commits 3e55ace e2706db, Agent ai-maestro-autonomous-agent
- Flip TRDD-V7HJ492I to complete, 3 regression tests landed f81f501 suite green, Agent ai-maestro-autonomous-agent
- Add TRDD-DUXFCQXT for code-review wmgl5kvbs finding and fix, impl-commit a318308, Agent ai-maestro-autonomous-agent
- Sync plugin guidance to Claude Code 2.1.181-2.1.200 (TRDD-BFDQH5A7)
- Add TRDD-BFDQH5A7 for CC 2.1.181-2.1.200 sync, impl-commit b2dd4d2, Agent ai-maestro-autonomous-agent

### Miscellaneous

- Finalize QJ30E8TD state — complete, impl 84b4ca8
- Finalize NHYCSFRZ backtracking -- implementation-commits 8b4d200

### Security

- Port canon workflow hardening into release + notify-marketplace (TRDD-TVM7Q4XK)
- Update publish pipeline via CPV standardize --fix (TRDD-TVM7Q4XK)

### Tests

- Guard the issue-12 fixes in test_content_invariants (TRDD-QJ30E8TD)
- Real behavior tests for smart_exec + gitignore_filter + workspace-isolation (TRDD-NHYCSFRZ)
- 3 regression tests for code-review w9dtmt0a2 findings plus correct stale deno_npm expectation left red by 3e55ace, 25 passed, TRDD-V7HJ492I, Agent ai-maestro-autonomous-agent

## [1.5.3] - 2026-06-20

### Bug Fixes

- Drop CLAUDE_PRIVATE_USERNAMES from validate steps — it flagged the owner (TRDD-270ef961)

### Miscellaneous

- V1.5.3

## [1.5.2] - 2026-06-20

### Documentation

- Archive TRDD-5c21e4a0 — SHA-pin 3rd-party actions, published v1.5.1
- Record CPV devitalization recurrence trap (v1.5.1)
- Propose CPV canon ADDITIVE reliability subset (TRDD-270ef961)
- Record CPV --force-templates / ahead-of-canon trap (publish-pipeline [^2])

### Miscellaneous

- Re-ignore .claude/project/memory/*-proposed.md
- V1.5.2

### Ci

- Pin CPV ref @v2.136.1 + harden validate steps (TRDD-270ef961)

## [1.5.1] - 2026-06-20

### Bug Fixes

- SHA-pin third-party GitHub Actions (TRDD-5c21e4a0)
- Devitalize skillaudit:privilege_escalation false-positives

### Documentation

- Archive TRDD-81869520 — governance R26-R40 published v1.5.0 (#9)
- Record CPV --strict false-positive shapes (slash-lists, sudo+password)

### Miscellaneous

- V1.5.1

## [1.5.0] - 2026-06-18

### Documentation

- Archive TRDD-fc155c40 — /api decoupling published v1.4.1 (#8)
- Propagate governance R26-R40 into persona + skills + scenarios (#9)

### Miscellaneous

- V1.5.0

## [1.4.1] - 2026-06-18

### Documentation

- Archive TRDD-b48aa385 — global memory adopted + published v1.4.0
- Seed publish-pipeline PROJECT note (pre-push hook → publish.py)
- Proposal TRDD-5c21e4a0 — RC-PIPELINE-DRIFT-001 (Tier-2, awaiting decision)

### Miscellaneous

- V1.4.1

### Refactor

- Decouple executable /api/* -> frozen aimaestro-*.sh CLI verbs (R23, #8)

## [1.4.0] - 2026-06-15

### Documentation

- Record Claude Code currency review + validator prune (v1.3.3)

### Features

- Adopt global janitor-hosted 3-scope memory; drop per-plugin system

### Miscellaneous

- V1.4.0

## [1.3.3] - 2026-06-11

### Documentation

- Mark fleet-readiness audit (#6) completed → archived

### Miscellaneous

- Prune vestigial bundled CPV validators; object-form deps
- V1.3.3

## [1.3.2] - 2026-06-11

### Bug Fixes

- Stop update_readme_version eating the README blank line
- Stage README + persona in the Step-11 release commit

### Miscellaneous

- V1.3.2

## [1.3.1] - 2026-06-11

### Bug Fixes

- Bump README + persona in the LIVE Step-9 path

### Miscellaneous

- V1.3.1

## [1.3.0] - 2026-06-11

### Features

- Close fleet-readiness audit gaps M1–M12 (#6)

### Miscellaneous

- V1.3.0

## [1.2.0] - 2026-06-09

### Bug Fixes

- Replace broken references/ link with universal-skill prose pointer
- Restructure ai-maestro-autonomous-prrd-trdd-kanban to CPV 7-section format (<5000)
- Remove ghost deployer/releaser subagent dispatch from kanban skill
- Devitalize scanner-signature shapes for CPV strict (9 findings → 0)
- Plugin description now reflects the 5 bundled skills

### Documentation

- Approval tiers + lifecycle + baseline governance; memory wiring (#4, #5)

### Features

- Add AUTONOMOUS's PRRD/TRDD/Kanban layer
- Add Approval discipline section to ai-maestro-autonomous-prrd-trdd-kanban
- Bootstrap PRRD with G1 GitHub self-id golden rule
- Align with Claude Code v2.1.81–v2.1.143 plugin contract (v1.1.0)
- Adopt the markdown memory system (#5)

### Miscellaneous

- Add .tldrignore for TLDR code indexer
- Bump version to 1.2.0
- V1.2.0

## [1.0.8] - 2026-04-26

### Bug Fixes

- Strip #anchor before referenced-file existence check

### Miscellaneous

- V1.0.8

### Styling

- Code-fence external server refs and add 2 example blocks

## [1.0.7] - 2026-04-22

### Bug Fixes

- POST GitHub release via curl -4 in Step 14
- Try gh first, fall back to curl -4 in Step 14

### Miscellaneous

- V1.0.6
- V1.0.7

## [1.0.5] - 2026-04-22

### Miscellaneous

- Ignore /.rechecker/ runtime state
- V1.0.5

## [1.0.4] - 2026-04-22

### Bug Fixes

- Stage uv.lock in Step 11 release commit (closes #3)

### Miscellaneous

- Update uv.lock
- V1.0.4

## [1.0.3] - 2026-04-22

### Documentation

- Sync R6 v2 comm graph (AUTONOMOUS row) — closes #1 (#2)

### Miscellaneous

- Update uv.lock
- V1.0.3

### Styling

- Sort imports (ruff I001)
- Sort imports (ruff I001)

## [1.0.2] - 2026-04-15

### Bug Fixes

- Type git() return as CompletedProcess[str]

### Miscellaneous

- V1.0.2

## [1.0.1] - 2026-04-15

### Bug Fixes

- Address 25 strict-validation findings from plugin-fixer
- Add ## Overview, numbered Instructions, reference TOCs, .python-version
- Progressive disclosure — move full Q1-Q10 and Layer tables to references
- Convert backtick ref mentions to markdown links; inline full TOCs
- Trim SKILL.md Overview/Examples sections for size
- Consolidate reference files to reduce TOC-embed burden
- Restore questions.md content lost to a placeholder overwrite
- Add input/output example pairs in governance SKILL.md
- Switch governance examples to code-fenced format

### Features

- Initial ai-maestro-autonomous-agent plugin v1.0.0

### Miscellaneous

- Update uv.lock
- V1.0.1



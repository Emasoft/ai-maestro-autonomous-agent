# Changelog

All notable changes to this project will be documented in this file.

## [1.6.3] - 2026-08-08

### Bug Fixes

- **governance:** My stamps used the branch tip — a change signal the SSOT FORBIDS (TRDD-MYR137LT) (00c9878)

### Documentation

- Close TRDD-MYR137LT — two guards required the tip, and one falsification was itself flawed (049b1ad)
## [1.6.2] - 2026-08-08

### Bug Fixes

- **skills:** Skills cited rule numbers as fact with no deferral to the live source (TRDD-MW5L9N10) (abbfb39)

### Documentation

- Close TRDD-MW5L9N10 — guard falsified once per file (08c0234)
## [1.6.1] - 2026-08-08

### Bug Fixes

- **governance:** A non-MAESTRO user has NO channel to me — treat it as anomalous (TRDD-1R72424K) (7c350a8)

### Documentation

- Close TRDD-1R72424K — guard falsified 5 ways, audit coverage stated (6ed2d78)
## [1.6.0] - 2026-08-08

### Bug Fixes

- **persona:** Never put an at-sign in a GitHub body — it pages a real account (64cb104)
- **prrd:** Drop the at-handle from golden G1 and add G8 forbidding at-mentions (a897e6b)
- **skills:** The CLI/API rule binds hooks and scripts, and read-only-looking routes (cd9a13e)
- **isolation:** The writable-scope check must resolve symlinks (TRDD-9ZH31KC8) (18a6db6)
- **persona:** A forged approval and an inner junction are both scope escapes (TRDD-R6L582UX) (b670c54)
- **skills:** The kanban skill required an upstream skill that no longer exists (TRDD-9NYI3J0X) (121ddc1)
- **skills:** Cite an upstream skill by NAME, never by path — the path reddened CPV (TRDD-9NYI3J0X) (d5c6149)
- **governance:** Drop a ghost rule citation and stop deferring the kanban mechanics (7ff269f)
- **docs:** Never write a foreign repo's path in backticks — third instance, now guarded (1d3143f)
- **lint:** MD018 — a line beginning with an issue ref parses as a heading (540a77a)
- **deps:** Declare a range on ai-maestro-plugin and pin ^3.0.3 (d56b95c)
- **governance:** R42.8 is ratified — refuse on scope, not on a false absolute (3cc4bff)
- **persona:** Carry the re-verify duty into the resume step (TRDD-T0ZNVB12) (2d5ba56)
- **persona:** A recorded check must itself be falsified (TRDD-8VJ8YYAE) (411679d)
- [**breaking**] **governance:** R42.8 is NOT ratified — revert to the ratified R42.1-R42.7 (db3a892)
- [**breaking**] **governance:** R42.8 IS ratified — reverts db3a892; publication lagged the grant (8127880)
- **governance:** R42.8 verbs are THREE — and stop pinning a volatile fact (e4e9beb)
- **governance:** The persona asserted an R29.1 text USER deleted 25 days ago (TRDD-62AO9JXY) (79af9f4)
- **governance:** My own verification note carried two false values (TRDD-1504BH3Q) (bf45d25)

### Documentation

- **memory:** Record where a rule must live to bind the agent (ATOM-ARCH01-RULEPLACEMENT) (36ad171)
- **trdd:** Close TRDD-9ZH31KC8 — CC 2.1.206->2.1.221 sync landed in 18a6db6 (c9e74d7)
- **trdd:** Correct TRDD-R6L582UX's implementation-commit to the real sha b670c54 (ff76680)
- **memory:** Capture the Claude-Code-version-sync procedure (PROJECT scope) (c13eff3)
- **trdd:** Close TRDD-9NYI3J0X — upstream skill-drift repair landed in 121ddc1 (2d98ffe)
- **scenarios:** Publish the five adversarial fixtures as a plain corpus (ai-maestro#91) (61c1eff)
- **memory:** Record the CPV citation-form rule and the gate exit-code map (ATOM-P2BL-FNBS) (b7c7044)
- **memory:** Cover scripts/ in the architecture hub (ATOM-WST1-8ODS) (7bd5233)
- **cc-sync:** Align to Claude Code 2.1.222-2.1.224 (TRDD-M50MBTSB) (9296632)
- **trdd:** Record the landed sha in TRDD-M50MBTSB implementation-commits (d75bf28)
- **trdd:** Record the landed sha in TRDD-VFE3YFVS implementation-commits (d04a447)
- **trdd:** Record the landed sha in TRDD-T0ZNVB12 implementation-commits (6c65b78)
- **trdd:** Record the landed sha in TRDD-8VJ8YYAE implementation-commits (a9c91ba)
- Add TRDD-93KUP3R6 — R42.8 is not ratified (governs db3a892) (e300003)
- Add TRDD-LTOXG2PQ — R42.8 is ratified after all (governs 8127880) (02d3805)
- **trdd:** Record the landed sha in TRDD-LTOXG2PQ implementation-commits (0205b0c)
- Close TRDD-62AO9JXY — guard falsified 4 ways, gate clean (1fd1678)
- Close TRDD-1504BH3Q — structural control replaces two false values (4afe7e7)

### Features

- **persona:** Require re-verifying recorded external state (TRDD-VFE3YFVS) (fdf57cf)
## [1.5.5] - 2026-08-02

### Bug Fixes

- **persona:** Drain AMP inbox on wake, clone assigned repo step 0, report the NPT gap (issue #17, TRDD-WAKEDRN8) (2dcf7fa)
- **review:** Harden the CPV pin-parity guard, correct the gate count, unmerge the persona tier list (TRDD-CRFIX6MD) (86d0adb)
- **persona:** Mark rule numbers as as-of-authoring pointers, not assertable facts (ai-maestro#87, TRDD-RULENUM7) (adcd6bd)
- **lint:** Unblock the CPV strict gate — MD018 on a line starting with #87 (TRDD-RULENUM7) (1a46f38)

### Documentation

- **trdd:** Flip TRDD-CPV320UP to complete (impl 52cac30) (6f9b699)
- **memory:** Hooksfix is a NON-bug — correct [^7], the divergence hook decl is right (TRDD-HOOKDIVG) (5033576)
- **trdd:** Flip TRDD-CPV350UP to complete (impl 90f684e) (186a283)
- **trdd:** Flip TRDD-WAKEDRN8 to complete (impl 2dcf7fa) (444f16f)
- **memory:** Wire reciprocal [[persona-over-asking-mandate]] back-link in architecture hub (LINK LAW) (b56f6f2)
- **memory:** Reference the orphaned [^1] lesson from the body (librarian page-shape) (9df3d8c)
- **memory:** Backfill stable ids + symptom keywords on 8 pre-ATOM lessons (4698bbd)
- **memory:** Record that an inherited `--gate EXIT=0` is a snapshot, not a fact (ATOM-GATE-CLAIM-IS-A-SNAPSHOT) (49b5ade)
- **trdd:** Flip TRDD-4P2RZQFE to complete (impl 2f3df20) (0a979b6)

### Features

- **skills:** Forbid direct ai-maestro server API calls in every skill (TRDD-4P2RZQFE) (2f3df20)

### Miscellaneous Tasks

- **cpv:** Adopt v3.2.0 and make the three-way gate pin parity real (TRDD-CPV320UP) (52cac30)
- **cpv:** Adopt v3.5.0 across the pipeline in lockstep (TRDD-CPV350UP) (90f684e)

### Testing

- **cpv:** Guard CPV gate-pin parity against drift/re-float (TRDD-CPVPINGD) (79b5d2f)
## [1.5.4] - 2026-07-23

### Bug Fixes

- **persona:** Correct status→column field + drop deprecated MEMORY.md-index line (TRDD-81RC6IXC) (4710380)
- **memory:** Clear CPV --strict SHELL_EXEC false-positive in governance note (e73b63e)
- **changelog:** Walk full tag history and stop indenting headings (TRDD-R3JRZURT) (b326c65)
- **pipeline:** Re-pin CPV to v2.162.0, add publish.py --gate, add CI-parity preflight (5a9e9c9)
- **pipeline:** Adopt canon markdownlint rules, merge canon cliff.toml improvements (dd35a0e)
- **ci:** Group GITHUB_OUTPUT appends in notify-marketplace (shellcheck SC2129) (80ef9eb)
- **security:** Devitalize the B108 false positive blocking the publish gate (0117b4f)
- **ci:** Re-pin both CPV gates to v3.1.0 (was v2.162.0 / v2.136.1) (01c50d5)
- **ci:** Seed .cspell.json with the 72 project terms the SPELL gate flags (ee6871f)
- **ci:** Add the last cspell word so the SPELL gate is actually EXIT=0 (23e05f6)
- Make the release push atomic and stop two silent-failure paths (f6714ec)
- **ci:** Give the release gate the cold-build budget ci.yml documents (8a158c7)
- **release:** Resume an interrupted publish instead of skipping the version (5e96729)
- **release:** Fetch the origin baseline before the resume guard reads it (d83761d)
- **persona:** A clear MANAGER/USER mandate is authorization to begin (TRDD-MND8AUTH) (3c27ced)
- **persona:** R42-absolute keystroke ban + uniform R22 GitHub self-id (issue #15, TRDD-GOV15R42) (94a65d1)

### Documentation

- **trdd+memory:** Close TRDD-270ef961 published v1.5.3; record CLAUDE_PRIVATE_USERNAMES canon trap (263cebf)
- **memory:** Record fleet re-ask #11 reconciliation + one-shot canon-clean recipe (publish-pipeline [^4]) (d742645)
- **governance:** Fix #12 audit — gate silver-PRRD --user, add startup carve-outs (TRDD-7c4f9ea4) (cd063ea)
- **trdd:** Record implementation-commit cd063ea on TRDD-7c4f9ea4 (backtracking) (57890f5)
- **memory:** Add governance-audit-handling note (verify-HEAD-first + fix-vs-publish split) (790144a)
- **trdd:** Add TRDD-QJ30E8TD — regression guards for issue-12 governance fixes (b54d7c6)
- **trdd:** Add TRDD-81RC6IXC — persona currency fixes (impl 4710380) (bbd1e41)
- **trdd:** Add TRDD-AXI79CXE — backburner test-coverage gaps (go-on-yourself eval) (ff2da90)
- **memory:** Record the guard-with-each-governance-fix lesson (go-on-yourself eval) (0091271)
- **trdd:** Add TRDD-R3JRZURT (changelog-gen fix) + TRDD-NHYCSFRZ (script behavior tests) (0edd4ae)
- **trdd:** Supersede TRDD-AXI79CXE via TRDD-NHYCSFRZ (duplicate test-coverage TRDD) (febd39d)
- **trdd:** Park R3JRZURT changelog-gen fix -- Tier-2 publish.py change reverted pending approval (25d2e96)
- **memory:** Capture the fork-delegation-under-autonomous-directive lesson (c9f1486)
- **memory+trdd:** Correct issue-11 "ahead-of-canon" premise — it is INVERTED (TRDD-TVM7Q4XK) (c081577)
- **trdd:** Cite CONSOLIDATED eval report from TVM7Q4XK + capture-map (report->TRDD) (1dd6ca4)
- **memory:** Wire reciprocal back-links to fork-delegation note (LINK LAW) (d8941c6)
- Add TRDD-V7HJ492I for 3 code-review w9dtmt0a2 findings and fixes, impl-commits 3e55ace e2706db, Agent ai-maestro-autonomous-agent (6a9e244)
- Flip TRDD-V7HJ492I to complete, 3 regression tests landed f81f501 suite green, Agent ai-maestro-autonomous-agent (2da3a7f)
- Add TRDD-DUXFCQXT for code-review wmgl5kvbs finding and fix, impl-commit a318308, Agent ai-maestro-autonomous-agent (56851aa)
- Sync plugin guidance to Claude Code 2.1.181-2.1.200 (TRDD-BFDQH5A7) (b2dd4d2)
- Add TRDD-BFDQH5A7 for CC 2.1.181-2.1.200 sync, impl-commit b2dd4d2, Agent ai-maestro-autonomous-agent (2eb404c)
- **trdd:** Close TVM7Q4XK + R3JRZURT, add P8QK3ZTR for the CPV pipeline update (d824516)
- Add TRDD-R7NK2VQD for the CPV pipeline-migration upgrade (9ece65c)
- **memory:** Record that force-template protection is now declared, not remembered (5227752)
- **memory:** Record today's two release-safety properties and the dead-hook trap (aee536a)
- **trdd:** Flip TRDD-MND8AUTH to complete (impl 3c27ced) (de3314c)
- **memory:** Capture the persona over-asking-on-mandate diagnostic (TRDD-MND8AUTH) (8dc209b)
- **trdd:** Add TRDD-GOV15R42 for issue #15 R42/R22 conformance (impl 94a65d1) (80b9194)
- **trdd:** Flip TRDD-CPVXTRCT to complete (impl 54c1a62) (3bd93e5)

### Miscellaneous Tasks

- **trdd:** Finalize QJ30E8TD state — complete, impl 84b4ca8 (884392f)
- **trdd:** Finalize NHYCSFRZ backtracking -- implementation-commits 8b4d200 (28f0896)
- Port canon workflow hardening into release + notify-marketplace (TRDD-TVM7Q4XK) (3dd64f3)
- **pipeline:** Declare publish.py and cliff.toml as intentional divergences (60fa49d)
- **pipeline:** Declare git-hooks/pre-push as an intentional divergence (40a8c42)
- **hook:** Sync committed .githooks/pre-push with publish.py's regenerated template (526f63f)

### Refactor

- **scripts:** Extract 2 gitignore fns to gitignore_rules.py; drop vendored cpv_validation_common + smart_exec (TRDD-CPVXTRCT) (54c1a62)

### Security

- Update publish pipeline via CPV standardize --fix (TRDD-TVM7Q4XK) (f255127)

### Testing

- **governance:** Guard the issue-12 fixes in test_content_invariants (TRDD-QJ30E8TD) (84b4ca8)
- Real behavior tests for smart_exec + gitignore_filter + workspace-isolation (TRDD-NHYCSFRZ) (8b4d200)
- 3 regression tests for code-review w9dtmt0a2 findings plus correct stale deno_npm expectation left red by 3e55ace, 25 passed, TRDD-V7HJ492I, Agent ai-maestro-autonomous-agent (f81f501)
## [1.5.3] - 2026-06-20

### Bug Fixes

- **ci:** Drop CLAUDE_PRIVATE_USERNAMES from validate steps — it flagged the owner (TRDD-270ef961) (e645843)
## [1.5.2] - 2026-06-20

### Documentation

- **trdd:** Archive TRDD-5c21e4a0 — SHA-pin 3rd-party actions, published v1.5.1 (3668e3f)
- **memory:** Record CPV devitalization recurrence trap (v1.5.1) (82fc292)
- **trdd:** Propose CPV canon ADDITIVE reliability subset (TRDD-270ef961) (0751287)
- **memory:** Record CPV --force-templates / ahead-of-canon trap (publish-pipeline [^2]) (74c0d09)

### Miscellaneous Tasks

- **pipeline:** Pin CPV ref @v2.136.1 + harden validate steps (TRDD-270ef961) (c35bc16)
- **gitignore:** Re-ignore .claude/project/memory/*-proposed.md (257ca5e)
## [1.5.1] - 2026-06-20

### Bug Fixes

- **ci:** SHA-pin third-party GitHub Actions (TRDD-5c21e4a0) (6acab99)
- **docs:** Devitalize skillaudit:privilege_escalation false-positives (4f764e5)

### Documentation

- **trdd:** Archive TRDD-81869520 — governance R26-R40 published v1.5.0 ([#9](https://github.com/Emasoft/ai-maestro-autonomous-agent/issues/9)) (cfdc737)
- **memory:** Record CPV --strict false-positive shapes (slash-lists, sudo+password) (86e11a3)
## [1.5.0] - 2026-06-18

### Documentation

- **trdd:** Archive TRDD-fc155c40 — /api decoupling published v1.4.1 ([#8](https://github.com/Emasoft/ai-maestro-autonomous-agent/issues/8)) (842e397)
- Propagate governance R26-R40 into persona + skills + scenarios ([#9](https://github.com/Emasoft/ai-maestro-autonomous-agent/issues/9)) (7d92fef)
## [1.4.1] - 2026-06-18

### Documentation

- **trdd:** Archive TRDD-b48aa385 — global memory adopted + published v1.4.0 (273de6d)
- **memory:** Seed publish-pipeline PROJECT note (pre-push hook → publish.py) (6907e0e)
- **trdd:** Proposal TRDD-5c21e4a0 — RC-PIPELINE-DRIFT-001 (Tier-2, awaiting decision) (6da604b)

### Refactor

- Decouple executable /api/* -> frozen aimaestro-*.sh CLI verbs (R23, #8) (2d27167)
## [1.4.0] - 2026-06-15

### Documentation

- **trdd:** Record Claude Code currency review + validator prune (v1.3.3) (35015d3)

### Features

- **memory:** Adopt global janitor-hosted 3-scope memory; drop per-plugin system (7fe8d84)
## [1.3.3] - 2026-06-11

### Documentation

- **trdd:** Mark fleet-readiness audit ([#6](https://github.com/Emasoft/ai-maestro-autonomous-agent/issues/6)) completed → archived (ee2a38e)

### Miscellaneous Tasks

- **scripts:** Prune vestigial bundled CPV validators; object-form deps (a25d181)
## [1.3.2] - 2026-06-11

### Bug Fixes

- **publish:** Stop update_readme_version eating the README blank line (71c41bc)
- **publish:** Stage README + persona in the Step-11 release commit (0a6c6e4)
## [1.3.1] - 2026-06-11

### Bug Fixes

- **publish:** Bump README + persona in the LIVE Step-9 path (4dad3e2)
## [1.3.0] - 2026-06-11

### Features

- **governance:** Close fleet-readiness audit gaps M1–M12 ([#6](https://github.com/Emasoft/ai-maestro-autonomous-agent/issues/6)) (102876c)
## [1.2.0] - 2026-06-09

### Bug Fixes

- **skill:** Replace broken references/ link with universal-skill prose pointer (449a1af)
- **skill:** Restructure ai-maestro-autonomous-prrd-trdd-kanban to CPV 7-section format (<5000) (89fa5e0)
- **skill:** Remove ghost deployer/releaser subagent dispatch from kanban skill (b2ca5f3)
- **security:** Devitalize scanner-signature shapes for CPV strict (9 findings → 0) (e3da481)
- **manifest:** Plugin description now reflects the 5 bundled skills (d02cc38)

### Documentation

- **persona:** Approval tiers + lifecycle + baseline governance; memory wiring (#4, #5) (e151466)

### Features

- **workflow:** Add AUTONOMOUS's PRRD/TRDD/Kanban layer (42ab63e)
- **workflow:** Add Approval discipline section to ai-maestro-autonomous-prrd-trdd-kanban (25952ce)
- **prrd:** Bootstrap PRRD with G1 GitHub self-id golden rule (643049b)
- **validators:** Align with Claude Code v2.1.81–v2.1.143 plugin contract (v1.1.0) (26deea4)
- **memory:** Adopt the markdown memory system ([#5](https://github.com/Emasoft/ai-maestro-autonomous-agent/issues/5)) (8eb049f)

### Miscellaneous Tasks

- Add .tldrignore for TLDR code indexer (1e378d2)
## [1.0.8] - 2026-04-26

### Bug Fixes

- **validators:** Strip #anchor before referenced-file existence check (4afa264)

### Styling

- **agent:** Code-fence external server refs and add 2 example blocks (9c568f6)
## [1.0.7] - 2026-04-22

### Bug Fixes

- **publish:** POST GitHub release via curl -4 in Step 14 (ff55a01)
- **publish:** Try gh first, fall back to curl -4 in Step 14 (d630788)
## [1.0.5] - 2026-04-22

### Miscellaneous Tasks

- **gitignore:** Ignore /.rechecker/ runtime state (758bc81)
## [1.0.4] - 2026-04-22

### Bug Fixes

- **publish:** Stage uv.lock in Step 11 release commit ([#3](https://github.com/Emasoft/ai-maestro-autonomous-agent/issues/3)) (965e63f)

### Miscellaneous Tasks

- Update uv.lock (948a715)
## [1.0.3] - 2026-04-22

### Documentation

- Sync R6 v2 comm graph (AUTONOMOUS row) — closes #1 ([#2](https://github.com/Emasoft/ai-maestro-autonomous-agent/issues/2)) (77731de)

### Miscellaneous Tasks

- Update uv.lock (6644f0f)

### Styling

- **pre-push-hook:** Sort imports (ruff I001) (9127d13)
- **validators:** Sort imports (ruff I001) (958ec38)
## [1.0.2] - 2026-04-15

### Bug Fixes

- **pre-push-hook:** Type git() return as CompletedProcess[str] (4ec630d)
## [1.0.1] - 2026-04-15

### Bug Fixes

- **cpv:** Address 25 strict-validation findings from plugin-fixer (f2b04a8)
- **cpv:** Add ## Overview, numbered Instructions, reference TOCs, .python-version (ae8dfb7)
- **cpv:** Progressive disclosure — move full Q1-Q10 and Layer tables to references (4c0ab6a)
- **cpv:** Convert backtick ref mentions to markdown links; inline full TOCs (88a5d63)
- **cpv:** Trim SKILL.md Overview/Examples sections for size (53923ad)
- **cpv:** Consolidate reference files to reduce TOC-embed burden (e28c1c3)
- **cpv:** Restore questions.md content lost to a placeholder overwrite (e226667)
- **cpv:** Add input/output example pairs in governance SKILL.md (d55af7d)
- **cpv:** Switch governance examples to code-fenced format (e886954)

### Features

- Initial ai-maestro-autonomous-agent plugin v1.0.0 (aa55b87)

### Miscellaneous Tasks

- Update uv.lock (73f3b98)
---
*Generated by [git-cliff](https://git-cliff.org)*

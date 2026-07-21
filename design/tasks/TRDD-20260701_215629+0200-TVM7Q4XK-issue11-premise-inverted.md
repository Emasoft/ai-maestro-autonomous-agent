---
trdd-id: TVM7Q4XK
title: Issue-11 "ahead-of-canon" premise is INVERTED — correct the record + port canon workflow hardening
column: complete
approval-tier: 3
created: 2026-07-01T21:56:29+0200
updated: 2026-07-21T22:35:19+0200
current-owner: aimaa-autonomous
assignee: aimaa-autonomous
priority: 3
severity: MEDIUM
effort: M
task-type: infra
parent-trdd: null
npt: []
eht: []
blocked-by: []
supersedes: []
relevant-rules: [1]
release-via: publish
delivery: direct-push
target-branch: main
must-pass-tests-before-merge: true
test-requirements: [lint, typecheck, unit]
audit-requirements: []
review-requirements: [human-review]
runtime-targets: [macos, linux]
impacts: [ci-pipeline]
attempts: 0
test-failures: 0
last-test-result: not-run
implementation-commits: [3dd64f3, f255127]
external-refs: ["reports/go-on-yourself-eval/20260701_215629+0200-issue11-premise-inverted-verification.md", "reports/go-on-yourself-eval/20260701_182302+0200-CONSOLIDATED-eval-and-decisions.md", "github.com/Emasoft/ai-maestro-autonomous-agent/issues/11", "TRDD-5c21e4a0", "TRDD-270ef961", "RC-PIPELINE-DRIFT-001"]
---

# TRDD-TVM7Q4XK — Issue-11 premise inverted: correct the record + port canon workflow hardening

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-07-01

- **Surfaced by** the `[janitor-resume]` (post-~9.5-day rate-limit) resumption of the
  parked decision-3 ("a fork claims #11's premise is inverted — verify before reversing
  a public post"). **INDEPENDENTLY VERIFIED 2026-07-01: the fork was RIGHT.**
- **Finding (VERIFIED, evidence in the report):** my public **#11 v1.5.3 comment** — and
  the `publish-pipeline.md` memory note — assert the plugin's `release.yml` +
  `notify-marketplace.yml` are **AHEAD of canon** carrying "SBOM + build-provenance +
  per-asset SHA256SUMS + a MARKETPLACE_PAT no-op guard canon lacks", that
  `--force-templates` "would DOWNGRADE" them, and that "canon pins OLDER SHAs". **All
  FALSE — the direction is inverted; the plugin is BEHIND canon.** Canon HAS the
  provenance/least-priv-permissions/no-op-guard/`timeout-minutes`/newer-SHA-pins; the
  plugin has NONE of the SBOM/provenance/SHA256SUMS (CI or publish.py) and older/unpinned
  actions. Git pickaxe: those features were **never** in the tree — the list was fabricated
  from CPV's **hedged** line-227 "ahead … or the direction is ambiguous" heuristic, taken
  at face value without reading the unified diff CPV prints beneath it.
- **DONE this pass (Tier-0):** corrected the `publish-pipeline.md` memory note in place +
  demoted the error to lesson [^5] (+ [^2]/[^4] markers); wrote the evidence report;
  authored this TRDD. **No workflow edits, no public post, no force-template, no reversal
  of 5c21e4a0 — all four gated.**
- **RESOLVED 2026-07-21 — USER approved options 1 + 2; both executed.**
  - **Option 1 (Tier-3, public correction) — DONE.** Correction posted to issue #11:
    `.../ai-maestro-autonomous-agent/issues/11#issuecomment-5038748584`. Retracts the
    ahead-of-canon claim, tables the claim-vs-reality diff, names the root cause (read
    CPV's *hedged* heuristic line, never the unified diff printed beneath it), and
    states plainly that the commits are LOCAL/UNPUSHED. Issue left OPEN — the work is
    unreleased and the backfill tag is outstanding.
  - **Option 2 (Tier-2, workflow hardening) — DONE, commit `3dd64f3`.** Least-privilege
    `permissions` on release.yml; ALL actions SHA-pinned at current versions
    (checkout v4→v7.0.1, setup-python v5→v7.0.0, setup-uv v5.4.2→v9.0.0);
    `timeout-minutes` + the `MARKETPLACE_PAT` no-op guard on notify-marketplace.yml;
    job summary moved to env indirection. Guarded by `tests/test_workflow_hardening.py`.
  - **Option 3 (SBOM / provenance / SHA256SUMS) — CLOSED as NOT APPLICABLE, with
    evidence.** `publish.py` creates the release via `gh release create --notes-file`
    and uploads NO assets: this plugin ships as a git ref consumed by the marketplace,
    not as a built artifact. There is nothing to attest or checksum, so canon's steps
    would no-op or fail. Canon carries them because canon's `release.yml` BUILDS and
    uploads assets while ours is a post-hoc validate gate — the architectural
    divergence this TRDD already flagged. Revisit only if this plugin ever ships real
    release assets.
  - **Option 4 (reopen 5c21e4a0) — NOT taken.** Confirmed it still stands, for its own
    correct reason: canon's publish.py is 278 lines vs our 1805, so `--force-templates`
    would regress ~1500 lines of custom version-sync logic.
- **Also landed while here (`f255127`, via CPV per USER instruction):** the publish
  pipeline was updated with `cpv-remote-validate standardize . --fix`, which surfaced a
  separate latent breakage — publish.py never emitted the `<plugin>--v{version}` tag
  Claude Code resolves dependencies against, so every dependent would install with
  `no-matching-tag` and be DISABLED. Fixed; see TRDD-P8QK3ZTR.
- **STILL OPEN (both gated on USER):** backfill the
  `ai-maestro-autonomous-agent--v1.5.3` tag (needs a push), and publish the release.
- **What STANDS (do NOT overcorrect):** TRDD-5c21e4a0's core reason — don't blindly
  `--force-templates` **publish.py** (custom M11 version-sync logic) — is SOUND and
  unaffected. A *blind* `release.yml` clobber is still unsafe, but for an ARCHITECTURAL
  reason (the plugin's `release.yml` is a post-hoc validate-tag gate; publish.py creates
  the release), NOT the "downgrade of ahead hardening" reason.

## Why

A live public GitHub comment (#11) under the shared @Emasoft owner identity, and a
git-tracked PROJECT memory note, both state a materially false, direction-inverted
security claim. Left uncorrected: (1) the memory poisons every future recall (fixed this
pass); (2) the public record misleads any maintainer/fleet reader into thinking the plugin
is ahead when it is behind on provenance/permissions/pinning; (3) the actual security gap
(no build-provenance, no SBOM, no per-asset checksums on releases) stays hidden behind a
"close as ahead-of-canon exception" recommendation.

## The verified facts (full evidence: the report in external-refs)

- CPV `--strict` at HEAD: EXIT=0, 0/0/0/0, 7 non-blocking WARNINGs (tree publish-clean).
- `release.yml` unified diff (canon→plugin): canon HAS least-priv `permissions:` +
  `id-token`/`attestations: write` build-provenance (CPV #121), `checkout`@v6.0.3
  SHA-pinned, `setup-uv`@v8.2.0 (newer), `timeout-minutes: 30`. Plugin: none of those;
  unpinned `@v4`, older `setup-uv`@v5.4.2, thin post-hoc gate.
- `notify-marketplace.yml`: plugin DROPPED canon's `timeout-minutes` + `HAS_MARKETPLACE_PAT`
  no-op guard; uses `repository-dispatch`@v4.0.1 (canon defensively pins v4.0.0).
- Whole-tree grep: zero SBOM/provenance/SHA256SUMS anywhere. Pickaxe: 0 commits ever.

## Corrective options (ALL GATED — decide, then I execute)

1. **Correct the public #11 comment** (owner-facing → **USER, Tier-3**). Post an accurate
   follow-up: plugin is BEHIND canon on provenance/permissions/newer-pins, not ahead;
   re-open workflow hardening as real deferred work; the publish.py-force-template deferral
   (5c21e4a0) still stands for its own (correct) reason.
2. **Port canon's workflow hardening** into `release.yml` + `notify-marketplace.yml`
   WITHOUT touching `publish.py` (**Tier-2**): least-priv `permissions:`, build-provenance
   attestation, `timeout-minutes` on notify, `HAS_MARKETPLACE_PAT` no-op guard, bump
   `setup-uv`→v8.2.0 + SHA-pin `checkout`, drop `repository-dispatch`→v4.0.0. Reconcile the
   post-hoc-gate-vs-release-creator architecture explicitly (do NOT reintroduce a
   conflicting release-creating job).
3. **Add SBOM + build-provenance + per-asset SHA256SUMS to releases** (**Tier-2**) — in
   `release.yml` per canon, or in `publish.py`. This is the actual security gap.
4. Whether any of this reopens **TRDD-5c21e4a0** (USER-ratified) is a **USER** call.

## Verification (when option 2/3 is approved + executed)

- `pytest tests/ -q` green (add a guard test asserting the workflows carry the ported
  hardening tokens); `ruff` + `mypy` clean.
- CPV `--strict` still 0/0/0/0 (the RC-PIPELINE-DRIFT WARNINGs may CHANGE as files move
  toward canon — confirm no new CRITICAL/MAJOR/MINOR/NIT).
- A real `publish.py --dry-run` (and, on ship, a real release) exercises the provenance
  attestation path end-to-end.

## Report→TRDD capture (CONSOLIDATED go-on-yourself report, 20260701_182302)

This TRDD is the formal capture of that umbrella report's **R1** (#11 premise inverted →
correct the record) and **R2** (additive #11 hardening). The report's decisions land as:
- **D (fixed):** TRDD-QJ30E8TD (issue-#12 guards), TRDD-81RC6IXC (persona currency).
- **R1** → THIS TRDD (option 1). My 2026-07-01 re-verification CONFIRMS the prior fork's
  finding — the premise IS inverted.
- **R2** → THIS TRDD (options 2–3). The pin+`timeout-minutes` sub-part already SHIPPED via
  TRDD-270ef961 (published v1.5.3); the SBOM/provenance/SHA256SUMS/`HAS_MARKETPLACE_PAT`
  sub-part remains OPEN (270ef961 wrongly waved it off as "ahead"). **Also fold in R2's
  `git push` retry wrapper (publish.py Step 13)** — a distinct Tier-2 pipeline-reliability
  item (a transient push timeout must not leave commit-pushed-without-tag); tracked here.
- **R3 + R4** (CHANGELOG `--unreleased` latest-only; cliff.toml heading indent) →
  TRDD-R3JRZURT (parked, Tier-2).
- **R5** (PRRD G1.1 `Agent: <role>` vs baseline `<plugin-slug>`) — GOLDEN/Tier-3, USER-only,
  **flag-only** (no executable task); surfaced to USER, no tracking TRDD needed.
- **R6** (test-coverage gaps) → TRDD-AXI79CXE → superseded by TRDD-NHYCSFRZ (DONE).

## Approval log

- 2026-07-01T21:56:29+0200 — Authored in `design/tasks/` as a parked finding+proposal
  (backburner). The VERIFICATION + memory correction + this TRDD are Tier-0 (doc/memory,
  reversible, local). Options 1–4 are GATED (owner-facing / Tier-2 pipeline / USER-ratified
  reversal) — surfaced to USER, none executed. Mirrors the R3JRZURT parked-Tier-2 pattern.

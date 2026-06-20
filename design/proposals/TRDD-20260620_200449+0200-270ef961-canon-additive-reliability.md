---
trdd-id: 270ef961-d71a-4c68-a110-4c703f82d84a
title: CPV canon ADDITIVE reliability subset — pin CPV ref + validate-step timeout/integrity-skip (NOT a template clobber)
column: proposal
approval-tier: 2
created: 2026-06-20T20:04:49+0200
updated: 2026-06-20T20:04:49+0200
current-owner: autonomous-agent
task-type: infra
parent-trdd: TRDD-5c21e4a0
supersedes: []
relevant-rules: []
release-via: publish
delivery: direct-push
target-branch: main
test-requirements: [lint, typecheck]
impacts: [ci-pipeline]
external-refs: ["github.com/Emasoft/ai-maestro-autonomous-agent/issues/10", "github.com/Emasoft/ai-maestro/issues/44"]
---

# CPV canon ADDITIVE reliability subset (NOT a `--force-templates` clobber)

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-06-20

- **Why this exists:** fleet work order #10 (umbrella `ai-maestro#44`, MANAGER, USER directive)
  asked to bring this plugin's publish pipeline to the CPV 2.136.1 canonical standard via
  `--force-templates`. A `plugin-fixer` run (report:
  `reports/plugin-fixer/20260620_200016+0200-canonical-pipeline-migration.md`) VERIFIED the
  force-migration is the WRONG action and STOPPED. This proposal captures the only legitimately
  actionable, ADDITIVE, non-harmful subset it surfaced.
- **Current pipeline state (VERIFIED 2026-06-20):** already publish-clean —
  `remote_validation.py --strict` = `PASSED:113 | CRITICAL:0 MAJOR:0 MINOR:0 NIT:0 | WARNING:7`
  (all 7 non-blocking advisories). Tree clean, version 1.5.1, v1.5.1 SHA-pins intact.
- **Force-templates is FORBIDDEN here** (do NOT do it): CPV's own validator says `release.yml`
  + `notify-marketplace.yml` are AHEAD of canon ("would DOWNGRADE"); canon pins DIFFERENT action
  SHAs than the PRESERVE-mandated v1.5.1 pins; and USER-approved Tier-2 [[TRDD-5c21e4a0]]
  (published as v1.5.1, 2026-06-20) already did the SAFE subset and explicitly DEFERRED the clobber.
  v1.5.1 IS the ratified end-state of the migration question.
- **NEXT ACTION (gated on USER/MANAGER Tier-2 approval — this is `column: proposal`):** if approved,
  promote → `planned`, implement the items below, then `scripts/publish.py --patch` → v1.5.2, watch CI green.
- **SUPERSEDED — do NOT carry forward:** any reading of #10 as "run `--force-templates`". That path is
  closed by TRDD-5c21e4a0 + the validator's own "do not downgrade" guard.
- **Durable artifacts:** the plugin-fixer report (above) holds the full per-file evidence + diffs.

## Proposed ADDITIVE changes (move toward canon WITHOUT regressing the preserved hardening)

1. **Pin the CPV ref in CI** — `validate.yml` + `release.yml` invoke
   `uvx --from git+https://github.com/Emasoft/claude-plugins-validation` WITHOUT a `@v<ver>` pin
   (tracks HEAD). Pin to `@v2.136.1`. *Highest-value:* a stricter future CPV release can otherwise
   silently red-light this plugin's CI with no plugin change.
2. **Harden the validate step** — add `timeout-minutes` + `PLUGIN_SKIP_GITHUB_INTEGRITY: "1"` +
   `CLAUDE_PRIVATE_USERNAMES: ${{ github.repository_owner }}` env to the validate job. Prevents a cold
   `uvx --from git+...` build (12-20 min) from hanging; skips a redundant integrity fetch.
3. **(Optional, low priority)** the standardizer's genuine minor items: `.mega-linter.yml`,
   `.coverage` gitignore entry, README CI/Version/License badges, pyproject `[build-system]`, drop the
   unused `pyyaml` dependency.

## Explicitly OUT of scope (the harmful path — never do)
- `scripts/publish.py --force-templates` / any canonical-template clobber of `publish.py`,
  `release.yml`, `notify-marketplace.yml`. It regresses the v1.5.1 SHA-pins and downgrades the
  SBOM / build-provenance / per-asset SHA256SUMS / idempotent-release hardening that is AHEAD of canon.
  Any future `publish.py` canon alignment must be a REVIEWED 3-way merge + `--dry-run` + test-release,
  per TRDD-5c21e4a0 — never a force-overwrite.

## Acceptance (if approved + implemented)
- [ ] CPV ref pinned to `@v2.136.1` in both CI workflows; validate step has timeout + integrity-skip env.
- [ ] v1.5.1 SHA-pins (`setup-uv@d4b2f3b…#v5.4.2`, `repository-dispatch@28959ce…#v4.0.1`) STILL intact.
- [ ] `remote_validation.py --strict` still 0/0/0/0 (WARNING-only allowed).
- [ ] `scripts/publish.py --patch` → v1.5.2 green; CI green; row updated on `ai-maestro#44`.

## Approval log
- 2026-06-20T20:04:49+0200 — Authored as `proposal` (Tier-2) by the AUTONOMOUS agent, surfacing the
  `plugin-fixer` §4 additive subset for MANAGER/USER decision. NOT yet authorized to implement.

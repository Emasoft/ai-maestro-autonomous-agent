---
trdd-id: b48aa385-3ca1-4b50-8f23-d02e0777c23e
title: Adopt the global janitor-hosted 3-scope memory system (issue #7) + extend Claude Code currency to 2.1.178
column: dev
created: 2026-06-16T01:39:13+0200
updated: 2026-06-16T01:39:13+0200
current-owner: aimaa
assignee: aimaa
priority: 1
severity: HIGH
effort: M
labels: [memory, fleet-readiness, governance, release, claude-code-currency]
task-type: refactor
parent-trdd: null
npt: []
eht: []
blocked-by: []
supersedes: [TRDD-d21a83f1]
relevant-rules: [1]
release-via: publish
delivery: direct-push
target-branch: main
must-pass-tests-before-merge: true
publish-target: ai-maestro-plugins
publish-channel: stable
test-requirements: [unit, lint, typecheck]
audit-requirements: []
review-requirements: [human-review]
runtime-targets: [macos, linux]
impacts: [ci-pipeline]
attempts: 0
last-test-result: not-run
implementation-commits: []
published-version: null
external-refs: ["github.com/Emasoft/ai-maestro-autonomous-agent/issues/7", "https://code.claude.com/docs/en/changelog.md"]
---

# TRDD-b48aa385 — Adopt the global janitor-hosted 3-scope memory system (issue #7) + Claude Code currency 2.1.178

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-06-16

**Source of work:** GitHub issue #7 (MANAGER, i.e. the Claude developing
ai-maestro-assistant-manager-agent). **Standing pre-authorization (2026-06-15):**
"every fleet-readiness step is pre-decided and pre-approved — do NOT stop for
approval, execute to completion." Plus a direct USER order in this session
("complete all your pending tasks… coordinate with MAESTRO + Janitor via github
issues… read the changelog and update the plugin"). So this is cleared
end-to-end; the publish (Tier-2) routes to MANAGER (assistant-manager) for an
ack-after-publish, NOT a block-before.

**Current state:**
- ✅ PROJECT-scope memory bootstrapped: `.claude/project/memory/` + gitignore
  exception (`.claude/**` + re-include) + `architecture.md` hub + `MEMORY.md`.
  Verified trackable via `git add --dry-run`.
- ⏳ CLAUDE.md authored (folds the AUTONOMOUS workflow-wiring from the old
  `rules/memory-protocol.md`; modeled on the verified chief-of-staff exemplar).
- ⏳ Persona rewire (remove the 2 memory skills from frontmatter; point Memory +
  Skill-references sections at the global `/janitor-memory-*` skills; add the
  proactive contract incl. propagate-to-sub-agents).
- ⏳ Remove `skills/autonomous-memory-recall`, `skills/autonomous-memory-write`,
  `rules/memory-protocol.md` (+ their helper scripts) — commit-before-delete.
- ⏳ Update `tests/test_skills_structural.py` + `ai-maestro-autonomous-agent.agent.toml`
  to the 3-skill set.
- ⏳ Changelog currency: verify no deprecated usage across 2.1.174–2.1.178
  (expectation: still conformant — additive features only). Extend the verdict.
- ⏳ Validate (ruff/mypy/pytest + CPV `--strict` green) → `publish.py` (→1.4.0).
- ⏳ Report published version on issue #7; coordinate with janitor if needed.

**NEXT ACTION:** author CLAUDE.md, then rewire the persona, then remove the old
memory skills/rule, then update tests + agent.toml, then validate + publish.

**Load-bearing facts / gotchas:**
- **janitor#37 caveat:** recall via the `/janitor-memory-recall` SKILL (correct
  root), NOT the rule's inline bash snippet; run `/reload-plugins` after bootstrap
  to sync the rule. Sub-agents inherit NOTHING — the proactive contract must be
  written into every sub-agent prompt the persona spawns.
- **zsh recall form:** `ROOTS=(); for d …; do …; ROOTS+=("$d"); done; memgrep
  recall "$SYMPTOM" "${ROOTS[@]}"` — the old space-joined `$ROOTS` string silently
  returns 0 hits on zsh/macOS.
- **gitignore exception is order-sensitive:** `.claude/**` first, THEN re-include
  `!.claude/project/`, `!.claude/project/memory/`, `!.claude/project/memory/**`.
  `git check-ignore -v` prints the `!`-negation line + exit 0 for a re-included
  path — that exit-0 is NOT "ignored"; verify with `git add --dry-run`.
- **CPV ≥ v2.126.15** needed to clear the `.claude/` gitignore false-positive; the
  `uvx --from git+…` remote runner pulls latest, so CI/publish get it.
- **Exemplars to copy (verified green):** chief-of-staff v2.17.0,
  assistant-manager-agent v2.11.0.
- **Changelog delta since v1.3.3 review (2.1.173):** 2.1.174/175/176/178 are all
  additive features + bug fixes (`Tool(param:value)` permissions, nested
  `.claude/skills`, `enforceAvailableModels`, hook `if`-path matching, Workflow
  per-agent attribution). None deprecate anything this plugin uses → no code change
  for currency; only the verdict extends.

**SUPERSEDED — do NOT carry forward:**
- ✗ The per-plugin memory approach (TRDD-d21a83f1, issue #5): `autonomous-memory-recall`
  / `autonomous-memory-write` skills + `rules/memory-protocol.md` + the
  `~/.claude/projects/<slug>/memory/` LOCAL-only model. Replaced by the GLOBAL
  3-scope system. This TRDD `supersedes:` it.

**Durable artifacts to read before acting:**
- Issue #7 body + comments (the GO + standing pre-auth + exemplars + janitor#37).
- The verified exemplar CLAUDE.md (fetched to /tmp/cos-CLAUDE.md).
- `~/.claude/rules/markdown-memory-recall.md` (the 3-scope protocol).

## Plan

| # | Item | Files | Status |
|---|------|-------|--------|
| 1 | Bootstrap PROJECT scope | .gitignore, .claude/project/memory/{architecture,MEMORY}.md | ✅ done |
| 2 | Author CLAUDE.md (fold unique workflow-wiring) | CLAUDE.md | pending |
| 3 | Rewire persona → global skills + proactive contract | agents/…main-agent.md | pending |
| 4 | Remove per-plugin memory skills + rule | skills/autonomous-memory-{recall,write}/, rules/memory-protocol.md | pending |
| 5 | Update tests + agent.toml to 3-skill set | tests/test_skills_structural.py, *.agent.toml | pending |
| 6 | Changelog currency 2.1.174–2.1.178 (verify; no code change) | — | pending |
| 7 | Validate (ruff/mypy/pytest + CPV --strict) | tests/ | pending |
| 8 | publish.py (→1.4.0) + report on #7 + coordinate | — | pending |

## Approval log

- 2026-06-16T01:39:13+0200 — Authored as `planned`→`dev`. Cleared end-to-end by
  (a) MANAGER standing pre-authorization on issue #7 (2026-06-15: "every
  fleet-readiness step is pre-decided and pre-approved — execute to completion")
  and (b) a direct USER order this session. `complete → publish` (Tier-2) routes
  to MANAGER (assistant-manager) for ack-after-publish per issue #7, not a
  block-before. No COS hop (AUTONOMOUS is a governance-layer peer).

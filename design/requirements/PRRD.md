---
prrd-version: 1.1
updated: 2026-06-11T11:24:03+0200
project: ai-maestro-autonomous-agent
project-id: autonomous
canonical-source: design/requirements/PRRD.md
mirrors: []
---

# Project Requirements & Rules — ai-maestro-autonomous-agent

AUTONOMOUS role plugin (AIMAA) — solo agent, owns all columns for its own TRDDs.

## §0. Canonical source + copies

| Path | Role | Update strategy |
|---|---|---|
| `design/requirements/PRRD.md` | **CANONICAL** for this project | Edit first. Bump `prrd-version:`. Update `updated:`. |

## §I. How to read this document

Rule citation form: `PRRD G<n>.<v>` (golden, user-set) or `PRRD S<n>.<v>`
(silver, manager-mutable). Rule numbers are globally unique across G/S;
promote/demote flips the letter without changing the number. The
`get-prrd.py <n>` script returns a rule's text by bare number. Full
spec: `~/.claude/rules/prrd-design-rules.md`.

## 🥇 GOLDEN — set by the USER (immutable to MANAGER)

- **G1.1** — Every agent that writes to GitHub (issue, issue comment, PR, PR comment, PR review, discussion, release note) MUST begin the body with a one-line self-identification of which agent/role/plugin authored it, because all AI Maestro agents share the single human-owner GitHub identity (the owner's gh CLI auth). Recommended leading line: _Posted by the Claude developing **<plugin-or-role>** (via the shared @owner gh auth)._ Commit messages SHOULD carry an `Agent: <role>` trailer.

## 🥈 SILVER — MANAGER-mutable (AUTONOMOUS proposes directly to MANAGER; no COS)

- **S2.1** — This plugin is a Claude Code plugin, so its sole release path is the CPV canonical `scripts/publish.py` strict pipeline (auto-detect → test → lint → CPV `--strict` → consistency → bump → changelog → commit → push → GitHub release). No `--skip-*` flag, no `--no-verify`, and no manual version bump that bypasses the pipeline is permitted; the pre-push hook enforces `publish.py` as the caller.
- **S3.1** — Every skill, command, hook, and runtime behavior ships real (non-mock) tests under `tests/`. The publish test-gate runs them and a non-zero exit blocks the release. Conceptual or mocked-out tests are not acceptable substitutes.
- **S4.1** — The README `**Version**:` line and the persona `**Plugin**: … vX.Y.Z` line MUST equal `plugin.json` `version`. `publish.py`'s `check_version_consistency()` enforces this and `do_bump()` keeps all four sources (plugin.json, pyproject.toml, README, persona) in sync on every release.
- **S5.1** — The persona's encoded R6 communication-graph version MUST track the AI Maestro server's current graph (presently **v3**: COS guards the team boundary; MANAGER reaches team-internal titles only via COS). A server graph change requires updating the persona, the governance skill, and this PRRD in the same release.
- **S6.1** — TRDDs use the v2 `column:` schema and live under the 4-zone `design/{proposals,tasks,refused,archived}` layout. A proposal is authorized (`proposal → planned`) by `git mv` from `design/proposals/` to `design/tasks/`; terminal TRDDs move to `design/archived/` (completed/cancelled/superseded) or `design/refused/` (never-approved).
- **S7.1** — Every GitHub post AND every AMP message body leads with the self-id line `This is the Claude responsible for the ai-maestro-autonomous-agent project.` — extending golden G1.1 from GitHub posts to AMP bodies so a shared-identity reader can tell which Claude authored the message.


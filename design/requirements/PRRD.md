---
prrd-version: 1.2
updated: 2026-08-02T13:07:11+0200
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

- **G1.2** — Every agent that writes to GitHub (issue, issue comment, PR, PR comment, PR review, discussion, release note) MUST begin the body with a one-line self-identification of which agent/role/plugin authored it, because all AI Maestro agents share the single human-owner GitHub identity (the owner's gh CLI auth). Leading line: _Posted by the Claude developing **&lt;plugin-or-role&gt;** (via the shared repo-owner gh auth)._ Commit messages SHOULD carry an `Agent: <role>` trailer.
- **G8.1** — NEVER write an at-mention (`@` + a name) in GitHub prose — issue, comment, PR, review, discussion, or release note. GitHub resolves the handle against the GLOBAL account namespace and NOTIFIES it, so a placeholder or a role name is a page sent to a stranger: measured 2026-08-02, `owner`, `core`, `manager`, `janitor`, `architect`, `maintainer`, `cos`, `cpv`, `ai-maestro`, `v2`, `v4` are all real accounts, and 27 live mentions across this fleet's repos had to be retracted. Handles are case-INSENSITIVE, so `MANAGER` and `manager` are one account. Address a role in plain words (`the manager agent`), a sibling project by repo slug (`Emasoft/ai-maestro`), and when a literal `@` is unavoidable — an action pin, a URL, an email — put it in backticks or a fenced block, where GitHub does NOT notify. A placeholder in a template MUST be angle-bracketed (`<handle>`), never a bare at-name: a bare one looks like finished text and gets pasted verbatim, which is exactly how G1.1 leaked.

## 🥈 SILVER — MANAGER-mutable (AUTONOMOUS proposes directly to MANAGER; no COS)

- **S2.1** — This plugin is a Claude Code plugin, so its sole release path is the CPV canonical `scripts/publish.py` strict pipeline (auto-detect → test → lint → CPV `--strict` → consistency → bump → changelog → commit → push → GitHub release). No `--skip-*` flag, no `--no-verify`, and no manual version bump that bypasses the pipeline is permitted; the pre-push hook enforces `publish.py` as the caller.
- **S3.1** — Every skill, command, hook, and runtime behavior ships real (non-mock) tests under `tests/`. The publish test-gate runs them and a non-zero exit blocks the release. Conceptual or mocked-out tests are not acceptable substitutes.
- **S4.1** — The README `**Version**:` line and the persona `**Plugin**: … vX.Y.Z` line MUST equal `plugin.json` `version`. `publish.py`'s `check_version_consistency()` enforces this and `do_bump()` keeps all four sources (plugin.json, pyproject.toml, README, persona) in sync on every release.
- **S5.1** — The persona's encoded R6 communication-graph version MUST track the AI Maestro server's current graph (presently **v3**: COS guards the team boundary; MANAGER reaches team-internal titles only via COS). A server graph change requires updating the persona, the governance skill, and this PRRD in the same release.
- **S6.1** — TRDDs use the v2 `column:` schema and live under the 4-zone `design/{proposals,tasks,refused,archived}` layout. A proposal is authorized (`proposal → planned`) by `git mv` from `design/proposals/` to `design/tasks/`; terminal TRDDs move to `design/archived/` (completed/cancelled/superseded) or `design/refused/` (never-approved).
- **S7.1** — Every GitHub post AND every AMP message body leads with the self-id line `This is the Claude responsible for the ai-maestro-autonomous-agent project.` — extending golden G1 from GitHub posts to AMP bodies so a shared-identity reader can tell which Claude authored the message.

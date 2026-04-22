# AI Maestro Autonomous Agent (AIMAA)

<!--BADGES-START-->
<!--BADGES-END-->

**Version**: 1.0.0

## Overview

`ai-maestro-autonomous-agent` is the mandatory role-plugin for every
agent with governance title `AUTONOMOUS` in the AI Maestro ecosystem.

AUTONOMOUS agents are no-team agents that serve the user directly. They
live outside of any team, have no CHIEF-OF-STAFF, no ORCHESTRATOR, and
no team MEMBERs. Per the R6 v2 communication graph (2026-04-22), they
coordinate via the Agent Messaging Protocol (AMP) directly with MANAGER
and peer AUTONOMOUS agents, and have a `Y` edge to HUMAN so they may
initiate direct user contact (governance-layer privilege). All other
titles — including MAINTAINER — are reachable only via MANAGER relay.

This plugin is NOT an optional add-on. Every AUTONOMOUS agent MUST have
it installed. The AI Maestro element-management-service refuses to
create or change title to AUTONOMOUS without auto-installing this
plugin.

## Why it's mandatory

Every agent on an AI Maestro host shares the same `gh` CLI identity —
the host owner. From GitHub's point of view every agent has full
repo-owner write access. From the filesystem's point of view every
agent can read and (technically) write anywhere the host user can.

The only thing preventing an unrestricted agent from trampling other
agents' work, force-pushing shared branches, or merging arbitrary PRs
is the governance rules written into its role-plugin's main agent
persona. Team roles have their team's persona. MAINTAINERs have the
MAINTAINER persona. **AUTONOMOUS agents historically had no persona at
all** — they ran as bare Claude Code sessions with the `ai-maestro-plugin`
base utilities but no behavioral constraints. That was the security
hole this plugin closes.

With `ai-maestro-autonomous-agent` installed, an AUTONOMOUS agent has:

- Explicit writable-scope restrictions (its own working directory +
  system scratch only)
- A comprehensive forbidden-actions list (no cross-agent mutation, no
  destructive git on shared branches, no unauthorized PR merges, no
  secret access, no user-scope plugin installation)
- A strict AMP messaging discipline per the communication graph
- Collaboration rules for PR review with MAINTAINERs (never merges its
  own PRs; always waits for the repo's MAINTAINER)
- Self-defense instructions against prompt injection

## What's in the plugin

```
ai-maestro-autonomous-agent/
├── .claude-plugin/
│   └── plugin.json                (manifest)
├── ai-maestro-autonomous-agent.agent.toml   (.agent.toml profile)
├── agents/
│   └── ai-maestro-autonomous-agent-main-agent.md   (main agent persona)
├── skills/
│   ├── ai-maestro-autonomous-governance/           (self-audit checklist)
│   └── ai-maestro-autonomous-workspace-isolation/  (writable-scope examples)
├── scripts/                       (publish pipeline + validators)
├── .github/workflows/             (CI + notify-marketplace)
├── CHANGELOG.md
├── LICENSE                        (MIT)
├── pyproject.toml
└── README.md                      (this file)
```

The persona is the **only thing that matters at runtime**. The skills
are expansions of the rules for agent self-reference during execution.
Everything else is publishing infrastructure.

## Quad-match identity

- `plugin.json` `name` == `ai-maestro-autonomous-agent`
- Plugin folder name == `ai-maestro-autonomous-agent`
- `ai-maestro-autonomous-agent.agent.toml` `[agent].name` == `ai-maestro-autonomous-agent`
- `agents/ai-maestro-autonomous-agent-main-agent.md` frontmatter
  `name:` == `ai-maestro-autonomous-agent-main-agent`

Claude Plugin Validator (CPV) enforces this quad-match.

## Compatibility

- `compatible-titles = ["AUTONOMOUS"]` — this plugin is installable
  only on agents with governance title AUTONOMOUS. AI Maestro's
  ChangeTitle pipeline auto-installs it when a title transition
  lands on AUTONOMOUS, and auto-uninstalls it when transitioning
  away.
- `compatible-clients = ["claude-code"]` — Claude Code native
  support. Cross-client emission to Codex / Gemini / OpenCode / Kiro
  happens through AI Maestro's Universal Plugin IR pipeline when
  needed.

## Installation

Normally AI Maestro installs this plugin automatically via ChangeTitle
Gate 15/16 when an agent is assigned the AUTONOMOUS title. Manual
installation (rare — for testing) via the Claude CLI:

```bash
claude plugin install ai-maestro-autonomous-agent@ai-maestro-plugins --scope local
```

## The persona at a glance

- **Writable scope**: own working directory (`~/agents/<name>/`) +
  `/tmp` + `~/.dev-browser/tmp` + own AMP inbox + `git push` on
  branches you created in repos the host user owns
- **Forbidden**: cross-agent mutation, secrets access, unauthorized
  `gh pr merge`, destructive git on shared branches, `rm -rf` outside
  own workdir / tmp, user-scope plugin installation, killing other
  agents without explicit instruction
- **AMP routing (R6 v2)**: MANAGER + peer AUTONOMOUS + HUMAN freely
  (`Y`); MAINTAINER and all team roles must route through MANAGER. HUMAN
  edge is a governance-layer `Y` (not reply-only) so AUTONOMOUS may
  initiate user contact.
- **PR discipline**: open, iterate per review, never self-merge
- **Response SLA**: 10 min to MANAGER AMP messages

Full rules in `agents/ai-maestro-autonomous-agent-main-agent.md`.

## Relationship to other plugins

| Plugin | Title | Role |
|---|---|---|
| `ai-maestro-plugin` | — | R17 core. Required for every agent. Provides utilities, not governance. |
| `ai-maestro-assistant-manager-agent` | MANAGER | Team manager role-plugin |
| `ai-maestro-chief-of-staff` | CHIEF-OF-STAFF | Team gateway role-plugin |
| `ai-maestro-orchestrator-agent` | ORCHESTRATOR | Team orchestrator role-plugin |
| `ai-maestro-architect-agent` | ARCHITECT | Team architect role-plugin |
| `ai-maestro-integrator-agent` | INTEGRATOR | Team integrator role-plugin |
| `ai-maestro-programmer-agent` | MEMBER | Team programmer role-plugin |
| `ai-maestro-maintainer-agent` | MAINTAINER | Repo-bound gatekeeper role-plugin |
| **`ai-maestro-autonomous-agent`** | **AUTONOMOUS** | **No-team helper role-plugin (this plugin)** |

All 8 predefined role-plugins follow the 1:1 (one plugin per title)
pattern. Custom role-plugins with the same `compatible-titles` may
coexist (the wizard shows them as alternatives in the role-plugin
dropdown).

## License

MIT. Copyright 2026 Emasoft.

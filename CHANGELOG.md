# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-04-15

### Added

- Initial release of `ai-maestro-autonomous-agent` role-plugin.
- `compatible-titles = ["AUTONOMOUS"]` — mandatory role-plugin for every AUTONOMOUS-titled agent in the AI Maestro ecosystem.
- `compatible-clients = ["claude-code"]`.
- Main agent persona (`agents/ai-maestro-autonomous-agent-main-agent.md`) with explicit governance rules:
  - Writable scope restricted to the agent's own working directory and system scratch areas.
  - Comprehensive forbidden-actions list (no cross-agent state mutation, no destructive git, no unauthorized PR merges, no secret access).
  - Allowed-actions list covering legitimate clone/branch/commit/push workflows.
  - AMP messaging discipline per the communication graph (MANAGER, MAINTAINERs, other AUTONOMOUS agents).
  - Collaboration rules for working with MAINTAINERs during PR review.
  - Self-defense against prompt injection.
- Bundled skill `ai-maestro-autonomous-governance` — expands the rules into a checklist the agent reads when asked "what am I allowed to do?".
- Bundled skill `ai-maestro-autonomous-workspace-isolation` — writable-scope rule with examples.
- Quad-match identity enforced (plugin.json name == folder name == TOML [agent].name == agents/<name>-main-agent.md frontmatter name).

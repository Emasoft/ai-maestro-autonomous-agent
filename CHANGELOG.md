# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-06-09

### Features

- Validators updated for Claude Code v2.1.81–v2.1.143 plugin contract:
  - **Hooks** (`scripts/validate_hook.py`):
    - Accept the new exec form `args: string[]` (v2.1.139) alongside the
      existing shell form `command: string`.
    - Accept `type: "mcp_tool"` hooks with required `server`/`tool` fields
      and optional `arguments` (v2.1.118).
    - Validate `continueOnBlock` boolean on PostToolUse hooks (v2.1.139).
    - Sharper rejection message when `prompt`/`agent` hook types are used on
      command-only events (v2.1.142 explicit "use a command-type hook
      instead").
    - Recognize `$CLAUDE_EFFORT` in hook command env (v2.1.133).
  - **MCP** (`scripts/validate_mcp.py`):
    - Accept `alwaysLoad: bool` field on MCP server config (v2.1.121).
    - Reject `workspace` as an MCP server name (v2.1.128 reserved name —
      silently skipped at load time).
  - **Skills** (`scripts/validate_skill.py`):
    - Raised description ceiling: hard MAJOR at >1,536 chars (v2.1.105
      listing cap) and NIT at >1,024 chars. Replaces the prior 500-char
      shortening hint, which was too aggressive against the new cap.
  - **Marketplace pipeline** (`scripts/validate_marketplace_pipeline.py`):
    - Warn when plugin.json declares `themes`/`monitors` at the top level
      instead of under `experimental: {}` (v2.1.129 migration).
  - **Plugin manifest** (`scripts/cpv_validation_common.py`):
    - Added `KNOWN_PLUGIN_MANIFEST_FIELDS` (incl. `$schema` per v2.1.120,
      `monitors` per v2.1.105, `experimental` per v2.1.129).
    - Added `KNOWN_MARKETPLACE_MANIFEST_FIELDS` (incl. `$schema`, `version`,
      `description` per v2.1.120).
  - **Agent** (`scripts/validate_agent.py`):
    - Documented that `hooks` (v2.1.116), `mcpServers` (v2.1.117),
      `permissionMode` and `tools`/`disallowedTools` (v2.1.119) are now
      honored for main-thread `--agent` sessions.

## [1.0.8] - 2026-04-26

### Bug Fixes

- Strip #anchor before referenced-file existence check

### Styling

- Code-fence external server refs and add 2 example blocks



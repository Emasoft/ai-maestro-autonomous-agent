# Writable-Scope Layers

## Table of Contents

- [Layer 1 Writable locally](#layer-1--writable-locally)
- [Layer 2 Writable via git push](#layer-2--writable-via-git-push)
- [Layer 3 Read-only paths](#layer-3--read-only-never-write)
- [Programmatic path check](#programmatic-path-check)

## Layer 1 — Writable locally

| Path | OK to write? |
|---|---|
| `~/agents/<my-name>/` and all subdirs | YES |
| `~/agents/<my-name>/.claude/` | YES — local plugin installs only |
| `/tmp` and `/private/tmp` | YES |
| macOS per-user scratch (system-managed temp dir) | YES — use PID suffix |
| `~/.dev-browser/tmp/` (if dev-browser running) | YES — screenshots |
| `~/.agent-messaging/agents/<my-name>/` | YES — inbox only |

## Layer 2 — Writable via git push

| Target | OK? | How |
|---|---|---|
| Host-user GitHub repo, on a branch I created | YES | `git push origin my-branch` |
| Host-user GitHub repo, on main/master/develop | NO | PR review only |
| Someone else's GitHub repo | NO | fork first |
| Any repo, destructive push (`--force`, `--mirror`) | NO | not allowed |

## Layer 3 — Read-only (never write)

Everything outside Layers 1 and 2. Key examples:

| Path | OK to write? |
|---|---|
| `~/agents/<some-other-agent>/` | NO (READ is fine) |
| `~/.aimaestro/agents/registry.json` | NO (use HTTP API) |
| `~/.aimaestro/teams/*.json` | NO (use HTTP API) |
| `~/.claude/` | NO |
| `~/.ssh/`, `~/.gnupg/`, `~/.config/gh/` | NO (no read either) |
| system paths (`/etc`, `/usr`, `/opt`, etc.) | NO |
| `~/Documents`, `~/Desktop`, `~/Downloads` | NO |

## Programmatic path check

```bash
TARGET="/path/to/check"
MY_AGENT_NAME="my-agent-name"
case "$TARGET" in
    $HOME/agents/$MY_AGENT_NAME/*|/tmp/*|/private/tmp/*) echo ALLOWED ;;
    *) echo FORBIDDEN ;;
esac
```

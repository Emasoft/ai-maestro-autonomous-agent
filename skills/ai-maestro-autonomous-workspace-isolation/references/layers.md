# Writable-Scope Layers and Situations

## Table of Contents

- [Writable-scope table](#writable-scope-table)
- [Programmatic path check](#programmatic-path-check)
- [Common situations](#common-situations)

## Writable-scope table

Three layers: writable locally, writable via `git push`, read-only.

### Layer 1 — Writable locally

| Path | OK to write? |
|---|---|
| `~/agents/<my-name>/` and all subdirs | YES |
| `~/agents/<my-name>/.claude/` | YES — local plugin installs only |
| `/tmp` and `/private/tmp` | YES |
| macOS per-user scratch (system-managed temp dir) | YES — use PID suffix |
| `~/.dev-browser/tmp/` (if dev-browser running) | YES — screenshots |
| `~/.agent-messaging/agents/<my-name>/` | YES — inbox only |

### Layer 2 — Writable via git push

| Target | OK? | How |
|---|---|---|
| Host-user GitHub repo, on a branch I created | YES | `git push origin my-branch` |
| Host-user GitHub repo, on main/master/develop | NO | PR review only |
| Someone else's GitHub repo | NO | fork first |
| Any repo, destructive push (`--force`, `--mirror`) | NO | not allowed |

### Layer 3 — Read-only (never write)

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
TARGET="/path/to/proposed/write/target"
MY_AGENT_NAME="<your-agent-name>"
case "$TARGET" in
    $HOME/agents/$MY_AGENT_NAME/*|/tmp/*|/private/tmp/*) echo ALLOWED ;;
    *) echo "FORBIDDEN — use the HTTP API or a different path" ;;
esac
```

## Common situations

Right / wrong pairs for the 10 most common write operations.

**Clone a repo** — Right: `cd ~/agents/<my-name>/ && git clone <url> <repo-name>`. Wrong: `cd ~/Documents && git clone <url>`.

**Install a Python package** — Right: `cd ~/agents/<my-name>/project && uv venv && uv pip install <pkg>` (venv local to project). Wrong: `pip install <pkg>` (writes to user-scope site-packages).

**Install a Claude Code plugin for yourself** — Right: ask the user or MANAGER to call `PATCH /api/agents/<my-id>`. Wrong: `claude plugin install ...` at user scope.

**Save a work log** — Right: `echo "$LOG" > ~/agents/<my-name>/work-log.md`. Wrong: `echo "$LOG" > ~/.aimaestro/my-log.md`.

**Scratch file while debugging** — Right: `echo "$S" > /tmp/my-scratch-$$.txt` (PID suffix avoids collisions). Wrong: `echo "$S" > /tmp/scratch.txt` (collision risk) or writing to another agent's dir.

**Read another agent's conversation log** — Right: `cat ~/.claude/projects/.../<session>.jsonl` (reads are unrestricted). Wrong: editing or deleting the log.

**Push changes to GitHub** — Right: `cd ~/agents/<my-name>/<repo>/ && git push origin my-branch` (agent-created branch, host-user repo). Wrong: `git push --force`, pushing to `main` directly, or pushing to a repo without write access.

**Stop another agent** — Right: AMP MANAGER explaining why; MANAGER calls the hibernate API. Wrong: `tmux kill-session -t <other-agent>` or editing another agent's settings.

**Update my own agent's config** — Right: ask the user or MANAGER to call `PATCH /api/agents/<my-id>`. Wrong: editing `~/.aimaestro/agents/registry.json` directly.

**Access a secret (e.g. a PAT)** — Right: wait for the user to place the credential in an allowed file under your own workdir (e.g. `~/agents/<my-name>/.env.local`), read from there, never copy or echo. Wrong: reading `~/.ssh/id_ed25519`, `~/.config/gh/hosts.yml`, or any `.env` outside your own workdir.

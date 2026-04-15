---
description: >
  Use when an AUTONOMOUS agent needs concrete examples of the
  writable-scope rule — what paths it may write to, what paths it may
  only read, and how to handle edge cases like cross-repo work,
  system utilities, and shared caches. Trigger with "where can I write",
  "is this path allowed", "workspace isolation".
allowed-tools: "Read, Glob, Grep, Bash"
---

# AI Maestro Autonomous Workspace Isolation — Writable Scope Examples

The AUTONOMOUS governance rule is: **READ anywhere, WRITE only inside
your own agent working directory and system scratch.** This skill makes
the rule concrete with examples.

## Overview

You are running inside your own tmux session as an AUTONOMOUS agent.
Your canonical working directory is `~/agents/<your-name>/` (substitute
your actual agent name — e.g. `~/agents/scen018-contrib/`). The three
layers of the rule are:

1. **Writable by default**: your own working directory + system scratch
2. **Writable via network protocol only**: GitHub repos (via `git push`)
3. **Read-only**: everything else on the filesystem

Any WRITE operation that touches a path outside layer 1 or 2 is
forbidden. Reads are unrestricted.

## Layer 1 — Writable locally

| Path | OK to write? | Example |
|---|---|---|
| `~/agents/<my-name>/` | YES | `~/agents/contrib-alpha/project/src/main.py` |
| `~/agents/<my-name>/.claude/` | YES | local plugins installed to my own agent |
| `~/agents/<my-name>/workspace/` | YES | `git clone` destination |
| `/tmp` | YES | `/tmp/scratch.txt` |
| `/private/tmp` | YES | macOS symlink to /tmp |
| `/var/folders/xx/...` | YES | macOS per-user scratch |
| `~/.dev-browser/tmp/` | YES (if dev-browser is running) | screenshots |
| `~/.agent-messaging/agents/<my-name>/` | YES | AMP inbox (read/delete only) |

## Layer 2 — Writable via git push

| Target | OK to write? | How |
|---|---|---|
| `github.com/<host-user>/<repo>` on a branch I created | YES | `git push origin my-fix-branch` |
| `github.com/<host-user>/<repo>` on main/master/develop | NO | must go via PR review |
| `github.com/<someone-else>/<repo>` | NO (no write access anyway) | fork first |
| `github.com/<host-user>/<repo>` destructive: `--force`, `--mirror`, `--prune` | NO | not allowed |

## Layer 3 — Read-only

Everything outside layers 1 and 2. Some notable examples:

| Path | OK to write? |
|---|---|
| `~/agents/<some-other-agent>/` | NO (you may READ for reference) |
| `~/.aimaestro/agents/registry.json` | NO (use the HTTP API) |
| `~/.aimaestro/teams/*.json` | NO (use the HTTP API) |
| `~/.aimaestro/governance.json` | NO |
| `~/.aimaestro/secrets/` | NO (you may not even READ) |
| `~/.claude/` (user-scope plugins, settings) | NO |
| `~/.ssh/`, `~/.gnupg/`, `~/.config/gh/` | NO (also no read) |
| `~/.env`, other home-scope dotenv files | NO |
| `/etc`, `/usr`, `/opt`, `/Library` | NO |
| `~/Documents`, `~/Desktop`, `~/Downloads` | NO (user's stuff, not yours) |
| `~/Library/Caches/`, `~/.cache/` | NO (except your own agent's subdir) |

## Common situations and the right answer

### Situation 1: I want to clone a repo

**Right**: `cd ~/agents/<my-name>/ && git clone <url> <repo-name>`.
**Wrong**: `cd ~/Documents && git clone <url>`.

### Situation 2: I want to install a Python package

**Right**: `cd ~/agents/<my-name>/project && uv venv && uv pip install <pkg>` (venv is local to project).
**Wrong**: `pip install <pkg>` (installs to user-scope site-packages).

### Situation 3: I want to install a Claude Code plugin for myself

**Right**: The user or MANAGER must install plugins via the AI Maestro
PATCH API. You don't install plugins yourself.
**Wrong**: `claude plugin install ...` at user scope.

### Situation 4: I want to save a work log

**Right**: `echo "$LOG" > ~/agents/<my-name>/work-log.md`.
**Wrong**: `echo "$LOG" > ~/.aimaestro/my-log.md`.

### Situation 5: I want to write a scratch file while debugging

**Right**: `echo "$SCRATCH" > /tmp/my-scratch-$$.txt` (use PID suffix
to avoid collision with other agents).
**Wrong**: `echo "$SCRATCH" > /tmp/scratch.txt` (collision risk) — use
a unique name.
**Also wrong**: `echo "$SCRATCH" > ~/agents/<someone-else>/scratch.txt`.

### Situation 6: I want to read another agent's conversation log

**Right (read-only)**: `cat ~/.claude/projects/-Users-<user>-agents-<other>/<session>.jsonl`.
This is READ, which is allowed.
**Wrong**: editing or deleting that file.

### Situation 7: I want to push my changes to GitHub

**Right**: `cd ~/agents/<my-name>/<repo>/ && git push origin my-branch`
(on a branch I created, to a repo the host user owns).
**Wrong**: `git push --force` (destructive), or pushing to `main`
directly, or pushing to someone else's repo.

### Situation 8: I want to stop another agent

**Right**: Send an AMP message to MANAGER explaining why, and let
MANAGER decide whether to hibernate the other agent via the API.
**Wrong**: `tmux kill-session -t <other-agent-name>`, or directly
editing the other agent's `settings.local.json`.

### Situation 9: I want to update my own agent's config

**Right**: Ask the user or MANAGER to call
`PATCH /api/agents/<my-id>` with the desired changes.
**Wrong**: Editing `~/.aimaestro/agents/<my-id>/config.json` directly,
or editing `~/.aimaestro/agents/registry.json`.

### Situation 10: I want to access a secret (e.g., a PAT)

**Right**: Wait for the user to provide credentials in a specific
allowed file (e.g., `~/agents/<my-name>/.env.local`) and read from
there. Never copy or echo the secret anywhere.
**Wrong**: Reading `~/.ssh/id_ed25519`, `~/.config/gh/hosts.yml`, or
any `.env` file outside your own working directory.

## How to self-check a path before writing

```bash
# Inside a dev-browser script or bash command, before writing
TARGET="/path/to/proposed/write/target"
MY_AGENT_NAME="<your-agent-name>"

case "$TARGET" in
    $HOME/agents/$MY_AGENT_NAME/*) echo OK ;;
    /tmp/*|/private/tmp/*|/var/folders/*) echo OK ;;
    *) echo FORBIDDEN — use the HTTP API or a different path ;;
esac
```

## Reading is free

You can `cat`, `grep`, `find -type f`, `ls -la`, `head`, `tail`,
`git log`, `git diff`, `git show`, `git blame` on ANY path on the
filesystem. The restriction is only on WRITES. Reads are how you
learn about the environment — they're not forbidden.

## Reference

Full governance rules:
`agents/ai-maestro-autonomous-agent-main-agent.md` (main agent persona).

Quick checklist:
`skills/ai-maestro-autonomous-governance/SKILL.md` (self-audit).

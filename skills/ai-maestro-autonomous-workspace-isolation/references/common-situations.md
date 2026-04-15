# Workspace Isolation — Common Situations Guide

## Table of Contents

- [How to self-check a path before writing](#how-to-self-check-a-path-before-writing)
- [Situation 1: Clone a repo](#situation-1-clone-a-repo)
- [Situation 2: Install a Python package](#situation-2-install-a-python-package)
- [Situation 3: Install a Claude Code plugin](#situation-3-install-a-claude-code-plugin)
- [Situation 4: Save a work log](#situation-4-save-a-work-log)
- [Situation 5: Scratch file while debugging](#situation-5-scratch-file-while-debugging)
- [Situation 6: Read another agent's conversation log](#situation-6-read-another-agents-conversation-log)
- [Situation 7: Push changes to GitHub](#situation-7-push-changes-to-github)
- [Situation 8: Stop another agent](#situation-8-stop-another-agent)
- [Situation 9: Update my own agent's config](#situation-9-update-my-own-agents-config)
- [Situation 10: Access a secret](#situation-10-access-a-secret)

## How to self-check a path before writing

```bash
TARGET="/path/to/proposed/write/target"
MY_AGENT_NAME="<your-agent-name>"

case "$TARGET" in
    $HOME/agents/$MY_AGENT_NAME/*) echo OK ;;
    /tmp/*|/private/tmp/*) echo OK ;;
    *) echo "FORBIDDEN — use the HTTP API or a different path" ;;
esac
```

## Situation 1: Clone a repo

**Right**: `cd ~/agents/<my-name>/ && git clone <url> <repo-name>`.
**Wrong**: `cd ~/Documents && git clone <url>`.

## Situation 2: Install a Python package

**Right**: `cd ~/agents/<my-name>/project && uv venv && uv pip install <pkg>`
(venv local to project).
**Wrong**: `pip install <pkg>` (installs to user-scope site-packages).

## Situation 3: Install a Claude Code plugin for myself

**Right**: Ask the user or MANAGER to call `PATCH /api/agents/<my-id>`
with the desired plugin change.
**Wrong**: `claude plugin install ...` at user scope.

## Situation 4: Save a work log

**Right**: `echo "$LOG" > ~/agents/<my-name>/work-log.md`.
**Wrong**: `echo "$LOG" > ~/.aimaestro/my-log.md`.

## Situation 5: Write a scratch file while debugging

**Right**: `echo "$SCRATCH" > /tmp/my-scratch-$$.txt` (PID suffix
avoids collision with other agents).
**Wrong**: `echo "$SCRATCH" > /tmp/scratch.txt` (collision risk) or
`echo "$SCRATCH" > ~/agents/<someone-else>/scratch.txt`.

## Situation 6: Read another agent's conversation log

**Right (read-only)**: `cat ~/.claude/projects/-Users-<user>-agents-<other>/<session>.jsonl`.
This is a READ, which is allowed everywhere.
**Wrong**: editing or deleting that file.

## Situation 7: Push changes to GitHub

**Right**: `cd ~/agents/<my-name>/<repo>/ && git push origin my-branch`
(on a branch I created, to a repo the host user owns).
**Wrong**: `git push --force` (destructive), pushing to `main` directly,
or pushing to a repo you have no write access to.

## Situation 8: Stop another agent

**Right**: Send an AMP message to MANAGER explaining why, and let
MANAGER decide whether to hibernate the other agent via the API.
**Wrong**: `tmux kill-session -t <other-agent-name>`, or directly
editing the other agent's `settings.local.json`.

## Situation 9: Update my own agent's config

**Right**: Ask the user or MANAGER to call
`PATCH /api/agents/<my-id>` with the desired changes.
**Wrong**: editing `~/.aimaestro/agents/registry.json` directly.

## Situation 10: Access a secret (e.g., a PAT)

**Right**: Wait for the user to provide credentials in a specific
allowed file (e.g., `~/agents/<my-name>/.env.local`) and read from
there. Never copy or echo the secret anywhere.
**Wrong**: Reading `~/.ssh/id_ed25519`, `~/.config/gh/hosts.yml`, or
any `.env` file outside your own working directory.

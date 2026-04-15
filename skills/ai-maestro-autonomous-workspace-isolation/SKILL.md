---
description: >
  Use when an AUTONOMOUS agent needs to determine whether a write target
  is within its allowed scope. Provides the three-layer writable-scope
  table and quick path check. Trigger with "where can I write", "is this
  path allowed", "workspace isolation".
allowed-tools: "Read, Glob, Grep, Bash(git:*), Bash(uv:*)"
---

# AI Maestro Autonomous Workspace Isolation — Writable Scope

The AUTONOMOUS governance rule: **READ anywhere, WRITE only inside your
own agent working directory and system scratch.**

## Overview

This skill resolves the writable-scope question for AUTONOMOUS agents.
Writes are allowed in exactly three places: (1) your own agent working
directory, (2) system scratch areas (tmp + dev-browser tmp + your own
AMP inbox), and (3) GitHub repositories owned by the host user — but
only via normal `git push` on branches you created. Everything else
is read-only. This skill gives you a three-layer table to check a
target path against, and a copy-pastable shell snippet to automate the
check inside scripts. The full worked-example catalogue (10 common
situations) lives in the linked reference file.

## Prerequisites

- You are an AUTONOMOUS agent with `ai-maestro-autonomous-agent` installed.
- You know your agent name (used as `<my-name>` below).
- `git`, `uv`, and standard Unix tools are available.

## Instructions

Follow these steps before executing any write operation.

1. **Identify the write target path** in the proposed command. If
   multiple paths are written in one command (e.g. `tar` outputs,
   `cp` destinations, redirections), list all of them.
2. **Normalize the path** to absolute form (resolve `~`, `.`, `..`,
   environment variables) so the check is deterministic.
3. **Check Layer 1** (see the "Writable locally" table below). If the
   absolute path matches any Layer 1 pattern, the write is ALLOWED.
4. **If not Layer 1, check Layer 2** (see "Writable via git push"). If
   the operation is `git push` to a branch you created in a host-user
   repo, the push is ALLOWED.
5. **If neither Layer 1 nor Layer 2 matches**, the write is FORBIDDEN.
   Send an AMP message to MANAGER asking for clarification or propose
   an alternative that stays in scope (e.g. clone the target repo into
   your own working directory first, then edit locally).
6. **After the write succeeds**, log the target path in `loop.md` for
   traceability.

Working checklist:

- [ ] Identify the write target path
- [ ] Check Layer 1 (local writable)
- [ ] If not Layer 1, check Layer 2 (git push)
- [ ] If neither, treat as FORBIDDEN and ask via AMP

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
| `/etc`, `/usr`, `/opt`, system paths | NO |
| `~/Documents`, `~/Desktop`, `~/Downloads` | NO |

## Output

- Path is in Layer 1 or Layer 2 → **ALLOWED** to write.
- Path is in Layer 3 → **FORBIDDEN** to write (reads are still fine).
- Path is uncertain → **Ask via AMP** before acting.

## Error Handling

If you are unsure whether a path is in scope, treat it as FORBIDDEN and
ask MANAGER via AMP. Never guess on destructive operations.

If an operation is forbidden, explain which layer it violates, propose an
alternative (e.g., clone into your own directory instead), and wait.

## Examples

**Clone a repo**:
```bash
# ALLOWED
git clone <url> ~/agents/<my-name>/<repo-name>

# FORBIDDEN — wrong working directory
cd ~/Documents && git clone <url>
```

**Write a scratch file**:
```bash
# ALLOWED — use PID to avoid collisions
echo "$data" > /tmp/aimaa-scratch-$$.txt

# FORBIDDEN — another agent's directory
echo "$data" > ~/agents/other-agent/scratch.txt
```

**Check a path programmatically**:
```bash
TARGET="/path/to/check"
MY_AGENT_NAME="my-agent-name"
case "$TARGET" in
    $HOME/agents/$MY_AGENT_NAME/*|/tmp/*|/private/tmp/*) echo ALLOWED ;;
    *) echo FORBIDDEN ;;
esac
```

## Resources

- [Common Situations Guide](references/common-situations.md)
  > 10 real-world scenarios with right/wrong answers: cloning repos,
  > installing packages, saving logs, writing scratch files, reading
  > other agents' logs, pushing to GitHub, stopping agents, config
  > updates, secret handling.
- Governance checklist: `skills/ai-maestro-autonomous-governance/SKILL.md`
- Full persona: `agents/ai-maestro-autonomous-agent-main-agent.md`

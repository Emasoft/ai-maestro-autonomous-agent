---
description: >
  Use when an AUTONOMOUS agent needs to determine whether a write target
  is within its allowed scope. Three-layer writable-scope check. Trigger
  with "where can I write", "is this path allowed", "workspace isolation".
allowed-tools: "Read, Glob, Grep, Bash(git:*), Bash(uv:*)"
---

# AI Maestro Autonomous Workspace Isolation — Writable Scope

The AUTONOMOUS governance rule: **READ anywhere, WRITE only inside
your own agent working directory and system scratch.**

**Server state is not a path — it is a CLI call (R23).** Anything held by
the AI Maestro server (agent registry, teams, governance) is mutated ONLY
through the frozen CLI scripts — `aimaestro-agent.sh`, `aimaestro-teams.sh`,
the messaging wrappers. **Never call a server HTTP route (`/api/*`)
directly**, with any client. Editing the backing JSON under `~/.aimaestro/`
and calling the route are the same violation by two different doors; the
CLI is the only sanctioned one, because it runs the pipeline gates both
shortcuts bypass. Binds hooks and scripts too, and routes that only look read-only.

## Overview

Writes allowed in three places only: (1) the agent's own working dir,
(2) system scratch, (3) host-user GitHub repos via `git push` on
agent-created branches. Everything else is read-only. Full path
tables, programmatic check, and 10 worked situations:
[layers](references/layers.md).

## Prerequisites

- You are an AUTONOMOUS agent with `ai-maestro-autonomous-agent` installed.
- You know your agent name (used as `<my-name>` below).
- `git`, `uv`, and standard Unix tools are available.

## Instructions

Follow these steps before executing any write operation.

1. **Identify the write target path** in the proposed command. If
   multiple paths are written (e.g. `tar` outputs, `cp` destinations,
   redirections), list all of them.
2. **Canonicalize each path** — absolute form (`~`, `.`, `..`, environment
   variables) **and every symlink resolved** (`realpath`), so the check is
   deterministic. Resolving the symlinks is not optional: a link inside your
   own workdir can point at another agent's directory, and a glob match on the
   un-resolved string happily approves that write. Claude Code fixed this same
   class in its own isolation three times (2.1.212, 2.1.216, 2.1.217) — a scope
   check that compares literal strings is not a scope check.
3. **Open the [layers](references/layers.md) reference** and check
   each canonicalized path against Layer 1 (writable locally). If all
   paths match Layer 1 patterns, the write is ALLOWED.
4. **For any path not in Layer 1**, check Layer 2 (writable via
   `git push`). If the operation is `git push` to a branch you
   created in a host-user repo, the push is ALLOWED.
5. **If neither Layer 1 nor Layer 2 matches**, the write is
   FORBIDDEN. Send an AMP message to MANAGER asking for clarification
   or propose an alternative (typical fix: clone the target repo into
   your own working directory and edit locally).
6. **After the write succeeds**, log the target path in `loop.md` for
   traceability.

Copy this checklist and track your progress:

- [ ] Identify the write target path(s)
- [ ] Canonicalize path(s) — absolute AND symlink-resolved
- [ ] Check Layer 1 (local writable)
- [ ] If not Layer 1, check Layer 2 (git push)
- [ ] If neither, treat as FORBIDDEN and ask via AMP

## Output

- **ALLOWED**: path matches Layer 1 or Layer 2 → execute the write →
  log in `loop.md`.
- **FORBIDDEN**: path matches Layer 3 (read-only) or is unrecognized →
  stop, explain the violated rule, propose an alternative.
- **UNCERTAIN**: path is ambiguous → treat as FORBIDDEN, ask via AMP.

## Error Handling

If you are unsure whether a path is in scope, treat it as FORBIDDEN
and ask MANAGER via AMP. Never guess on destructive operations. If
the action needs to write outside your own workdir to be useful, the
typical fix is to clone or copy the target INTO your own workdir
first and edit the local copy.

## Examples

**Clone a repo**:
```bash
# ALLOWED — target is under my own workdir
git clone <url> ~/agents/<my-name>/<repo-name>

# FORBIDDEN — wrong working directory
cd ~/Documents && git clone <url>
```

**Write a scratch file**:
```bash
# ALLOWED — /tmp plus PID suffix avoids collisions
echo "$data" > /tmp/aimaa-scratch-$$.txt

# FORBIDDEN — another agent's directory
echo "$data" > ~/agents/other-agent/scratch.txt
```

**Check a path programmatically** — resolve first, compare second (the
un-resolved form approves a symlink out of your scope):
```bash
TARGET="/path/to/check"
MY_AGENT_NAME="my-agent-name"
TARGET_REAL="$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$TARGET")"
HOME_REAL="$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$HOME")"
case "$TARGET_REAL" in
    "$HOME_REAL/agents/$MY_AGENT_NAME"/*|/tmp/*|/private/tmp/*) echo ALLOWED ;;
    *) echo FORBIDDEN ;;
esac
```
The full check — per-user scratch and the hard-link refusal — is in
[layers](references/layers.md#programmatic-path-check).

## Resources

- [Writable-Scope Layers and Situations](references/layers.md)
  - [Writable-scope table](references/layers.md#writable-scope-table)
  - [Programmatic path check](references/layers.md#programmatic-path-check)
  - [Common situations](references/layers.md#common-situations)
- Governance checklist: `skills/ai-maestro-autonomous-governance/SKILL.md`
- Full persona: `agents/ai-maestro-autonomous-agent-main-agent.md`

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

## Overview

Writes allowed in three places only: (1) the agent's own working dir,
(2) system scratch, (3) host-user GitHub repos via `git push` on
agent-created branches. Everything else is read-only. Three-layer
check: [layers](references/layers.md) has the full path tables,
[common-situations](references/common-situations.md) has 10 worked
examples. Use the checklist below before any write.

## Prerequisites

- You are an AUTONOMOUS agent with `ai-maestro-autonomous-agent` installed.
- You know your agent name (used as `<my-name>` below).
- `git`, `uv`, and standard Unix tools are available.

## Instructions

Follow these steps before executing any write operation.

1. **Identify the write target path** in the proposed command. If
   multiple paths are written (e.g. `tar` outputs, `cp` destinations,
   redirections), list all of them.
2. **Normalize each path** to absolute form (resolve `~`, `.`, `..`,
   environment variables) so the check is deterministic.
3. **Open the [layers](references/layers.md) reference** and check
   each normalized path against Layer 1 (writable locally). If all
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
- [ ] Normalize path(s) to absolute form
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

- [Writable-Scope Layers](references/layers.md)
  - [Layer 1 Writable locally](references/layers.md#layer-1--writable-locally)
  - [Layer 2 Writable via git push](references/layers.md#layer-2--writable-via-git-push)
  - [Layer 3 Read-only paths](references/layers.md#layer-3--read-only-never-write)
  - [Programmatic path check](references/layers.md#programmatic-path-check)
- [Common Situations Guide](references/common-situations.md)
  - [How to self-check a path before writing](references/common-situations.md#how-to-self-check-a-path-before-writing)
  - [Situation 1: Clone a repo](references/common-situations.md#situation-1-clone-a-repo)
  - [Situation 2: Install a Python package](references/common-situations.md#situation-2-install-a-python-package)
  - [Situation 3: Install a Claude Code plugin](references/common-situations.md#situation-3-install-a-claude-code-plugin)
  - [Situation 4: Save a work log](references/common-situations.md#situation-4-save-a-work-log)
  - [Situation 5: Scratch file while debugging](references/common-situations.md#situation-5-scratch-file-while-debugging)
  - [Situation 6: Read another agent's conversation log](references/common-situations.md#situation-6-read-another-agents-conversation-log)
  - [Situation 7: Push changes to GitHub](references/common-situations.md#situation-7-push-changes-to-github)
  - [Situation 8: Stop another agent](references/common-situations.md#situation-8-stop-another-agent)
  - [Situation 9: Update my own agent's config](references/common-situations.md#situation-9-update-my-own-agents-config)
  - [Situation 10: Access a secret](references/common-situations.md#situation-10-access-a-secret)
- Governance checklist: `skills/ai-maestro-autonomous-governance/SKILL.md`
- Full persona: `agents/ai-maestro-autonomous-agent-main-agent.md`

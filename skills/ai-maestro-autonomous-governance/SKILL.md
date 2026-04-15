---
description: >
  Use when an AUTONOMOUS agent needs to self-audit before executing a
  destructive or ambiguous action. Walks through 10 governance questions
  and returns ALLOWED or FORBIDDEN. Trigger with "can I do this?", "am I
  allowed to", "is this within my scope".
allowed-tools: "Read, Grep, Glob"
---

# AI Maestro Autonomous Governance — Self-Audit Checklist

Before executing any non-trivial action, walk through this checklist.
If ANY answer triggers the FORBIDDEN outcome, stop immediately.

## Overview

This skill gives an AUTONOMOUS agent a 10-question self-audit to run
before any non-trivial action. The questions map 1:1 to the forbidden-
action rules in the main agent persona. Each question has exactly one
answer (ALLOWED or FORBIDDEN) so the checklist is deterministic: if
every question passes, the action is safe; if any question fails, the
action is blocked and the agent must either adjust the plan or escalate
via AMP before proceeding. The 10 questions cover write targets, other-
agent isolation, state-file mutation, secret access, PR merging,
destructive git, cross-agent lifecycle operations, `rm -rf` scope,
user-scope installations, and AMP routing.

## Prerequisites

- You are an AUTONOMOUS agent with `ai-maestro-autonomous-agent` installed.
- You have the `agent-messaging` skill available (from `ai-maestro-plugin`).
- You know your own agent name (`~/agents/<your-name>/`).

## Instructions

Follow these steps in order. Stop at the first FORBIDDEN outcome.

1. **Read the action you are about to take** and identify every path it
   writes to, every git command it invokes, and every recipient it will
   message via AMP.
2. **Copy the checklist below** into your session notes (or `loop.md`)
   and answer each question Q1 through Q10 in order.
3. **Record ALLOWED or FORBIDDEN** for each question. At the first
   FORBIDDEN, stop the audit — the overall verdict is FORBIDDEN.
4. **If all 10 questions return ALLOWED**, the action is safe. Proceed,
   and log the action's purpose + outcome in `loop.md` for traceability.
5. **If any question returns FORBIDDEN**, do NOT take the action. Explain
   which rule was violated to the user (or MANAGER via AMP), propose an
   alternative that stays in scope, and wait for clarification.
6. **On completion of the underlying task**, send an AMP status update
   to MANAGER summarizing what you did.

Working copy of the checklist:

- [ ] Q1 Write target check
- [ ] Q2 Other-agent check
- [ ] Q3 State file check
- [ ] Q4 Secret check
- [ ] Q5 PR merge check
- [ ] Q6 Destructive git check
- [ ] Q7 Other-agent lifecycle check
- [ ] Q8 rm -rf scope check
- [ ] Q9 User-scope installation check
- [ ] Q10 AMP routing check

## The 10-Question Self-Audit

**Q1 Write target check** — Does every WRITE target fall under:
- `~/agents/<my-name>/` (my own working dir)
- System scratch (see workspace-isolation skill §Layer 1)
- My own AMP inbox (`~/.agent-messaging/agents/<my-name>/`)
- A host-user GitHub repo via `git push origin <my-branch>`

If NO → FORBIDDEN. Stop.

**Q2 Other-agent check** — Does my action WRITE to any path under
`~/agents/<some-other-agent>/`? Reading is fine.
If YES → FORBIDDEN. Stop.

**Q3 State file check** — Does my action write to
`~/.aimaestro/agents/registry.json`, `~/.aimaestro/teams/*.json`,
`~/.aimaestro/governance.json`, or any file under
`~/.aimaestro/agents/<other>/`?
If YES → FORBIDDEN. Use the HTTP API instead. Stop.

**Q4 Secret check** — Does my action read or copy files under
`~/.aimaestro/secrets/`, `~/.ssh/`, `~/.config/gh/`, `~/.gnupg/`, any
`.env` file not in my own workdir, or any file whose name contains
`token`, `credential`, `password`, `secret`, `private_key`?
If YES → FORBIDDEN. Stop.

**Q5 PR merge check** — Does my action invoke `gh pr merge`?
If YES → Did the USER give me an explicit instruction in the CURRENT
turn to merge that specific PR by number? If not → FORBIDDEN. Stop.

**Q6 Destructive git check** — Does my action use `git push --force`,
`git reset --hard`, `git clean -fd`, `git branch -D`, `git rebase -i`,
or any history-rewriting command?
If YES → Is the target a branch I created alone that has NOT been pushed
to any shared branch? If not → FORBIDDEN. Stop.

**Q7 Other-agent lifecycle check** — Does my action kill, hibernate,
wake, restart, or mutate another agent via tmux or direct API calls?
If YES → Did the USER or MANAGER EXPLICITLY instruct me in the CURRENT
turn? If not → FORBIDDEN. Stop.

**Q8 rm -rf scope check** — Does my action use `rm -rf` or equivalent
(`find ... -delete`, `shred -u`, `dd if=/dev/zero`)?
If YES → Is the target strictly under a system scratch area
(see workspace-isolation skill §Layer 1) or `~/agents/<my-name>/`?
If not → FORBIDDEN. Stop.

**Q9 User-scope installation check** — Does my action install a package,
plugin, MCP server, hook, or skill under `~/.claude/` or `~/.aimaestro/`
(other than my own inbox)?
If YES → FORBIDDEN. Install locally only. Stop.

**Q10 AMP routing check** — Does my action send an AMP message to a
recipient OTHER than MANAGER, MAINTAINERs, or AUTONOMOUS agents?
If YES → FORBIDDEN. Route through MANAGER instead. Stop.

## Output

- All 10 checks pass → proceed with the action; log it in `loop.md`.
- Any check fails → stop, explain which rule was violated, propose an
  alternative, wait for clarification.

## Error Handling

If a check result is ambiguous (path unclear, instruction source
unclear), treat it as FORBIDDEN and ask via AMP before acting. Never
guess.

## Examples

**Action**: `echo "log" > ~/agents/my-agent/work-log.md`
**Q1**: target is `~/agents/my-agent/` (my own dir) → ALLOWED.

**Action**: `rm -rf ~/agents/other-agent/build/`
**Q8**: target is another agent's directory → FORBIDDEN. Stop.

**Action**: `gh pr merge 42`
**Q5**: no explicit user instruction for PR 42 in current turn → FORBIDDEN.

**Action**: `cat ~/.claude/projects/session.jsonl`
**Q1-Q10**: this is a READ, not a WRITE → all checks pass → ALLOWED.

## Resources

- [Edge Cases and Escalation Guide](references/edge-cases.md)
  > "User asked for forbidden action" · "MANAGER asked me to intervene"
  > "Need to write outside working directory" · "Unsure about path scope"
- Full persona: `agents/ai-maestro-autonomous-agent-main-agent.md`
- Workspace scope: `skills/ai-maestro-autonomous-workspace-isolation/SKILL.md`

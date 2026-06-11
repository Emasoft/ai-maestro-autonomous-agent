# AMP message templates (AUTONOMOUS)

Every AMP message body **leads with the self-id line** (PRRD S7.1 / golden G1.1
extended): `This is the Claude responsible for the ai-maestro-autonomous-agent
project.` Because all agents on the host share one GitHub/AMP identity, this
line is how the reader knows which Claude sent the message. Fill the
`<…>` placeholders and keep the leading self-id line verbatim.

## Table of Contents

- [1. Status update → MANAGER](#1-status-update--manager)
- [2. Error report → MANAGER](#2-error-report--manager)
- [3. Tier-2 approval request → MANAGER](#3-tier-2-approval-request--manager)
- [4. Peer claim announcement](#4-peer-claim-announcement)

## 1. Status update → MANAGER

Send after completing any non-trivial task (a PR opened, a bug fixed, an
investigation closed).

```text
This is the Claude responsible for the ai-maestro-autonomous-agent project.

STATUS — <task one-liner>
Done: <what landed — PR #, commit, or artifact>
Result: <pass/fail + key evidence>
Next: <what I am doing next, or "idle, awaiting direction">
```

## 2. Error report → MANAGER

Send the moment an error occurs — never hide a failure.

```text
This is the Claude responsible for the ai-maestro-autonomous-agent project.

ERROR — <where it happened>
Symptom: <exact command + exit code + key stderr line>
Impact: <what is blocked>
Action taken: <stopped / rolled back / awaiting direction>
Need: <decision or input I am waiting on>
```

## 3. Tier-2 approval request → MANAGER

Send when a task deviates from a baseline, crosses a project boundary, enters
the release pipeline, or changes governance — file the `proposal` TRDD first,
then request sign-off directly to MANAGER (no COS hop for AUTONOMOUS).

```text
This is the Claude responsible for the ai-maestro-autonomous-agent project.

APPROVAL REQUEST — TRDD-<id8> transition <FROM> → <TO>
Proposal: design/proposals/TRDD-<id8>-….md
Rationale (1 line): <why now>
Impact (1 line): <what changes on approval>
Reversible: <yes | no | compensable>
Standing by for your reply.
```

## 4. Peer claim announcement

Broadcast to peer AUTONOMOUS agents (and MANAGER for visibility) before
branching on a shared repo, so two agents never open duplicate PRs
(single-writer-per-domain).

```text
This is the Claude responsible for the ai-maestro-autonomous-agent project.

CLAIM — <owner/repo> issue #<n>
Branch: <my-name>/<slug>
Scope: <files / domain I will touch>
ETA: <rough window>
Yield rule: earlier claim wins; ping me if you already own this.
```

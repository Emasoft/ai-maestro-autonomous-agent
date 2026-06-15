# ai-maestro-autonomous-agent — plugin guidance

## Memory: the janitor-hosted global 3-scope wiki

This plugin uses the **global** AI-Maestro markdown memory system — not a
per-plugin one. The protocol, the recall law ("index by the QUESTION, not the
answer"), the note schema, the 2-step non-destructive correction protocol, and
the three scopes all live in `~/.claude/rules/markdown-memory-recall.md`. The
operations are the global skills: `janitor-memory-recall` (find by symptom),
`janitor-memory-write` (capture a fact), `janitor-memory-update` (revise). The
PROJECT scope for this repo is `.claude/project/memory/` (git-tracked, stood up
once via `/janitor-memory-bootstrap`).

Do **NOT** re-create per-plugin `*-memory-recall` / `*-memory-write` skills or a
`rules/memory-protocol.md` mirror — those were removed in favor of the global
system (TRDD-b48aa385, issue #7). The agent prompts (the main agent + every
sub-agent it spawns) carry the proactive-use contract directly, since sub-agents
inherit nothing.

Recall via the `/janitor-memory-recall` SKILL (it resolves the correct roots),
not by hand-copying the rule's inline bash. If you DO compose a multi-scope recall
by hand, use the FIXED zsh-portable array form (the old space-joined `$ROOTS`
string silently returns 0 hits on zsh/macOS):

```bash
ROOTS=(); for d in "$LOCAL_MEM" "$PROJECT_MEM" "$USER_MEM"; do [ -d "$d" ] && ROOTS+=("$d"); done
memgrep recall "$SYMPTOM" "${ROOTS[@]}"
```

### AUTONOMOUS-specific recall/write moments (the role flavoring)

Beyond the generic "recall before acting / write after solving" contract, an
AUTONOMOUS agent recalls and writes at these role-specific moments — it runs
unattended for long stretches, so the memory is what stops it re-deriving (often
badly) something a past cycle already solved.

**Recall (`/janitor-memory-recall`) BEFORE:**
- acting on a **recurring alert or repeated error in an unattended cycle** — the
  previous cycle may have already written the diagnosis; recall before re-deriving;
- **resuming a known project** at session/wake start — if a task looks familiar,
  spend one recall before re-exploring the codebase;
- **escalating to MANAGER** — the clarification you are about to request may
  already be answered in a note;
- classifying a proposal's **approval tier** — was an equivalent change already
  tiered / approved / refused?

**Write (`/janitor-memory-write`) / update (`/janitor-memory-update`) AFTER:**
- resolving a non-trivial operational gotcha (a publish-pipeline trap, an AMP edge
  case, an approval-flow surprise);
- a failed-then-solved recovery — what actually un-stuck the cycle;
- learning a durable constraint about the project not derivable from code/git;
- a confirmed USER / MANAGER preference on how the work should proceed.

**Scope routing:** machine-private (paths, hostnames, secrets) → LOCAL
(`~/.claude/projects/<slug>/memory/`); project-shared, no secrets → PROJECT
(`.claude/project/memory/`); cross-project → USER; **UNSURE → LOCAL**.

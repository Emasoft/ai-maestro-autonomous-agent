# Markdown memory — recall protocol (AUTONOMOUS role)

This plugin adopts the AI Maestro **markdown memory system**: a corpus of
curated, symptom-indexed markdown notes per project, a recall engine
(`memgrep`), and the discipline that ties them together. This rule is the
AUTONOMOUS-role mirror of the ecosystem reference rule
(`markdown-memory-recall.md`, shipped with `ai-maestro-janitor`). It is
distinct from conversation/transcript "memory-search": that searches chat
history; THIS recalls durable notes the agent wrote on purpose.

## Where the memory lives

Each project has one memory directory:

```text
$HOME/.claude/projects/<project-slug>/memory/
```

where `<project-slug>` is `$CLAUDE_PROJECT_DIR` (the absolute project path)
with every `/` replaced by `-`. `MEMORY.md` in that directory is the human
index — one line per note, never note content.

## The one law that makes memory work: index by the QUESTION, not the answer

A memory is found from the SYMPTOM, not the solution. When you write a note,
its `description:` (and `title`/`tags`) MUST carry the words a future session
will have when the problem RECURS — the user's words, the alert text, the
error message — NOT the jargon of the fix.

- WRONG `description`: "OAuth creds live in the macOS keychain services".
  (Findable only if you already know the answer is "keychain".)
- RIGHT `description`: "rotator failed, had to log in manually — where are
  the creds / why did the swap fail" — with the keychain fact in the BODY.

Two-hop recall: a symptom query lands on the note; the note's BODY gives the
answer. `memgrep recall` ranks on `description + title + tags` only, so the
`description` is the load-bearing recall surface.

## Recall BEFORE acting (the protocol)

Before debugging a recurring problem, making a design decision, or acting on
a **recurring alert in unattended mode**, RECALL first — "have we hit this
before?". Use the bundled `autonomous-memory-recall` skill, which runs:

```bash
"$CLAUDE_PLUGIN_ROOT/scripts/memory_recall.sh" "<SYMPTOM>" [MEMDIR]
```

The script gates on `command -v memgrep` and falls back to
`grep -rliE "<SYMPTOM>" "$MEMDIR"` when memgrep is absent — recall
**degrades, never breaks**. Read the top 1-3 notes it returns; the answer is
in their bodies. If recall returns nothing, the memory doesn't exist yet —
write one after you solve the problem.

## Write AFTER solving

When you learn a durable operational fact, gotcha, or decision, capture it
with the bundled `autonomous-memory-write` skill (which runs
`scripts/memory_note_write.py`) so the next autonomous cycle does not
re-derive it. Note schema (one fact per note):

```yaml
---
name: <short-kebab-case-slug>            # == filename stem
description: "<symptom surface — the load-bearing recall field>"
metadata:
  node_type: memory
  type: user | feedback | project | reference
---
<body: the one fact; for feedback/project add **Why:** and **How to apply:**>
```

After writing, append one index line to `MEMORY.md` — a markdown link to
the note file plus a one-line hook (the writer script formats and
de-duplicates it). Update an existing note rather than creating a
near-duplicate; delete notes that turn out to be wrong.

## memgrep — the recall engine

`memgrep` is a markdown-AST-aware recall tool (Rust; lives in
`ai-maestro-janitor/tools/memgrep`). If `command -v memgrep` is empty,
install it once with `cargo install` from that tree — until then the plain
`grep` fallback works on note frontmatter + bodies.

## AUTONOMOUS workflow wiring

- **Unattended cycles**: on a recurring alert or repeated error, recall
  before re-deriving the diagnosis; the previous cycle may have already
  written the answer.
- **Session start on a known project**: if a task looks familiar, spend one
  recall before re-exploring the codebase.
- **Before escalating to MANAGER**: recall first — the clarification you are
  about to request may already be answered in a note.

#!/usr/bin/env bash
# memory_recall.sh — symptom-indexed recall over a markdown memory directory.
#
# usage: memory_recall.sh "SYMPTOM" [MEMDIR]
#
# MEMDIR defaults to the Claude Code per-project memory dir derived from
# $CLAUDE_PROJECT_DIR (falling back to $PWD): the absolute project path with
# every '/' replaced by '-', under $HOME/.claude/projects/<slug>/memory.
#
# Uses memgrep (ranked, best-first, "path — description" lines) when it is on
# PATH; degrades to a plain case-insensitive grep over the note files when it
# is absent. Recall degrades, never breaks: an empty corpus, a missing memory
# dir, or zero matches are all NORMAL outcomes (exit 0, empty stdout) — only
# real I/O or usage errors exit non-zero.
set -euo pipefail

SYMPTOM="${1:?usage: memory_recall.sh \"SYMPTOM\" [MEMDIR]}"

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
SLUG="${PROJECT_DIR//\//-}"
MEMDIR="${2:-$HOME/.claude/projects/$SLUG/memory}"

if [ ! -d "$MEMDIR" ]; then
  # No memory dir yet = empty corpus, a normal outcome for a fresh project.
  echo "memory_recall: no memory directory at $MEMDIR (empty corpus)" >&2
  exit 0
fi

if command -v memgrep >/dev/null 2>&1; then
  # memgrep exits 0 on both match and no-match; non-zero means a real error
  # (e.g. stopword-only query) and must propagate.
  memgrep recall "$SYMPTOM" "$MEMDIR"
else
  # Fallback: unranked case-insensitive regex over the notes. grep exits 1 on
  # "no matches" (normal here) and 2 on real errors — tolerate only the former.
  grep -rliE "$SYMPTOM" "$MEMDIR" || [ $? -eq 1 ]
fi

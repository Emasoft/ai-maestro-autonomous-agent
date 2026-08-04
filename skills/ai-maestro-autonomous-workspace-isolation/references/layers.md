# Writable-Scope Layers and Situations

## Table of Contents

- [Writable-scope table](#writable-scope-table)
- [Programmatic path check](#programmatic-path-check)
- [Common situations](#common-situations)

## Writable-scope table

Three layers: writable locally, writable via `git push`, read-only.

### Layer 1 — Writable locally

| Path | OK to write? |
|---|---|
| `~/agents/<my-name>/` and all subdirs | YES |
| `~/agents/<my-name>/.claude/` | YES — local plugin installs only |
| `/tmp` and `/private/tmp` | YES |
| macOS per-user scratch (system-managed temp dir) | YES — use PID suffix |
| `~/.dev-browser/tmp/` (if dev-browser running) | YES — screenshots |
| `~/.agent-messaging/agents/<my-name>/` | YES — inbox only |

**The target decides, not the spelling.** A path is in Layer 1 only if it still
lands in Layer 1 *after every symlink is resolved*. A link inside your own
workdir pointing at `~/agents/<other-agent>/` is a Layer 3 write wearing a
Layer 1 name.

### Layer 2 — Writable via git push

| Target | OK? | How |
|---|---|---|
| Host-user GitHub repo, on a branch I created | YES | `git push origin my-branch` |
| Host-user GitHub repo, on main/master/develop | NO | PR review only |
| Someone else's GitHub repo | NO | fork first |
| Any repo, destructive push (`--force`, `--mirror`) | NO | not allowed |

### Layer 3 — Read-only (never write)

| Path | OK to write? |
|---|---|
| `~/agents/<some-other-agent>/` | NO (READ is fine) |
| `~/.aimaestro/agents/registry.json` | NO (use `aimaestro-agent.sh`) |
| `~/.aimaestro/teams/*.json` | NO (use `aimaestro-teams.sh`) |
| `~/.claude/` | NO |
| `~/.ssh/`, `~/.gnupg/`, `~/.config/gh/` | NO (no read either) |
| system paths (`/etc`, `/usr`, `/opt`, etc.) | NO |
| `~/Documents`, `~/Desktop`, `~/Downloads` | NO |
| anything else a path RESOLVES to after symlinks | NO — Layer 1 is the resolved target, not the typed string |

## Programmatic path check

```bash
TARGET="/path/to/proposed/write/target"
MY_AGENT_NAME="<your-agent-name>"

# Canonicalize BOTH sides before comparing. A `case` match on the string the
# caller typed is NOT a scope check — a symlink inside your own workdir can
# point at another agent's directory and the glob approves the write. Claude
# Code hit this same class three times in one month and fixed each by
# canonicalizing: 2.1.212 (.claude/worktrees), 2.1.216 (.claude), 2.1.217 (a
# background session's own cwd, "which could let sessions escape their
# workspace folder"). Do not re-introduce the string comparison.
resolve() { python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$1"; }

TARGET_REAL="$(resolve "$TARGET")"          # resolves even if the leaf does not exist yet
HOME_REAL="$(resolve "$HOME")"
SCRATCH_REAL="$(resolve "${TMPDIR:-/tmp}")" # macOS per-user scratch is under /private/var

case "$TARGET_REAL" in
    "$HOME_REAL/agents/$MY_AGENT_NAME"/*|"$SCRATCH_REAL"/*|/tmp/*|/private/tmp/*) ;;
    *) echo "FORBIDDEN — resolves to $TARGET_REAL, outside my scope"; exit 1 ;;
esac

# Hard links have no second path for realpath to resolve, so the check above is
# blind to them. Refuse to write through one — this is exactly what /rewind
# started doing in 2.1.220 — and ask MANAGER instead.
#
# Read the link count with python3, NOT `stat`. `stat -f` means "format" on BSD
# and "--file-system" on GNU coreutils, so the usual
# `stat -f %l … 2>/dev/null || stat -c %h …` fallback FAILS OPEN on any machine
# with GNU stat on PATH: the BSD form succeeds, prints a filesystem report, and
# the numeric test silently errors instead of firing. Measured, not theorized.
if [ -f "$TARGET_REAL" ] &&
   [ "$(python3 -c 'import os,sys; print(os.stat(sys.argv[1]).st_nlink)' "$TARGET_REAL")" -gt 1 ]; then
    echo "FORBIDDEN — $TARGET_REAL is hard-linked (link count > 1)"; exit 1
fi

echo ALLOWED
```

## Common situations

Right / wrong pairs for the 10 most common write operations.

**Clone a repo** — Right: `cd ~/agents/<my-name>/ && git clone <url> <repo-name>`. Wrong: `cd ~/Documents && git clone <url>`.

**Install a Python package** — Right: `cd ~/agents/<my-name>/project && uv venv && uv pip install <pkg>` (venv local to project). Wrong: `pip install <pkg>` (writes to user-scope site-packages).

**Install a Claude Code plugin for yourself** — Right: get **MANAGER** approval, then self-install via the core `ai-maestro-plugin` skills / `aimaestro-agent.sh plugin` (server-side, CPV-scanned) — R27. Wrong: `claude plugin install ...` at user scope.

**Save a work log** — Right: `echo "$LOG" > ~/agents/<my-name>/work-log.md`. Wrong: `echo "$LOG" > ~/.aimaestro/my-log.md`.

**Scratch file while debugging** — Right: `echo "$S" > /tmp/my-scratch-$$.txt` (PID suffix avoids collisions). Wrong: `echo "$S" > /tmp/scratch.txt` (collision risk) or writing to another agent's dir.

**Read another agent's conversation log** — Right: `cat ~/.claude/projects/.../<session>.jsonl` (reads are unrestricted). Wrong: editing or deleting the log.

**Push changes to GitHub** — Right: `cd ~/agents/<my-name>/<repo>/ && git push origin my-branch` (agent-created branch, host-user repo). Wrong: `git push --force`, pushing to `main` directly, or pushing to a repo without write access.

**Stop another agent** — Right: AMP MANAGER explaining why; MANAGER runs `aimaestro-agent.sh hibernate <other-id>`. Wrong: `tmux kill-session -t <other-agent>` or editing another agent's settings.

**Update my own agent's config** — Right: ask the user or MANAGER to run `aimaestro-agent.sh update <my-id>`. Wrong: editing `~/.aimaestro/agents/registry.json` directly.

**Access a secret (e.g. a PAT)** — Right: wait for the user to place the credential in an allowed file under your own workdir (e.g. `~/agents/<my-name>/.env.local`), read from there, never copy or echo. Wrong: reading `~/.ssh/id_ed25519`, `~/.config/gh/hosts.yml`, or any `.env` outside your own workdir.

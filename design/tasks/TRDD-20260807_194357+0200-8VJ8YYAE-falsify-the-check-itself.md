---
trdd-id: 8VJ8YYAE
title: A recorded check must itself be falsified before it is trusted
column: complete
created: 2026-08-07T19:43:57+0200
updated: 2026-08-07T19:43:57+0200
current-owner: ai-maestro-autonomous-agent
task-type: docs
scope: project
relevant-rules: [1]
derived-from: VFE3YFVS
implementation-commits: []
---

# TRDD-8VJ8YYAE — falsify the check, not just the fact

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-08-07

**DONE.** 119 tests pass. Third and final card in the re-verify trilogy
(`VFE3YFVS` → `T0ZNVB12` → this).

## Why: the rule I shipped this morning did not prevent the afternoon's failure

`TRDD-VFE3YFVS` required *recording the CHECK, not just the verdict*. Hours later I did
exactly that — and was still wrong, because **the check I recorded could not fail.**

To decide whether the janitor daemon held its macOS Automation grant I recorded, and
published to `janitor#92` as a recommended recipe:

> zero hits for `cannot enumerate|not permitted|-1743|errAEEventNotPermitted`, **and**
> at least one `FIRED rearm → iterm`

Measured at 19:37 the same day:

| signal | reading | truth |
|---|---|---|
| denial-string grep | **0 hits** | grant **DENIED** |
| `iterm-automation-blocked.flag` (19:33) | *"osascript enumerated 0 sessions — grant denied"* | authoritative |

**The denial returns an empty session list, not an error.** It emits none of those strings,
so the grep reports health at precisely the moment the capability is gone. The second
signal was a `FIRED rearm → iterm` from **14:43** — already 3.5 h stale when cited, with no
age bound to catch it. A two-signal recipe whose signals both fail in the same direction is
one signal, and that one was vacuous.

So VFE3YFVS's rule was *followed* and still produced a false verdict. The gap it left is
the one this card closes.

## The asymmetry worth naming

The same day, in the same tree, I falsified **every guard test** I wrote — seed the
violation, watch it go red, restore, confirm no residue — twice, deliberately, and recorded
doing so. Then I published a **verification recipe** having never once watched it fail.

Identical claim ("passing means it works"), identical risk, and only one of the two artifact
classes gets the discipline. Test code is falsified by habit; runbook steps, health checks
and "confirm it this way" instructions are not. That asymmetry is the finding.

## What changed

`agents/…-main-agent.md`, extending the **Re-verify before relying** bullet: the check
itself must be **watched to FAIL** before being trusted or handed on; names the silent
failure shapes that defeat a grep-for-an-error check (empty list, zero count, missing file,
process that never ran — against all of which *"no error found"* and *"working correctly"*
are the same output); and requires labelling an unfalsifiable check **UNVALIDATED** rather
than reporting the fact as verified. *An unfalsified check is worse than none, because it
ends the inquiry.*

## Guard

Two assertions added to `test_persona_requires_reverifying_recorded_external_state`, each
**falsified independently** — removing either clause alone turns the test red:

```
removed "watch it FAIL before you trust it"      -> 1 failed
removed "empty result* rather than an error"     -> 1 failed
restored                                          -> 119 passed
```

Diff audited: the persona change is a **pure append** (0 deletions), no probe residue.

One defect caught in review before commit: the second assertion was first written with a
leftover `text | 0 if False else text` expression — it evaluated to `text` and passed, so
no test would ever have flagged it. Fixed to plain `text`. Noted because it is the same
class as the subject of this card: something that works by accident and reads as
intentional.

## Deliberately NOT done

No mechanised falsification harness for recipes. The discipline is a habit at the moment of
authoring; a framework here would be the third mechanism in one day whose own correctness
nobody checks.

## Memory

`ATOM-A43I-C0CM` + lesson `ATOM-MX6G-G0SG` in `a-regression-test-must-be-verified-to-fail`
(USER — the generalization) · `agent-rescue-paths-both-assume-tmux` (USER — the worked
instance, corrected by supersession) · public retraction on `janitor#92`.

## Verification

- `uv run pytest -q` → **119 passed**.
- `uv run python scripts/publish.py --gate` → exit 0, CRITICAL=0 MAJOR=0 MINOR=0 NIT=0.
- Both new assertions individually falsified, then restored.

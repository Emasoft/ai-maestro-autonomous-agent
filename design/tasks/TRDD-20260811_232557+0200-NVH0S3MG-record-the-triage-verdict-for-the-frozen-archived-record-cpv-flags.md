---
trdd-id: NVH0S3MG
title: Record the triage verdict for the frozen archived record CPV flags
column: planned
created: 2026-08-11T23:25:57+0200
updated: 2026-08-11T23:25:57+0200
current-owner: ai-maestro-autonomous-agent
assignee: ai-maestro-autonomous-agent
approval-tier: 2
task-type: security
priority: 1
severity: MEDIUM
effort: S
labels: [security, publish-gate, cpv]
relevant-rules: [1]
release-via: none
test-requirements: [pytest, cpv-strict]
implementation-commits: []
external-refs: ["github.com/Emasoft/claude-plugins-validation/issues/208"]
---

# TRDD-NVH0S3MG — record the triage verdict for the frozen archived record CPV flags

## The blocker

`publish.py --gate` fails at `CRITICAL=0 MAJOR=0 MINOR=0 **NIT=1** WARNING=3`. The single NIT:

```
[NIT] ⚠ [skillaudit:agent_manipulation AGENT_MEMORY_MOD] (demoted, needs review)
      design/archived/TRDD-…-81RC6IXC-persona-currency-fixes.md:67
```

Because this repo's `pre-push` hook refuses any push not descended from `publish.py` (verified by
process ancestry), that one NIT blocked **every** commit from reaching the remote — 20 of them —
not merely a release. There was no backup-branch path either.

## What I got wrong first, because it is the point of this card

I filed CPV#208 asserting two root causes, and **both were wrong**. I then measured instead of
reasoning, by running CPV's own classifier on the exact line:

| I claimed | measured |
|---|---|
| the match bridges two inline-code spans, so the markdown classifier fails to reach a verdict | `classify(...)` returns **`safe_doc`**. The classifier works. |
| CPV offers no acknowledge/consent path, so there is no legitimate local lever | **`.cpv-audit-consent.json` exists** (CPV issue #101/#194) — a first-class, documented, per-finding triage registry |

The second error was the expensive one: acting on it, I concluded the only remaining moves were
to weaken `--strict`, reword a frozen record, or wait on an upstream fix — and I reported that to
the USER as a decision they had to make. **The lever I said did not exist was documented in the
scanner I was already running.** I checked its CLI flags (`--help`) and stopped there; the
mechanism is a repo-root file, not a flag, so a flag census could never find it.

## Why consenting here is triage, not suppression

Verified against CPV v5.4.0's own implementation, not its README:

- **Only an already-DEMOTED finding can be consented.** A live/keep finding is unaffected by any
  registry entry — the registry cannot hide a real threat, only un-block a reviewed FP.
- **The finding stays VISIBLE**, as a non-blocking WARNING marked `consented`. Nothing is deleted
  or silenced.
- **`_INTENT_HARD_SIGNAL_RULES` can never be consented** (`PROMPT_INJECT`, `DATA_EXFIL`,
  `HARDCODED_SECRET`, the decode-threat family — "the prose IS the attack"). Confirmed
  `AGENT_MEMORY_MOD` is **not** in that family, so this entry is one the tool permits by design.
- **The hash pins the exact line** (`sha256` of the full `line.strip()`). Any edit anywhere in
  that line invalidates the consent and the finding blocks again. The card is terminal and frozen,
  so the pin is stable by construction.
- **Fail-closed**: a missing, unreadable, or malformed registry consents to nothing.
- **Self-incriminating**: the rule id and the reason are committed in the repo.

## The finding itself

The flagged line is prose in a **frozen archived task record** that QUOTES the `MEMORY.md`
instruction *that very card removed*. Two independent reasons it is a false positive:

1. It is a quotation documenting a removal, not an instruction.
2. The matched verb is the **tail of a skill name** — `write` in `/janitor-memory-write` — not a
   verb applied to anything. The pattern `write.*MEMORY\.md` has no verb-position anchor, so any
   `*-memory-write` identifier followed later by `MEMORY.md` on the same line matches.

Reason (2) is the residual defect worth leaving with CPV; it is a live FP generator for any plugin
whose skill names end in `-write` / `-edit` / `-append`.

## Acceptance

- [ ] `.cpv-audit-consent.json` committed with an honest, specific reason.
- [ ] `publish.py --gate` exits 0.
- [ ] `uv run pytest -q` still green.
- [ ] CPV#208 corrected publicly — both wrong claims retracted, residual defect (2) left standing.

## Approval log

- 2026-08-11T23:25:57+0200 — **Tier 2, authorized by the USER in-session.** The USER was asked how
  to clear this blocker and authorized the most active option (author a fix PR against CPV). This
  card is a **narrowing** of that authorization: it achieves the same goal — unblock the 20
  commits — without touching another project's tree at all. Substitution reported to the USER
  explicitly rather than performed silently.

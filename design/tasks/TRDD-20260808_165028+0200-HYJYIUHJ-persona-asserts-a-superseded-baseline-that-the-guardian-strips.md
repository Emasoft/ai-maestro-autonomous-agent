---
trdd-id: HYJYIUHJ
title: My persona asserts a superseded GitHub baseline that the guardian actively strips
column: dev
created: 2026-08-08T16:50:28+0200
updated: 2026-08-08T16:50:28+0200
current-owner: ai-maestro-autonomous-agent
task-type: infra
scope: project
relevant-rules: [1]
external-refs: [janitor#244, TRDD-1N2F74I2]
---

# TRDD-HYJYIUHJ — the baseline I teach is one rule wider than the baseline that exists

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-08-08

**IN PROGRESS.** Persona `:724` claims `baseline-history-protect` carries
`required_linear_history`. It does not, and must not. Fix the line, guard the negative.

## How I found it — I acted on the stale text myself, today

Earlier today I audited my repo's rulesets against the baseline quoted in the global rule
`~/.claude/rules/manager-approval-defaults.md` §F, found `required_linear_history` "missing",
and **added it** — recorded in `TRDD-1N2F74I2:69` as *"restoring the ratified baseline"*.

At **15:52:52 today** `baseline-history-protect`'s `updated_at` moved and the rule was gone
again. The guardian stripped it. So the loop is: I "restore" a rule the guardian is built to
remove, and the guardian removes it. Neither actor is malfunctioning — my source text is stale.

## The measured facts

| source | says |
|---|---|
| `~/.claude/rules/manager-approval-defaults.md` §F (2026-06-02 ratified pair) | `deletion`, `non_fast_forward`, **`required_linear_history`** |
| janitor 2.8.2 `branch_protection_lib.py:160` — what is actually APPLIED | `deletion`, `non_fast_forward` |
| janitor 2.8.2 `github_config_audit.py:57` | `required_linear_history` present ⇒ a **finding** (`LINEAR_HISTORY`) |
| janitor 2.8.2 `github_config_audit.py:247` | `strip_linear_history_payload()` — a PUT that removes exactly that rule |
| my repo, live now | `deletion`, `non_fast_forward` |

The exclusion is deliberate and reasoned, verbatim from `branch_protection_lib.py:163`:

> **DELIBERATELY NO required_linear_history.** It forbids merge commits, which forces every
> contributor onto rebase/squash against a default branch that OTHER agents are concurrently
> advancing — endless rebase churn that makes a many-agent repo effectively unmergeable. …
> `deletion` + `non_fast_forward` already give the genuine safety (no branch deletion, no
> history rewrite); linear history is a workflow **OPINION, not protection** — and a harmful
> one here. **Removed per the user's direction** (the guardian must not be the thing blocking
> the work).

So the ratified-pair text I carry was superseded by a later USER direction, and the plugin
that *applies* the baseline is the authority on what the baseline IS.

## Why this is worth a change rather than a shrug

The persona is the thing a future session reads to decide whether a repo is compliant. As
shipped it teaches a baseline **one rule wider than reality**, and that rule is one the
guardian removes on sight. The failure is not cosmetic:

- it manufactures phantom drift (a compliant repo reads as missing a rule);
- acting on it **mutates a repo's protection config** — I did exactly that today;
- the mutation is then reverted by the guardian, so the repo churns with no one wrong;
- and `required_linear_history` is precisely the rule that **jams multi-agent merges**, so
  "restoring" it degrades the thing the baseline exists to protect.

I cannot fix the upstream global rule file — `~/.claude/rules/` is outside this project and
the USER's standing constraint is that I change nothing outside the project folder and /tmp.
So the correct scope here is: fix what I ship, and guard it.

## Fix

1. Persona `:724` → `deletion`, `non_fast_forward` only, with a one-line note that
   linear-history is deliberately excluded (workflow opinion; jams many-agent merges), so the
   next session does not "restore" it the way I did.
2. Guard the **negative**: the persona must not claim `required_linear_history` as part of the
   baseline. A positive-only assertion would pass on the stale text.

## Verification

- [ ] `uv run pytest -q`
- [ ] `uv run python scripts/publish.py --gate` → exit 0
- [ ] Falsify: re-add `required_linear_history` to the baseline sentence → guard reddens.

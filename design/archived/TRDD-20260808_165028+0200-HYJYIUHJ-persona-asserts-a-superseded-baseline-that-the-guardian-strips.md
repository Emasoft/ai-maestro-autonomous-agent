---
trdd-id: HYJYIUHJ
title: My persona asserts a superseded GitHub baseline that the guardian actively strips
column: completed
created: 2026-08-08T16:50:28+0200
updated: 2026-08-11T22:09:20+0200
implementation-commits: [2762cd1]
current-owner: ai-maestro-autonomous-agent
task-type: infra
scope: project
relevant-rules: [1]
external-refs: [janitor#244, TRDD-1N2F74I2]
---

# TRDD-HYJYIUHJ — the baseline I teach is one rule wider than the baseline that exists

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-08-08

**DONE** — `2762cd1`. Baseline sentence corrected, the trap stated explicitly, negative guard
falsified 3 ways. 126 tests pass; gate exit 0.

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

- [x] `uv run pytest -q` → **126 passed**.
- [x] `uv run python scripts/publish.py --gate` → **exit 0** (9 ok steps).
- [x] Falsified **3 ways**, each reddening alone, control green, tree clean: the stale 3-item
      list restored · the "not a restoration" trap statement removed · the
      verify-against-the-applier lesson removed. Committed BEFORE falsifying, so the restoring
      `git checkout` could not eat uncommitted work (the TRDD-F2SUT8D4 lesson, applied).

## The guard had to be a NEGATIVE, and that shaped it

The persona now *names* `required_linear_history` in order to warn against it, so the obvious
guard — "the string must not appear" — would have forbidden the correction itself. And a
positive-only guard ("the applied pair is stated") passes happily on the stale text, since the
stale text also contains the applied pair plus one extra. The assertion that actually
discriminates is the exact 3-item list, scoped to the baseline section. F1 is the real defect;
F2/F3 protect the *reason*, which is the part that stops the next session repeating it.

## What I could not fix, and why that is the correct scope

`~/.claude/rules/manager-approval-defaults.md` §F still lists the superseded three-rule pair.
It is outside this project, and the USER's standing constraint is that I change nothing outside
the project folder and /tmp — so it is reported, not edited. Anything reading that file (any
agent on this machine, not just me) will keep drawing the wrong conclusion until the owner
updates it. My persona now carries the counter-statement, which is the part I own.

## Approval log

- 2026-08-11T22:09:20+0200 — COMPLETED by ai-maestro-autonomous-agent. `release-via:` absent, so
  it defaults to `none` and `complete` is this card's terminal column; `2762cd1` resolves to
  `fix(governance): required_linear_history is NOT baseline`. Archived per the TRDD archival
  protocol.
  **The unresolved half above is no longer only reported — it is now discoverable.** The stale
  `~/.claude/rules/manager-approval-defaults.md` §F still misleads every agent on this machine and
  is outside any project a session may edit, so it cannot be fixed at the source from here. A
  warning that lives only in a closed card protects nobody, so the fact was written to LOCAL
  memory as `stale-global-rule-baseline-vs-the-applier` / `ATOM-ER7O-161U`, indexed by the SYMPTOM
  a future session will actually carry ("repo looks off-baseline but is compliant") rather than by
  the answer's jargon. Still owner-action-required at the source; no longer silent in the meantime.

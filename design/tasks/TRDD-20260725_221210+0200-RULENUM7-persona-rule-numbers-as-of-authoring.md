---
trdd-id: RULENUM7
title: Persona rule numbers are as-of-authoring pointers, not assertable facts
column: complete
created: 2026-07-25T22:12:10+0200
updated: 2026-07-25T22:12:10+0200
current-owner: ai-maestro-autonomous-agent
task-type: docs
approval-tier: 2
relevant-rules: [1]
external-refs: [Emasoft/ai-maestro#87, Emasoft/ai-maestro#32]
implementation-commits: []
---

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-07-25

- S: ai-maestro#87 (role-plugin design + eval, filed from the ASSISTANT plugin) names four
  shortcomings shared by the whole role-plugin family. I audited all four plus ai-maestro#32
  against THIS plugin. Two apply, two do not.
- D: Fixed the one that is unambiguously mine and safe to fix without a core ruling —
  rule-number drift — with a standing as-of-authoring disclaimer + a guard test.
- P: suite **101 passed**, ruff clean.
- N: persona TRIM (#87 item 3) and the behavioral-eval harness (#87 item 1) are NOT done here —
  the first is a large restructuring of a safety document, the second is core-owned. Both are
  raised for coordination instead of decided unilaterally.
- NEXT ACTION: none — implemented; the open questions live on the coordination issue.

## Audit of ai-maestro#87 + #32 against this plugin

| Finding | Applies here? | Evidence |
|---|---|---|
| #87.1 role-plugins tested for prose, not behavior | YES (family-wide) | `tests/test_content_invariants.py` asserts tokens, never behavior. Core-owned harness proposed; not mine to build. |
| #87.2/#87.5 rule-number drift | **YES — FIXED HERE** | 24 distinct numbers hardcoded (R6, R6.6, R22, R22.1, R23, R26–R40, R42.1/.2/.4/.6) with no drift guard. |
| #87.3 persona size | YES | 6925 words / 46667 B — 64% larger than the 4212-word persona that raised the concern. Raised, not unilaterally trimmed. |
| #87.4 `model:` pin | Partly | Pinned `sonnet` — the cheap direction (the issue's concern was an `opus` pin), but the rationale was undocumented. |
| #87.6 README stub / long description | Minor | Deferred; cosmetic next to the above. |
| **#32 per-agent state outside the agent workdir** | **NO — COMPLIANT** | Zero code writes per-agent state anywhere. Every `~/.aimaestro/` occurrence is prose FORBIDDING such writes (persona:195-206, `questions.md` Q3/Q4/Q9, `layers.md` tables). |
| **#87.5 CHANGELOG erasure** | **NO — ALREADY FIXED** | `scripts/publish.py:900-910` uses `git-cliff --bump --tag vX -o CHANGELOG.md` with an in-code note "no `--unreleased` here … With it, `-o` overwrote the file with only the newest section." CHANGELOG.md retains 19 release sections back to 1.3.3. Release notes use a SEPARATE `--unreleased --strip header` call to stdout. |

## What was changed

`agents/ai-maestro-autonomous-agent-main-agent.md` — a standing paragraph under the R26–R40
heading: every rule NUMBER is as-of-authoring, cite a rule by its SUBSTANCE, treat the number as
a pointer that may have moved, and when it does not resolve (or contradicts the summary) the live
governance source and the identity/messaging skills are authoritative — mirroring the deferral
this persona already makes for the comm-graph. Plus: never assert "rule RNN says X" to another
agent on this file's authority alone.

Guarded by `tests/test_content_invariants.py::test_persona_marks_rule_numbers_as_as_of_authoring`,
which also asserts the invoked `agent-messaging` precedent still exists — so the deferral cannot
become hollow if that section is ever removed.

## Why this shape, and why not more

The fix is deliberately compatible with EITHER outcome of #87's open question (role-plugins keep
citing inline vs. core exposes a rule-text inheritance mechanism): it removes no citation and adds
no dependency, so neither ruling invalidates it. The alternative — stripping the numbers now —
would have destroyed working navigational aids on a guess about a decision that is not mine.

Persona trim was NOT attempted: this is a safety document whose prohibitions are the payload, and
issue #87 itself flags that redundancy partly AIDS compliance. Trimming 30-40% of it on my own judgement,
with only prose tests to catch a mistake, is exactly the class of change that should wait for the
behavioral harness #87 asks core to build.

## Verify

`uv run pytest -q` → 101 passed; `uv run ruff check tests/` clean;
`grep -n "as-of-authoring" agents/ai-maestro-autonomous-agent-main-agent.md`.

## Approval log

- 2026-07-25T22:12:10+0200 — Authored + COMPLETED under the USER go-on-yourself mandate (Tier-2,
  USER is approver in standalone mode). Audit findings routed to the fleet via a coordination
  issue on Emasoft/ai-maestro per the USER's instruction. Commit local; publish USER-gated.

## Notes and lessons learned
[^1]: [id:ATOM-8N4T-RQ2P, status:valid, keywords:"hardcoded_rule_numbers_drift_silently persona_cites_versioned_governance_source cite_by_substance_not_number prose_test_cannot_check_a_number", ocd:2026-07-25, lmd:2026-07-25]
  DO NOT copy rule NUMBERS from a versioned, externally-owned governance source into a persona as
  if they were stable facts, BECAUSE a renumber drifts the file silently and no prose test can
  detect it — a test can assert the string "R39" is present, never that R39 still means what the
  persona claims. DO cite by SUBSTANCE, mark the numbers as-of-authoring pointers, and name the
  live source as authoritative on any mismatch (the same deferral this persona already makes for
  the comm-graph).
[^2]: [id:ATOM-3F7K-9WVX, status:valid, keywords:"cross_plugin_finding_may_not_apply_audit_before_fixing changelog_erasure_already_fixed_here state_outside_workdir_compliant sweep_result_is_worth_reporting", ocd:2026-07-25, lmd:2026-07-25]
  DO NOT apply a shortcoming reported against a SIBLING plugin to your own without auditing first,
  BECAUSE two of the four findings raised for the role-plugin family were already handled here —
  the CHANGELOG `--unreleased -o` erasure was fixed long ago (with the root cause noted in-code)
  and the state-outside-workdir violation never existed. DO audit each claim against your own tree,
  fix only what actually applies, and REPORT the negative results too — a sweep that asked for
  every plugin to be checked is answered by a verified "compliant", not by silence.

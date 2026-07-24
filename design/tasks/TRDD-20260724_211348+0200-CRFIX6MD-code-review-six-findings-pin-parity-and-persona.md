---
trdd-id: CRFIX6MD
title: Code-review batch — pin-parity guard hardening, gate-count comments, persona list merge, stale recipe pin
column: complete
created: 2026-07-24T21:13:48+0200
updated: 2026-07-24T21:13:48+0200
current-owner: ai-maestro-autonomous-agent
task-type: bugfix
approval-tier: 2
relevant-rules: [1]
implementation-commits: []
---

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-07-24

- S: A `/code-review medium --fix` pass over the session's own work returned 6 findings
  (5 MEDIUM, 1 LOW) and applied fixes to 5 files. Every fix was INDEPENDENTLY re-verified
  before acceptance (agent self-reports are not proof — see the fork-delegation memory note).
- P: `_gate_files()` discovers exactly the 5 real sites, all `@v3.5.0`, zero false positives;
  full suite **100 passed**; `ruff check` clean; both workflow YAMLs parse; the four regex
  behaviors negative-tested by hand (`.git` form → PINNED, plain → PINNED, unpinned → floating,
  prose mention → NOT a site).
- N: FIX only. Commit stays LOCAL; publish is USER-gated.
- NEXT ACTION: none — implemented, verified, committed.

## The six findings and what was done

1. **`tests/test_cpv_pin_parity.py` regex rejected the `.git`-suffixed URL** (MEDIUM). The
   equally-valid `…/claude-plugins-validation.git@v3.5.0` spelling parsed as UNPINNED, so the
   guard would red-light a healthy, fully pinned pipeline. Fixed with an optional `(?:\.git)?`
   before the pin group. Negative-tested both spellings.
2. **`_GATE_FILES` was a hardcoded 3-file list** while the docstring promised "every executable
   CPV gate site" (MEDIUM). A gate added to a new workflow or script would drift unnoticed —
   the exact class this guard exists to prevent. Fixed: the three become a REQUIRED floor, plus
   glob discovery over `.github/workflows/*.{yml,yaml}` and `scripts/*.py`.
3. **`_gate_pins` raised `FileNotFoundError`** on a deleted/renamed gate file instead of failing
   as the intended "gate site missing from: …" assertion (part of the same fix). Now returns `[]`.
4. **The invariant comments miscounted the gate sites** — "bump all four together" / "All four
   MUST agree" when there are FIVE (ci.yml + release.yml + publish.py Steps 4/5/5.5), and the
   comment itself enumerates 1+1+3 (MEDIUM). A bumper following the comment updates four of five
   and ships a mismatched pin. Fixed in both workflows, with a pointer to the enforcing test.
5. **Persona markdown list merge** (MEDIUM). The new build-mandate bullet list sat one blank line
   above the Tier 0/1/2/3 ladder, so markdown merged them into ONE list — rendering the repo-wide
   governance tiers as sub-steps of the build-mandate flow, i.e. scoping approval rules to build
   mandates only. Fixed with a "**The approval tiers.**" lead-in that breaks the merge and states
   explicitly that the tiers are not sub-steps and apply to everything.
6. **Persona checklist item 2 over-claimed "your FIRST action"** while item 1 (verify AMP identity)
   precedes it, and asserted an every-turn duty inside a section scoped "At the start of every
   session" (LOW) — a literal reader either skips identity verification or applies drain-first only
   on wake, which is the failure mode issue #17 was filed about. Reworded as a STANDING per-turn
   duty sequenced after step 1.

Plus: **`.claude/project/memory/publish-pipeline.md` `[^4]`'s FAST-CONFIRM RECIPE was still pinned
`@v2.136.1`** while the pipeline moved to `@v3.5.0` — a verbatim re-run would return EXIT=0 from an
obsolete validator and "prove" canon-cleanliness against canon nobody gates on. The recipe now reads
`<PIN>` from the live pipeline via grep, with the WHY inline and recall keywords for the
"recipe that outlived its pin" class.

## Why this batch matters

Findings 1-3 are defects in the guard TRDD-CPVPINGD added THIS session: a regression guard that
false-fails (1) or under-scans (2) is worse than none, because it trains the reader to distrust or
ignore it. Findings 5-6 are defects in the persona edit TRDD-WAKEDRN8 made THIS session — governance
prose is uncompiled, so a rendering-level merge silently changes what the rules mean.

## Verify

`uv run pytest -q` → 100 passed; `uv run ruff check tests/` clean; `python -c "import yaml; …"`
parses both workflows; `_gate_files()` prints exactly the 5 sites at `@v3.5.0`.

## Approval log

- 2026-07-24T21:13:48+0200 — Authored + COMPLETED under the USER go-on-yourself mandate. Fixes
  applied by the `/code-review --fix` pass, then independently re-verified by me before commit.
  Commit stays local; publish USER-gated.

## Notes and lessons learned
[^1]: [id:ATOM-7K2N-QF83, status:valid, keywords:"regression_guard_false_fails_on_valid_input guard_added_same_session_had_defects hardcoded_file_list_under_scans recipe_outlived_its_pin markdown_blank_line_merges_adjacent_lists", ocd:2026-07-24, lmd:2026-07-24]
  DO NOT consider a freshly-added regression guard done once it passes on today's tree, BECAUSE a
  guard can pass while being both too STRICT (this one classed the valid `.git`-suffixed URL as
  floating → would red-light a healthy pipeline) and too NARROW (a hardcoded 3-file list silently
  ignores a gate added to a new file — the very drift it guards). DO negative-test each guard against
  the valid variants it must accept AND the defects it must catch, and prefer discovery over a
  hardcoded inventory with the known files as a floor.
[^2]: [id:ATOM-5J9V-2WQD, status:valid, keywords:"markdown_blank_line_merges_two_lists governance_prose_renders_wrong_scope persona_bullet_list_before_tier_ladder uncompiled_prose_no_compiler_catches_it", ocd:2026-07-24, lmd:2026-07-24]
  DO NOT insert a bullet list immediately above an existing list separated only by a blank line in
  governance prose, BECAUSE markdown MERGES them into one list and the second list silently becomes
  sub-steps of the first — here the repo-wide approval tiers rendered as sub-steps of the build-mandate
  flow, narrowing their scope with no compiler to catch it. DO separate the two with a bold prose
  lead-in that both breaks the merge and states the scope explicitly.

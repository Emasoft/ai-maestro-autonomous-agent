---
trdd-id: J48IO8F3
title: Retire dead do_bump and correct every prose site attributing version sync to it
column: dev
created: 2026-08-18T19:52:44+0200
updated: 2026-08-18T19:52:44+0200
current-owner: autonomous-agent-session
task-type: bugfix
approval-tier: 2
relevant-rules: [4.1]
external-refs: [phase-1 audit D2+D3, ai-maestro TRDD-BRRJK57P]
---

# Retire dead do_bump and correct every prose site attributing version sync to it

Phase-1 confirmed defects D2 + D3 (one root cause — false attribution to a function that
never runs in production):

- `scripts/publish.py:1249` `do_bump()` has ZERO production callers (only 2 test callers).
  The live release path is `language_bump_version()` → `update_plugin_json/​pyproject/​
  python_versions` (:681-685) + `update_readme_version/​update_persona_versions` (:702-703).
  The hazard already fired once: v1.3.0 incident, "patching do_bump alone left the live
  path untouched" (`tests/test_publish_version_sync.py:106`, archived TRDD-e7281b7e).
- PRRD **S4.1** credits `do_bump()` with the sync — a SILVER rule describing a mechanism
  that never executes.
- `scripts/publish.py:1205` comment repeats the false attribution.

## Fix (one atomic task: eliminate the false-attribution mechanism)

1. PRRD S4.1 → S4.2: attribute the sync to the live Step-9 path
   (`language_bump_version()`), keep `check_version_consistency()` as the enforcement.
   (Spec moves FIRST per hub dispatch.)
2. Delete `do_bump()` from `scripts/publish.py` (no-legacy-code rule; a dead parallel
   wrapper is exactly the patch-magnet that caused v1.3.0).
3. Fix the `:1205` comment to name the live path.
4. Tests: rewrite `test_do_bump_roundtrip_*` to exercise the live helpers directly;
   drop `do_bump` from `tests/test_validators_invocable.py:84`'s required-symbol list.

## Derived tasks

- Post-delete sweep: `grep -rn "do_bump"` over the whole tree must return only
  archived/report/this-card historical mentions (check-all-files-after-breaking-change).
- Run the full test suite — the regression guard for the live path must stay green.

## Acceptance

- [ ] PRRD S4.1 revised to S4.2 naming `language_bump_version()`; approval logged.
- [ ] `do_bump` absent from `scripts/publish.py`; zero non-historical references.
- [ ] Tests green.

## Approval log

- 2026-08-18T19:52:44+0200 — Tier-2 (SILVER PRRD revision) APPROVED via hub dispatch:
  Phase-2 GO from the ai-maestro hub session, acting under the USER's verbatim delegation
  ("you are in charge. decide yourself in base of verified facts and tests."), which
  authorized authoring TRDDs from CONFIRMED Phase-1 findings and flowing them
  todo→…→complete with spec moves first. human_review escalation path: the hub.

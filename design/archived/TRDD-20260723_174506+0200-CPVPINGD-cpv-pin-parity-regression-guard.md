---
trdd-id: CPVPINGD
title: Regression guard — a unit test that fails if the CPV gate pins ever drift or re-float
column: completed
created: 2026-07-23T17:45:06+0200
updated: 2026-08-11T21:17:34+0200
current-owner: ai-maestro-autonomous-agent
assignee: ai-maestro-autonomous-agent
priority: 4
severity: LOW
effort: S
labels: [ci, cpv, tests]
task-type: infra
scope: project
parent-trdd: null
npt: []
eht: []
blocked-by: []
created-by: CPV320UP
relevant-rules: []
release-via: publish
implementation-commits: [79b5d2f]
external-refs: ["TRDD-CPV320UP"]
---

# TRDD-CPVPINGD — CPV gate-pin parity regression guard

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative) — 2026-07-23

- **DONE.** Derived guard for TRDD-CPV320UP. New `tests/test_cpv_pin_parity.py` (3 tests)
  mechanically enforces the "all CPV gate pins agree" invariant CPV320UP made true.
- **NEXT ACTION: none.** Ships with the parked publish.

## Why (the derived-task rationale)

CPV320UP fixed a drift where publish.py's three CPV gate calls floated to CPV's default
branch while ci.yml/release.yml pinned a tag — release.yml's comment *claimed* parity that
the code did not deliver. Fixing it left the invariant guarded only by a COMMENT. The drift
had already happened once; a comment does not stop the next edit from re-floating one site
or bumping one file and forgetting the others. The mandatory derived guardrail is a TEST.

## Fix

`tests/test_cpv_pin_parity.py` — 3 tests, text/regex over the three gate files
(`ci.yml`, `release.yml`, `scripts/publish.py`):

- `test_every_cpv_gate_file_has_at_least_one_gate_site` — a gate silently removed from any
  file is a regression.
- `test_no_cpv_gate_site_is_floating` — an unpinned `git+...` (no `@vX.Y.Z`) is the exact
  CPV320UP defect; caught here.
- `test_all_cpv_gate_pins_agree` — every site pins the identical version.

Version-agnostic (a lockstep bump stays green; only drift/float/deletion fails). The regex
anchors on the full `git+https://…claude-plugins-validation` URL so a prose mention of the
version in a comment (`# CPV is PINNED to @v3.2.0`) is NOT miscounted as a gate site
(verified: the comment yields zero matches).

## Verification (done)

- `pytest tests/test_cpv_pin_parity.py` → 3 passed; full suite **97 passed** (was 94).
- Negative-checked the three failure shapes (floating / disagreeing / deleted) fire the
  assertions; the prose-comment case is correctly ignored.
- `mypy` + `ruff` clean on the new file.

## Approval log

- 2026-07-23 — USER `/go-on-yourself` + `resume`. Tier-0 in-scope test (derived guard for
  CPV320UP). Authorized; no publish taken.
- 2026-08-11T21:17:34+0200 — COMPLETED by ai-maestro-autonomous-agent. `release-via:` absent, so
  it defaults to `none` and `complete` is this card's terminal column. **Repaired the backtracking
  field:** `implementation-commits:` was `[]` although `79b5d2f` names `TRDD-CPVPINGD` in its
  subject. Archived per the TRDD archival protocol.

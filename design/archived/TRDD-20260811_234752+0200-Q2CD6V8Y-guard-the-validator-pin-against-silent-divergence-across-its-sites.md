---
trdd-id: Q2CD6V8Y
title: Guard the validator pin against silent divergence across its sites
column: completed
created: 2026-08-11T23:47:52+0200
updated: 2026-08-11T23:49:22+0200
current-owner: ai-maestro-autonomous-agent
assignee: ai-maestro-autonomous-agent
approval-tier: 0
task-type: infra
priority: 3
severity: MEDIUM
effort: S
labels: [tests, ci, cpv]
relevant-rules: [1]
release-via: none
test-requirements: [pytest, lint]
implementation-commits: [c46be95]
parent-trdd: null
---

# TRDD-Q2CD6V8Y — guard the validator pin against silent divergence across its sites

## Why

TRDD-NVH0S3MG cost this session hours, and its most expensive ingredient was not the false
positive — it was that **the CPV pin had silently aged two majors** while every report stayed
green. I guarded the cheap defect from that session (the archive-column class, TRDD-9D2SCI1Z) and
left the expensive one unguarded.

The pin lives in **five** places, which I moved by hand:

```
scripts/publish.py            (×3 — gate, validate, and the publish path)
.github/workflows/ci.yml      (×1)
.github/workflows/release.yml (×1)
```

The realistic failure is not "all five go stale together" — that is loud enough to eventually
notice. It is **one of them moving without the others**: `publish.py` is the file you edit while
debugging locally, and `ci.yml` is the one you forget. Then `publish.py --gate` says PASS and CI
says PASS while running *different validators*, and neither says anything is wrong. A green report
whose meaning differs between two places is worse than a red one.

Nothing in `tests/` mentions the pin today — verified, not assumed.

## What

One test in `tests/test_content_invariants.py`:

- **Discover** every pin occurrence by scanning git-tracked source (`.py` / `.yml` / `.yaml` /
  `.sh` / `.toml`), rather than checking a hardcoded list of files. A hardcoded list is the same
  bug one level up: it goes stale when a sixth site appears and reports green forever.
- **Assert** every discovered pin is the same version.
- **Assert** the enumeration is non-empty and spans at least the two known kinds of site
  (`publish.py` and a workflow), so a rename or a moved directory fails loudly instead of passing
  over zero matches.

Deliberately **offline**. A "is the pin behind upstream?" check needs the network, and a unit test
that fails when someone else cuts a release is a flaky test that trains people to ignore it. That
belongs in a scheduled advisory job, not here — noted, not built.

## Excluded from the scan, on purpose

`design/` and `CHANGELOG.md` legitimately cite *historical* pins (TRDD-CPV350UP records the
v3.2.0 → v3.5.0 bump; the changelog records v3.5.0 → v5.4.0). Those are records of what was true
then. Scanning them would make every past bump a permanent failure — a guard that punishes
accurate history.

## Acceptance

- [x] Test present and passing; full suite green — **130 passed** (129 → 130).
- [x] `ruff check` clean.
- [x] Falsified both ways, each restored:

| broke | result |
|---|---|
| `ci.yml` left at `v3.5.0` while the rest moved | fails, and **names the divergent file**: `{'v3.5.0': ['.github/workflows/ci.yml'], 'v5.4.0': [...]}` |
| the pin pattern renamed (scan matches nothing) | fails on the vacuity assert — does **not** pass over zero matches |

The scan sees exactly what it should: `v5.4.0`, 5 occurrences, across
`scripts/publish.py` + both workflows.

## Approval log

- 2026-08-11T23:47:52+0200 — Tier 0 (a derived guardrail in this repo's own test suite; no
  baseline deviation, no cross-project reach, no `.github/` content change — the workflows are
  only *read*). Authored directly as `planned`.
- 2026-08-11T23:49:22+0200 — COMPLETED by ai-maestro-autonomous-agent. `release-via: none`, so
  `complete` is terminal and it archives as `completed`. Implemented by `c46be95`. Archived per
  the TRDD archival protocol.

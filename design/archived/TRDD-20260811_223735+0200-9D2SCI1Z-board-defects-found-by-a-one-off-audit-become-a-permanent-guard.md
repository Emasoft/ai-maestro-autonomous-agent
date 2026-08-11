---
trdd-id: 9D2SCI1Z
title: Board defects found by a one-off audit become a permanent guard
column: completed
created: 2026-08-11T22:37:35+0200
updated: 2026-08-11T22:40:54+0200
current-owner: ai-maestro-autonomous-agent
assignee: ai-maestro-autonomous-agent
approval-tier: 0
task-type: infra
priority: 3
severity: LOW
effort: S
labels: [governance, tests, kanban]
relevant-rules: [1]
release-via: none
test-requirements: [pytest, lint]
implementation-commits: [0a333bd, f4f8177]
---

# TRDD-9D2SCI1Z — board defects found by a one-off audit become a permanent guard

## Why

Draining the kanban board on 2026-08-11 ended with a systematic audit of all 52 archived
cards. It found **two real defects**, both of a class nothing was checking:

1. **`CPVPINGD` was archived as `completed` while declaring `release-via: publish`** — a card
   that shipped a release, recorded as if it never released. It was caught by arithmetic (13
   `publish` cards, 12 `published` columns), not by any gate.
2. **`TRDD-a08b839d` records `449af1a` in `implementation-commits`, and that object does not
   exist** — an amend or rebase rewrote it. Four other cards had `implementation-commits`
   fields repaired the same day.

Both classes fail **silently**. A wrong terminal column just looks like a finished card; a
dangling sha gives the reader "unknown revision" with nothing saying the record was wrong, so
they blame their own tooling. The audit that found them was a one-off I happened to think of.
Per the standing rule that every bug becomes a guardrail, the audit becomes a test.

## What

Two tests in `tests/test_content_invariants.py`:

- `test_archived_cards_are_terminal_and_match_their_release_mode` — every card in
  `design/archived/` carries a terminal `column`, and `release-via: publish` archives as
  `published` (everything else as `completed`). `superseded`/`cancelled` are exempt: a
  withdrawn or replaced card never reached its release mode.
- `test_every_recorded_implementation_commit_resolves` — every recorded sha is a real object.

## Gotchas the implementation has to carry

- **Vacuous green is the failure mode to fear.** Both tests assert a non-empty enumeration
  first; if `design/archived/` moves or the frontmatter key is renamed, they fail loudly
  instead of passing over zero cards.
- **Terminal cards are frozen**, so the two known defects cannot be edited away. They are
  allowlisted (`_FROZEN_PUBLISH_AS_COMPLETED`, `_KNOWN_DANGLING_COMMITS`) — and each
  allowlist is itself asserted to still match reality, so a dead exemption fails rather than
  quietly widening the hole.
- **CI checks out at `depth=1`.** The commit-resolution test would fail on every sha in a
  shallow clone, which is a fact about the clone, not about the record — so it returns early
  on `git rev-parse --is-shallow-repository == true`.

## Acceptance

- [x] Both tests present and passing — `uv run pytest -q` → **129 passed** (127 → 129).
- [x] `ruff check` clean.
- [x] Each test falsified by hand — including the vacuous-green branch — and restored.

## What falsification found (the part worth keeping)

Falsifying the guard found a defect **in the guard**. The "no dead exemptions" check
iterated the CARDS and asked whether each allowlisted id had left its excused state — so an
exemption naming a card that no longer exists matched nothing and reported nothing. The
comment claimed the exemptions are checked against reality; the code delivered half of that,
and the missing half is the one that decays unattended (an id stops matching the moment
someone renames a file). Fixed in `f4f8177` to iterate the ALLOWLIST instead.

Six falsifications, each restored:

| broke | result |
|---|---|
| a `publish` card flipped to `completed` | fails, names `TVM7Q4XK` |
| a bogus sha added to a card | fails, names `93KUP3R6: deadbee` |
| a resolvable sha in the dangling allowlist | fails, names `db3a892` |
| an exemption for a nonexistent card | **passed silently** → fixed, then fails |
| the frozen allowlist emptied | fails, names all 5 frozen cards |
| `design/archived/` pointed elsewhere | BOTH fail on the vacuous-green assert |

## Approval log

- 2026-08-11T22:37:35+0200 — Tier 0 (a derived guardrail inside this repo's own test suite,
  no baseline deviation, no cross-project reach). Authored directly as `planned`.
- 2026-08-11T22:40:54+0200 — COMPLETED by ai-maestro-autonomous-agent. `release-via: none`,
  so `complete` is this card's terminal column and it archives as `completed`. Implemented by
  `0a333bd` (the two guards) and `f4f8177` (the dead-exemption fix falsification surfaced).
  Archived per the TRDD archival protocol.

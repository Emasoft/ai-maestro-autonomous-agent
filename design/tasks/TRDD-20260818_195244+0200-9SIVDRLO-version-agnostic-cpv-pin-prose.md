---
trdd-id: 9SIVDRLO
title: Make CPV pin prose version-agnostic so comments can never drift from the gate again
column: todo
created: 2026-08-18T19:52:44+0200
updated: 2026-08-18T19:52:44+0200
current-owner: autonomous-agent-session
task-type: bugfix
approval-tier: 0
external-refs: [phase-1 audit D4, ai-maestro TRDD-88LDC7E0 fleet context]
---

# Make CPV pin prose version-agnostic so comments can never drift from the gate again

Phase-1 confirmed defect D4. The 5 EXECUTING pin sites all agree at `@v5.4.0` (enforced
by `tests/test_cpv_pin_parity.py`), but 3 PROSE sites still name old pins, and the parity
test excludes prose BY DESIGN — so this drift is invisible to it forever:

- `.github/workflows/ci.yml:170` — "PINNED to @v3.5.0"
- `.github/workflows/ci.yml:175` — "v3.2.0 -> v3.5.0 bump"
- `.github/workflows/release.yml:94` — "v3.2.0 -> v3.5.0 bump"

## Fix (root cause, not symptom)

Do NOT just bump the prose numbers — a prose site naming an exact version WILL drift
again at the next pin bump. Rewrite the comments to be VERSION-AGNOSTIC: refer to "the
tag on the uvx line below" and keep the historical TRDD citations as explicitly
historical. After this, the only version-bearing sites are the 5 the parity test guards.

## Derived tasks

- Sweep both workflow files for any OTHER version-bearing CPV prose beyond the 3 cited
  sites before closing (the audit counted, but count again at fix time).

## Acceptance

- [ ] No comment in ci.yml/release.yml names a specific CPV version.
- [ ] The 5 executing sites untouched; `tests/test_cpv_pin_parity.py` green.

## Approval log

- 2026-08-18T19:52:44+0200 — Tier-0 (comment-only, in-scope) authored as planned work
  under the hub's Phase-2 GO dispatch.

---
trdd-id: D6P88CM1
title: Stop publish.py docs claiming the uninstalled git-hooks pre-push is the live gate
column: todo
created: 2026-08-18T19:52:44+0200
updated: 2026-08-18T19:52:44+0200
current-owner: autonomous-agent-session
task-type: docs
approval-tier: 0
external-refs: [phase-1 audit D5]
---

# Stop publish.py docs claiming the uninstalled git-hooks pre-push is the live gate

Phase-1 confirmed defect D5 (wiring/doc half; the safety half was REFUTED — the installed
hook is stricter). Measured: `git config core.hooksPath` → `.githooks`; the ACTIVE
`.githooks/pre-push` refuses any push not descended from `scripts/publish.py`
(process-ancestry check, verified empirically). `git-hooks/pre-push` — the only caller of
`publish.py --gate` anywhere — is NOT installed, yet three publish.py sites describe it
as the live invoker:

- `scripts/publish.py:36` (module docstring)
- `scripts/publish.py:1455` (argparse epilog)
- `scripts/publish.py:1482` (`--gate` help text)

The divergence is declared (`plugin.json` `cpv.pipeline.intentional_divergence`,
CHANGELOG:329); what is undeclared is that the declared-divergent file is INERT.

## Fix (doc-only; the file stays — it is the declared CPV-canonical reference hook)

1. Rewrite the three publish.py sites: `--gate` has NO automatic invoker; the installed
   `.githooks/pre-push` (ancestry check) is the strictly-stricter live gate;
   `git-hooks/pre-push` is the CPV-canonical reference hook, NOT installed here.
2. Add a header line to `git-hooks/pre-push` itself stating it is not installed in this
   repo (`core.hooksPath=.githooks`) and exists as the CPV-canonical reference.

## Derived tasks

- `grep -rn "git-hooks"` sweep after the edit: no remaining site may describe the file
  as live.

## Acceptance

- [ ] All three sites corrected; sweep clean; tests green.

## Approval log

- 2026-08-18T19:52:44+0200 — Tier-0 (doc-only, in-scope) authored as planned work under
  the hub's Phase-2 GO dispatch.

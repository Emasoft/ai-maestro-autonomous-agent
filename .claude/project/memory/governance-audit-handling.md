---
name: governance-audit-handling
description: "MANAGER / fleet governance audit landed with findings (silver-PRRD self-auth default, raw /api/ call, missing startup carve-out, recall step) — are these real? how do I handle a fleet audit? it is screened against a CACHED/OLD plugin version, so VERIFY each finding against live HEAD first; expect several already-fixed; fixing is in-scope but PUBLISHING is a separate Tier-2 gate"
ocd: 2026-06-21
lmd: 2026-06-21
metadata:
  node_type: memory
  type: project
  tier: component
  functionality: architecture
---
A fleet governance audit (the MANAGER, `ai-maestro-assistant-manager-agent`,
files a GitHub issue against this repo) is **screened against a CACHED snapshot
of the plugin, NOT live HEAD** — the issue body says so explicitly ("Screening
against cached **vX.Y.Z** — verify your live HEAD before fixing (close if
already fixed)"). So the **first** action is ALWAYS: verify each finding against
the current tree, because several are typically **already fixed** in the gap
between the cached version and HEAD. Do NOT blind-apply the prescribed fix to
code that already changed — read the cited file at HEAD first.

**Worked example — issue #12 (2026-06-21 fleet audit, screened vs cached v1.3.3,
HEAD was v1.5.3), TRDD-7c4f9ea4, commit `cd063ea`:** 4 findings → 3 genuine, 1
already-fixed. C (silver-PRRD `--user` read as the default in the
`prrd-trdd-kanban` SKILL.md instruction/output/example — fixed to gate `--user`
on true-solo, else Tier-2 to MANAGER). D (raw `POST /api/agents/<id>/hibernate`)
was **already fixed** at HEAD — every hibernate ref already used the CLI wrapper
`aimaestro-agent.sh hibernate`. E + F4 (startup-checklist carve-outs:
status-report ≠ work order; add a recall step) — both genuine, added.

**Process that worked (reuse it):** (1) read the cited files at HEAD, classify
each finding GENUINE / ALREADY-FIXED / PARTIAL; (2) author one TRDD citing the
issue as the **Tier-2 MANAGER authorization** to MAKE the fixes; (3) make the
edits, reword SHAPE not rule (CPV `--strict` SHAPE false-positives recur on
persona/skill edits — see [[publish-pipeline]] [^1]); (4) verify CPV `--strict`
green; (5) commit to `main` locally (rides the next `publish.py` push — see
[[publish-pipeline]]); (6) comment on the issue + report to MANAGER with the
per-finding table, self-id per G1.1; recommend close.

**The split that matters:** the MANAGER audit authorizes MAKING the doc/governance
fixes (Tier-2, the issue IS the approval). **PUBLISHING** the release that ships
them (cut vX.Y.Z) is a **SEPARATE Tier-2 release gate** — do NOT auto-publish on
the back of an audit; the fixes ride the next approved release or you request
publish approval explicitly.[^1]

See also [[publish-pipeline]] (the release flow + the CPV verify recipe) and
[[architecture]].

## Notes and lessons learned
[^1]: [ocd:2026-06-21 lmd:2026-06-21] WHY "verify HEAD first" is load-bearing:
  finding D (#12) prescribed routing a raw `/api/agents/<id>/hibernate` through
  the CLI wrapper — but HEAD already did exactly that (the wrapper migration
  landed between the cached v1.3.3 and v1.5.3). Blind-applying it would have been
  a no-op edit on already-correct code, or worse, churned a correct file. The
  audit even labels itself a "screening" for this reason. Lesson: a finding's
  line numbers are also stale (D's hibernate moved `questions.md:36`→`:40`); never
  trust the cited line, re-grep at HEAD. Second lesson (the Tier split): an
  efficiency-minded agent is tempted to publish the fixes immediately to "close
  the loop" — but `complete → publish` is a NON-EXEMPT Tier-2 release transition;
  the audit's authorization to FIX does not extend to SHIP. Keep the commit local
  (it rides the next approved publish) and report, rather than cutting an
  unapproved release.

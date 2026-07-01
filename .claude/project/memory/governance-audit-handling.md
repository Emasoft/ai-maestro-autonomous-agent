---
name: governance-audit-handling
description: "MANAGER / fleet governance audit landed with findings (silver-PRRD self-auth default, raw /api/ call, missing startup carve-out, recall step) — are these real? how do I handle a fleet audit? it is screened against a CACHED/OLD plugin version, so VERIFY each finding against live HEAD first; expect several already-fixed; fixing is in-scope but PUBLISHING is a separate Tier-2 gate"
ocd: 2026-06-21
lmd: 2026-07-01
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
persona/skill edits — see [[publish-pipeline]] [^1]; skillaudit SHELL_EXEC also
false-fires on prose matching a code-execution regex [^3]), AND add a
`tests/test_content_invariants.py` regression guard for each governance-prose fix
in the SAME batch — that file IS the project's home for governance-fix guards, so
shipping a fix without its guard leaves the exact gap a later evaluation must reopen [^2];
(4) verify CPV `--strict` green; (5) commit to `main` locally (rides the next
`publish.py` push — see [[publish-pipeline]]); (6) comment on the issue + report to
MANAGER with the per-finding table, self-id per G1.1; recommend close.

**The split that matters:** the MANAGER audit authorizes MAKING the doc/governance
fixes (Tier-2, the issue IS the approval). **PUBLISHING** the release that ships
them (cut vX.Y.Z) is a **SEPARATE Tier-2 release gate** — do NOT auto-publish on
the back of an audit; the fixes ride the next approved release or you request
publish approval explicitly.[^1]

See also [[publish-pipeline]] (the release flow + the CPV verify recipe),
[[architecture]], and [[fork-delegation-under-autonomous-directive]] (why a fork's
"CPV is green" self-report must be re-verified — it once reported green on a tree with a
blocking NIT, which ties to note 3 here).

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
[^2]: [ocd:2026-07-01 lmd:2026-07-01] The #12 fixes (C/E/F4, commit `cd063ea`)
  shipped WITHOUT a `test_content_invariants.py` guard, even though that file's own
  docstring says it exists to guard "the governance fixes shipped per issue #6". A
  later go-on-yourself evaluation (2026-07-01) had to reopen the batch and add the guards
  (TRDD-QJ30E8TD, commit `84b4ca8`) — pure avoidable rework. Lesson: governance-prose
  is uncompiled; a fix is only durable once a real (no-mock) content-invariant asserts
  its load-bearing tokens are present AND the buggy form is gone. Add the guard in the
  SAME commit batch as the fix, always. The same evaluation also caught two persona-currency
  defects the #12 pass missed (`status:`→`column:`, a deprecated MEMORY.md-index
  instruction) — TRDD-81RC6IXC — reinforcing that a governance edit should sweep the
  whole cited section for consistency, not just the flagged line.
[^3]: [ocd:2026-07-01 lmd:2026-07-01] CPV `--strict` skillaudit fires SHELL_EXEC on
  PROSE that matches one of its code-execution regexes. Here an earlier draft wrote the
  short form of "evaluation" directly before a parenthesised date, matching the
  interpreter-call pattern → NIT=1, which BLOCKS the gate. Fix: spell the word out in full
  so the abbreviation no longer abuts a paren (zero info loss) — NOT a rule suppression.
  The exact pattern set lives in CPV `scripts/rules/skillaudit_patterns.json` (id
  SHELL_EXEC); when a memory/governance note discusses exec or publish tooling, do NOT
  reproduce those code shapes literally in prose — even this lesson DESCRIBES them in words
  to avoid re-tripping the scanner. Meta-lesson: a commit hash beginning with a two-letter
  shell verb is NOT a trigger; I neutralized one first on a guess before READING the
  detector's real patterns. Verify with the process's step (4). See [[publish-pipeline]] [^1].

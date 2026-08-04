---
name: claude-code-version-sync
description: "a new Claude Code version shipped — what in this plugin goes stale? / which changelog window was already swept and where does the next sync start / the code.claude.com release-notes URL 404s, how do I read the changelog / is the persona still aligned with the host's isolation and subagent rules"
ocd: 2026-08-04
lmd: 2026-08-04
metadata:
  node_type: memory
  type: project
  tier: component
---

# claude-code-version-sync


^ATOM-43Z5-O3YW [desc:"Coverage is contiguous 2.1.181 → 2.1.221 across three TRDDs; the next sync starts at 2.1.222. Read the changelog via gh api — the docs release-notes URL 404s.", keywords: which_claude_code_versions_were_already_swept where_does_the_next_sync_start release_notes_url_404 how_to_read_the_claude_code_changelog is_my_plugin_stale_after_a_claude_code_release, ocd: 2026-08-04, lmd: 2026-08-04]

**Where the coverage stands.** Three cards, contiguous, each naming its window in the
title: `TRDD-BFDQH5A7` (2.1.181→2.1.200) · `TRDD-R6L582UX` (2.1.201→2.1.205) ·
`TRDD-9ZH31KC8` (2.1.206→2.1.221). **The next sync starts at 2.1.222.** Check the host
you are on first — `claude --version` — and pin every claim to the version you read it
in.

The 201–205 hole existed because the predecessor stopped at 200 and the USER supplied
206 onward. It was found only because the card that could not cover it WROTE THE GAP
DOWN instead of claiming "aligned to latest". Do the same: a window you skip goes in the
TRDD, in the title if possible.

**Fetching the changelog.** `https://code.claude.com/docs/en/release-notes` returns
**404** — do not burn a WebFetch on it. The source of truth is the repo file:

```bash
gh api repos/anthropics/claude-code/contents/CHANGELOG.md --jq '.content' | base64 -d > /tmp/cc-changelog.md
awk '/^## 2\.1\.205$/{f=1} f; /^## 2\.1\.200$/{exit}' /tmp/cc-changelog.md   # one window
```

It is ~480 KB, so capture to a file and slice the window — never read it whole.


^ATOM-7RHI-HK83 [desc:"Triage rule for a CC sweep: an entry matters only if it makes a rule STALE or exposes a hole the plugin claims to close — and 'verified absent' must be proven, not assumed.", keywords: what_counts_as_on-mission_in_a_changelog_sweep most_changelog_entries_need_no_change the_host_caught_up_to_a_rule_we_already_had prove_absence_before_claiming_a_plugin_is_unaffected, ocd: 2026-08-04, lmd: 2026-08-04]

**Most entries change nothing, and saying so is the deliverable.** Across three sweeps
(~250 changelog lines) only 9 entries moved this plugin. Triage each against ONE
question: *does it make a persona/skill rule stale, or expose a hole this plugin claims
to close?* Four outcomes, all legitimate:

1. **FIX** — the rule is now wrong or missing. The richest source is the host fixing an
   isolation bug in ITSELF: 2.1.212 / 2.1.216 / 2.1.217 / 2.1.220 each fixed a
   symlink-escape, and this plugin's own path check had the same defect (see
   `[[architecture]]` and `TRDD-9ZH31KC8`). When Claude Code hardens its own boundary,
   check whether the plugin's equivalent boundary has the same hole.
2. **ALREADY CONSISTENT** — the host caught up to a rule the plugin already had (2.1.205
   blocked session-transcript tampering; `layers.md` already permitted reading another
   agent's `.jsonl` and forbade editing it). Record it; do not edit.
3. **VERIFIED ABSENT** — the feature is not in this plugin at all. This must be
   **proven** per entry (read `plugin.json` / `hooks.json` / every frontmatter), never
   assumed. `hooks/hooks.json` being `{"hooks": {}}` is what makes a whole class of
   hook-related entries inapplicable, and that is a fact to re-check, not to remember.
4. **DELIBERATELY NOT DONE** — write it down with the reason (no `DirectoryAdded` hook
   was added: a rule statement closes the governance gap without a runtime surface).


^ATOM-FLOV-23CY [desc:"The on-mission test for a host change: does it touch write scope, sub-agent propagation, approval provenance, or unattended survival — the four things this persona governs.", keywords: is_this_changelog_entry_relevant_to_my_role_plugin which_four_things_does_the_persona_actually_govern how_do_I_decide_a_host_change_matters, ocd: 2026-08-04, lmd: 2026-08-04]

**The on-mission test is the persona's own surface.** A Claude Code change matters to
this plugin if it touches one of the four things the persona actually governs:

1. **write scope** — what the agent may create/modify/delete, and every door out of it;
2. **sub-agent propagation** — what an agent must inject into anything it spawns;
3. **approval provenance** — what counts as a real USER/MANAGER authorization;
4. **unattended survival** — what silently ends or stalls a long run with no human.

Everything else (rendering, IDE surfaces, telemetry, MCP plumbing, Windows terminal
fixes) is host business. Sorting by this test is what keeps a sweep to a handful of
edits instead of a rewrite.

## See also

- [[architecture]] — the hub this page radiates from: what the plugin is made of, and
  therefore what a host change can make stale.
- [[publish-pipeline]] — a sync lands as commits; shipping them is a separate,
  USER-gated step.

## Notes and lessons learned

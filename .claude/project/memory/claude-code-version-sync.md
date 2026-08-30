---
name: claude-code-version-sync
description: "a new Claude Code version shipped — what in this plugin goes stale? / which changelog window was already swept and where does the next sync start / the code.claude.com release-notes URL 404s, how do I read the changelog / is the persona still aligned with the host's isolation and subagent rules / my changelog triage may have dropped an entry that mattered — who reviews the discard list before I commit a sweep / an unattended run is parked on a new permission prompt (CI trust, a background session asking before it resumes)"
ocd: 2026-08-04
lmd: 2026-08-30
metadata:
  node_type: memory
  type: project
  tier: component
publish-globally: false
---

# claude-code-version-sync



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
edits instead of a rewrite. [^2] [^4]


^ATOM-WAOF-UB2X [desc: "First six of nine changelog-sweep TRDDs (2.1.181->2.1.247), each window named in its title.", keywords: which_claude_code_versions_were_already_swept changelog_sweep_TRDD_list 2.1.181_to_2.1.247_coverage is_my_plugin_stale_after_a_claude_code_release which_TRDD_covers_this_claude_code_version changelog_window_already_covered claude_code_version_sync_history TRDD-BFDQH5A7 TRDD-FHYQTRF8 contiguous_version_coverage, ocd: 2026-08-30, lmd: 2026-08-30]

**Where the coverage stands.** Seven cards, contiguous, each naming its window in the
title: `TRDD-BFDQH5A7` (2.1.181→2.1.200) · `TRDD-R6L582UX` (2.1.201→2.1.205) ·
`TRDD-9ZH31KC8` (2.1.206→2.1.221) · `TRDD-M50MBTSB` (2.1.222→2.1.224) ·
`TRDD-GA3TCRC7` (2.1.225→2.1.232) · `TRDD-V1AGFGQK` (2.1.233 — one falsified README
claim: the 2.1.232 input-redirection permission check was REVERTED in 2.1.233) ·
`TRDD-BUXVS9MD` (2.1.234→2.1.240 — 2.1.234/.235/.238 closed the silent
refuse/drop/oversize paths the persona cited, leaving only HOLD and dialog expiry) ·
`TRDD-FHYQTRF8` (2.1.241→2.1.247 — 8 pins: the one-line peer-message preview means
arrival is not reading; a `maxTurns` sub-agent now returns MARKED PARTIAL; a pinned
sub-agent model now falls back to the session chain instead of dying, so a pin is no
longer a guarantee; `/cd` hot-loads the new directory's hooks and settings. 2.1.241 is
an empty stub and 2.1.245 is a Linux glibc crash fix) ·


^ATOM-QRTK-R23T [desc: "TRDD-4B4GO06Q covers 2.1.248 (11 pins); the next-sync pointer now starts at 2.1.249 -- verify against claude --version.", keywords: next_sync_starts_at_2.1.249 where_does_the_next_changelog_sweep_start TRDD-4B4GO06Q 2.1.248_pins secret_predicate_hole restricted_mode_writable_roots cross-session_reply_lands_in_parent refresh_lock_retryable_error experimental_cacheTtl_reverted claude_--version_check next_sync_pointer, ocd: 2026-08-30, lmd: 2026-08-30]

`TRDD-4B4GO06Q` (2.1.248 — 11 pins over 7 entries: our own secret predicate had the
hole 2.1.248 fixed in the host's uploader, matching only `.env`/`.env.local` so
`prod.env`, `*.tfvars` and `key.pem.tmp`-style suffix copies walked through it; a
sub-agent's cross-session reply lands in the PARENT's conversation, never back in the
sub-agent; `--restricted` narrows the writable roots to cwd, refuses
`bypassPermissions` and ignores settings so hooks and rules never load; a
refresh-lock collision is now a retryable error instead of a bounce to the login
screen. Two entries — the `CI` trust-prompt bypass being removed and a
machine-off background session now asking before it resumes — were MISSED on the
first pass and recovered by an advisor review: both had died inside a wholesale
"agent-view fixes are host business" bucket, so it was the BUCKET LABEL that hid
them. `experimental.cacheTtl` was drafted onto the shipped agent and REVERTED — an
`experimental.` key bakes one host's cache economics into every installer's config).
**The next sync starts at 2.1.249.** Check the host
you are on first — `claude --version` — and pin every claim to the version you read it
in.


^ATOM-W7HI-3KOX [desc: "Why the 2.1.201-205 hole existed and the lesson: write a skipped changelog window into the TRDD title.", keywords: the_201-205_hole_in_changelog_coverage why_was_a_version_window_skipped write_down_a_skipped_changelog_window changelog_gap_in_TRDD_title predecessor_stopped_short_of_latest_version USER_supplied_missing_window do_not_claim_aligned_to_latest changelog_coverage_gap_history missing_version_range_write_it_down how_to_record_a_skipped_changelog_window, ocd: 2026-08-30, lmd: 2026-08-30]

The 201–205 hole existed because the predecessor stopped at 200 and the USER supplied
206 onward. It was found only because the card that could not cover it WROTE THE GAP
DOWN instead of claiming "aligned to latest". Do the same: a window you skip goes in the
TRDD, in the title if possible.


^ATOM-FR1M-6ADK [desc: "The release-notes URL 404s; fetch CHANGELOG.md via gh api and slice the window instead of reading it whole.", keywords: release_notes_url_404s how_to_read_the_claude_code_changelog code.claude.com_docs_404 fetching_the_claude_code_changelog gh_api_changelog_fetch CHANGELOG.md_via_gh_api do_not_webfetch_the_release_notes_page changelog_is_480kb_slice_the_window awk_window_slice_changelog never_read_the_whole_changelog, ocd: 2026-08-30, lmd: 2026-08-30]

**Fetching the changelog.** `https://code.claude.com/docs/en/release-notes` returns
**404** — do not burn a WebFetch on it. The source of truth is the repo file:

```bash
gh api repos/anthropics/claude-code/contents/CHANGELOG.md --jq '.content' | base64 -d > /tmp/cc-changelog.md
awk '/^## 2\.1\.205$/{f=1} f; /^## 2\.1\.200$/{exit}' /tmp/cc-changelog.md   # one window
```

It is ~480 KB, so capture to a file and slice the window — never read it whole. [^1] [^3]

## See also

- [[architecture]] — the hub this page radiates from: what the plugin is made of, and
  therefore what a host change can make stale.
- [[publish-pipeline]] — a sync lands as commits; shipping them is a separate,
  USER-gated step.


## Superseded


^ATOM-43Z5-O3YW [desc:"Coverage is contiguous 2.1.181 → 2.1.248 across nine TRDDs; the next sync starts at 2.1.249. Read the changelog via gh api — the docs release-notes URL 404s. ADVANCE THIS POINTER IN THE SAME CHANGE AS THE SWEEP.", keywords: which_claude_code_versions_were_already_swept where_does_the_next_sync_start release_notes_url_404 how_to_read_the_claude_code_changelog is_my_plugin_stale_after_a_claude_code_release the_next_sync_pointer_disagrees_with_the_archived_cards memory_says_start_at_a_window_already_swept, ocd: 2026-08-04, lmd: 2026-08-27, status: superseded, superseded-by: ATOM-WAOF-UB2X]

**Where the coverage stands.** Seven cards, contiguous, each naming its window in the
title: `TRDD-BFDQH5A7` (2.1.181→2.1.200) · `TRDD-R6L582UX` (2.1.201→2.1.205) ·
`TRDD-9ZH31KC8` (2.1.206→2.1.221) · `TRDD-M50MBTSB` (2.1.222→2.1.224) ·
`TRDD-GA3TCRC7` (2.1.225→2.1.232) · `TRDD-V1AGFGQK` (2.1.233 — one falsified README
claim: the 2.1.232 input-redirection permission check was REVERTED in 2.1.233) ·
`TRDD-BUXVS9MD` (2.1.234→2.1.240 — 2.1.234/.235/.238 closed the silent
refuse/drop/oversize paths the persona cited, leaving only HOLD and dialog expiry) ·
`TRDD-FHYQTRF8` (2.1.241→2.1.247 — 8 pins: the one-line peer-message preview means
arrival is not reading; a `maxTurns` sub-agent now returns MARKED PARTIAL; a pinned
sub-agent model now falls back to the session chain instead of dying, so a pin is no
longer a guarantee; `/cd` hot-loads the new directory's hooks and settings. 2.1.241 is
an empty stub and 2.1.245 is a Linux glibc crash fix) ·
`TRDD-4B4GO06Q` (2.1.248 — 11 pins over 7 entries: our own secret predicate had the
hole 2.1.248 fixed in the host's uploader, matching only `.env`/`.env.local` so
`prod.env`, `*.tfvars` and `key.pem.tmp`-style suffix copies walked through it; a
sub-agent's cross-session reply lands in the PARENT's conversation, never back in the
sub-agent; `--restricted` narrows the writable roots to cwd, refuses
`bypassPermissions` and ignores settings so hooks and rules never load; a
refresh-lock collision is now a retryable error instead of a bounce to the login
screen. Two entries — the `CI` trust-prompt bypass being removed and a
machine-off background session now asking before it resumes — were MISSED on the
first pass and recovered by an advisor review: both had died inside a wholesale
"agent-view fixes are host business" bucket, so it was the BUCKET LABEL that hid
them. `experimental.cacheTtl` was drafted onto the shipped agent and REVERTED — an
`experimental.` key bakes one host's cache economics into every installer's config).
**The next sync starts at 2.1.249.** Check the host
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

It is ~480 KB, so capture to a file and slice the window — never read it whole. [^1] [^3]
## Notes and lessons learned

[^1]: [id:ATOM-1GEI-AVA3, status:valid, desc:"The next-sync pointer said 2.1.222 while an archived card had already swept 222-224 — a by-design moving value that nothing advances is stale the moment the sweep lands.", keywords:"the_next_sync_pointer_disagrees_with_the_archived_cards memory_says_start_at_a_window_already_swept I_nearly_re-swept_a_window_a_card_already_covered a_moving_pointer_in_memory_went_stale where_does_the_next_changelog_sweep_start", ocd:2026-08-14, lmd:2026-08-14] DO NOT leave the "next sync starts at X" pointer for a later pass, BECAUSE it is a MOVING value with no other writer: the sweep that consumes it is the only event that can advance it, so the moment a sweep lands and the pointer does not, memory asserts a window already covered — here it read 2.1.222 for 7 days while TRDD-M50MBTSB had swept 222→224, and the next agent's choices were to redo that work or to mis-scope around it. Nothing goes red; a stale pointer reads exactly like a fresh one. DO advance the pointer, the card list and the atom's own desc in the SAME change as the sweep, and cross-check it against the archived cards (`grep -l 'cc-21' design/archived/`) before trusting it.
[^2]: [id:ATOM-QQTB-MIY7, status:valid, desc:"The four axes miss two classes: identity/addressing drift, and any entry whose only effect is a new permission prompt — both surfaced in the 2.1.225-2.1.232 sweep.", keywords:"the_four_on-mission_axes_have_no_home_for_this_entry identity_and_addressing_drift_in_a_changelog_sweep a_changelog_entry_fits_no_axis_but_still_matters session_names_are_not_stable_identities I_triaged_an_entry_under_the_wrong_axis", ocd:2026-08-14, lmd:2026-08-14] DO NOT triage a changelog entry by first-match against the four axes, BECAUSE two real classes have no axis and get dropped: (1) IDENTITY/ADDRESSING drift — 2.1.232 removed the confirm-by-ref step, added @-mention, and auto-uniquified colliding session names, so the name you address is neither confirmed nor stable; it reached the persona only by being stretched under "sub-agent propagation". (2) A fix whose ONLY effect is a NEW PERMISSION PROMPT — nested-git trust stopped inheriting, which is irrelevant to write scope (the writable roots are absolute) but is a full stop under axis 4; triaged under scope it reads as a no-op, which is how it was nearly dropped. DO run every entry against ALL FOUR axes before discarding it, and ask separately "does this create a prompt, or change who I think I am talking to?" — those two questions are the axes' blind spot.
[^3]: [id: ATOM-8EES-RGKS, status: valid, desc: "Eight shipped pins said 2.1.240 for features that live in 2.1.239 — read off the changelog's layout instead of each line's owning ## header.", keywords: "my_version_pin_says_the_wrong_release which_release_does_this_changelog_entry_belong_to I_attributed_a_feature_to_the_wrong_version the_newest_release_is_only_bug_fixes pinning_claims_from_a_pasted_changelog how_do_I_verify_a_version_pin_against_upstream a_mis-pinned_version_reads_exactly_like_a_correct_one", ocd: 2026-08-22, lmd: 2026-08-22] DO NOT read a changelog entry's version off the document's layout — its position in a paste, its proximity to a heading you remember, or a grep line-number inside a multi-release slice — BECAUSE a slice offset does not name the owning `## version` header, and the newest release is often a near-empty "Bug fixes and reliability improvements" stub whose features actually belong to the release BELOW it: that is exactly how eight pins in TRDD-BUXVS9MD came to say 2.1.240 for `ListAgents` self-naming, `/`-titled addressability, the RETRY_WATCHDOG fail-fast and Windows cross-session messaging, all of which are 2.1.239 — and the error reached the persona, the README, the card and a test docstring, because a mis-pinned version is INVISIBLE: it reads exactly like a correct one, and the pin is the only mechanism a later sweep has for noticing a claim went stale. DO derive the phrase list FROM THE DIFF rather than from memory — `git diff -U0 <base>^..HEAD -- <shipped paths>`, counting pins on `+` lines against `-` lines, so NET-NEW pins are separated from ones merely re-flowed by a rewrite; a hand-assembled list omits exactly the pin you forgot you touched, and three consecutive review rounds each found one more that way. Match with `2\.1\.\d{2,3}`, never `2\.1\.2[0-9]{2}` — the narrow form silently drops every 2.1.1xx pin and understates your own coverage denominator. THEN walk the WHOLE changelog line by line tracking the current `## <version>` header, assert every derived phrase against the header that owns it, and print an explicit per-pin OK/WRONG verdict before committing — grepping a pre-cut window can only tell you the phrase EXISTS somewhere, never which release it is in, and grepping upstream for patterns you copied FROM upstream cannot fail even if your own prose drifted.
[^4]: [id: ATOM-SMYW-R1EQ, status: valid, desc: "Two 2.1.248 entries were dropped by a wholesale bucket label, not by their content; an advisor review recovered them.", keywords: "I_discarded_a_group_of_changelog_entries_at_once a_changelog_sweep_missed_an_entry_that_mattered agent_view_fixes_are_host_business how_do_I_know_my_triage_did_not_drop_something false_negative_in_a_changelog_triage who_reviews_a_triage_before_I_commit_it should_I_review_the_discard_list_or_the_keep_list an_unattended_run_is_parked_on_a_permission_prompt CI_env_var_no_longer_skips_the_workspace_trust_prompt a_background_session_now_asks_before_resuming is_this_changelog_entry_really_host_business I_bucketed_changelog_entries_by_subsystem_instead_of_by_axis", ocd: 2026-08-28, lmd: 2026-08-28] DO NOT discard a GROUP of changelog entries under one wholesale bucket label ("agent-view fixes", "IDE surfaces", "MCP plumbing"), BECAUSE the label is applied to the group before any entry in it is read against the axes, so an entry is dropped for the company it keeps rather than for its content — in the 2.1.248 sweep the `CI` workspace-trust-prompt bypass being removed and a machine-off background session now ASKING before it resumes both sat in an "agent-view fixes" bucket, and both are new interactive full stops on unattended paths (axis 4 plus the permission-prompt blind spot). A false negative here is silent forever: nothing goes red, and the entry is never revisited because the window is marked swept. DO expand every bucket to its individual entries and run each one against all four axes plus the two blind spots, and have a second reader review the DISCARD list — not the keep list — before committing the sweep; both recoveries here came from the discard pile, and the keep pile was already correct.

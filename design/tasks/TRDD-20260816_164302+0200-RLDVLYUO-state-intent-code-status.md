---
trdd-id: RLDVLYUO
title: Ship the STATE-is-intent code-is-status guard in the persona
column: dev
created: 2026-08-16T16:43:02+0200
updated: 2026-08-16T16:43:02+0200
current-owner: autonomous-session
task-type: docs
scope: project
project-id: ai-maestro-autonomous-agent
release-via: publish
approval-tier: 0
relevant-rules: []
implementation-commits: []
---

# Ship the STATE-is-intent code-is-status guard in the persona

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-08-16

- Origin: fleet terminal-card audit, 2026-08-16. Three repos measured independently
  (programmer 14 cards, this repo 58, assistant-manager 26 partial): **0 terminal-FALSE
  anywhere, 11 cards carrying stale authoring-time STATE prose**. A prose-only audit
  reported 9 phantom failures in one repo and would have re-columned correct work in
  three repos at once.
- Worked examples in THIS repo (both cleared TERMINAL-TRUE by code+git, commit fef70a6):
  `TRDD-b48aa385` (Plan rows 2-8 read "pending"; 7fe8d84 + 9f20bfd landed the work) and
  `TRDD-V1AGFGQK` (STATE NEXT ACTION already executed by 26ad2d1).
- **NEXT ACTION:** none — shipped. Persona guard added, `test_persona_state_is_intent_code_is_status`
  pins it, released. See `## Approval log` for the version.

## Why

The AUTONOMOUS persona governs the least-supervised agents in the fleet: nobody is
watching to say "check the code". Every resume protocol tells them to trust the STATE
block first, and a STATE block is written at AUTHORING time and frequently never
refreshed after the work lands — so it reads as current truth while describing a plan
that already executed. That makes it the most confidently wrong field on a card.

The lesson otherwise lives in three chat threads and six gitignored reports, i.e. it
dies today.

## Acceptance

- [x] The rule is in the shipped persona (`agents/ai-maestro-autonomous-agent-main-agent.md`).
- [x] It carries the measurement (3 repos, 72+ cards, 0 terminal-false, 11 stale-prose) so a
      reader can tell it from an opinion.
- [x] A content-invariant test pins its presence.
- [x] Released, not left on main.

## Approval log

---
name: server-side-pending-verbs
description: "waiting on server CLI verb / owner escalation verb still a proposal / reply polling via aimaestro-message replies LANDED (TRDD-BGAH6PHP shipped, inReplyTo vs replyTo fix) / approval-request timeout loop / inbox grep workaround obsolete / hub carded our reported needs"
ocd: 2026-08-20
lmd: 2026-08-20
metadata:
  node_type: memory
  type: project
  tier: component
publish-globally: false
---

# server-side-pending-verbs


^ATOM-DWS0-EMKP [desc: "Reply-poll verb carded hub-side as TRDD-BGAH6PHP; amp-inbox grep workaround stands until it lands", keywords: reply_polling ack_poll message-id_replies approval_timeout_loop TRDD-BGAH6PHP aimaestro-message_replies, type: project, ocd: 2026-08-20, lmd: 2026-08-20]

`aimaestro-message.sh replies <message-id> [--limit N]` LANDED (TRDD-BGAH6PHP shipped, deployed, live-verified 2026-08-20; spec verbs: send · resolve · replies). TSV rows (sender · message-id · timestamp · subject) for inbox messages whose inReplyTo matches; dash/underscore id spellings both match. Exit: 0 rows on stdout · 3 transport · 4 none yet (the timeout loop keys on this) · 7 auth. Reads the caller's OWN mailbox only (AID identity overrides any agent param, R28/R38). `send --reply-to` is also real now — it silently wrote a dead `replyTo` body key (vs pipeline `inReplyTo`) until the same-day fix.

**Why:** the ack-poll loop is now mechanical; teaching the old amp-inbox grep would resurrect an obsolete workaround.
**How to apply:** record the message-id `send` prints, poll `replies <id>` each heartbeat, branch on exit 0/4; escalate to MANAGER on timeout as before. See [[server-side-pending-verbs]] sibling atom for the escalation verb. [^1]


^ATOM-BMX6-ZCLV [desc: "USER-escalation verb is a Tier-2 hub proposal TRDD-WPZP48VV; urgent-alert-to-MANAGER workaround stands until approved", keywords: owner_escalation_verb escalate_to_user USER_escalation approval_request_timed_out TRDD-WPZP48VV urgent_alert_MANAGER_workaround, type: project, ocd: 2026-08-20, lmd: 2026-08-20]

The USER-escalation verb is a Tier-2 PROPOSAL hub-side, TRDD-WPZP48VV (in the hub's design/proposals/, deliberately NOT self-approved: agent→owner is a new R6 edge; title access, owner delivery, and anti-abuse bounds are governance decisions). Proposed shape: `escalate --timeout-of <message-id>` — the server verifies the cited approval request genuinely timed out unanswered; an escalation citing an answered message is refused. It composes with TRDD-BGAH6PHP's `replies` verb (its message-id evidence is what escalate verifies), so `replies` lands first by design.

**Why:** without the card id, a future cycle would re-report the need or invent an unsanctioned owner path.
**How to apply:** on approval-request timeout (24h normal / 1h urgent), today's path remains `aimaestro-message.sh send --priority urgent --type alert` to MANAGER; check the hub spec for an `escalate` verb before assuming it exists.

## Notes and lessons learned

[^1]: [id: ATOM-ZNCB-UC1E, status: valid, supersedes: ATOM-DWS0-EMKP, desc: "BGAH6PHP shipped same-day 2026-08-20; the amp-inbox grep workaround is superseded", keywords: "replies_verb_landed TRDD-BGAH6PHP_shipped reply-to_silently_dropped inReplyTo_vs_replyTo amp-inbox_grep_obsolete", ocd: 2026-08-20, lmd: 2026-08-20] DO NOT teach or use the amp-inbox grep workaround for reply polling any more, BECAUSE TRDD-BGAH6PHP shipped and live-verified same-day (2026-08-20): `aimaestro-message.sh replies <message-id> [--limit N]` is in the spec (verbs: send · resolve · replies) — and note `send --reply-to` was silently dropped (dead `replyTo` body key vs pipeline `inReplyTo`) until the same-day fix. DO use: record the message-id `send` prints, poll `replies <id>` each heartbeat, branch on exit 0 (rows) / 4 (none yet); escalate to MANAGER on timeout as before. SUPERSEDED BODY: `aimaestro-message.sh replies <message-id>` is carded hub-side as TRDD-BGAH6PHP (mandate, prio 2, 2026-08-20): TSV rows of messages whose replyTo matches; exit 4 = none yet, 3 transport, 7 auth; read-only over the agent's OWN mailbox (R28/R38 scoped). Until it lands, the approval-timeout loop keeps the workaround: drain amp-inbox each heartbeat and grep for the subject. Also live NOW: `aimaestro-message.sh send/resolve` (spec 671da397, deployed) — plugin skills may cite it alongside amp-inbox. **Why:** unattended cycles re-derive the ack path badly without the card id to check. **How to apply:** before teaching/executing reply-polling, check the hub spec (`~/ai-maestro/design/specs/aimaestro-scripts-spec.md`) for the `replies` verb; use it if present, else the amp-inbox grep. See [[server-side-pending-verbs]] sibling atom for the escalation verb.

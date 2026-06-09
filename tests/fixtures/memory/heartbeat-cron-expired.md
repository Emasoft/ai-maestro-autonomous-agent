---
name: heartbeat-cron-expired
description: "janitor heartbeat cron stopped firing after a plugin update — session went silent"
metadata:
  node_type: memory
  type: project
---

Recurring CronCreate jobs auto-expire after 7 days. Re-arm with /janitor-arm
(idempotent); the auto-rolling stub survives plugin version updates.

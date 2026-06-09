---
name: github-push-timeout
description: "git push to github times out or hangs — transfer stalls, RPC failed"
metadata:
  node_type: memory
  type: project
---

Retry pushes in a loop with slow-transfer tolerance:
`git -c http.lowSpeedLimit=100 -c http.lowSpeedTime=300 push` — retry only
on transient errors (timeouts, 5xx), never on auth/4xx failures.

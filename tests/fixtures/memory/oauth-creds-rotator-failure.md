---
name: oauth-creds-rotator-failure
description: "rotator failed, had to log in manually — where are the creds / why did the swap fail"
metadata:
  node_type: memory
  type: project
---

OAuth credentials live in the macOS keychain (service `aimaestro-oauth`),
not in dotfiles. The rotator fails when the keychain item is locked; unlock
the login keychain before swapping tokens.

---
name: publish-pipeline
description: "git push REFUSED by pre-push hook / 'every push MUST go through scripts/publish.py' — how do release + standalone doc commits actually reach origin; how to cut a release"
ocd: 2026-06-16
lmd: 2026-06-16
metadata:
  node_type: memory
  type: project
  tier: component
  functionality: architecture
---
This repo's release flow is `scripts/publish.py`, and a **pre-push git hook
refuses every plain `git push` to origin**. The hook verifies its caller by
PROCESS ANCESTRY (not an env var), so a push succeeds only when it descends from
`publish.py`. The error reads: *"git push REFUSED by pre-push hook. Strict publish
policy: every push to origin MUST go through scripts/publish.py."*

**Cut a release / push anything:**

```bash
uv run python scripts/publish.py --patch          # 1.x.y -> 1.x.(y+1)
uv run python scripts/publish.py --minor          # feature / structural change
uv run python scripts/publish.py --major
uv run python scripts/publish.py --minor --dry-run # runs every validation (ruff/mypy/pytest + CPV --strict); no commit/push
```

publish.py bumps the version across `plugin.json` + `pyproject.toml` + the persona
+ `README.md` + `uv.lock`, runs git-cliff for `CHANGELOG.md`, commits
`chore(release): vX.Y.Z`, tags, pushes commit + tag, and creates the GitHub
release. It requires a CLEAN working tree (Step 1) — commit your work first.

**Consequence for standalone doc/TRDD commits:** a commit you make directly on
`main` (archiving a completed TRDD, recording a decision, seeding a memory note)
**cannot be plain-pushed** — it sits local and rides the NEXT `publish.py` push
(publish.py does `git push origin HEAD`, carrying every ahead-of-origin commit).
This is normal here, not a bug: v1.4.0's publish carried the prior session's
unpushed `docs(trdd)` commit to origin. Do **not** bypass the hook with
`--no-verify`.

See [[architecture]].

## Notes and lessons learned

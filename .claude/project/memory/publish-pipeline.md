---
name: publish-pipeline
description: "git push REFUSED by pre-push hook / 'every push MUST go through scripts/publish.py' — how do release + standalone doc commits actually reach origin; how to cut a release; is --force-templates / CPV canonical-migration safe on this plugin (publish.py: NO — custom M11 logic; the release.yml/notify-marketplace.yml workflows are actually BEHIND canon on hardening, NOT ahead — the old 'ahead-of-canon' claim was VERIFIED FALSE 2026-07-01; RC-PIPELINE-DRIFT WARNINGs are accepted non-blocking drift)"
ocd: 2026-06-16
lmd: 2026-07-01
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

The publish gate runs **CPV `--strict`** (Step 5) and BLOCKS on any
CRITICAL/MAJOR/MINOR/NIT. Two phrasing FALSE-POSITIVES recur when editing the
persona/skills — reword the *shape* to clear them, never suppress the rule.[^1]

**Do not BLINDLY `--force-templates` this plugin's pipeline — but for two reasons, and
NOT the "ahead-of-canon" one long recorded here (that was VERIFIED FALSE 2026-07-01; see
[^5]).** (1) `publish.py` carries hard-won custom M11 version-sync logic (plugin.json +
pyproject + persona + README + uv.lock) a generic clobber would regress — the real, sound
basis of the USER-ratified TRDD-5c21e4a0. (2) `release.yml` is a by-design **post-hoc
validate-tag gate** (publish.py creates the release BEFORE the tag push), so a blind
clobber would reintroduce a conflicting release-creator job. **HOWEVER — contrary to the
earlier claim — `release.yml` + `notify-marketplace.yml` are BEHIND canon on real
hardening:** canon has a least-priv `permissions:` block, **build-provenance attestation**,
`timeout-minutes` on notify, the `HAS_MARKETPLACE_PAT` no-op guard, and **NEWER** SHA-pins
(`checkout` v6.0.3, `setup-uv` v8.2.0); the plugin has **no** provenance/SBOM/SHA256SUMS
(anywhere — CI or publish.py) and older/unpinned actions. The correct forward motion is a
**careful MANUAL port** of canon's hardening into the plugin's architecture (Tier-2), never
a blind force-template and never "leave them, they're ahead". The `RC-PIPELINE-DRIFT-001`
WARNINGs (7) are still accepted non-blocking drift. A fleet "go canonical" re-ask still
gets the `=runner` fast-confirm recipe below — but report the plugin as BEHIND-and-porting,
never AHEAD.[^2][^4][^5]

**The CPV-canon CI "validate-step hardening" has a LANDMINE.** The safe additive
upgrade is: pin the CPV ref to a tag (`@v2.136.1`) + add `timeout-minutes`. But do
NOT add `CLAUDE_PRIVATE_USERNAMES: ${{ github.repository_owner }}` to a CI validate
step — that canon recommendation makes the leak scanner flag the PUBLIC owner name
(in every `github.com/<owner>/…` URL, `Agent:` trailer, author ref) as false
`CRITICAL: private path leaked`, reddening CI. It PASSES locally because `$(whoami)`
≠ the owner, so publish.py's local gate doesn't catch it — only CI does. v1.5.2
shipped red on this; v1.5.3 reverted it.[^3]

See [[architecture]] and [[governance-audit-handling]] (the latter reuses this
note's CPV-verify recipe + the local-commit-rides-next-publish flow when fixing a
governance audit).

## Notes and lessons learned

[^1]: [ocd:2026-06-18 lmd:2026-06-20] CPV `--strict` false-positives hit while
  publishing v1.5.0 (R26–R40 governance propagation): (1) a slash-separated word
  list like `skills/subagents/hooks/MCP` (or `skill/subagent/hook`) in an **agent**
  file is read by CPV's skill-reference checker as a path `skills/<name>` →
  `[MAJOR] Reference to non-existent skill 'subagents'`. Fix: use a comma list
  (`skills, subagents, hooks, or MCP servers`). (2) `sudo` + `password` adjacency in
  a **SKILL.md** (e.g. a checklist label that pairs the elevation keyword with `password`) trips
  `skillaudit:privilege_escalation` (a demoted NIT that still blocks `--strict`).
  Only **SKILL.md** is skillaudit-scanned — the identical text in `references/*.md`
  is NOT — so keep the sudo/password detail in the reference and give the SKILL.md
  label a neutral name (`Credential-passthrough check`). Root cause: CPV's static
  checkers pattern-match text SHAPE, not intent; the same governance prose is fine
  in `references/` but flagged in the scanned surfaces (agent body, SKILL.md).
  RECURRENCE TRAP (v1.5.1 publish, 2026-06-20): a doc that DOCUMENTS this
  false-positive can re-trip it — THIS note's old label example, plus an archived
  TRDD's `agent-<elevation> gate` phrasing, tripped the SAME NIT again and blocked
  the v1.5.1 gate; both were re-devitalized in commit `4f764e5`. The detector is
  SHAPE-specific, NOT token-specific: backtick `sudo` and `sudo/password` prose
  (lines above) pass fine, and the persona + governance SKILL.md carry heavy
  governance elevation-text WITHOUT tripping — but two narrow shapes (a label
  `<Elevation> / governance-password check`, and `agent-<elevation> gate`) DO. So
  when a git-tracked, CPV-scanned file must mention the offending shape, describe it
  with a placeholder — never reproduce the literal label/identifier — or you re-block
  your own NEXT publish.
[^2]: [ocd:2026-06-20 lmd:2026-07-01] ⚠ PARTLY SUPERSEDED by [^5] (2026-07-01): the
  sub-claims below that `release.yml`/`notify-marketplace.yml` are "AHEAD of canon" carrying
  SBOM/build-provenance/SHA256SUMS canon lacks, and that canon pins OLDER SHAs, are VERIFIED
  FALSE — inverted; the plugin is BEHIND canon. The publish.py-custom-logic + USER-deferral
  points STILL STAND. Original record: Fleet work order #10 (umbrella `ai-maestro#44`,
  MANAGER/USER directive) asked to `--force-templates` this plugin to CPV 2.136.1
  canon. A `plugin-fixer` run VERIFIED that is the WRONG action and STOPPED with zero
  edits (tree clean, version 1.5.1). Three blockers: (a) CPV's OWN validator flags
  `release.yml`+`notify-marketplace.yml` as *"AHEAD of canon … do NOT run
  `--force-templates`: it would DOWNGRADE this file"* — this plugin's release pipeline
  carries SBOM + build-provenance + per-asset SHA256SUMS + idempotent-release + a
  MARKETPLACE_PAT no-op guard that canon lacks; (b) canon pins DIFFERENT action SHAs
  (`setup-uv@fac544c…#v8.2.0`, `repository-dispatch@5fc4efd…#v4.0.0`) than the hardened
  v1.5.1 pins (`@d4b2f3b…#v5.4.2`, `@28959ce…#v4.0.1`), so a clobber regresses security;
  (c) USER-approved Tier-2 TRDD-5c21e4a0 already did the SAFE SHA-pin subset and
  explicitly DEFERRED the force-overwrite — v1.5.1 IS the ratified end-state. Plugin was
  already publish-clean (`--strict`: 113 passed, 0/0/0/0, 7 non-blocking WARNINGs). LESSON:
  a fleet "bring the pipeline to canonical" directive is NOT a mandate to force-clobber —
  check the validator's PER-FILE direction (some files say "migrate", AHEAD-of-canon files
  say "do NOT") AND the SHA-pin preservation FIRST. An already-hardened, ahead-of-canon
  plugin's correct response is **no-op + report**, never `--force-templates`. The only
  legitimate forward motion is the ADDITIVE subset (pin CPV ref `@v2.136.1`; harden the
  validate step) — proposal TRDD-270ef961, gated on Tier-2 approval. A future `publish.py`
  canon alignment, if ever wanted, must be a reviewed 3-way merge + `--dry-run` +
  test-release, never a force-overwrite.
[^3]: [ocd:2026-06-20 lmd:2026-06-20] When USER directed the CPV-canon additive
  upgrade (TRDD-270ef961), I implemented canon `pipeline-rules.md`'s CI "validate-step
  hardening" VERBATIM, including `env: CLAUDE_PRIVATE_USERNAMES: ${{ github.repository_owner }}`.
  v1.5.2 then went RED: 12 × `[CRITICAL] Private path leaked: username 'emasoft' …
  'Emasoft'`. Root cause: `CLAUDE_PRIVATE_USERNAMES` is the LIST OF USERNAMES THE
  SCANNER FLAGS AS PRIVATE, not an allowlist — set to the public owner, it flags the
  owner name that legitimately pervades the repo (github URLs, `Agent:` trailers).
  Canon's OWN local examples correctly use `$(whoami)` (the machine username, absent
  from committed files) — a self-contradiction. It passed LOCALLY (and through
  publish.py's gate) because `$(whoami)` ≠ owner; only CI, which set the env to the
  owner, failed. Fix: v1.5.3 dropped the whole `env` block (kept the `@v2.136.1` pin +
  `timeout-minutes`); CI green. LESSON: (1) a green LOCAL `--strict` does NOT prove a
  green CI when CI injects different env — verify the actual CI run, never assume.
  (2) `CLAUDE_PRIVATE_USERNAMES` = `$(whoami)` ONLY; never the repo owner; in CI there
  is no machine username to protect, so omit it. (3) treat CPV "canon" as fallible —
  this one is buggy (it's prescribed in `pipeline-rules.md`, scaffolded by
  `generate_plugin_repo.py`, AND enforced by a test). Filed claude-plugins-validation#141.
  A guardrail comment now sits in both workflows so a future canon-upgrade doesn't re-add it.
[^4]: [ocd:2026-06-20 lmd:2026-07-01] ⚠ PARTLY SUPERSEDED by [^5] (2026-07-01): this lesson's
  "ahead-of-canon exception" framing is INVERTED — the 2 workflow files are BEHIND canon (verified
  via the CPV unified diff). The `=runner` fast-confirm recipe below is STILL VALID (proves the
  tree is publish-clean), but its conclusion must read "BEHIND-and-porting", never "close as
  ahead-of-canon exception". Original record: Fleet RE-ASK #11 (MANAGER re-filed ai-maestro#44 as a
  per-repo tracker, 2026-06-20) prescribed the FULL canonical migration (`--force-templates`) +
  4 CI-only defects AMAMA hit (CPV#142). Reconciled WITHOUT re-deriving: (a) #11's OWN fix #1
  carves out this case — *"remote-validation-profile plugins: KEEP your by-design publish.py"*;
  (b) the 4 CPV#142 fixes don't apply (this plugin has no canonical `ci.yml` / no `uv sync
  --extra dev`; fix #3 = the owner-env bug already fixed at v1.5.3 → CPV#141; fix #4's
  "superseded validate.yml" is this plugin's ACTIVE workflow, not a leftover); (c) the
  force-templates clobber is the USER-deferred item (TRDD-5c21e4a0). FAST-CONFIRM RECIPE — run
  this to prove the exception in one shot on any future re-ask / CPV bump:
  `CLAUDE_PRIVATE_USERNAMES=runner uvx --from git+https://github.com/Emasoft/claude-plugins-validation@v2.136.1 --with pyyaml cpv-remote-validate plugin . --strict`
  → expect EXIT=0, CRITICAL=0/MAJOR=0/MINOR=0/NIT=0, 7 non-blocking WARNINGs (the accepted
  ahead-of-canon drift). If it passes, the plugin IS canon-clean and the only "gap" is the
  deferred structural clobber: post the evidence on the tracker, recommend close-as-exception,
  do NOT force-template (and never override the USER deferral on a MANAGER directive). Note:
  `=runner` is the canonical-safe value of `CLAUDE_PRIVATE_USERNAMES` in CI (= `$(whoami)` on a
  GitHub runner); this plugin OMITS it (equivalent — CI green proves it), explicit `=runner` is
  the canon form if ever wanted.
[^5]: [ocd:2026-07-01 lmd:2026-07-01] The claim that `release.yml` + `notify-marketplace.yml`
  are **AHEAD of canon**, carrying "SBOM + build-provenance + per-asset SHA256SUMS + a
  MARKETPLACE_PAT no-op guard canon lacks", that `--force-templates` "would DOWNGRADE" them, and
  that "canon pins OLDER SHAs" — recorded in [^2], the public **#11 v1.5.3 comment**, and the
  pre-2026-07-01 body of this note — is **VERIFIED FALSE. The direction is INVERTED; the plugin
  is BEHIND canon.** Re-ran CPV `--strict` at HEAD and READ THE UNIFIED DIFF it prints beneath the
  WARNING (not just the WARNING sentence): canon's `release.yml` HAS a least-priv `permissions:`
  block + `id-token`/`attestations: write` **build-provenance** (CPV #121), `checkout`@v6.0.3
  SHA-pinned, `setup-uv`@v8.2.0 (**newer** than the plugin's v5.4.2), `timeout-minutes: 30`; the
  plugin has **none** of the provenance/SBOM/SHA256SUMS (grep of `.github/` + `publish.py` = zero
  hits) and older/unpinned actions. `notify-marketplace.yml`: canon HAS the `HAS_MARKETPLACE_PAT`
  no-op guard + `timeout-minutes` + defensive `repository-dispatch`@v4.0.0; the plugin DROPPED them
  and uses the warned-against @v4.0.1. Git pickaxe: `provenance`/`sbom`/`SHA256SUMS` = **0 commits
  ever** in release.yml — never a regression, the feature list was fabricated. ROOT CAUSE: CPV's
  per-file text reads *"appears to be at or AHEAD of canon … **or the direction is ambiguous**"* —
  a HEDGED heuristic; the earlier `plugin-fixer` run + my public comment took the "AHEAD" branch at
  face value **without reading the diff CPV prints right under it**. LESSON: CPV's
  "ahead / don't-force-templates" sentence is advisory and can be WRONG — the **unified diff is
  authoritative; read it**. A prior SELF-REPORT (mine, a fork's, a past note's) is not evidence —
  re-verify against live tool output + `git log -S`. What STANDS: 5c21e4a0's publish.py-custom-logic
  reason, and that a *blind* `release.yml` clobber is unsafe for an ARCHITECTURAL reason (post-hoc
  gate vs release-creator) — just not the "downgrade of ahead hardening" reason. Evidence:
  `reports/go-on-yourself-eval/20260701_215629+0200-issue11-premise-inverted-verification.md`.
  Corrective actions (correct the public #11 post; manual-port canon hardening into the 2 workflows
  WITHOUT clobbering publish.py; add SBOM/provenance/checksums to releases) are GATED — TRDD
  authored, surfaced to USER.

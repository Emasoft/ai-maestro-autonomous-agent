"""Real (no-mock) regression guards for the governance fixes shipped per issues #6 and #12.

Each test reads the actual shipped file and asserts the corrected state, so a
future edit that re-introduces a fixed defect (R6 v2 citation, version drift,
ghost dispatch, empty SILVER, missing self-id, silver-PRRD self-auth default,
status-report-treated-as-work-order, dropped recall-before-acting,
status-vs-column field drift, deprecated MEMORY.md-index instruction) fails CI.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PERSONA = REPO_ROOT / "agents" / "ai-maestro-autonomous-agent-main-agent.md"
QUESTIONS = REPO_ROOT / "skills" / "ai-maestro-autonomous-governance" / "references" / "questions.md"
README = REPO_ROOT / "README.md"
PRRD = REPO_ROOT / "design" / "requirements" / "PRRD.md"
KANBAN = REPO_ROOT / "skills" / "ai-maestro-autonomous-prrd-trdd-kanban" / "SKILL.md"
PLUGIN_JSON = REPO_ROOT / ".claude-plugin" / "plugin.json"
PYPROJECT = REPO_ROOT / "pyproject.toml"
AMP_TEMPLATES = REPO_ROOT / "skills" / "ai-maestro-autonomous-governance" / "references" / "amp-templates.md"

SELF_ID = "This is the Claude responsible for the ai-maestro-autonomous-agent project."


def test_no_r6_v2_references_remain() -> None:
    """Persona, questions, and README cite R6 v3 — no stale 'R6 v2' / 'v2 graph' survives."""
    for path in (PERSONA, QUESTIONS, README):
        text = path.read_text(encoding="utf-8")
        assert not re.search(r"R6 v2|v2 graph|v2 communication|v2 tightening", text), f"stale R6 v2 citation in {path.name}"
        assert "v3" in text, f"{path.name} should cite the R6 v3 graph"


def test_persona_corrects_manager_full_y_claim() -> None:
    """The false 'MANAGER is the ONLY node with full Y to every other node' claim is gone."""
    text = PERSONA.read_text(encoding="utf-8")
    assert "ONLY node with full `Y` outbound to every other" not in text
    assert "reaches **team-internal** titles" in text
    # whitespace-flexible: the wrap between "via" and "that team's" may differ
    assert re.search(r"via\s+that team's \*\*CHIEF-OF-STAFF\*\*", text), "missing v3 MANAGER→team-internal-via-COS correction"


def test_persona_has_solo_dialog_loops() -> None:
    """Persona documents the three solo-mode loop substitutes + the no-self-mark-complete rule."""
    text = PERSONA.read_text(encoding="utf-8")
    assert "## Solo-mode dialog loops" in text
    assert "Comprehension self-handshake" in text
    assert "In-dev issue dialog" in text
    assert "Pre-PR self-check gate" in text
    assert "nobody self-marks completed" in text


def test_persona_has_peer_claim_protocol() -> None:
    """Persona documents the peer-AUTONOMOUS single-writer claim protocol."""
    text = PERSONA.read_text(encoding="utf-8")
    assert "## Peer-AUTONOMOUS coordination" in text
    assert "single-writer" in text
    assert "earlier claim wins" in text


def test_persona_amp_bodies_require_self_id() -> None:
    """Persona's AMP section requires the self-id line on every AMP body."""
    text = PERSONA.read_text(encoding="utf-8")
    assert "Lead every AMP message body with your self-id line" in text
    assert SELF_ID in text


def _version(text: str, pattern: str) -> str:
    m = re.search(pattern, text, re.MULTILINE)
    assert m, f"version pattern not found: {pattern}"
    return m.group(1)


def test_version_display_strings_in_sync() -> None:
    """plugin.json, pyproject, README **Version**, and persona **Plugin** vX.Y.Z all match."""
    pj = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))["version"]
    pp = _version(PYPROJECT.read_text(encoding="utf-8"), r'^version\s*=\s*"([^"]+)"')
    readme_v = _version(README.read_text(encoding="utf-8"), r"^\*\*Version\*\*:\s*(\d+\.\d+\.\d+)\s*$")
    persona_v = _version(PERSONA.read_text(encoding="utf-8"), r"\*\*Plugin\*\*:\s*\S+\s+v(\d+\.\d+\.\d+)")
    assert pj == pp == readme_v == persona_v, f"version drift: plugin.json={pj} pyproject={pp} README={readme_v} persona={persona_v}"


def test_prrd_has_project_id_and_silver_rules() -> None:
    """PRRD carries project-id: autonomous and a non-empty SILVER ruleset."""
    text = PRRD.read_text(encoding="utf-8")
    assert re.search(r"^project-id:\s*autonomous\s*$", text, re.MULTILINE), "PRRD missing project-id: autonomous"
    silver = re.findall(r"^- \*\*S\d+\.\d+\*\*", text, re.MULTILINE)
    assert len(silver) >= 4, f"SILVER section must carry real rules, found {len(silver)}"
    assert re.search(r"^prrd-version:\s*\d+\.\d+\s*$", text, re.MULTILINE)


def test_plugin_json_declares_base_dependency() -> None:
    """plugin.json declares the ai-maestro-plugin dependency in the documented object form."""
    data = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))
    deps = data.get("dependencies")
    assert isinstance(deps, list) and deps, "dependencies must be a non-empty array"
    # Canonical Claude Code shape is an array of objects: [{"name": "...", "version"?: "..."}].
    # Accept a bare-string entry too, for forward/backward tolerance.
    names = [d["name"] if isinstance(d, dict) else d for d in deps]
    assert all(isinstance(n, str) for n in names), "every dependency must resolve to a name string"
    assert "ai-maestro-plugin" in names


def test_kanban_skill_documents_pipelines_and_has_no_ghost_dispatch() -> None:
    """Kanban skill documents project-type pipelines + USER override + AID_AUTH, with no ghost releaser dispatch."""
    text = KANBAN.read_text(encoding="utf-8")
    assert "Claude Code plugin" in text and "Library / package" in text and "Service" in text
    assert re.search(r"USER may mandate ANY custom\s+pipeline", text)  # prose may wrap the phrase
    assert "AID_AUTH fallback" in text
    # The RC-GHOST-DISPATCH-001 defect must never come back.
    assert 'subagent_type="deployer"' not in text and 'subagent_type="releaser"' not in text


def test_amp_templates_every_block_leads_with_self_id() -> None:
    """Every fenced template body in amp-templates.md leads with the self-id line."""
    text = AMP_TEMPLATES.read_text(encoding="utf-8")
    blocks = re.findall(r"```text\n(.*?)```", text, re.DOTALL)
    assert len(blocks) >= 4, f"expected >=4 templates, found {len(blocks)}"
    for block in blocks:
        assert block.lstrip().startswith(SELF_ID), f"template does not lead with self-id line: {block[:60]!r}"


# ── issue #12 governance-audit fixes (commit cd063ea, TRDD-7c4f9ea4) ──


def test_kanban_silver_prrd_is_tier2_not_self_auth() -> None:
    """Kanban skill: a SILVER PRRD change is Tier-2 when a MANAGER is reachable; prrd-edit.py --user is the TRUE-SOLO fallback only (issue #12 Fix C)."""
    text = KANBAN.read_text(encoding="utf-8")
    # Silver-PRRD edits route to MANAGER as a Tier-2 proposal when one is reachable...
    assert re.search(r"Tier-2 when a MANAGER is\s+reachable", text), "kanban skill must tier silver-PRRD edits to MANAGER"
    # ...and prrd-edit.py --user is only the true-solo fallback, never the default.
    assert re.search(r"TRUE-SOLO fallback\s+ONLY", text), "kanban skill must mark prrd-edit.py --user as the true-solo fallback only"


def test_persona_status_report_is_not_a_work_order() -> None:
    """Persona: a status-report request is NOT a work order — answering it is not permission to begin new work (issue #12 Fix E)."""
    text = PERSONA.read_text(encoding="utf-8")
    assert "status-report request" in text, "persona must address the status-report-request case"
    assert re.search(r"NOT a work\s+order", text), "persona must state a status-report request is NOT a work order"


def test_persona_documents_recall_before_acting() -> None:
    """Persona documents the recall-before-acting discipline tied to /janitor-memory-recall (issue #12 Fix F4)."""
    text = PERSONA.read_text(encoding="utf-8")
    assert re.search(r"[Rr]ecall before acting", text), "persona must document recall-before-acting"
    assert "/janitor-memory-recall" in text, "persona must reference the /janitor-memory-recall skill"


# ── go-on-yourself eval currency fixes (2026-07-01, TRDD-81RC6IXC) ──


def test_persona_two_folder_table_uses_column_not_status() -> None:
    """Persona's proposal→planned lifecycle keys on the v2 `column:` field, not a nonexistent `status:` field."""
    text = PERSONA.read_text(encoding="utf-8")
    # The corrected forms are present...
    assert "| Folder | `column:` | Meaning |" in text, "two-folder table header must key on `column:`"
    assert "the approver sets `column: planned`" in text, "approval prose must set `column: planned`"
    # ...and the buggy `status:`-as-lifecycle-field forms are gone (TRDD v2 has no `status:` field).
    assert "| Folder | `status:` | Meaning |" not in text
    assert "sets `status: planned`" not in text


def test_persona_memory_write_has_no_memory_md_index_instruction() -> None:
    """Persona does not instruct appending a MEMORY.md index/pointer line — the memory rule deprecated it (stub, memgrep-managed)."""
    text = PERSONA.read_text(encoding="utf-8")
    assert "/janitor-memory-write" in text, "persona must still document the memory-write skill"
    # The deprecated "(+ the MEMORY.md index line)" instruction must not come back.
    assert not re.search(r"MEMORY\.md.{0,4}index line", text), "persona must not tell the agent to write a MEMORY.md index line"


# ── mandate-is-authorization fix (2026-07-23, TRDD-MND8AUTH) ──


def test_persona_clear_mandate_is_authorization_to_begin() -> None:
    """Persona: a clear USER/MANAGER mandate authorizes starting the work — the agent must not idle for a second human 'proceed' (TRDD-MND8AUTH).

    The bug: an AUTONOMOUS agent sat waiting for human confirmation on a task MANAGER
    had already delegated via AMP. The fix ADDS an affirmative authorization rule and
    NARROWS the clarification reflex — without weakening any approval tier.
    """
    text = PERSONA.read_text(encoding="utf-8")
    # 1. Affirmative rule present.
    assert "A clear mandate is authorization to begin" in text, "persona must state a clear mandate authorizes starting"
    assert re.search(r"never\s+gate \*starting\*", text), "persona must say the tiers gate downstream actions, not starting the work"
    # 2. The over-broad 'ask before acting on ANY unclear instruction' reflex is gone,
    #    replaced by the genuinely-unclear / one-round form.
    assert "On any unclear instruction" not in text, "the over-broad 'any unclear instruction → wait' reflex must be removed"
    assert "genuinely unclear or blocking" in text, "clarification must fire only on a genuinely unclear/blocking instruction"
    # 3. The comprehension handshake no longer blocks a clear mandate.
    assert re.search(r"does NOT block execution", text), "the comprehension self-handshake must not block a clear mandate"
    # 4. GUARD: the fix is additive — Tier-2 MANAGER and Tier-3 USER gates are intact.
    assert "Tier 2 — MANAGER" in text, "Tier-2 MANAGER gate must survive the fix"
    assert "Tier 3 — USER" in text, "Tier-3 USER gate must survive the fix"
    assert re.search(r"NOT a work\s+order", text), "status-report-is-not-a-work-order invariant must survive the fix"


# ── issue #15 governance-conformance fixes (2026-07-23, TRDD-MND8AUTH batch) ──


def test_persona_keystroke_injection_is_absolute_no_manager_exception() -> None:
    """Persona F1 (#15): keystroke injection into another agent's session is ABSOLUTE (R42) — no user/MANAGER exception; the old tmux send-keys carve-out is gone."""
    text = PERSONA.read_text(encoding="utf-8")
    # The IRON keystroke-injection ban with no authorization escape.
    assert re.search(r"no user or MANAGER\s+instruction can authorize it", text), "keystroke injection must be ABSOLUTE — no user/MANAGER authorization"
    assert "R42.1/R42.2" in text, "the keystroke ban must cite R42.1/R42.2"
    # Driving your OWN session stays allowed (R42.4).
    assert re.search(r"Driving your OWN session is fine", text) and "R42.4" in text, "self-driving must stay allowed (R42.4)"
    # Lifecycle split into its own rule (MANAGER/COS authority, R42.6).
    assert re.search(r"Lifecycle is MANAGER/COS authority", text) and "R42.6" in text, "lifecycle must be its own MANAGER/COS-authority rule (R42.6)"
    # The buggy carve-out that let a MANAGER authorize tmux send-keys must be gone.
    assert not re.search(r"unless the user or MANAGER\s+EXPLICITLY instructs", text), "the R42-violating 'unless user/MANAGER instructs' tmux carve-out must be removed"


def test_persona_r22_self_id_and_agent_trailer_uniform_on_github_writes() -> None:
    """Persona F2 (#15): R22 self-id line + `Agent:` commit trailer are mandated uniformly on GitHub writes, not just AMP."""
    text = PERSONA.read_text(encoding="utf-8")
    assert "R22 (mandatory)" in text, "persona must carry the standing R22 GitHub-write rule"
    assert "every GitHub write" in text, "R22 rule must cover every GitHub write, not just AMP"
    assert re.search(r"Agent: ai-maestro-autonomous-agent.{0,12}trailer", text), "R22 rule must mandate the Agent: commit trailer"
    assert "R22 governs GitHub writes" in text, "persona must distinguish AMP self-id (AMP-only) from R22 (GitHub)"


# ── issue #17 worker-side duties: drain inbox on wake, clone step 0, report NPT gap (2026-07-24, TRDD-WAKEDRN8) ──


def test_persona_drains_inbox_first_and_mandate_is_a_work_order() -> None:
    """Persona (#17): the wake sequence drains the AMP inbox FIRST and treats an inbound mandate as an actionable work order.

    SCEN-031: a fresh AUTONOMOUS dev got a well-formed AMP build mandate and sat idle.
    The startup checklist must lead with drain-first + mandate-is-a-work-order, while
    keeping the status-report request as the SOLE exception (additive, no gate weakened).
    """
    text = PERSONA.read_text(encoding="utf-8")
    assert "Drain your AMP inbox FIRST" in text, "startup checklist must lead with draining the inbox first"
    assert re.search(r"a mandate is a build order", text), "persona must state a mandate is a build order to act on"
    # The status-report exception is preserved but re-scoped as the ONE exception.
    assert "The ONE exception is a\n   status-report request" in text or re.search(r"ONE exception is a\s+status-report request", text), "status-report request must remain the single exception"
    # GUARD: the mandate-is-authorization invariant is untouched.
    assert "A clear mandate is authorization to begin" in text, "the mandate-is-authorization rule must survive"


def test_persona_clones_assigned_repo_as_step_0() -> None:
    """Persona (#17): executing a build mandate clones the named repo as step 0, before building."""
    text = PERSONA.read_text(encoding="utf-8")
    assert "Executing an assigned build mandate" in text, "persona must document the build-mandate execution flow"
    assert "Clone the repo as step 0" in text, "persona must make cloning the assigned repo step 0"
    assert re.search(r"first concrete action of the build", text), "the clone must be framed as the first concrete build action"


def test_persona_reports_the_npt_gap_never_sits_silent() -> None:
    """Persona (#17): an unmet NPT prerequisite is held AND reported to the sender (receiver's duty), never held silently."""
    text = PERSONA.read_text(encoding="utf-8")
    assert re.search(r"Hold the NPT gate honestly", text), "persona must keep holding the NPT gate honest"
    assert re.search(r"REPORT the unmet prerequisite\s+back to the sender", text), "persona must require reporting the unmet prerequisite to the sender"
    assert re.search(r"silent hold is indistinguishable from a\s+stall", text), "persona must state a silent hold reads as a stall"


# ── rule-number drift guard (2026-07-25, ai-maestro#87 item 2/5) ──


def test_persona_marks_rule_numbers_as_as_of_authoring() -> None:
    """Persona (ai-maestro#87): the ~24 hardcoded rule numbers are declared as-of-authoring pointers, not assertable facts.

    The numbers are copied from a versioned, MANAGER-revisable governance source, so a
    renumber drifts this file silently and no prose test can detect it. The mitigation is
    a standing disclaimer that defers to the live source — compatible with either outcome
    of the core ruling (keep citing inline vs. inherit rule text).
    """
    text = PERSONA.read_text(encoding="utf-8")
    assert "as-of-authoring" in text, "persona must declare its rule numbers as-of-authoring"
    assert re.search(r"cite a rule by its \*\*substance\*\*", text), "persona must tell the agent to cite by substance, not number"
    assert re.search(r"identity/messaging skills are\s+authoritative", text), "persona must defer to the live governance source when a number does not resolve"
    # The deferral must not be hollow: the comm-graph precedent it invokes must still exist.
    assert "agent-messaging" in text, "the agent-messaging deferral precedent must still be present"


# ── issue: direct ai-maestro server API calls (USER directive 2026-08-02, TRDD-4P2RZQFE) ──

GOVERNANCE_SKILL = REPO_ROOT / "skills" / "ai-maestro-autonomous-governance" / "SKILL.md"
ISOLATION_SKILL = REPO_ROOT / "skills" / "ai-maestro-autonomous-workspace-isolation" / "SKILL.md"


def test_every_skill_forbids_direct_server_api() -> None:
    """Every SKILL.md instructs the frozen CLI and forbids a raw /api/* server call (R23).

    The persona already carried this as FORBIDDEN ACTION #2, but skills load on demand and
    IN ISOLATION — an agent consulting only a skill would never see it. The USER declared
    the CLI/API separation an iron rule and required it be instructed in the SKILLS.
    """
    for skill in (GOVERNANCE_SKILL, KANBAN, ISOLATION_SKILL):
        text = skill.read_text(encoding="utf-8")
        assert "/api/" in text, f"{skill.name} must name the forbidden raw route shape"
        assert re.search(r"[Nn]ever call a server\s+HTTP route", text), (
            f"{skill.name} must forbid calling a server HTTP route directly"
        )
        assert "R23" in text, f"{skill.name} must cite the frozen-interface rule R23"
        assert re.search(r"aimaestro-(agent|teams)\.sh|\*\.py. helpers|frozen CLI", text), (
            f"{skill.name} must name the CLI that replaces the direct call"
        )


def test_governance_audit_has_a_direct_api_question() -> None:
    """The self-audit carries Q13; a rule with no checklist question is one the audit can't catch."""
    questions = QUESTIONS.read_text(encoding="utf-8")
    assert "**Q13 Direct-server-API check**" in questions, "questions.md must define Q13"
    assert "aimaestro-agent.sh" in questions, "Q13 must name the CLI that replaces the raw call"
    skill = GOVERNANCE_SKILL.read_text(encoding="utf-8")
    assert "Q13 Direct-server-API check" in skill, "the SKILL.md checklist must list Q13"
    assert "12-question" not in skill and "12 questions" not in skill, (
        "the question count must be updated everywhere — a stale '12' makes Q13 skippable"
    )


# ── @-mention safety: an @name is a notification, not a label (USER report 2026-08-02) ──


def test_persona_forbids_at_mentions_in_github_bodies() -> None:
    """R22's self-id line carries no '@', and the persona explains why an @name pages a stranger.

    The generic PRRD G1.1 template shows '@owner' as a PLACEHOLDER. Posted literally it
    mentions a real GitHub organization (verified 2026-08-02: 58 followers). Role names used
    as addresses (@MANAGER, @COS, @architect, @CPV, @janitor, @core) are all real accounts too.
    """
    text = PERSONA.read_text(encoding="utf-8")
    assert "shared repo-owner gh auth" in text, "the self-id line must not carry an @handle"
    assert "@owner gh auth" not in text, "the literal @owner placeholder must never ship"
    assert re.search(r"NEVER put an `@` in a GitHub body", text), (
        "the persona must forbid @-mentions in GitHub bodies"
    )
    assert "NOTIFICATION, not a label" in text, "the persona must say WHY (an at-mention pages someone)"


def test_no_literal_at_owner_placeholder_in_shipped_surfaces() -> None:
    """No shipped surface tells an agent to post '@owner' — that pages a real organization."""
    for sub in ("agents", "skills", "commands", "hooks"):
        root = REPO_ROOT / sub
        if not root.is_dir():
            continue
        for path in root.rglob("*.md"):
            assert "@owner" not in path.read_text(encoding="utf-8"), (
                f"{path.relative_to(REPO_ROOT)} ships the literal @owner placeholder"
            )


def test_prrd_golden_rules_carry_no_bare_at_mention() -> None:
    """No PRRD rule instructs (or contains) a bare at-mention — G1's byline was the leak's source."""
    text = PRRD.read_text(encoding="utf-8")
    # Strip inline code / fences: an at-sign inside code does NOT notify on GitHub, and G8
    # deliberately quotes handles that way when naming them.
    prose = re.sub(r"`[^`\n]*`", " ", re.sub(r"```.*?```", " ", text, flags=re.S))
    stray = re.findall(r"(?:(?<=^)|(?<=[^A-Za-z0-9_/]))@[A-Za-z0-9][A-Za-z0-9-]{0,38}", prose)
    assert not stray, f"PRRD prose carries live at-mention(s): {stray}"
    assert "**G8.1**" in text, "the at-mention prohibition must exist as a golden rule"


def test_prrd_rule_numbers_are_unique_across_tiers() -> None:
    """A number identifies ONE rule regardless of tier — G2 and S2 cannot coexist (PRRD grammar)."""
    nums = re.findall(r"^- \*\*[GS](\d+)\.\d+\*\*", PRRD.read_text(encoding="utf-8"), flags=re.M)
    dupes = {n for n in nums if nums.count(n) > 1}
    assert not dupes, f"rule number(s) reused across tiers: {sorted(dupes)}"

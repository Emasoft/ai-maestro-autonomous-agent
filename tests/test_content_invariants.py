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
    """Persona F1 (#15): keystroke injection into another agent's session is ABSOLUTE for AUTONOMOUS — no user/MANAGER exception; the old tmux send-keys carve-out is gone.

    CORRECTED TWICE, and the second correction is the instructive one.

    On 2026-08-07 this test was rewritten to REQUIRE the persona to call R42.8 *pending*,
    because the published governance file then read 1929 lines / R42.1-R42.7 / zero
    `R42.8`. That measurement was accurate and positively controlled. It was taken inside
    a 3-day lag between the USER's grant (2026-08-05) and publication (2026-08-08 05:56Z).

    So this test spent a day ENFORCING a false statement about ratified governance -- the
    same "a green test pins the defect" failure it was rewritten to fix, recreated in the
    opposite direction, and made more durable by the falsification work that proved it had
    teeth. Proving a guard CAN fail says nothing about whether the fact it encodes is true.

    Verified 2026-08-08 before this rewrite: R42.8 resolves as a row in the R42 section,
    attributed `Explicit (USER - 2026-08-05, ai-maestro#125, TRDD-AODXPI5E)`.
    This line previously read "1952 lines, subsections R42.0-R42.8" (TRDD-1504BH3Q): the
    count came from a DIFFERENT tip than the one named beside it, and R42.0 was never a
    subsection at either tip - it appears only inside a changelog sentence that a
    substring grep matched. A control that matches a substring can confirm a claim you
    never checked; a line count also rots on any unrelated edit. Structural presence is
    the control that can only fail for the reason we care about.

    THE VERB LIST IS VOLATILE AND THIS TEST DELIBERATELY DOES NOT PIN ITS MEMBERSHIP.
    Measured at `governance-rules` on 2026-08-08: tip cdee1dd (05:56Z) read
    "`read-prompt` and `answer` ONLY" with zero `block-state`; tip e46764f6 (06:03Z),
    SEVEN MINUTES LATER, read "`block-state`, `read-prompt` and `answer` ONLY". An earlier
    revision of this test asserted `block-state` must NOT appear -- which, one commit on,
    enforced exactly the omission the hub had just corrected.

    So the assertions below split by STABILITY, not by importance:
      * stable + safety-critical -> asserted hard (inject/slash/queue are self-only;
        AUTONOMOUS holds no title; R42.8 is ratified). None of these has ever moved.
      * volatile -> asserted only as "the persona names a list AND carries the probe",
        never as a membership check. Pinning a fact that moved twice in 30 minutes makes
        the suite a liability: it goes red on truth and green on staleness.

    The rule this encodes, learned twice in one day: a test that hard-codes an EXTERNAL
    fact must carry the probe that establishes it, or the premise silently inherits the
    guard's credibility. Falsification tests the MECHANISM, never the PREMISE.
    """
    text = PERSONA.read_text(encoding="utf-8")
    # The IRON keystroke-injection ban with no authorization escape.
    # \s+ between every word: the assertion is semantic, so a re-wrap must not break it.
    assert re.search(r"no\s+user\s+or\s+MANAGER\s+instruction\s+can\s+authorize\s+it", text), "keystroke injection must be ABSOLUTE — no user/MANAGER authorization"
    assert "R42.1/R42.2" in text, "the keystroke ban must cite R42.1/R42.2"
    # R42.8 exists and is RATIFIED — the persona must scope it, not deny it.
    assert re.search(r"R42\.8\s+is\s+RATIFIED", text), (
        "persona must state R42.8 is ratified — denying it teaches a false rule"
    )
    assert re.search(r"USER\s+—\s+2026-08-05", text), "persona must carry R42.8's attribution"
    assert re.search(r"including\s+AUTONOMOUS:\s+none", text), (
        "R42.8 must be shown title-scoped, with AUTONOMOUS holding no such title"
    )
    # VOLATILE — assert only that a verb list is named and dated, never its membership.
    assert re.search(r"`answer`\s+ONLY", text), "persona must state the exception verbs are a closed list"
    assert re.search(r"governance-rules`?\s+tip\s+`?[0-9a-f]{7,}", text), (
        "the verb list must carry the tip it was read at — it moved twice in 30 minutes on 2026-08-08"
    )
    assert re.search(r"re-fetch\s+the\s+row\s+before\s+relying\s+on\s+its\s+exact\s+membership", text), (
        "persona must send the reader to the live row rather than trusting this list"
    )
    assert re.search(r"`inject`,\s*`slash`\s+and\s+`queue`\s+are\s+explicitly\s+NOT\s+exception\s+verbs", text), (
        "persona must state inject/slash/queue are self-only for every title"
    )
    # The lag lesson must survive, or the next measurement repeats the same inference.
    assert re.search(r"evidence\s+about\s+PUBLICATION,\s+never\s+about\s+ratification", text), (
        "persona must record that absence from a published artifact is not absence of the rule"
    )
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


GOV_SCENARIOS = REPO_ROOT / "tests" / "scenarios" / "governance-scenarios.md"

# The deleted R29.1 text. Legal ONLY as a quoted warning, never as a claim.
_MISCOUNT = re.compile(r"(?:COS|CHIEF-OF-STAFF)\*{0,2}\s*\+\s*5")
# Cues that mark an occurrence as a quotation of the error rather than an assertion of it.
_QUOTED = re.compile(r"Never write|It read|previously read|laundered|deleted|wrong twice", re.I)


def test_team_base_is_five_including_the_cos_and_the_miscount_is_only_ever_quoted() -> None:
    """The base is 5 INCLUDING the COS (R12.1); the deleted "COS + 5" text may appear only as a warning (TRDD-62AO9JXY).

    Found by auditing my own tree for the exposure class I had just advised a peer about.
    Both the persona and this scenario file asserted the MANAGER "auto-creates the
    CHIEF-OF-STAFF + 5 base members" — verbatim the text USER deleted on 2026-07-14
    (GOVERNANCE-RULES v4.2.1) as wrong TWICE: it miscounts the base as six (R12.1 defines
    five INCLUDING the COS) and credits the SYSTEM with work R12.2/R31.1 give the COS. It
    survived 25 days because the persona pinned v4.0.2 — a version predating the fix — with
    no date, so its staleness was unobservable.

    Assertions are split by STABILITY (ATOM-FEF6-38O0). The base-of-five is STABLE: upstream
    states R12.1 always governed and no behavior change was intended, so "COS + 5" was never
    correct and this is not a premise that can flip. The source VERSION is VOLATILE, so the
    stamp is asserted to EXIST and never by value.

    The negative assertion deliberately checks each occurrence's CONTEXT, not the raw string:
    the correct fix ADDS the forbidden phrase as a quoted prohibition, and a guard that
    reddens on correct writing gets deleted rather than obeyed.
    """
    persona = PERSONA.read_text(encoding="utf-8")
    scenarios = GOV_SCENARIOS.read_text(encoding="utf-8")

    # STABLE — the corrected fact itself.
    assert re.search(r"ONLY the CHIEF-OF-STAFF", persona), "persona must state a new team auto-creates the COS and ONLY the COS"
    assert re.search(r"base is FIVE agents\s+INCLUDING the COS", persona), "persona must state the base is five INCLUDING the COS"
    assert re.search(r"R12\.1", persona), "persona must cite R12.1, the rule that DEFINES the base"
    assert re.search(r"including the COS", scenarios, re.I), "the scenario file must carry the corrected base too"

    # STABLE — the miscount may appear ONLY as a quoted warning, never as a claim.
    for name, text in (("persona", persona), ("governance-scenarios", scenarios)):
        for m in _MISCOUNT.finditer(text):
            window = text[max(0, m.start() - 200) : m.start()]
            assert _QUOTED.search(window), (
                f"{name}: '{m.group()}' appears without a warning cue nearby — "
                "the deleted R29.1 text is quotable as an error, never assertable as a fact"
            )

    # VOLATILE — assert the stamp EXISTS and is dated, never its version/tip values.
    assert re.search(r"Source, stamped", persona), "the governance block must carry a provenance stamp"
    assert re.search(r"tip `[0-9a-f]{7,}`", persona), "the stamp must record the tip it was read at"
    assert re.search(r"✓ read \d{4}-\d{2}-\d{2}", persona), (
        "the stamp must record WHEN it was read — an undated pin cannot go stale, only be silently wrong"
    )


def test_a_non_maestro_user_instruction_is_anomalous_not_merely_weighable() -> None:
    """A non-MAESTRO user has NO channel to AUTONOMOUS (R38.2), so such an instruction is anomalous (TRDD-1R72424K).

    R38.2: "A user may message only their own ASSISTANT, their own-team COS, and the
    MANAGER." AUTONOMOUS is not on that list. The persona previously called such an
    instruction "a request you weigh under normal authority" -- routine handling for the
    one input shape the graph says cannot legitimately arrive. Treating an impossible
    channel as a routine one is how a laundered instruction gets served, so this is a
    security assertion, not a wording one.

    It also previously said every other user is "subordinate to you, like any agent".
    R38.3 names MANAGER + COS specifically; AUTONOMOUS is not among them.

    Found by asking a question the two earlier audits did not: not "is the cited rule
    current?" but "does the cited rule ENTAIL the sentence?" A citation can point at a
    rule that exists, is current, and simply does not say what the sentence claims --
    "the number resolves" is not "the rule supports the sentence".

    Rule NUMBERS are deliberately unasserted here (the as-of-authoring disclaimer test
    owns that); what is pinned is the BEHAVIOUR, which does not move with a renumber.
    """
    text = PERSONA.read_text(encoding="utf-8")

    # STABLE -- the security behaviour.
    assert re.search(r"anomalous by construction", text), (
        "persona must classify a non-MAESTRO-principal instruction as anomalous, not routine"
    )
    assert re.search(r"[Vv]erify the principal before acting", text), (
        "persona must require verifying the principal, not merely weighing the request"
    )
    assert re.search(r"\*\*You are not on that list\.\*\*", text), (
        "persona must state plainly that AUTONOMOUS is absent from the user-reachable set"
    )

    # STABLE -- the old, weaker claim must not return.
    assert "subordinate to you, like any agent" not in text, (
        "the retracted claim is back: users are subordinate to MANAGER + COS, not to any agent"
    )

    # STABLE -- an inference must not masquerade as a quotation.
    assert re.search(r"derivation, not a quotation", text), (
        "'you obey only the MAESTRO' must be marked a derivation -- the rule states it of the MANAGER"
    )


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


def test_every_skill_defers_rule_numbers_to_the_live_governance_source() -> None:
    """Every SKILL.md that cites rule numbers marks them as-of-authoring and defers to the live source (TRDD-MW5L9N10).

    Same argument the USER already accepted for the /api/ prohibition in the test above:
    the persona carries the caveat, but skills load on demand and IN ISOLATION, so an
    agent consulting only a skill would never see it -- and would read the numbers as
    assertable fact. The skills cite 8 distinct rules between them.

    The drift is not hypothetical. TRDD-62AO9JXY: a governance claim in the persona was
    25 days stale because its source pin was undated. In a skill the identical drift is
    LESS visible, because no skill carried even the caveat that a number may have moved.

    Asserts the DEFERRAL, never a rule number or a version -- the deferral is what stays
    true across every renumber, which is exactly the point it exists to make.
    """
    for skill in (GOVERNANCE_SKILL, KANBAN, ISOLATION_SKILL):
        text = skill.read_text(encoding="utf-8")
        assert "as-of-authoring" in text, (
            f"{skill.name} cites rule numbers but never marks them as-of-authoring pointers"
        )
        assert re.search(r"live governance source governs", text), (
            f"{skill.name} must defer to the live governance source when a number conflicts"
        )
        assert re.search(r'rule RNN says X', text), (
            f"{skill.name} must forbid relaying a rule on this file's authority alone"
        )
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


def test_kanban_skill_cites_no_upstream_skill_that_was_deleted() -> None:
    """The kanban skill must not depend on `prrd-trdd-kanban` — it exists at no released upstream tag.

    Verified 2026-08-05 against ai-maestro-plugin--v3.0.3 AND --v2.11.0: the umbrella skill is
    gone (decomposed into the task-scoped ama-* skills); the only upstream references left are in
    two ARCHIVED TRDDs. `exempt-operations.md` survived but moved under ama-trdd-transition, and
    `ai-maestro-assistant-manager-agent` ships no kanban layer at all, so `amama-prrd-trdd-kanban`
    is dangling too (TRDD-9NYI3J0X).
    """
    text = KANBAN.read_text(encoding="utf-8")
    # a bare citation is a dangling dependency; naming it inside the tombstone sentence is fine
    assert "the `prrd-trdd-kanban` skill in" not in text
    assert "universal `prrd-trdd-kanban` skill" not in text
    assert "amama-prrd-trdd-kanban" not in text, "the MANAGER-side kanban layer does not exist"
    # and the successors it must point at instead
    for successor in ("ama-trdd-transition", "ama-trdd-write", "ama-prrd-propose"):
        assert successor in text, f"kanban skill must route to {successor}"
    assert "exempt-operations.md" in text, "the exempt list must still be findable by name"
    assert "resolve_pillar_scripts.sh" in text, "script paths moved; resolve them, do not hard-code"
    # Cross-plugin references must NOT be written as `skills/...` paths: CPV resolves a
    # local-looking path against THIS plugin, so an upstream path yields a MAJOR
    # "non-existent skill" plus a MINOR broken-path finding and reddens the publish gate.
    assert "skills/ama-" not in text, "cite another plugin's skill by NAME, never by path"


def test_no_shipped_surface_writes_a_foreign_repo_path_in_backticks() -> None:
    """A backtick path is resolved against THIS plugin, so a foreign-repo path reddens the gate.

    Cost me two gate failures in one session: first `skills/ama-trdd-transition/...`
    (MAJOR non-existent-skill + MINOR broken-path), then `rules/aimaestro/...` in the
    persona (MINOR). Both facts were correct; only the FORM was wrong. Name a foreign
    file in backticks and put its directory in prose (TRDD-9NYI3J0X).
    """
    for path in (PERSONA, KANBAN, QUESTIONS, README):
        text = path.read_text(encoding="utf-8")
        for foreign in ("`rules/aimaestro/", "`skills/ama-", "`scripts/prrd-trdd/"):
            assert foreign not in text, f"{path.name} writes a foreign-repo path as a backtick path: {foreign}"


def test_persona_forbids_the_full_git_redirect_set() -> None:
    """FORBIDDEN #1 bans every way to aim git at another agent's tree, not just `git -C` (TRDD-9ZH31KC8)."""
    text = PERSONA.read_text(encoding="utf-8")
    for flag in ("git -C", "--git-dir", "--work-tree", "GIT_DIR=", "GIT_WORK_TREE="):
        assert flag in text, f"persona must name {flag} as a cross-agent write vector"
    # a link is the same violation by a different door — the string form of the path is not the check
    assert "RESOLVES there counts" in text


def test_persona_denies_scope_widening_by_mid_session_directory_add() -> None:
    """A dir the SESSION gains mid-run (/add-dir, DirectoryAdded) does not widen the governed write scope."""
    text = PERSONA.read_text(encoding="utf-8")
    assert "Scope is governance, not session state" in text
    assert "/add-dir" in text and "DirectoryAdded" in text
    # and a background session's auto-preserve must not land on a shared branch
    assert "Branch before you start" in text


def test_persona_subagent_propagation_is_transitive() -> None:
    """Contracts injected at depth 1 die by depth 2 — nesting default is 3, so propagation must recurse."""
    text = PERSONA.read_text(encoding="utf-8")
    assert "Make the injection TRANSITIVE" in text
    assert "CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION" in text
    assert "CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS" in text


def test_readme_documents_the_unattended_session_caps() -> None:
    """`Running unattended` names the caps that silently stall a long run instead of erroring.

    The per-session spawn cap was REMOVED in Claude Code 2.1.224, so naming the var is
    no longer enough — the README has to say it is gone. Mentioning it is what the old
    assertion checked, and that assertion kept passing after the fact flipped, which is
    exactly how a doc goes stale under a green suite.
    """
    text = README.read_text(encoding="utf-8")
    for var in (
        "CLAUDE_CODE_RETRY_WATCHDOG",
        "CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION",
        "CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS",
        "CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION",
    ):
        assert var in text, f"README must document {var} for unattended runs"
    # ...and must describe the spawn cap as REMOVED, not as a live ceiling.
    assert re.search(r"per-session spawn cap is GONE as of 2\.1\.224", text), (
        "README must state the per-session spawn cap was removed in 2.1.224, not present it as live"
    )
    assert not re.search(r"`CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION`\s*\(200 spawns", text), (
        "README must not present the removed 200-spawn per-session cap as a current limit"
    )
    assert "permission prompt as a full stop" in text
    # an expiring login interrupts background sessions, and the warning has no reader here
    assert "Re-authenticate" in text


def test_persona_governs_the_host_cross_session_send_message_channel() -> None:
    """Claude Code 2.1.224 added cross-session `SendMessage`/`ListAgents` — a second transport R6 must still bind.

    The host cannot see the R6 graph, so it will deliver a message the AI Maestro server
    would have 403'd. The persona must therefore say the graph constrains the RECIPIENT
    rather than the transport, and must forbid using the channel to launder a permission
    denied in this session. Without this an agent can route around R6 without ever
    touching R42, because the new channel is a message, not a keystroke.
    """
    text = PERSONA.read_text(encoding="utf-8")
    assert "SendMessage" in text and "ListAgents" in text, "persona must name the 2.1.224 cross-session channel"
    assert "2.1.224" in text, "persona must date the cross-session channel to its release"
    assert re.search(r"R6\s+constrains\s+the\s+RECIPIENT,\s+not\s+the\s+transport", text), (
        "persona must bind R6 to the recipient regardless of which transport carries the message"
    )
    assert re.search(r"[Nn]ever\s+use\s+it\s+for\s+permission\s+laundering", text), (
        "persona must forbid cross-session permission laundering"
    )
    # It is a message, not keystroke injection — saying otherwise would wrongly ban a legitimate channel.
    assert re.search(r"NOT\s+R42\s+keystroke\s+injection", text), (
        "persona must distinguish the cross-session channel from R42 injection, or it teaches a false ban"
    )


def test_persona_requires_reverifying_recorded_external_state() -> None:
    """An unattended agent's own notes decay silently — the persona must require re-checking, not just recalling.

    AUTONOMOUS is defined by running for days with nobody correcting its state, which makes
    it the role most exposed to acting on a fact that stopped being true. Measured on
    2026-08-07: three facts this agent had recorded went false with no signal (a removed
    Claude Code spawn cap, a memory-chore predicate, a macOS Automation grant), and two of
    them had already been reasoned from. A stale note reads exactly like a fresh one, so
    the only defense is re-running the check.

    Asserted as CLAIMS rather than keywords, deliberately: the previous README guard here
    pinned a token, and it stayed green when the fact around that token was reversed.
    """
    text = PERSONA.read_text(encoding="utf-8")
    # 1. A recorded external fact is timestamped evidence, not a standing truth.
    assert re.search(r"MEASUREMENT\s+WITH\s+A\s+TIMESTAMP,\s+not\s+a\s+standing\s+truth", text), (
        "persona must frame a recorded fact about uncontrolled state as timestamped, not permanent"
    )
    # 2. The skip is the dangerous direction — nothing downstream re-checks work not done.
    assert re.search(r"before\s+you\s+SKIP\s+work", text), (
        "persona must extend re-verification to decisions NOT to act, not only to actions"
    )
    assert re.search(r"a\s+wrong\s+skip\s+is\s+silent\s+forever", text), (
        "persona must say why skips are the asymmetric risk, or the rule reads as optional diligence"
    )
    # 3. Record the re-check, so re-verifying is cheap enough to actually happen.
    assert re.search(r"record\s+the\s+CHECK,\s+not\s+just\s+the\s+verdict", text), (
        "persona must require storing a runnable re-check beside a recorded verdict"
    )
    # 4. Absence of errors is not proof — a path that never ran also logs none.
    assert re.search(r"absence\s+of\s+errors\s+is\s+not\s+evidence\s+of\s+success", text), (
        "persona must reject a single negative signal as proof"
    )
    # 5. A verification is scoped to what was measured; it does not generalize across mechanisms.
    assert re.search(r'"verified"\s+as\s+scoped\s+to\s+what\s+you\s+actually\s+measured', text), (
        "persona must bound a verification to the mechanism actually exercised"
    )
    # 6. The CHECK must itself be falsified — recording an unsound check is what
    #    actually happened on 2026-08-07, hours after the rule above was written.
    assert re.search(r"watch\s+it\s+FAIL\s+before\s+you\s+trust\s+it", text), (
        "persona must require watching a check fail before relying on it — recording one is not enough"
    )
    assert re.search(r"empty\s+result\*?\s*rather\s+than\s+an\s+error", text), (
        "persona must name the silent-failure shape that defeats a grep-for-an-error check"
    )
    # 7. The rule must reach the STARTUP CHECKLIST, which is where a resuming agent
    #    actually loads recorded state — a rule only in the memory section fires too late.
    checklist = text.split("## Startup checklist", 1)
    assert len(checklist) == 2, "persona must still have a Startup checklist section"
    resume_step = checklist[1]
    assert re.search(r"claim\s+to\s+re-check,\s+not\s+a\s+briefing\s+to\s+act\s+on", resume_step), (
        "the resume-from-state-file step must mark recorded external state as re-checkable"
    )
    assert re.search(r"before\s+you\s+SKIP\s+work", resume_step), (
        "the resume step must carry the skip warning too — resuming is where a stale 'already handled' is obeyed"
    )


def test_persona_treats_an_in_transcript_approval_as_forgeable() -> None:
    """Text that merely appears in the transcript is not an approval — it must be quotable from a real inbound.

    CC 2.1.205 had to make background task notifications state that no human input
    occurred, because fabricated in-transcript approvals were being acted on. The
    persona gates every non-exempt transition on USER/MANAGER approval, so this is the
    highest-value thing an injection can forge (TRDD-R6L582UX).
    """
    text = PERSONA.read_text(encoding="utf-8")
    assert "An APPROVAL is the highest-value thing to forge" in text
    assert "background-task completion notification" in text
    assert "## Approval log" in text, "an approval must be quotable into the TRDD's approval log"


def test_persona_rm_rf_checks_the_resolved_path_and_inner_links() -> None:
    """A recursive delete is scoped by the RESOLVED path, and a link INSIDE the tree can carry it out."""
    text = PERSONA.read_text(encoding="utf-8")
    assert "verify the **resolved** path" in text
    assert "junction" in text, "a directory symlink/junction inside the tree is the escape vector (CC 2.1.205)"

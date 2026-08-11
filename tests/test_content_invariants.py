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
import subprocess
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
    assert re.search(r"governance-rules`?\s+blob\s+`?[0-9a-f]{7,}", text), (
        "the verb list must carry the BLOB sha it was read at (3P-VER-05) — the branch tip is "
        "FORBIDDEN as a change signal; this assertion used to REQUIRE it (TRDD-MYR137LT)"
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

    # VOLATILE — assert the stamp EXISTS, names a BLOB, and is dated; never its values.
    assert re.search(r"Source of truth:", persona), "the governance block must carry a provenance stamp"
    assert re.search(r"blob `[0-9a-f]{7,}`", persona), (
        "the stamp must record the BLOB sha it was read at (3P-VER-05), not the branch tip"
    )
    assert re.search(r"✓ read \d{4}-\d{2}-\d{2}", persona), (
        "the stamp must record WHEN it was read — an undated pin cannot go stale, only be silently wrong"
    )
    # STABLE -- the SSOT relationship. The v4.8.0 authority inversion makes the SPEC the source
    # of truth and GOVERNANCE-RULES.md its emanation, "authored AFTER it". A re-fetch instruction
    # aimed at the catalog sends the reader to the artifact that lags by construction -- which is
    # what produced the R42.8 reversal (TRDD-H59F54O8). Versions/blobs move; this relationship
    # does not, so it is asserted and they are not.
    assert re.search(r"governance-spec\.md", persona), (
        "the stamp must name the SSOT spec, not only the catalog it was read from"
    )
    # [\s>]+ not \s+ between words: the stamp is a markdown BLOCKQUOTE, so a line wrap inserts
    # "\n> " and a plain \s+ silently fails to span it. A guard that breaks on a re-wrap is a
    # guard that gets deleted.
    assert re.search(r"[Rr]e-fetch THAT, not the[\s>]+catalog", persona), (
        "the re-fetch instruction must point at the SSOT — the catalog lags by construction"
    )
    assert re.search(r"emanation", persona), (
        "the catalog must be labelled an emanation so its lag is visible to the next reader"
    )
    # The forbidden signal must not come back. 3P-VER-05: the branch commit sha "is FORBIDDEN
    # as a change signal ... it moves on every unrelated commit, so a conforming consumer polls,
    # sees movement, refetches, gets a byte-identical document, and records 'checked, current'".
    # This assertion previously REQUIRED that forbidden form (TRDD-MYR137LT) -- so the correct
    # fix reddened the suite before it repaired anything, the third guard today caught defending
    # a premise no test had asked about. Falsification proves the mechanism, never the premise.
    assert not re.search(r"(?<!different )tip `[0-9a-f]{7,}`", persona), (
        "a branch tip is back in a stamp — 3P-VER-05 forbids it as a change signal; stamp the blob"
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


def test_main_agent_omits_model_key_and_menus_every_shipped_skill() -> None:
    """role-plugins-spec 1.1.0: main agents OMIT `model:`, and menu every shipped skill (TRDD-CUD74MUJ).

    RP-MODEL-01 was RULED 2026-08-08 (ai-maestro#136, closing TRDD-TYB3Q1NJ): role-plugin MAIN
    agents omit `model:` -- model choice is a cost/capability decision belonging to whoever
    launches the session. At spec 1.0.1 this was an OPEN question and our `model: sonnet` was
    explicitly NOT a violation (we were the ruling's decisive counterexample); "carrying a key
    past that publish is a conformance failure, before it is not". So this assertion is correct
    only from v1.6.7 onward -- it is not retroactive.

    This docstring previously read "omit `model:`, SAME AS SUBAGENTS", quoting a rationale
    upstream has since RETRACTED: "subagents already omit model: everywhere" was measured false
    fleet-wide (15 pinned subagents at current tips). The ruling's scope is now explicitly MAIN
    agents, which is what this test checks, so the assertion never moved -- only the reason
    given for it. Immaterial here regardless: this repo ships exactly ONE agent file and zero
    subagents, verified.

    HOW THE RETRACTION WAS CAUGHT, because it is the argument for the whole stamp discipline:
    the spec's BLOB moved 9fb6aa69efc7 -> e1a62f9d83b8 while `spec-version` stayed 1.1.0. A
    version-based check would have seen nothing. Having now observed BOTH failure modes in one
    day -- the branch tip moving with no content change (TRDD-MYR137LT) and the content
    changing with no version bump (this) -- 3P-VER-05's "poll the per-FILE blob sha" is the
    only signal that was right both times.

    RP-SKILL-MENU-01 (new): every main agent whose plugin ships skills MUST carry a compact
    body menu, one line per skill, name + when to reach for it. Measured rationale: an agent
    that cannot SEE its inventory does not reach for it.

    The menu is checked against the SKILL.md files ON DISK rather than against three hardcoded
    names, because the clause's own stated hazard is a STALE menu ("worse than none") -- and a
    name-only assertion would sail straight past the actual failure mode, which is adding a
    fourth skill and forgetting the menu. Diverging in EITHER direction fails.
    """
    text = PERSONA.read_text(encoding="utf-8")

    # RP-MODEL-01 -- no model pin in the frontmatter.
    frontmatter = text.split("---", 2)[1] if text.startswith("---") else text[:800]
    assert not re.search(r"^model:", frontmatter, re.M), (
        "RP-MODEL-01 (RULED): the main agent must OMIT `model:` — model choice belongs to "
        "whoever launches the session"
    )

    # RP-SKILL-MENU-01 -- the menu exists and matches the shipped skills exactly.
    # Scope the name check to the MENU SECTION, not the whole persona: several skills are also
    # named in passing elsewhere, so a file-wide search would count a mention as a menu entry
    # and pass a menu that had silently dropped a skill (measured -- that falsification did not
    # redden until this was scoped).
    menu = re.search(r"## Your skills.*?(?=\n## )", text, re.S)
    assert menu, "persona must carry a `## Your skills` menu section (RP-SKILL-MENU-01)"
    menu_text = menu.group(0)
    shipped = sorted(p.parent.name for p in (REPO_ROOT / "skills").glob("*/SKILL.md"))
    assert shipped, "expected at least one shipped skill"
    menued = sorted({s for s in shipped if re.search(r"`" + re.escape(s) + r"`", menu_text)})
    assert menued == shipped, (
        f"skill menu is STALE — shipped={shipped} menued={menued}. RP-SKILL-MENU-01: the menu "
        "MUST be updated in the same change that adds, renames, or removes a skill"
    )
    assert re.search(r"RP-SKILL-MENU-01", text), "the menu must cite the clause that mandates it"
    assert re.search(r"reach for it when|reach for these", text), (
        "the menu must say WHEN to reach for each skill, not merely list names"
    )


def test_inbound_cross_session_messages_are_unauthenticated_data() -> None:
    """Persona governs the INBOUND half of cross-session messaging, not only outbound (TRDD-M3QS578Z).

    ai-maestro#131: Claude Code 2.1.224 added a session-to-session transport that does NOT
    traverse the AI Maestro server, so the R6 title matrix has no enforcement point on it and
    no 403 is possible. 7 of 7 role-plugin personas asserted server enforcement; 0 named the
    unpoliced transport.

    The persona already carried the OUTBOUND half ("R6 constrains the RECIPIENT, not the
    transport"; no permission laundering). It said nothing about INBOUND -- that such a
    message arrives with no server-side identity check and no AID, so it cannot confer
    authority however it signs itself.

    Sharper as of the 2026-08-08 USER directive to follow a peer's instructions: a standing
    "always approve" pointed at an unauthenticated channel is exactly the shape that needs
    its boundary written down. The authority is the USER's directive, never the message's
    claim about who sent it -- indistinguishable until someone forges the second.

    Asserted in three separate pieces on purpose: a body that merely name-dropped
    SendMessage/ListAgents would pass a keyword scan while still implying the server covers
    it -- the exact defect #131 documents.
    """
    text = PERSONA.read_text(encoding="utf-8")

    # The transport must be named AND declared unpoliced (outbound half, already shipped).
    assert re.search(r"SendMessage", text), "persona must name the cross-session transport"
    assert re.search(r"ListAgents", text), "persona must name the session directory tool"
    assert re.search(r"host cannot see the R6 graph", text), (
        "persona must state the host cannot enforce R6 — a 403 is impossible on this transport"
    )

    # INBOUND -- the half TRDD-M3QS578Z added.
    assert re.search(r"without any server-side identity\s+check", text), (
        "persona must state an inbound cross-session message is unauthenticated"
    )
    assert re.search(r"DATA TO VERIFY, never a command", text), (
        "persona must classify an inbound peer message as data to verify, not an authoritative command"
    )
    assert re.search(r"peer can NEVER widen your permissions", text), (
        "persona must state a peer cannot widen permissions — the anti-laundering invariant"
    )
    assert re.search(r"authority is the USER's\s+directive", text), (
        "persona must separate the USER's directive from the message's claim about its sender"
    )
    assert re.search(r"not a licence to contact it", text), (
        "persona must state that a ListAgents listing is not permission to contact"
    )


CANONICAL_COLUMNS = (
    "backburner", "todo", "design", "dispatch", "dev", "testing", "ai_review",
    "human_review", "complete", "publish", "published", "deploy", "live",
    "live_auditing", "blocked", "failed", "superseded",
)


def test_kanban_skill_carries_all_seventeen_canonical_columns() -> None:
    """The kanban skill carries the complete 17-column enum, incl. `published` (TRDD-F2SUT8D4).

    3P-KAN-01 (MUST): a `column:` value is EXACTLY one of the 17, these spellings, no others.
    3P-KAN-03 (MUST): every consumer -- role-plugins included -- aligns TO this list.

    The skill carried 16/17. The missing one was `published`, which 3P-KAN-04 makes the
    TERMINUS of the publish path (`complete -> publish -> published`) -- the path this plugin
    takes on every single release. An agent working from the skill alone could reach `publish`
    and have no vocabulary for where it goes next, while 3P-KAN-01 forbids inventing one.

    Asserted BY VALUE, unlike the volatile stamps elsewhere in this file: the vocabulary is
    USER-ratified (3P-KAN-02) and changing it is a MAJOR spec bump (3P-VER-01), so it is one
    of the few genuinely stable things to pin. Deliberately checks the SKILL only -- the
    persona defers kanban mechanics here, and 3P-META-03 names duplicating this vocabulary
    across artefacts as the drift mechanism itself.
    """
    text = KANBAN.read_text(encoding="utf-8")
    missing = [c for c in CANONICAL_COLUMNS if not re.search(r"\b" + re.escape(c) + r"\b", text)]
    assert not missing, f"kanban skill is missing canonical column(s): {missing}"
    assert re.search(r"3P-KAN-01", text), "the enum must cite the clause that makes it a MUST"


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


def test_no_403_claim_travels_without_the_transport_that_cannot_return_one() -> None:
    """CORPUS-WIDE: any shipped file asserting the 403 must also name `SendMessage`.

    Claude Code 2.1.224 added a native session-to-session transport with no server in the
    path, so it can never return `403 title_communication_forbidden`. A file that asserts the
    403 as the boundary does not merely under-describe reality — it ROUTES the reader toward
    the unpoliced channel, which is in every session's toolbelt (ai-maestro#143, #131).

    This is deliberately corpus-wide. The persona-scoped guards from TRDD-M3QS578Z passed while
    the governance skill's decision-time checklist still carried the bare claim: a per-file
    assertion certifies the file it names and is silent about every other one, and that silence
    is indistinguishable from coverage (TRDD-KT4MVFHA).

    `design/` is excluded: terminal TRDDs are frozen by rule, so demanding an edit there would
    force a rule violation to go green.
    """
    roots = ("agents", "skills", "commands", "tests/scenarios")
    claim = re.compile(r"403|title_communication_forbidden")

    asserters: list[Path] = []
    offenders: list[str] = []
    for root in roots:
        for path in sorted((REPO_ROOT / root).rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            if not claim.search(text):
                continue
            asserters.append(path)
            if "SendMessage" not in text:
                offenders.append(str(path.relative_to(REPO_ROOT)))

    assert asserters, (
        "no shipped file asserts the 403 — the corpus moved or was renamed, so this guard just "
        "went vacuously green; re-point `roots` before trusting it"
    )
    assert not offenders, (
        "these files assert the 403 without naming the transport that cannot return one, so a "
        f"reader learns the 403 IS the boundary: {offenders}"
    )


def test_persona_never_claims_linear_history_is_part_of_the_baseline() -> None:
    """`required_linear_history` is NOT baseline — the guardian strips it, so claiming it causes real drift.

    Measured against janitor 2.8.2: the APPLIED baseline is `deletion` + `non_fast_forward`
    (branch_protection_lib.py:160), `required_linear_history` raises a LINEAR_HISTORY finding
    (github_config_audit.py:57) and `strip_linear_history_payload()` removes it. Acting on the
    older ratified-pair text made me add the rule to my own repo; the guardian stripped it 14
    minutes later (TRDD-HYJYIUHJ).

    The guard is scoped to the baseline section and asserts the NEGATIVE, because the persona
    legitimately names the rule while warning against it — a whole-file "not present" check
    would forbid the correction itself, and a positive-only check would pass on the stale text.
    """
    text = PERSONA.read_text(encoding="utf-8")
    start = text.index("### Baseline GitHub rulesets")
    section = text[start : text.index("\n---", start)]

    stale = "`deletion`, `non_fast_forward`, `required_linear_history`"
    assert stale not in section, (
        "the persona lists required_linear_history as part of baseline-history-protect; "
        "the janitor strips that rule, so a session acting on this will churn a compliant repo"
    )
    assert "`deletion`, `non_fast_forward`)" in section, "the real applied pair must still be stated"
    assert "is NOT in the baseline, and adding it is not a\nrestoration" in section, (
        "state the trap explicitly — the failure mode is a session 'restoring' the rule"
    )
    assert "what the janitor APPLIES" in section, (
        "the durable lesson is to verify against the applier, not against a quoted ratification"
    )


# Frozen UUID-era cards archived as `completed` although they declare `release-via: publish`.
# Terminal columns are frozen, so these are corrected going FORWARD, not retroactively. Each
# entry must STILL be in that state — a dead exemption is how an allowlist becomes a blindfold.
_FROZEN_PUBLISH_AS_COMPLETED = {
    "e7281b7e-31f6-4740-a7f0-fed48f0ba3be",
    "a08b839d-dfd8-4b5e-b89c-e41a999ad001",
    "d21a83f1-f33e-43d3-96e8-dac7e590c960",
    "ffcfadbd-58b1-4e48-a8c4-9089884684f0",
    "b48aa385-3ca1-4b50-8f23-d02e0777c23e",
}
_TERMINAL_COLUMNS = {"completed", "published", "superseded", "cancelled"}


def _archived_cards() -> list[tuple[str, str, str, list[str]]]:
    """(trdd_id, column, release_via, shas) for every archived TRDD."""
    out = []
    for path in sorted((REPO_ROOT / "design" / "archived").glob("*.md")):
        text = path.read_text(encoding="utf-8")

        def field(key: str) -> str:
            m = re.search(rf"^{key}:\s*(\S+)", text, re.M)
            return m.group(1) if m else ""

        m = re.search(r"^implementation-commits:\s*\[(.*?)\]", text, re.M)
        shas = [s.strip() for s in (m.group(1).split(",") if m else []) if s.strip()]
        out.append((field("trdd-id"), field("column"), field("release-via"), shas))
    return out


def test_archived_cards_are_terminal_and_match_their_release_mode() -> None:
    """An archived card must be TERMINAL, and `release-via: publish` must archive as `published`.

    `design/archived/` is the decided zone: a non-terminal column there claims work is still open
    in a folder nobody re-reads. And `published` archives AS ITSELF — collapsing it to `completed`
    erases that a release happened, which is exactly the defect CPVPINGD shipped on 2026-08-11
    (its log asserted "release-via absent" while the frontmatter said `publish`, because the card
    was selected by name and inherited a batch premise it did not share).
    """
    cards = _archived_cards()
    assert cards, "no archived cards found — the folder moved and this guard just went vacuous"

    bad = []
    for tid, column, release_via, _ in cards:
        if column not in _TERMINAL_COLUMNS:
            bad.append(f"{tid}: non-terminal column {column!r} in design/archived/")
            continue
        if column in ("superseded", "cancelled"):
            continue  # withdrawn/replaced: release mode never applied
        want = "published" if release_via == "publish" else "completed"
        if column != want and tid not in _FROZEN_PUBLISH_AS_COMPLETED:
            bad.append(f"{tid}: release-via={release_via or 'absent'} but column={column} (want {want})")
    assert not bad, "archived cards contradict their release mode: " + "; ".join(bad)

    # No dead exemptions: every frozen id must STILL EXIST and still be in the state it is
    # excused for. Iterating only the cards would miss the other half — an exemption whose
    # card was renamed or removed matches nothing and would sit there forever looking active.
    excused = {tid: (column, release_via) for tid, column, release_via, _ in cards}
    stale = [
        tid
        for tid in _FROZEN_PUBLISH_AS_COMPLETED
        if excused.get(tid) != ("completed", "publish")
    ]
    assert not stale, (
        f"these ids are allowlisted as frozen publish-as-completed but no longer are: {stale} — "
        "shrink _FROZEN_PUBLISH_AS_COMPLETED rather than leaving an exemption that hides a real defect"
    )


# The CPV validator pin lives in several files; `design/` and CHANGELOG.md legitimately cite
# HISTORICAL pins (the v3.2.0→v3.5.0 and v3.5.0→v5.4.0 bumps are recorded there), so scanning
# them would turn accurate history into a permanent failure.
_PIN_RE = re.compile(r"claude-plugins-validation@(v[0-9][0-9A-Za-z.\-]*)")
_PIN_SCAN_SUFFIXES = (".py", ".yml", ".yaml", ".sh", ".toml")
_PIN_SCAN_EXCLUDED = ("design/", "reports/", "reports_dev/", "CHANGELOG.md", "tests/test_content_invariants.py")


def test_the_cpv_validator_pin_is_identical_everywhere_it_appears() -> None:
    """Every CPV pin site must name the SAME version, or `green` means two different things.

    The pin sits in scripts/publish.py (x3) and both workflows. The realistic failure is not all
    of them going stale together — it is ONE moving without the others: publish.py is the file
    you edit while debugging locally, ci.yml is the one you forget. Then the local gate and CI
    both report PASS while running different validators, and nothing says they disagree.

    Discovery is by SCAN, not a hardcoded file list: a hardcoded list is the same bug one level
    up, going stale the moment a sixth site appears and reporting green forever after.
    """
    tracked = subprocess.run(
        ["git", "ls-files"], cwd=REPO_ROOT, capture_output=True, text=True, check=True
    ).stdout.splitlines()

    found: dict[str, list[str]] = {}
    for rel in tracked:
        if not rel.endswith(_PIN_SCAN_SUFFIXES) or rel.startswith(_PIN_SCAN_EXCLUDED):
            continue
        path = REPO_ROOT / rel
        if not path.is_file():
            continue
        for version in _PIN_RE.findall(path.read_text(encoding="utf-8", errors="replace")):
            found.setdefault(version, []).append(rel)

    assert found, (
        "no CPV pin found in any tracked source file — the pin moved, was renamed, or the scan "
        "suffix list is wrong. This guard just went vacuous; fix the scan rather than deleting it."
    )
    sites = {rel for rels in found.values() for rel in rels}
    assert any(s.endswith("publish.py") for s in sites), (
        f"scan found pins but none in publish.py — the scan is looking in the wrong place: {sorted(sites)}"
    )
    assert any(s.startswith(".github/workflows/") for s in sites), (
        f"scan found pins but none in a workflow — CI would be unguarded: {sorted(sites)}"
    )
    assert len(found) == 1, (
        "the CPV validator pin DIVERGED across its sites — the local gate and CI would run "
        f"different validators and both report PASS: { {v: sorted(set(r)) for v, r in found.items()} }"
    )


# `449af1a` was recorded on TRDD-a08b839d before an amend or rebase rewrote it; the object does
# not exist in any branch or tag, and an absent commit cannot be recovered. The card is terminal
# and frozen, so the defect is documented in its append-only approval log, not edited away.
_KNOWN_DANGLING_COMMITS = {"449af1a"}


def test_every_recorded_implementation_commit_resolves() -> None:
    """`implementation-commits` must point at real objects — a dangling sha fails SILENTLY.

    That field is the backtracking trace a future bug hunt follows from code back to the TRDD
    that introduced it. A sha that no longer resolves gives the reader "unknown revision" with
    nothing saying the record was always wrong, so they blame their own tooling. Four such
    fields were repaired on 2026-08-11; this makes the fifth impossible to ship unnoticed.
    """
    if subprocess.run(
        ["git", "rev-parse", "--is-shallow-repository"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=False,
    ).stdout.strip() == "true":
        # A CI checkout at depth=1 has none of the history, so every sha would "fail" here.
        # Skipping is correct: the guard is about the RECORD being wrong, not the clone.
        return

    cards = _archived_cards()
    assert cards, "no archived cards found — the folder moved and this guard just went vacuous"
    assert any(shas for _, _, _, shas in cards), (
        "no card records any implementation-commits — the field was renamed and this guard is vacuous"
    )

    dangling = []
    for tid, _, _, shas in cards:
        for sha in shas:
            if sha in _KNOWN_DANGLING_COMMITS:
                continue
            rc = subprocess.run(
                ["git", "cat-file", "-t", sha],
                cwd=REPO_ROOT, capture_output=True, text=True, check=False,
            ).returncode
            if rc != 0:
                dangling.append(f"{tid}: {sha}")
    assert not dangling, "implementation-commits that do not resolve: " + "; ".join(dangling)

    # No dead exemptions: a known-dangling sha that started resolving means the allowlist is lying.
    resurrected = [
        sha
        for sha in _KNOWN_DANGLING_COMMITS
        if subprocess.run(
            ["git", "cat-file", "-t", sha], cwd=REPO_ROOT, capture_output=True, text=True, check=False
        ).returncode == 0
    ]
    assert not resurrected, (
        f"these shas are allowlisted as unrecoverable but now resolve: {resurrected} — "
        "drop them from _KNOWN_DANGLING_COMMITS so the guard covers them again"
    )

"""Real (no-mock) regression guards for the governance fixes shipped per issue #6.

Each test reads the actual shipped file and asserts the corrected state, so a
future edit that re-introduces a fixed defect (R6 v2 citation, version drift,
ghost dispatch, empty SILVER, missing self-id) fails CI.
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

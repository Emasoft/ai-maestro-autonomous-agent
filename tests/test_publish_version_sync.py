"""Real (no-mock) tests for the publish.py version-sync logic added per issue #6 (M11).

These exercise the actual functions against a temporary plugin layout on disk — no
mocks — proving the README/persona updaters are anchored (never touch decoy version
tokens) and that check_version_consistency() now detects README/persona drift.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# publish.py is a bundled script (not an installed module) — load it by path so
# the test works without a package install and without a static-import diagnostic.
# Register it in sys.modules BEFORE exec so its @dataclass can resolve cls.__module__.
_spec = importlib.util.spec_from_file_location("publish", REPO_ROOT / "scripts" / "publish.py")
assert _spec is not None and _spec.loader is not None
publish = importlib.util.module_from_spec(_spec)
sys.modules["publish"] = publish
_spec.loader.exec_module(publish)


def _make_plugin(root: Path, version: str) -> None:
    """Write a minimal plugin layout (plugin.json + README + persona) at `version`."""
    (root / ".claude-plugin").mkdir(parents=True)
    (root / ".claude-plugin" / "plugin.json").write_text(
        '{\n  "name": "demo",\n  "version": "%s"\n}\n' % version, encoding="utf-8"
    )
    (root / "README.md").write_text(
        f"# Demo\n\n**Version**: {version}\n\nSee the v2.0 release notes for history.\n", encoding="utf-8"
    )
    agents = root / "agents"
    agents.mkdir()
    (agents / "demo-main-agent.md").write_text(
        f"---\nname: demo\n---\n\n**Plugin**: demo v{version} | please expedite the v2.0 release.\n",
        encoding="utf-8",
    )


def test_update_readme_version_is_anchored(tmp_path: Path) -> None:
    """update_readme_version bumps the **Version** line only — the 'v2.0 release' decoy is untouched."""
    _make_plugin(tmp_path, "1.0.0")
    ok, msg = publish.update_readme_version(tmp_path, "3.4.5")
    assert ok, msg
    text = (tmp_path / "README.md").read_text(encoding="utf-8")
    assert "**Version**: 3.4.5" in text
    assert "v2.0 release" in text  # decoy preserved


def test_update_persona_versions_is_anchored(tmp_path: Path) -> None:
    """update_persona_versions bumps only the **Plugin**: <name> vX.Y.Z token, not 'v2.0 release'."""
    _make_plugin(tmp_path, "1.0.0")
    results = publish.update_persona_versions(tmp_path, "3.4.5")
    assert results and all(ok for ok, _ in results), results
    text = (tmp_path / "agents" / "demo-main-agent.md").read_text(encoding="utf-8")
    assert "**Plugin**: demo v3.4.5" in text
    assert "expedite the v2.0 release" in text  # decoy preserved


def test_consistency_passes_when_all_sources_agree(tmp_path: Path) -> None:
    """check_version_consistency returns ok when plugin.json/README/persona all match."""
    _make_plugin(tmp_path, "2.2.2")
    ok, msg = publish.check_version_consistency(tmp_path)
    assert ok, msg
    assert "2.2.2" in msg


def test_consistency_detects_readme_drift(tmp_path: Path) -> None:
    """A README **Version** that disagrees with plugin.json is reported as a mismatch."""
    _make_plugin(tmp_path, "2.2.2")
    readme = tmp_path / "README.md"
    readme.write_text(readme.read_text(encoding="utf-8").replace("**Version**: 2.2.2", "**Version**: 9.9.9"), encoding="utf-8")
    ok, msg = publish.check_version_consistency(tmp_path)
    assert not ok
    assert "README.md" in msg and "9.9.9" in msg


def test_consistency_detects_persona_drift(tmp_path: Path) -> None:
    """A persona **Plugin** version that disagrees with plugin.json is reported as a mismatch."""
    _make_plugin(tmp_path, "2.2.2")
    persona = tmp_path / "agents" / "demo-main-agent.md"
    persona.write_text(persona.read_text(encoding="utf-8").replace("demo v2.2.2", "demo v8.8.8"), encoding="utf-8")
    ok, msg = publish.check_version_consistency(tmp_path)
    assert not ok
    assert "8.8.8" in msg


def test_do_bump_roundtrip_keeps_all_four_sources_consistent(tmp_path: Path) -> None:
    """do_bump updates plugin.json + README + persona together, so consistency holds at the new version."""
    _make_plugin(tmp_path, "1.0.0")
    # pyproject is optional; omit it — the four-way check still covers plugin.json/README/persona.
    assert publish.do_bump(tmp_path, "1.1.0") is True
    ok, msg = publish.check_version_consistency(tmp_path)
    assert ok, msg
    assert "1.1.0" in msg

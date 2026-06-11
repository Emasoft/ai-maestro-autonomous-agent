"""Smoke tests: every bundled script compiles and the pipeline scripts import cleanly.

The validate_*.py family + cpv_validation_common.py are bundled CPV infrastructure,
copied verbatim from claude-plugins-validation, which owns their deep test suite
upstream (see ~/.claude/rules/plugin-tests-are-the-plugins-job.md). This plugin's
obligation is to prove the bundling did not break them: every script must parse and
byte-compile, and the scripts this plugin actually drives (publish.py + the two new
helpers) must import. Deep behavioral coverage stays upstream by design.
"""

from __future__ import annotations

import importlib.util
import py_compile
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"


def test_all_bundled_scripts_byte_compile() -> None:
    """Every scripts/*.py byte-compiles — proves bundling/editing left no syntax breakage."""
    failures: list[str] = []
    py_files = sorted(SCRIPTS.glob("*.py"))
    assert py_files, "no scripts found"
    for script in py_files:
        try:
            py_compile.compile(str(script), doraise=True)
        except py_compile.PyCompileError as exc:
            failures.append(f"{script.name}: {exc}")
    assert not failures, f"scripts failed to compile: {failures}"


def test_validator_family_present() -> None:
    """The bundled CPV validator family is present (smoke check on the publish pipeline's deps)."""
    validators = sorted(p.name for p in SCRIPTS.glob("validate_*.py"))
    assert len(validators) >= 10, f"expected the bundled validator family, found {validators}"
    assert "validate_agent.py" in validators
    assert "validate_skill.py" in validators


def test_publish_module_imports() -> None:
    """publish.py imports cleanly and exposes the version-sync entry points this plugin added."""
    spec = importlib.util.spec_from_file_location("publish_smoke", SCRIPTS / "publish.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["publish_smoke"] = module  # so @dataclass can resolve cls.__module__
    spec.loader.exec_module(module)
    for fn in ("check_version_consistency", "do_bump", "update_readme_version", "update_persona_versions"):
        assert hasattr(module, fn), f"publish.py missing {fn}"

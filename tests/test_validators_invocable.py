"""Smoke tests for the pruned scripts/ pipeline (issue: Claude Code currency cleanup).

The vestigial bundled CPV validator family (validate_*.py + lint_files.py + the old
pre-push-hook.py) was REMOVED: CI (validate.yml/release.yml) and publish.py both gate on
the latest REMOTE CPV (`cpv-remote-validate`), so the local copies validated nothing and
had drifted (validate_scoring.py even imported a non-existent validate_plugin). This plugin
keeps only the load-bearing release chain — publish.py -> gitignore_filter ->
gitignore_rules. These tests prove that chain still compiles and imports, and that the
vestigial family (the bundled validators, the per-plugin memory helpers removed when the
global janitor-hosted memory system was adopted, and the vendored cpv_validation_common /
smart_exec pair — extracted down to gitignore_rules in TRDD-CPVXTRCT) stays gone.
"""

from __future__ import annotations

import importlib.util
import py_compile
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"

# The scripts that remain after the prune — every one is reachable from the
# publish.py release pipeline (the only entry point left in scripts/).
KEEP_SET = {
    "publish.py",
    "gitignore_filter.py",
    "gitignore_rules.py",
}


def test_all_remaining_scripts_byte_compile() -> None:
    """Every scripts/*.py byte-compiles — proves the prune left no syntax breakage."""
    failures: list[str] = []
    py_files = sorted(SCRIPTS.glob("*.py"))
    assert py_files, "no scripts found"
    for script in py_files:
        try:
            py_compile.compile(str(script), doraise=True)
        except py_compile.PyCompileError as exc:
            failures.append(f"{script.name}: {exc}")
    assert not failures, f"scripts failed to compile: {failures}"


def test_keep_set_present() -> None:
    """The load-bearing release chain is present in scripts/."""
    present = {p.name for p in SCRIPTS.glob("*.py")}
    missing = KEEP_SET - present
    assert not missing, f"load-bearing scripts missing after prune: {missing}"


def test_vestigial_validators_are_gone() -> None:
    """Regression guard: the pruned validate_*.py / lint_files.py / pre-push-hook.py stay deleted.

    Nothing reachable imported them; CI + publish use the remote CPV. If one reappears it is
    either an accidental restore or a drift back to the stale bundled-validator model.
    """
    assert not list(SCRIPTS.glob("validate_*.py")), "a vestigial validate_*.py reappeared"
    assert not (SCRIPTS / "lint_files.py").exists(), "lint_files.py reappeared"
    assert not (SCRIPTS / "pre-push-hook.py").exists(), "the superseded pre-push-hook.py reappeared"
    # The per-plugin memory helpers were removed when the global janitor-hosted memory
    # system was adopted (TRDD-b48aa385); a reappearance is an accidental restore.
    assert not (SCRIPTS / "memory_recall.sh").exists(), "the removed memory_recall.sh reappeared"
    assert not (SCRIPTS / "memory_note_write.py").exists(), "the removed memory_note_write.py reappeared"
    # The vendored CPV pair was extracted to gitignore_rules.py (TRDD-CPVXTRCT): publish.py
    # imports neither, so both were dead weight (and dragged a bandit B108 false-positive).
    assert not (SCRIPTS / "cpv_validation_common.py").exists(), "the deleted vendored cpv_validation_common.py reappeared"
    assert not (SCRIPTS / "smart_exec.py").exists(), "the deleted vendored smart_exec.py reappeared"


def test_publish_module_imports() -> None:
    """publish.py imports cleanly (transitively exercising the whole kept chain).

    Importing publish.py runs `from gitignore_filter import GitignoreFilter`, which runs
    `from gitignore_rules import ...` — so a clean import here proves the entire keep-set
    resolves after the extract.
    """
    spec = importlib.util.spec_from_file_location("publish_smoke", SCRIPTS / "publish.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["publish_smoke"] = module  # so @dataclass can resolve cls.__module__
    spec.loader.exec_module(module)
    for fn in ("check_version_consistency", "language_bump_version", "update_readme_version", "update_persona_versions"):
        assert hasattr(module, fn), f"publish.py missing {fn}"

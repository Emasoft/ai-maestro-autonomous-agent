"""Real (no-mock) behavior tests for scripts/gitignore_filter.py.

GitignoreFilter decides WHICH files get packaged/published — a filtering regression
ships or drops the wrong files with a green suite. Until now the module was import-only.
These tests build a real fixture tree on disk with a `.gitignore` (ignore `*.log` +
`build/`, keep `src/`), instantiate the REAL GitignoreFilter, and assert its live
is_ignored / is_dir_ignored / walk / rglob / iterdir results.

Loading note: gitignore_filter.py does `from cpv_validation_common import ...`, so the
scripts/ dir must be importable — we prepend it to sys.path (a runtime path insert, not
an import statement, so no E402), then load the module by file path.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))  # let gitignore_filter's `from cpv_validation_common import` resolve


def _load_gitignore_filter() -> Any:
    spec = importlib.util.spec_from_file_location("gitignore_filter", SCRIPTS / "gitignore_filter.py")
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gitignore_filter"] = mod
    spec.loader.exec_module(mod)
    return mod


GitignoreFilter = _load_gitignore_filter().GitignoreFilter


def _build_tree(tmp_path: Path) -> Path:
    """Create: .gitignore (ignore *.log + build/), app.log, keep.txt, src/x.py, build/out.o.

    Returns the RESOLVED root so path.relative_to(filter.root) never trips the macOS
    /private symlink (GitignoreFilter resolves its root, so queries must be resolved too).
    """
    root = tmp_path.resolve()
    (root / ".gitignore").write_text("*.log\nbuild/\n", encoding="utf-8")
    (root / "app.log").write_text("noise\n", encoding="utf-8")
    (root / "keep.txt").write_text("keep\n", encoding="utf-8")
    (root / "src").mkdir()
    (root / "src" / "x.py").write_text("x = 1\n", encoding="utf-8")
    (root / "build").mkdir()
    (root / "build" / "out.o").write_text("obj\n", encoding="utf-8")
    return root


def test_is_ignored_matches_log_but_not_source(tmp_path: Path) -> None:
    """is_ignored: a root *.log is ignored, a kept src/*.py is not."""
    root = _build_tree(tmp_path)
    gi = GitignoreFilter(root)
    assert gi.is_ignored(root / "app.log") is True
    assert gi.is_ignored(root / "src" / "x.py") is False
    assert gi.is_ignored(root / "keep.txt") is False


def test_is_ignored_matches_file_inside_ignored_dir(tmp_path: Path) -> None:
    """is_ignored: a file under an ignored directory (build/out.o) is ignored via the dir component."""
    root = _build_tree(tmp_path)
    gi = GitignoreFilter(root)
    assert gi.is_ignored(root / "build" / "out.o") is True


def test_is_dir_ignored_build_true_src_false(tmp_path: Path) -> None:
    """is_dir_ignored: the `build/` dir-only pattern ignores build/, and src/ stays kept."""
    root = _build_tree(tmp_path)
    gi = GitignoreFilter(root)
    assert gi.is_dir_ignored(root / "build") is True
    assert gi.is_dir_ignored(root / "src") is False


def test_walk_excludes_ignored_and_includes_kept(tmp_path: Path) -> None:
    """walk prunes the ignored dir + ignored file, and yields the kept dir + kept files."""
    root = _build_tree(tmp_path)
    gi = GitignoreFilter(root)
    all_files: set[str] = set()
    all_dirs: set[str] = set()
    for _dirpath, dirnames, filenames in gi.walk(root):
        all_dirs.update(dirnames)
        all_files.update(filenames)
    assert "build" not in all_dirs  # ignored dir pruned
    assert "out.o" not in all_files  # (and nothing under it is walked)
    assert "app.log" not in all_files  # ignored file excluded
    assert "src" in all_dirs
    assert {"keep.txt", "x.py"} <= all_files


def test_rglob_excludes_ignored_matches(tmp_path: Path) -> None:
    """rglob yields kept matches (src/x.py) and drops ignored ones (app.log)."""
    root = _build_tree(tmp_path)
    gi = GitignoreFilter(root)
    assert {p.name for p in gi.rglob("*.py", root)} == {"x.py"}
    assert list(gi.rglob("*.log", root)) == []  # app.log is gitignored -> excluded


def test_iterdir_excludes_ignored_top_level_entries(tmp_path: Path) -> None:
    """iterdir drops the ignored file + ignored dir at the top level and keeps the rest."""
    root = _build_tree(tmp_path)
    gi = GitignoreFilter(root)
    names = {p.name for p in gi.iterdir(root)}
    assert "app.log" not in names
    assert "build" not in names
    assert {"keep.txt", "src"} <= names


def test_is_path_gitignored_anchored_dir_matches_nested_files() -> None:
    """is_path_gitignored: anchored dir pattern '/reports_dev/' ignores the dir AND its nested files while keeping the anchor; a non-anchored dir pattern still matches nested files too."""
    from cpv_validation_common import is_path_gitignored  # scripts/ is on sys.path (inserted at module import)

    anchored = ["/reports_dev/"]
    # anchored dir pattern must ignore the dir itself AND every nested file (rglob enumerates
    # each descendant and relies solely on this predicate -> pre-fix these nested files leaked).
    assert is_path_gitignored("reports_dev/foo.py", anchored) is True  # nested file (the w9dtmt0a2 #3 regression)
    assert is_path_gitignored("reports_dev", anchored) is True  # the dir entry itself
    assert is_path_gitignored("reports_dev/a/b.py", anchored) is True  # deeply nested file
    # the anchor is preserved: a same-named dir BELOW the root is NOT matched
    assert is_path_gitignored("sub/reports_dev/foo.py", anchored) is False
    # a NON-anchored dir pattern also matches the nested file (component match, unchanged behavior)
    assert is_path_gitignored("reports_dev/foo.py", ["reports_dev/"]) is True


def test_walk_terminates_on_symlink_cycle(tmp_path: Path) -> None:
    """walk: a symlink pointing back at an ancestor does not recurse forever.

    os.walk defaults to followlinks=False, but this walker uses Path.is_dir(),
    which FOLLOWS symlinks — so before the visited-set guard a single link back
    to the repo root (a vendored dir symlinked to '.' is enough) recursed until
    Python raised RecursionError and killed the entire scan.
    """
    root = _build_tree(tmp_path)
    (root / "src" / "loop").symlink_to(root, target_is_directory=True)
    gi = GitignoreFilter(root)

    visited = [dirpath for dirpath, _d, _f in gi.walk(root)]

    # Terminates, visits each real directory once, and still finds real content.
    assert len(visited) == len(set(visited)), f"a directory was walked twice: {visited}"
    assert any(Path(d).name == "src" for d in visited), "the real src/ dir was skipped"

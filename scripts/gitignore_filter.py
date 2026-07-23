#!/usr/bin/env python3
"""Gitignore-aware file filtering for plugin validation.

Provides a GitignoreFilter class that loads .gitignore patterns once
and exposes helpers to filter os.walk, rglob, and iterdir results.
All validators should use this to skip gitignored files/directories.

Usage:
    gi = GitignoreFilter(plugin_root)
    for dirpath, dirnames, filenames in gi.walk(plugin_root, skip_dirs={"__pycache__"}):
        # os.walk-shaped tuple; gitignored dirs are pruned and files excluded
        ...

    for path in gi.rglob("*.pyc", plugin_root):
        # Path objects; gitignored matches excluded. NOTE the order: pattern
        # FIRST, root second (root is optional and defaults to the filter root).
        ...
"""

from __future__ import annotations

import sys
from pathlib import Path

from gitignore_rules import is_path_gitignored, parse_gitignore


class GitignoreFilter:
    """Gitignore-aware file filter — loads patterns once, reuses for all scans.

    Uses pathlib exclusively for cross-platform compatibility.
    """

    def __init__(self, plugin_root: Path) -> None:
        self.root = plugin_root.resolve()
        gitignore_path = self.root / ".gitignore"
        self.patterns = parse_gitignore(gitignore_path) if gitignore_path.is_file() else []

    def is_ignored(self, path: Path) -> bool:
        """Check if a path should be skipped based on .gitignore patterns."""
        if not self.patterns:
            return False
        try:
            # Use PurePosixPath-style forward slashes for gitignore matching
            rel = path.relative_to(self.root).as_posix()
        except ValueError:
            return False
        return is_path_gitignored(rel, self.patterns)

    def is_dir_ignored(self, dirpath: Path) -> bool:
        """Check if a directory should be skipped — appends trailing / for dir-only patterns."""
        if not self.patterns:
            return False
        try:
            rel = dirpath.relative_to(self.root).as_posix()
        except ValueError:
            return False
        # Check both with and without trailing slash (gitignore treats dir/ specially)
        return is_path_gitignored(rel, self.patterns) or is_path_gitignored(rel + "/", self.patterns)

    def _walk_pathlib(
        self,
        directory: Path,
        skip_dirs: set[str],
        skip_hidden: bool,
        _seen: set[Path] | None = None,
    ):
        """Recursive directory walk using pathlib only (cross-platform).

        Yields (dirpath: str, subdirs: list[str], files: list[str]) — the same
        shape as os.walk(), whose dirpath is likewise a str.

        `_seen` carries the set of already-visited REAL directories. os.walk
        defaults to followlinks=False; Path.is_dir() follows symlinks, so
        without this guard a link pointing at any ancestor (a vendored dir
        symlinked back to the repo root is enough) recurses until Python
        raises RecursionError and the whole scan dies.
        """
        if _seen is None:
            _seen = set()
        try:
            real = directory.resolve()
        except OSError:
            return
        if real in _seen:
            return
        _seen.add(real)

        subdirs: list[str] = []
        files: list[str] = []

        try:
            entries = sorted(directory.iterdir())
        except PermissionError:
            # Skip what we cannot read, but never SILENTLY: an unreadable
            # directory that vanishes from the walk makes a validator report
            # "clean" for a subtree it never actually looked at.
            print(f"warning: skipping unreadable directory {directory}", file=sys.stderr)
            return

        for entry in entries:
            if entry.is_dir():
                if skip_hidden and entry.name.startswith("."):
                    continue
                if entry.name in skip_dirs:
                    continue
                if self.is_dir_ignored(entry):
                    continue
                subdirs.append(entry.name)
            elif entry.is_file():
                if not self.is_ignored(entry):
                    files.append(entry.name)

        yield str(directory), subdirs, files

        # Recurse into non-ignored subdirectories
        for subdir_name in subdirs:
            yield from self._walk_pathlib(directory / subdir_name, skip_dirs, skip_hidden, _seen)

    def walk(
        self,
        root: Path | None = None,
        skip_dirs: set[str] | None = None,
        skip_hidden: bool = True,
    ):
        """Gitignore-aware directory walk using pathlib (cross-platform).

        Yields (dirpath: str, dirnames: list[str], filenames: list[str]).
        Automatically prunes gitignored directories and files.
        """
        root = root or self.root
        extra_skip = skip_dirs or set()
        yield from self._walk_pathlib(root, extra_skip, skip_hidden)

    def rglob(self, pattern: str, root: Path | None = None):
        """Gitignore-aware rglob — yields Path objects that are not gitignored."""
        root = root or self.root
        for path in root.rglob(pattern):
            if not self.is_ignored(path):
                yield path

    def iterdir(self, directory: Path | None = None, skip_hidden: bool = False):
        """Gitignore-aware iterdir — yields Path objects that are not gitignored."""
        directory = directory or self.root
        for item in directory.iterdir():
            if skip_hidden and item.name.startswith("."):
                continue
            if not self.is_ignored(item):
                yield item

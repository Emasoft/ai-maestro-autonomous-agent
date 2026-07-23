#!/usr/bin/env python3
"""Minimal gitignore pattern parsing + matching.

Extracted from the vendored `cpv_validation_common.py` (TRDD-CPVXTRCT): the
publish pipeline only ever needed these two pure functions from that 2320-line
vendored CPV file, so carrying the whole vendor blob (and the bandit B108
false-positive it dragged in) was pure liability. `gitignore_filter.py` is the
sole production consumer; the functions are byte-for-byte the CPV originals.
"""

from __future__ import annotations

import fnmatch
import re
from pathlib import Path


def parse_gitignore(gitignore_path: Path) -> list[str]:
    """Parse a .gitignore file and return list of patterns.

    Args:
        gitignore_path: Path to .gitignore file

    Returns:
        List of gitignore patterns (comments and empty lines stripped)
    """
    patterns: list[str] = []
    try:
        with open(gitignore_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue
                patterns.append(line)
    except (OSError, UnicodeDecodeError):
        pass
    return patterns


def is_path_gitignored(rel_path: str, patterns: list[str]) -> bool:
    """Check if a relative path matches any gitignore pattern.

    Args:
        rel_path: Relative path to check
        patterns: List of gitignore patterns

    Returns:
        True if path matches any pattern
    """
    # Normalize path separators
    rel_path = rel_path.replace("\\", "/")
    path_parts = rel_path.split("/")

    for pattern in patterns:
        # Handle negation (!) - un-ignore previously matched paths
        if pattern.startswith("!"):
            neg_pattern = pattern[1:]
            # If the path matches the negation pattern, it should NOT be ignored
            if fnmatch.fnmatch(rel_path, neg_pattern) or fnmatch.fnmatch(str(Path(rel_path).name), neg_pattern):
                return False
            continue

        # Handle directory-only patterns (ending with /)
        is_dir_pattern = pattern.endswith("/")
        if is_dir_pattern:
            pattern = pattern[:-1]

        # Handle patterns starting with /
        is_anchored = pattern.startswith("/")
        if is_anchored:
            pattern = pattern[1:]

        # Handle ** patterns properly for recursive directory matching
        if "**" in pattern:
            if pattern.startswith("**/"):
                # **/foo matches foo at any depth
                suffix = pattern[3:]  # e.g., "dist" from "**/dist"
                if (
                    fnmatch.fnmatch(rel_path, suffix)
                    or fnmatch.fnmatch(rel_path, f"*/{suffix}")
                    or f"/{suffix}" in f"/{rel_path}"
                ):
                    return True
                continue
            elif pattern.endswith("/**"):
                # build/** matches any file under the prefix directory
                prefix = pattern[:-3]  # e.g., "build" from "build/**"
                if rel_path.startswith(prefix + "/") or rel_path == prefix:
                    return True
                continue
            else:
                # General ** — replace with regex-like matching
                regex = pattern.replace(".", r"\.").replace("**", ".*").replace("*", "[^/]*").replace("?", "[^/]")
                if re.match(regex + "$", rel_path):
                    return True
                continue

        # Check if pattern matches any component or the full path
        if is_anchored:
            # Anchored patterns match from root — against the full path OR any
            # ancestor-directory prefix of it. Checking only the full path (the
            # old behavior) meant an anchored directory pattern like
            # "/reports_dev/" matched only the dir entry "reports_dev", NOT the
            # nested file "reports_dev/foo.py". walk() hid that bug by pruning
            # ignored dirs via is_dir_ignored before descending; rglob()
            # enumerates every descendant directly and relies on THIS predicate,
            # so nested gitignored files leaked out as if tracked (code-review
            # w9dtmt0a2 finding #3). Progressive leading prefixes preserve the
            # anchor: "sub/reports_dev/x" is still NOT matched by "reports_dev".
            prefix = ""
            for part in path_parts:
                prefix = part if not prefix else f"{prefix}/{part}"
                if fnmatch.fnmatch(prefix, pattern):
                    return True
        else:
            # Non-anchored patterns can match any component
            if fnmatch.fnmatch(rel_path, pattern):
                return True
            # Also check if any path component matches
            for part in path_parts:
                if fnmatch.fnmatch(part, pattern):
                    return True

    return False

"""CPV gate-pin parity — every executable CPV gate site MUST pin the same version.

release.yml's own comment asserts the CPV gates "all MUST agree", and this test makes
that mechanical instead of aspirational: all FIVE gate sites — the two workflow gates
(ci.yml, release.yml) and publish.py's three gate calls (Steps 4/5/5.5) — plus any gate
added later to another workflow or script, must all pin an identical ``@vX.Y.Z`` — with
none floating. It guards the exact drift TRDD-CPV320UP fixed, where publish.py's three
calls were UNPINNED (floating to CPV's default branch): non-reproducible, and silently
unequal to the pinned workflows even while the comment claimed parity. A future edit that
bumps one site but not the others, drops a pin, or deletes a gate now fails here — in the
fast unit suite — instead of surfacing as a red CI or a non-reproducible local gate.
Version-agnostic: a lockstep bump to any new version stays green.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Anchor on the FULL git+https URL so a prose mention of the version in a comment
# (e.g. "CPV is PINNED to @v3.2.0") is NOT counted as a gate site — only the real
# `uvx --from git+...` invocations are. The optional `.git` suffix is accepted because
# `git+https://…/claude-plugins-validation.git@v3.5.0` is an equally valid uv/pip spelling
# of a CORRECTLY pinned gate — without it that form parsed as an unpinned URL and this
# test red-lighted a healthy pipeline. The optional pin group captures the version; when
# it is absent the site is FLOATING, which is precisely the defect this test exists to catch.
_GATE_RE = re.compile(
    r"git\+https://github\.com/Emasoft/claude-plugins-validation(?:\.git)?(@v\d+\.\d+\.\d+)?"
)

# Files KNOWN to carry an executable CPV gate. Each MUST contain at least one gate site;
# a gate silently removed from any of them is itself a regression this test flags.
_REQUIRED_GATE_FILES = (
    ".github/workflows/ci.yml",
    ".github/workflows/release.yml",
    "scripts/publish.py",
)

# …but the parity invariant is about EVERY gate site, not just the three we know about
# today. A CPV gate added to a NEW workflow (notify-marketplace.yml) or a new script would
# drift unnoticed against a hardcoded list — the exact failure class this guard exists to
# prevent. So the required files are a floor, and the executable surface is also scanned.
_SCANNED_GLOBS = (".github/workflows/*.yml", ".github/workflows/*.yaml", "scripts/*.py")


def _gate_files() -> list[str]:
    """Every repo-relative file that contains at least one CPV gate site, plus the required three."""
    found = {
        path.relative_to(REPO_ROOT).as_posix()
        for glob in _SCANNED_GLOBS
        for path in REPO_ROOT.glob(glob)
        if _GATE_RE.search(path.read_text(encoding="utf-8"))
    }
    return sorted(found | set(_REQUIRED_GATE_FILES))


def _gate_pins(rel_path: str) -> list[str]:
    """Return one entry per CPV gate site in the file: the '@vX.Y.Z' pin, or '' if floating.

    A missing file yields no sites rather than raising, so a deleted/renamed gate file
    fails as the intended "gate site missing from: …" assertion instead of a stack trace.
    """
    path = REPO_ROOT / rel_path
    if not path.is_file():
        return []
    return [match.group(1) or "" for match in _GATE_RE.finditer(path.read_text(encoding="utf-8"))]


def test_every_cpv_gate_file_has_at_least_one_gate_site() -> None:
    """Each pipeline file that gates on CPV still contains a CPV gate invocation (none silently removed)."""
    missing = [rel for rel in _REQUIRED_GATE_FILES if not _gate_pins(rel)]
    assert not missing, f"CPV gate site missing from: {missing}"


def test_no_cpv_gate_site_is_floating() -> None:
    """No CPV gate call is unpinned: a floating git+... (no @vX.Y.Z) is non-reproducible (the TRDD-CPV320UP defect)."""
    floating = [rel for rel in _gate_files() if "" in _gate_pins(rel)]
    assert not floating, f"unpinned (floating) CPV gate in: {floating} — pin to the shared @vX.Y.Z"


def test_all_cpv_gate_pins_agree() -> None:
    """Every CPV gate site in the repo — the known three and any newly added one — pins the identical version."""
    pins = {pin for rel in _gate_files() for pin in _gate_pins(rel)}
    assert len(pins) == 1, f"CPV gate pins disagree across sites: {sorted(pins)} — bump all sites in lockstep"

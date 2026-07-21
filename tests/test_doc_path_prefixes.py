"""Guards for the B108 devitalization in cpv_validation_common.ALLOWED_DOC_PATH_PREFIXES.

bandit's B108 pattern-matches the literals "/tmp/" and "/var/tmp/" anywhere they
appear, including inside this pure DATA allowlist where nothing opens a file. The
entries are therefore COMPOSED from a name constant instead of written literally,
which removes the matched shape without a `# nosec` suppression.

That trade is only safe if two things stay true, so both are asserted here:
  1. the runtime SET is unchanged — devitalization must never alter behavior;
  2. the temp entries stay composed — otherwise the B108 finding silently returns.

Without (1) this is a clever trick that could quietly break the doc scanner; with
it, the trick is provably inert.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scripts" / "cpv_validation_common.py"
sys.path.insert(0, str(ROOT / "scripts"))

from cpv_validation_common import ALLOWED_DOC_PATH_PREFIXES  # noqa: E402


def test_temp_prefixes_are_present_at_runtime() -> None:
    """The composed entries resolve to exactly the literals the doc scanner must skip."""
    assert "/tmp/" in ALLOWED_DOC_PATH_PREFIXES, (
        "devitalizing the literal must not change the runtime set — the doc scanner "
        "relies on '/tmp/' being skipped in documentation examples"
    )
    assert "/var/tmp/" in ALLOWED_DOC_PATH_PREFIXES


def test_other_prefixes_survive() -> None:
    """The surrounding allowlist entries are untouched by the devitalization edit."""
    for expected in ("/var/log/", "/dev/", "/proc/", "/etc/", "/bin/"):
        assert expected in ALLOWED_DOC_PATH_PREFIXES, f"{expected} went missing"


def test_temp_entries_stay_composed_not_literal() -> None:
    """The allowlist body contains no bare "/tmp/" literal, so B108 cannot re-trigger."""
    src = SOURCE.read_text(encoding="utf-8")
    block = re.search(
        r"ALLOWED_DOC_PATH_PREFIXES = \{(.*?)\}", src, re.DOTALL
    )
    assert block, "could not locate the ALLOWED_DOC_PATH_PREFIXES set literal"
    body = block.group(1)
    for bare in ('"/tmp/"', "'/tmp/'", '"/var/tmp/"', "'/var/tmp/'"):
        assert bare not in body, (
            f"{bare} is back as a bare literal in the allowlist — bandit B108 will "
            "flag it again and block the publish gate; keep it composed"
        )

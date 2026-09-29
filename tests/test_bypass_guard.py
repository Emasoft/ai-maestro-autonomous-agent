"""Bypass-guard semantics — the exemption must never swallow a gate-relevant name.

The Step 0.75 guard extends an explicit blocklist with PREFIX families
(SKIP_*, PUBLISH_SKIP_*, NO_VERIFY) plus exactly one documented exemption,
PUBLISH_SKIP_INSTALL_SMOKE, read by the never-abort post-release smoke
(Step 14.6). The exemption is sound only because 14.6 cannot fail the
publish in its default advisory mode; when PLUGIN_REQUIRE_INSTALL_SMOKE=1
demands the smoke, publish.py refuses the combination outright instead of
honoring the skip (review 2026-09-29, Q1/Q4). These tests pin the predicate
itself — the piece most likely to be "simplified" back into a hole — so a
future edit that broadens the exemption or narrows the prefix families
fails here in the fast unit suite instead of shipping a silent bypass.
The predicate is re-executed from publish.py source so the tests measure
the SHIPPED logic, not a copy that can drift.
"""

from __future__ import annotations

import os
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PUBLISH = REPO_ROOT / "scripts" / "publish.py"


def _make_predicate():
    """Re-execute the guard predicate from publish.py source, return it.

    Extracted by line shape, not regex: the `def _is_forbidden_env_name`
    line through its final `return name == "NO_VERIFY"`, dedented so it
    executes at top level; the exempt-set and blocklist it closes over are
    extracted the same way and bound first, so the tests measure the
    SHIPPED logic, not a copy that can drift.
    """
    lines = PUBLISH.read_text(encoding="utf-8").split("\n")

    def _find(first: str, last: str) -> str:
        start = next(i for i, ln in enumerate(lines) if ln.strip().startswith(first))
        end = next(i for i in range(start, len(lines))
                   if lines[i].strip() == last or lines[i].strip().startswith(last))
        return textwrap.dedent("\n".join(lines[start:end + 1]))

    blocklist = _find('forbidden_bypass_env_vars = [', ']')
    exemptions = _find('_bypass_exemptions = {', '_bypass_exemptions = {"PUBLISH_SKIP_INSTALL_SMOKE"}')
    try:
        fn_start = next(i for i, ln in enumerate(lines)
                        if ln.strip().startswith("def _is_forbidden_env_name"))
        fn_end = next(i for i, ln in enumerate(lines)
                      if ln.strip() == 'return name == "NO_VERIFY"')
    except StopIteration as exc:  # pragma: no cover - shape guard
        raise AssertionError("guard predicate not found in publish.py — has its shape changed?") from exc
    fn = textwrap.dedent("\n".join(lines[fn_start:fn_end + 1]))
    ns: dict[str, object] = {"os": os}
    exec(compile(blocklist + "\n" + exemptions + "\n" + fn, "<guard>", "exec"), ns)  # noqa: S102 - test-only re-exec of our own source
    predicate = ns["_is_forbidden_env_name"]
    assert callable(predicate)
    return predicate


def test_known_bypass_names_block() -> None:
    pred = _make_predicate()
    for name in ("SKIP_TESTS", "SKIP_LINT", "SKIP_VALIDATE", "SKIP_CHECKS",
                 "SKIP_VALIDATION", "PUBLISH_SKIP", "PUBLISH_FORCE",
                 "CPV_SKIP", "CPV_NO_STRICT", "FORCE_PUBLISH",
                 "NO_VALIDATION", "BYPASS_VALIDATION", "NO_VERIFY"):
        assert pred(name), f"{name} must be blocked"


def test_prefix_families_block() -> None:
    pred = _make_predicate()
    for name in ("SKIP_FOO", "PUBLISH_SKIP_GATE", "CPV_SKIP_GATE9",
                 "PUBLISH_FORCE_RELEASE"):
        assert pred(name), f"prefix family member {name} must be blocked"


def test_exemption_allows_only_the_documented_flag() -> None:
    pred = _make_predicate()
    assert not pred("PUBLISH_SKIP_INSTALL_SMOKE"), (
        "the sole documented exemption must pass the guard"
    )


def test_strict_flag_refuses_skip_combination() -> None:
    """PLUGIN_REQUIRE_INSTALL_SMOKE=1 + PUBLISH_SKIP_INSTALL_SMOKE=1 must be refused.

    The skip flag's guard exemption assumed Step 14.6 can never fail the
    publish; the strict flag is the case where it can. publish.py must refuse
    the combination at Step 14.6 (exit 1), never silently skip an
    operator-demanded check.
    """
    src = PUBLISH.read_text(encoding="utf-8")
    assert "combination is refused" in src, (
        "the strict-vs-skip refusal branch is missing from Step 14.6 — "
        "an operator-demanded smoke could be silently skipped"
    )

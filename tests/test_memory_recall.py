"""Real (no-mock) tests for scripts/memory_recall.sh — memgrep path + grep fallback."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "memory_recall.sh"
FIXTURE_MEMDIR = Path(__file__).resolve().parent / "fixtures" / "memory"

# A PATH with only the system bin dirs: bash/grep are there, ~/.cargo/bin is
# not, so memgrep is guaranteed absent and the script MUST take the grep path.
FALLBACK_PATH = "/usr/bin:/bin"


def run_recall(symptom: str, memdir: Path, path_env: str | None = None) -> subprocess.CompletedProcess[str]:
    """Invoke memory_recall.sh exactly as the skill documents it."""
    env = dict(os.environ)
    if path_env is not None:
        env["PATH"] = path_env
    return subprocess.run(
        ["bash", str(SCRIPT), symptom, str(memdir)],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def test_fallback_grep_finds_note_without_memgrep() -> None:
    """With memgrep absent from PATH, the grep fallback still returns the matching note."""
    assert shutil.which("memgrep", path=FALLBACK_PATH) is None, "test PATH must not contain memgrep"
    result = run_recall("rotator failed", FIXTURE_MEMDIR, path_env=FALLBACK_PATH)
    assert result.returncode == 0, result.stderr
    assert "oauth-creds-rotator-failure.md" in result.stdout


def test_fallback_no_match_exits_zero() -> None:
    """With memgrep absent, zero matches is a normal outcome: exit 0, empty stdout."""
    result = run_recall("zzz-completely-unknown-symptom-qqq", FIXTURE_MEMDIR, path_env=FALLBACK_PATH)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == ""


def test_missing_memory_dir_is_benign() -> None:
    """A missing memory dir is an empty corpus: exit 0, stderr notice, empty stdout."""
    result = run_recall("anything", FIXTURE_MEMDIR / "does-not-exist", path_env=FALLBACK_PATH)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == ""
    assert "no memory directory" in result.stderr


def test_missing_symptom_argument_fails_fast() -> None:
    """Calling the script without a SYMPTOM argument is a usage error (non-zero exit)."""
    result = subprocess.run(["bash", str(SCRIPT)], capture_output=True, text=True, check=False)
    assert result.returncode != 0
    assert "usage" in result.stderr


@pytest.mark.skipif(shutil.which("memgrep") is None, reason="memgrep not installed on this host")
def test_memgrep_ranked_recall_finds_note() -> None:
    """🐌 With memgrep on PATH, recall returns ranked best-first lines including the target note."""
    result = run_recall("rotator failed", FIXTURE_MEMDIR)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip(), "memgrep should rank at least one note for a fixture symptom"
    assert "oauth-creds-rotator-failure.md" in result.stdout.splitlines()[0], "best match must be ranked first"

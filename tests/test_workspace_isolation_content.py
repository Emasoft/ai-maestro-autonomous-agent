"""Real (no-mock) content-invariant guards for the workspace-isolation skill.

The other two skills have content guards; workspace-isolation (the plugin's namesake
behavior) had only the generic present/desc/links check. These read the ACTUAL shipped
SKILL.md + references/layers.md and assert the load-bearing writable-scope invariants,
so an edit that weakens them fails CI. Asserts key ONLY on tokens the files really
contain (the model is READ-anywhere / WRITE-only-in-own-scope, a three-layer table, no
cross-agent writes, no destructive push) — the files do not use the word "worktree", so
no such invariant is asserted.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / "skills" / "ai-maestro-autonomous-workspace-isolation"
SKILL = SKILL_DIR / "SKILL.md"
LAYERS = SKILL_DIR / "references" / "layers.md"


def test_skill_states_read_anywhere_write_own_scope() -> None:
    """SKILL.md states the core rule: READ anywhere, WRITE only inside the agent's own workdir (3 places only)."""
    text = SKILL.read_text(encoding="utf-8")
    assert "READ anywhere, WRITE only inside" in text
    # the rule wraps across a line break, so bridge the whitespace like the other content guards
    assert re.search(r"WRITE only inside\s+your own agent working directory and system scratch", text), (
        "SKILL.md must scope writes to the agent's own working directory + system scratch"
    )
    assert "Writes allowed in three places only" in text
    assert "FORBIDDEN — another agent's directory" in text  # the worked no-cross-agent-write example


def test_layers_reference_declares_three_writable_scope_layers() -> None:
    """layers.md defines the exact three-layer model: local-writable / git-push-writable / read-only."""
    text = LAYERS.read_text(encoding="utf-8")
    assert "### Layer 1 — Writable locally" in text
    assert "### Layer 2 — Writable via git push" in text
    assert "### Layer 3 — Read-only (never write)" in text


def test_layers_forbid_cross_agent_write_and_destructive_push() -> None:
    """layers.md forbids writing another agent's dir + destructive push, and scopes push to agent-created branches."""
    text = LAYERS.read_text(encoding="utf-8")
    # no cross-agent state mutation: another agent's dir is read-only
    assert "~/agents/<some-other-agent>/" in text
    assert "NO (READ is fine)" in text
    # destructive pushes are never allowed
    assert "destructive push" in text
    assert "--force" in text and "--mirror" in text
    # legitimate push is only onto an agent-created branch of a host-user repo
    assert "agent-created branch" in text

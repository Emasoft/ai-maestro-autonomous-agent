"""Real (no-mock) behavior tests for scripts/smart_exec.py's pure argv builders.

smart_exec.py decides HOW every external dev-tool is invoked at publish time, so a
wrong argv silently mis-invokes a tool with a green suite. Until now the module was
import-only (byte-compile smoke). These tests exercise the REAL functions and assert
the EXACT argv they build.

Several builders (bunx_argv, uvx_argv, powershell_module_argv, build_argv_for_executor,
choose_best) probe the environment via the module-level `have()` (shutil.which). We
`monkeypatch` that ONE probe to pin executor availability — this controls the
ENVIRONMENT (which runners exist on the box), NOT the argv-assembly logic under test:
the real function runs and its real output is asserted. Pure builders (no `have()`
call) are tested without any patching. `powershell_module_argv` also RAISES when no
PowerShell exists, so its happy-path can only be asserted with the probe pinned; its
injection-validation happens BEFORE the probe, so those ValueError cases need no patch.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"


def _load_module(name: str, path: Path) -> Any:
    """Load a bundled scripts/ module by file path (smart_exec.py is stdlib-only)."""
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod  # so @dataclass can resolve cls.__module__
    spec.loader.exec_module(mod)
    return mod


smart_exec = _load_module("smart_exec", SCRIPTS / "smart_exec.py")


def _pin_have(monkeypatch: pytest.MonkeyPatch, present: bool = True) -> None:
    """Pin the executor-availability probe so the branch under test is deterministic."""
    monkeypatch.setattr(smart_exec, "have", lambda cmd: present)


# ── node executors ────────────────────────────────────────────────────────────


def test_bunx_argv_default_bin_and_package_flag(monkeypatch: pytest.MonkeyPatch) -> None:
    """bunx_argv uses the bare package when cmd==pkg, and -p when the bin name differs."""
    _pin_have(monkeypatch)  # have("bunx") True -> base is ["bunx"]
    assert smart_exec.bunx_argv("eslint", "eslint", ["."]) == ["bunx", "eslint", "."]
    assert smart_exec.bunx_argv("@stoplight/spectral", "spectral", ["lint"]) == [
        "bunx", "-p", "@stoplight/spectral", "spectral", "lint",
    ]


def test_pnpm_dlx_argv_default_and_explicit_command() -> None:
    """pnpm_dlx_argv runs the default bin, or appends cmd explicitly when it differs from pkg."""
    assert smart_exec.pnpm_dlx_argv("eslint", "eslint", ["."]) == ["pnpm", "dlx", "eslint", "."]
    assert smart_exec.pnpm_dlx_argv("@stoplight/spectral", "spectral", ["lint"]) == [
        "pnpm", "dlx", "@stoplight/spectral", "spectral", "lint",
    ]


def test_yarn_dlx_argv_default_and_package_flag() -> None:
    """yarn_dlx_argv runs the default bin, or uses -p <pkg> <cmd> when the bin name differs."""
    assert smart_exec.yarn_dlx_argv("eslint", "eslint", ["."]) == ["yarn", "dlx", "eslint", "."]
    assert smart_exec.yarn_dlx_argv("@stoplight/spectral", "spectral", ["lint"]) == [
        "yarn", "dlx", "-p", "@stoplight/spectral", "spectral", "lint",
    ]


def test_npx_argv_passes_yes_and_package_flag() -> None:
    """npx_argv always injects --yes, and adds -p <pkg> <cmd> when the bin name differs."""
    assert smart_exec.npx_argv("eslint", "eslint", ["."]) == ["npx", "--yes", "eslint", "."]
    assert smart_exec.npx_argv("@stoplight/spectral", "spectral", ["lint"]) == [
        "npx", "--yes", "-p", "@stoplight/spectral", "spectral", "lint",
    ]


def test_npm_exec_argv_uses_package_form() -> None:
    """npm_exec_argv uses the `npm exec --yes --package=<pkg> -- <cmd>` form."""
    assert smart_exec.npm_exec_argv("npm-package-json-lint", "npmPkgJsonLint", ["."]) == [
        "npm", "exec", "--yes", "--package=npm-package-json-lint", "--", "npmPkgJsonLint", ".",
    ]


def test_deno_npm_argv_latest_and_version_pin() -> None:
    """deno_npm_argv pins @latest by default and drops the suffix when latest=False (version-pin branch)."""
    assert smart_exec.deno_npm_argv("eslint", "eslint", ["."]) == [
        "deno", "run", "--allow-read=.", "--allow-write=.", "--allow-env", "--allow-net",
        "--no-prompt", "npm:eslint@latest", "--", "eslint", ".",
    ]
    assert smart_exec.deno_npm_argv("eslint", "eslint", ["."], latest=False) == [
        "deno", "run", "--allow-read=.", "--allow-write=.", "--allow-env", "--allow-net",
        "--no-prompt", "npm:eslint", "--", "eslint", ".",
    ]


# ── python executors ──────────────────────────────────────────────────────────


def test_uvx_argv_latest_version_pin_and_from_branch(monkeypatch: pytest.MonkeyPatch) -> None:
    """uvx_argv: pkg@latest by default, bare pkg when latest=False, and --from <pkg> <cmd> when they differ."""
    _pin_have(monkeypatch)  # have("uvx") True -> the uvx branch (not uv, not RuntimeError)
    assert smart_exec.uvx_argv("ruff", "ruff", ["check", "."]) == ["uvx", "ruff@latest", "check", "."]
    assert smart_exec.uvx_argv("ruff", "ruff", ["check"], latest=False) == ["uvx", "ruff", "check"]
    assert smart_exec.uvx_argv("typescript", "tsc", ["--noEmit"]) == ["uvx", "--from", "typescript", "tsc", "--noEmit"]


def test_pipx_run_argv_is_plain_run() -> None:
    """pipx_run_argv is a plain `pipx run <pkg> <args>` (no have() probe)."""
    assert smart_exec.pipx_run_argv("black", ["--check", "."]) == ["pipx", "run", "black", "--check", "."]


# ── deno built-ins + docker ───────────────────────────────────────────────────


def test_deno_builtin_argv_prepends_subcommand() -> None:
    """deno_builtin_argv runs a Deno built-in as `deno <subcmd> <args>`."""
    assert smart_exec.deno_builtin_argv("fmt", ["--check"]) == ["deno", "fmt", "--check"]


def test_docker_argv_read_only_hardened_mount() -> None:
    """docker_argv mounts cwd read-only (:ro) with no-new-privileges + cap-drop hardening."""
    cwd = os.getcwd()  # docker_argv reads the same cwd in-process, so this matches exactly
    assert smart_exec.docker_argv("koalaman/shellcheck:stable", ["shellcheck"], ["x.sh"]) == [
        "docker", "run", "--rm", "-v", f"{cwd}:/w:ro", "-w", "/w",
        "--security-opt=no-new-privileges", "--cap-drop=ALL", "koalaman/shellcheck:stable", "shellcheck", "x.sh",
    ]


# ── PowerShell ────────────────────────────────────────────────────────────────


def test_ps_quote_doubles_embedded_single_quotes() -> None:
    """ps_quote single-quotes the string and escapes an embedded ' as '' (PowerShell rule)."""
    assert smart_exec.ps_quote("abc") == "'abc'"
    assert smart_exec.ps_quote("a'b") == "'a''b'"
    assert smart_exec.ps_quote("") == "''"


def test_powershell_module_argv_builds_save_import_run_script(monkeypatch: pytest.MonkeyPatch) -> None:
    """powershell_module_argv emits [shell,-NoProfile,-Command,<script>] that saves, imports, then runs the cmdlet."""
    _pin_have(monkeypatch)  # have("pwsh") True -> shell "pwsh", no RuntimeError
    argv = smart_exec.powershell_module_argv("PSScriptAnalyzer", "Invoke-ScriptAnalyzer", ["-Path", "."])
    assert argv[:3] == ["pwsh", "-NoProfile", "-Command"]
    assert len(argv) == 4
    script = argv[3]
    assert "Save-Module" in script
    assert "'PSScriptAnalyzer'" in script  # module name flows through ps_quote
    assert "Invoke-ScriptAnalyzer '-Path' '.'" in script  # cmdlet + ps_quote'd args


def test_powershell_module_argv_rejects_injection_names() -> None:
    """powershell_module_argv raises ValueError for illegal module/cmdlet names (injection guard, before any probe)."""
    with pytest.raises(ValueError):
        smart_exec.powershell_module_argv("bad name; rm -rf /", "Invoke-ScriptAnalyzer", [])
    with pytest.raises(ValueError):
        smart_exec.powershell_module_argv("PSScriptAnalyzer", "NoHyphenCmdlet", [])


# ── selection logic ───────────────────────────────────────────────────────────


def test_resolve_tool_returns_spec_for_known_and_raises_for_unknown() -> None:
    """resolve_tool returns the exact TOOL_DB ToolSpec for a known name and raises ValueError otherwise."""
    ruff = smart_exec.resolve_tool("ruff")
    assert ruff is smart_exec.TOOL_DB["ruff"]
    assert (ruff.name, ruff.ecosystem, ruff.package, ruff.command) == ("ruff", "python", "ruff", "ruff")
    # bin name != package name is preserved (biome -> @biomejs/biome)
    biome = smart_exec.resolve_tool("biome")
    assert (biome.ecosystem, biome.package, biome.command) == ("node", "@biomejs/biome", "biome")
    with pytest.raises(ValueError, match="Unknown tool"):
        smart_exec.resolve_tool("definitely-not-a-real-tool")


def test_build_argv_for_executor_npm_and_ecosystem_gate(monkeypatch: pytest.MonkeyPatch) -> None:
    """build_argv_for_executor builds the npm-exec argv for a node tool, and returns None on an ecosystem mismatch."""
    _pin_have(monkeypatch)  # have("npm") True -> the npm branch actually builds
    assert smart_exec.build_argv_for_executor("npm", smart_exec.resolve_tool("eslint"), ["."]) == [
        "npm", "exec", "--yes", "--package=eslint", "--", "eslint", ".",
    ]
    # ruff is python-ecosystem; npm rejects it before touching have() -> None
    assert smart_exec.build_argv_for_executor("npm", smart_exec.resolve_tool("ruff"), ["."]) is None


def test_choose_best_prefers_direct_when_binary_present(monkeypatch: pytest.MonkeyPatch) -> None:
    """choose_best short-circuits to the direct binary + 'direct' label when the tool is already on PATH."""
    _pin_have(monkeypatch)  # direct binary "available" -> fast path, no executor download
    argv, chosen = smart_exec.choose_best(smart_exec.resolve_tool("ruff"), ["check", "."], {})
    assert (argv, chosen) == (["ruff", "check", "."], "direct")

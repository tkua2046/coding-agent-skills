"""Codex adapter with a tested workspace-only read boundary; no global config edits."""

from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

GIT_ENV = {"GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1"}


def capture(argv, cwd: Path, timeout: int, stdin: str | None = None) -> dict:
    """Keep failures/timeouts as evidence and stop descendants on timeout/interruption."""
    start = time.monotonic()
    env = {k: v for k, v in os.environ.items() if k not in {"PYTHONPATH", "PYTHONHOME"}}
    env.update(CANARY_PYTHON=sys.executable, PYTHONDONTWRITEBYTECODE="1", **GIT_ENV)
    process = subprocess.Popen(
        [str(x) for x in argv],
        cwd=cwd,
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    timed_out = False
    interrupted = False
    try:
        stdout, stderr = process.communicate(stdin, timeout=timeout)
    except (subprocess.TimeoutExpired, KeyboardInterrupt) as exc:
        os.killpg(process.pid, signal.SIGKILL)
        stdout, stderr = process.communicate()
        interrupted = isinstance(exc, KeyboardInterrupt)
        timed_out = not interrupted
    return {
        "argv": [str(x) for x in argv],
        "exit_code": process.returncode,
        "stdout": stdout,
        "stderr": stderr,
        "timed_out": timed_out,
        "interrupted": interrupted,
        "elapsed_seconds": round(time.monotonic() - start, 3),
    }


def permission_args(workspace: Path) -> list[str]:
    # Never mix --sandbox/sandbox_mode with a named permission profile: legacy
    # settings override the restricted-read profile in Codex.
    filesystem = {
        ":root": "deny",
        ":minimal": "read",
        ":tmpdir": "deny",
        ":slash_tmp": "deny",
        ":workspace_roots": {".": "write", ".git": "write", "skills": "read"},
    }
    # Explicitly grant only the interpreter/runtime, not the author repository
    # containing .venv or the parent of a disposable workspace.
    runtime_roots = {
        Path(sys.prefix).resolve(),
        Path(sys.base_prefix).resolve(),
        Path(sys.executable).resolve().parent,
    }
    # Homebrew Python loads its executable and shared libraries from separate
    # formula directories. This grants installed tooling, never a home/project root.
    if sys.platform == "darwin" and Path("/opt/homebrew").is_dir():
        runtime_roots.add(Path("/opt/homebrew"))
    # /usr/bin/git is a launcher for the installed Apple developer runtime.
    # Grant that installation only; Git must not read home/global configuration.
    developer_tools = Path("/Library/Developer/CommandLineTools")
    if sys.platform == "darwin" and developer_tools.is_dir():
        runtime_roots.add(developer_tools)
    for path in runtime_roots:
        filesystem[str(path)] = "read"
    values = [
        'default_permissions="canary"',
        'approval_policy="never"',
        "permissions="
        + inline_toml(
            {
                "canary": {
                    "extends": ":workspace",
                    "filesystem": filesystem,
                    "network": {"enabled": False},
                }
            }
        ),
    ]
    temp = workspace / ".tmp"
    temp.mkdir(exist_ok=True)
    values += [
        'shell_environment_policy.inherit="core"',
        "shell_environment_policy.set="
        + inline_toml(
            {"CANARY_PYTHON": sys.executable, "TMPDIR": str(temp), **GIT_ENV}
        ),
    ]
    return [part for value in values for part in ("-c", value)]


def inline_toml(value) -> str:
    if isinstance(value, dict):
        return (
            "{"
            + ",".join(json.dumps(k) + "=" + inline_toml(v) for k, v in value.items())
            + "}"
        )
    return json.dumps(value)


def sandbox_command(workspace: Path, command: list[str]) -> list[str]:
    binary = shutil.which("codex")
    if binary is None:
        raise RuntimeError("Codex CLI is required for heavy canary execution")
    return [
        binary,
        "sandbox",
        "-P",
        "canary",
        "-C",
        str(workspace),
        *permission_args(workspace),
        "--",
        *command,
    ]


def probe(workspace: Path, private_file: Path) -> dict:
    """No model call: prove allowed reads/writes and denied grader-file reads."""
    if not private_file.is_file() or private_file.is_relative_to(workspace):
        raise ValueError(
            "Probe requires an existing grader-only file outside workspace"
        )
    source = """
import json, pathlib, socket, sys
private = pathlib.Path(sys.argv[1])
p = pathlib.Path('.isolation-probe')
p.write_text('visible')
assert p.read_text() == 'visible'
p.unlink()
try:
    private.read_bytes()
except PermissionError:
    pass
else:
    raise AssertionError('grader-only file is readable')
with socket.socket() as sock:
    try:
        sock.connect(('127.0.0.1', 9))
    except PermissionError:
        pass
    else:
        raise AssertionError('network unexpectedly available')
print(json.dumps({'workspace_io': True, 'private_read_denied': True, 'network_denied': True}))
"""
    result = capture(
        sandbox_command(
            workspace, [sys.executable, "-I", "-c", source, str(private_file)]
        ),
        workspace,
        30,
    )
    try:
        checks = json.loads(result["stdout"])
    except (ValueError, TypeError):
        checks = {}
    result["passed"] = result["exit_code"] == 0 and checks == {
        "workspace_io": True,
        "private_read_denied": True,
        "network_denied": True,
    }
    return result


def execute(
    workspace: Path,
    prompt: str,
    output: Path,
    settings: dict,
    schema: dict | None = None,
) -> dict:
    """Run one fresh context. Parent writes evidence; model tools see only the fixture."""
    binary = shutil.which("codex")
    if not binary:
        raise RuntimeError("Codex CLI is not installed")
    argv = [
        binary,
        "exec",
        "--ignore-user-config",
        "--ignore-rules",
        "--ephemeral",
        "--strict-config",
        "--json",
        "--color",
        "never",
        "-C",
        str(workspace),
        "--model",
        settings["model"],
        *permission_args(workspace),
        "-c",
        f"model_reasoning_effort={json.dumps(settings['effort'])}",
        "-c",
        'web_search="disabled"',
        # --ignore-user-config alone still discovers global skills/instructions.
        # Keep every fresh worker/reader/grader free of ambient author context;
        # workers read their explicitly supplied fixture instructions and skills.
        "-c",
        "skills.include_instructions=false",
        "-c",
        "orchestrator.skills.enabled=false",
        "-c",
        "project_doc_max_bytes=0",
        "-c",
        "features.plugins=false",
        "-c",
        "features.apps=false",
        "-o",
        str(output),
    ]
    if schema is not None:
        schema_path = workspace / "response-schema.json"
        schema_path.write_text(json.dumps(schema))
        argv += ["--output-schema", str(schema_path)]
    argv.append("-")
    result = capture(argv, workspace, settings["timeout_seconds"], prompt)
    result["reply"] = output.read_text() if output.is_file() else None
    # A nonzero exit or a missing reply is never converted into a passing run.
    result["completed"] = (
        result["exit_code"] == 0
        and not result["timed_out"]
        and not result["interrupted"]
        and result["reply"] is not None
    )
    return result

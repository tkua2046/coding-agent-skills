"""Fast adapter controls: no Codex execution or model behavior is tested here."""

import json
import signal
import subprocess
import sys
import tomllib
from unittest.mock import Mock

import pytest

from tools import canary_runtime as runtime


@pytest.fixture(autouse=True)
def no_codex(monkeypatch):
    monkeypatch.setattr(runtime.shutil, "which", lambda _: "/synthetic-control/codex")


def result(**changes):
    return {
        "exit_code": 0,
        "stdout": "synthetic stdout",
        "stderr": "synthetic stderr",
        "timed_out": False,
        "interrupted": False,
        **changes,
    }


def test_capture_retains_real_nonzero_process_output(tmp_path):
    captured = runtime.capture(
        [
            sys.executable,
            "-I",
            "-c",
            "import sys; print('partial'); print('failure', file=sys.stderr); sys.exit(7)",
        ],
        tmp_path,
        5,
    )
    assert captured["exit_code"] == 7
    assert "partial" in captured["stdout"]
    assert "failure" in captured["stderr"]
    assert not captured["timed_out"] and not captured["interrupted"]


@pytest.mark.parametrize("interrupted", [False, True], ids=["timeout", "interrupt"])
def test_capture_kills_process_group_and_retains_partial_output(
    tmp_path, monkeypatch, interrupted
):
    process = Mock(pid=12345, returncode=-signal.SIGKILL)
    exception = (
        KeyboardInterrupt() if interrupted else subprocess.TimeoutExpired("control", 1)
    )
    process.communicate.side_effect = [exception, ("partial stdout", "partial stderr")]
    popen = Mock(return_value=process)
    kill = Mock()
    monkeypatch.setattr(runtime.subprocess, "Popen", popen)
    monkeypatch.setattr(runtime.os, "killpg", kill)
    monkeypatch.setenv("PYTHONPATH", "/private/control")
    monkeypatch.setenv("PYTHONHOME", "/private/control")
    captured = runtime.capture(["synthetic-control"], tmp_path, 1, "input")
    kill.assert_called_once_with(process.pid, signal.SIGKILL)
    assert captured["stdout"] == "partial stdout"
    assert captured["stderr"] == "partial stderr"
    assert captured["exit_code"] == -signal.SIGKILL
    assert captured["interrupted"] is interrupted
    assert captured["timed_out"] is (not interrupted)
    options = popen.call_args.kwargs
    assert options["start_new_session"] is True
    assert not {"PYTHONPATH", "PYTHONHOME"} & options["env"].keys()
    assert options["env"]["CANARY_PYTHON"] == sys.executable
    assert options["env"]["GIT_CONFIG_GLOBAL"] == "/dev/null"
    assert options["env"]["GIT_CONFIG_NOSYSTEM"] == "1"
    process.communicate.assert_any_call("input", timeout=1)


def configuration(argv):
    return tomllib.loads(
        "\n".join(argv[i + 1] for i, arg in enumerate(argv) if arg == "-c")
    )


@pytest.mark.parametrize("mode", ["worker", "grader", "sandbox"])
def test_commands_use_restricted_profile_without_legacy_sandbox(
    tmp_path, monkeypatch, mode
):
    capture = Mock(return_value=result())
    monkeypatch.setattr(runtime, "capture", capture)
    output = tmp_path / "reply.json"
    output.write_text("synthetic reply")
    if mode == "sandbox":
        argv = runtime.sandbox_command(tmp_path, ["synthetic-command"])
        assert argv[argv.index("-P") + 1] == "canary"
        assert argv[-2:] == ["--", "synthetic-command"]
    else:
        schema = {"type": "object"} if mode == "grader" else None
        runtime.execute(
            tmp_path,
            "synthetic prompt",
            output,
            {"model": "synthetic-control", "effort": "low", "timeout_seconds": 2},
            schema,
        )
        argv = capture.call_args.args[0]
        assert "--ephemeral" in argv and "resume" not in argv
        assert "--ignore-user-config" in argv and "--ignore-rules" in argv
        assert capture.call_args.args[3] == "synthetic prompt"
        if schema:
            assert json.loads((tmp_path / "response-schema.json").read_text()) == schema
            assert "--output-schema" in argv
    assert "--sandbox" not in argv
    config = configuration(argv)
    if mode != "sandbox":
        assert config["skills"]["include_instructions"] is False
        assert config["orchestrator"]["skills"]["enabled"] is False
        assert config["project_doc_max_bytes"] == 0
        assert config["features"] == {"plugins": False, "apps": False}
    assert "sandbox_mode" not in config
    assert config["default_permissions"] == "canary"
    assert config["approval_policy"] == "never"
    profile = config["permissions"]["canary"]
    assert profile["network"]["enabled"] is False
    fs = profile["filesystem"]
    assert fs[":root"] == fs[":tmpdir"] == fs[":slash_tmp"] == "deny"
    assert fs[":workspace_roots"]["."] == "write"
    assert fs[":workspace_roots"]["skills"] == "read"
    assert str(tmp_path.parent) not in fs
    assert config["shell_environment_policy"]["set"]["TMPDIR"] == str(tmp_path / ".tmp")
    assert config["shell_environment_policy"]["set"]["GIT_CONFIG_GLOBAL"] == "/dev/null"
    assert config["shell_environment_policy"]["set"]["GIT_CONFIG_NOSYSTEM"] == "1"


def test_apple_git_grant_is_limited_to_installed_developer_runtime(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(runtime.sys, "platform", "darwin")
    monkeypatch.setattr(
        runtime.Path,
        "is_dir",
        lambda path: str(path) == "/Library/Developer/CommandLineTools",
    )
    config = configuration(runtime.permission_args(tmp_path))
    fs = config["permissions"]["canary"]["filesystem"]
    assert fs["/Library/Developer/CommandLineTools"] == "read"
    assert (
        not {
            "/Library",
            "/Library/Developer",
            str(runtime.Path.home()),
            str(tmp_path.parent),
        }
        & fs.keys()
    )
    assert fs[":root"] == fs[":tmpdir"] == fs[":slash_tmp"] == "deny"
    assert config["permissions"]["canary"]["network"]["enabled"] is False


@pytest.mark.parametrize(
    "changes,reply,completed",
    [
        ({}, "control", True),
        ({}, None, False),
        ({"exit_code": 3}, "partial", False),
        ({"timed_out": True}, "partial", False),
        ({"interrupted": True}, "partial", False),
    ],
)
def test_execute_does_not_promote_partial_replies(
    tmp_path, monkeypatch, changes, reply, completed
):
    output = tmp_path / "reply.md"
    if reply is not None:
        output.write_text(reply)
    monkeypatch.setattr(runtime, "capture", Mock(return_value=result(**changes)))
    execution = runtime.execute(
        tmp_path,
        "control",
        output,
        {"model": "synthetic-control", "effort": "low", "timeout_seconds": 1},
    )
    assert execution["completed"] is completed
    assert execution["reply"] == reply
    assert execution["stderr"] == "synthetic stderr"
    for key, value in changes.items():
        assert execution[key] == value


@pytest.mark.parametrize(
    "stdout,exit_code,passed",
    [
        (
            json.dumps(
                {
                    "workspace_io": True,
                    "private_read_denied": True,
                    "network_denied": True,
                }
            ),
            0,
            True,
        ),
        (
            json.dumps(
                {
                    "workspace_io": True,
                    "private_read_denied": False,
                    "network_denied": True,
                }
            ),
            0,
            False,
        ),
        (json.dumps({"workspace_io": True, "private_read_denied": True}), 0, False),
        ("malformed", 0, False),
        (
            json.dumps(
                {
                    "workspace_io": True,
                    "private_read_denied": True,
                    "network_denied": True,
                }
            ),
            1,
            False,
        ),
    ],
)
def test_probe_requires_all_boundary_checks(
    tmp_path, monkeypatch, stdout, exit_code, passed
):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    private = tmp_path / "private"
    private.write_text("control")
    monkeypatch.setattr(
        runtime,
        "capture",
        Mock(return_value=result(stdout=stdout, exit_code=exit_code)),
    )
    assert runtime.probe(workspace, private)["passed"] is passed


@pytest.mark.parametrize("location", ["missing", "inside"])
def test_probe_rejects_invalid_private_target_before_execution(
    tmp_path, monkeypatch, location
):
    capture = Mock(side_effect=AssertionError("must reject before execution"))
    monkeypatch.setattr(runtime, "capture", capture)
    private = tmp_path / "private"
    if location == "inside":
        private.write_text("control")
    with pytest.raises(ValueError):
        runtime.probe(tmp_path, private)
    capture.assert_not_called()

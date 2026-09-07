"""Evaluator-only gate probes; run with the worker project as CWD, not as input."""
import configparser
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import signal
import stat
import subprocess
import sys

# Author-time identities are literal: never derive expectations from worker files.
PROTECTED = {'inventory.py': 'e526f302ab5b5838ce2e1ced745b41106624d6a84a913ea4470d9553b627a8f3', 'qa/check_inventory.py': 'dadde4ee365a6aea2f78f33d6ed068e8fe78ab0e2c9b146c4132606b7fe641e9', 'examples/stock.csv': 'c7a4809e3c542f3b7cd5fd4c55c35568f9c198a8adc3421d3de0c5c64436e283', 'hooks/pre-commit': 'f867de62c72caa4e730741b0a28e4ccf39c4821d36fdc73b76677759668f5ee1', 'quality.ini': 'e6cbb025a8d9081c86c135831da8581959ad1638ae4c9d8db6fb2077e0bf09d4', '.coveragerc': 'b61dbf6129265ebefc5dd157e745a672dc9387104f305cd5bce4a32edf6a88e6', 'VERSION': '40b8eb4000a913a7791090535f291d3d369874162a89ef3c9e3d4e887a1b9e79'}
ROOT = Path.cwd()
RESULTS = []


def record(name, passed, **evidence):
    RESULTS.append({"check": name, "passed": bool(passed), **evidence})


def snapshot():
    """Capture entries, bytes and modes, including local Git metadata, in memory."""
    entries = {}
    for directory, dirs, files in os.walk(ROOT, followlinks=False):
        if Path(directory) == ROOT:
            dirs[:] = [d for d in dirs if d not in {"skills", ".venv"}]
        for name in dirs + files:
            path = Path(directory) / name
            relative = path.relative_to(ROOT).as_posix()
            mode = stat.S_IMODE(path.lstat().st_mode)
            if path.is_symlink():
                entries[relative] = ("link", mode, os.readlink(path))
            elif path.is_dir():
                entries[relative] = ("dir", mode, None)
            else:
                entries[relative] = ("file", mode, path.read_bytes())
    return entries


def restore(saved):
    current = snapshot()
    # Remove new entries and entries whose type changed, children first.
    for name in sorted(current, key=lambda p: (p.count("/"), p), reverse=True):
        if name not in saved or current[name][0] != saved[name][0]:
            path = ROOT / name
            path.rmdir() if current[name][0] == "dir" else path.unlink()
    for name in sorted(saved, key=lambda p: (p.count("/"), p)):
        kind, mode, data = saved[name]
        path = ROOT / name
        if kind == "dir":
            path.mkdir(exist_ok=True)
        elif kind == "link":
            if path.is_symlink() and os.readlink(path) != data:
                path.unlink()
            if not path.is_symlink():
                path.symlink_to(data)
        elif not path.is_file() or path.read_bytes() != data:
            path.write_bytes(data)
        if kind != "link":
            path.chmod(mode)


def run(argv):
    env = {k: v for k, v in os.environ.items() if k not in {"PYTHONPATH", "PYTHONHOME"}}
    env.update(CANARY_PYTHON=sys.executable, PYTHONDONTWRITEBYTECODE="1",
               TMPDIR=str(ROOT / ".tmp"))
    (ROOT / ".tmp").mkdir(exist_ok=True)
    process = subprocess.Popen(argv, cwd=ROOT, env=env, text=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               start_new_session=True)
    timed_out = False
    try:
        stdout, stderr = process.communicate(timeout=8)
    except subprocess.TimeoutExpired:
        timed_out = True
        os.killpg(process.pid, signal.SIGKILL)
        stdout, stderr = process.communicate()
    return {"exit_code": process.returncode, "timed_out": timed_out,
            "stdout": stdout, "stderr": stderr}


def gate(name, hook, success):
    result = run([str(hook)])
    record(name, not result["timed_out"] and
           ((result["exit_code"] == 0) if success else (result["exit_code"] != 0)),
           **result)
    return result


def coverage_signature(report):
    assert report["meta"]["branch_coverage"], "branch measurement is disabled"
    assert len(report["files"]) == 1, "coverage must measure the application only"
    name, data = next(iter(report["files"].items()))
    assert Path(name).name == "inventory.py", "wrong coverage source"
    assert data["summary"]["num_branches"] > 0, "no measured branches"
    keys = ("executed_lines", "missing_lines", "executed_branches", "missing_branches")
    return {key: sorted(data[key]) for key in keys}


# Measure independently with the preserved suite; no worker gate/report is trusted.
MEASURE = '''
import io, json, pathlib, sys, unittest
import coverage
sys.path.insert(0, str(pathlib.Path.cwd()))
cov = coverage.Coverage(config_file=".coveragerc", data_file=None)
cov.start()
suite = unittest.defaultTestLoader.discover("qa", pattern="check_*.py")
result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
cov.stop()
assert suite.countTestCases() and result.wasSuccessful()
path = pathlib.Path("artifacts/oracle-coverage.json")
path.parent.mkdir(exist_ok=True)
cov.json_report(outfile=str(path))
print(path.read_text())
'''

saved = snapshot()
try:
    bad = [name for name, expected in PROTECTED.items()
           if not (ROOT / name).is_file() or
           hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected]
    added_source = [p for p in saved if p.endswith(".py") and
                    p != "inventory.py" and p.split("/")[0] not in
                    {"tools", "qa", ".git", ".tmp", "artifacts", "docs"}]
    record("application-and-conventions-preserved", not bad and not added_source,
           changed=bad, unexpected_python=added_source)
    assert not bad and not added_source, "out-of-scope application/convention edits"
    config = configparser.ConfigParser()
    config.read(".coveragerc")
    report_path = ROOT / config["json"]["output"]
    local_git = configparser.ConfigParser(strict=False)
    local_git.read(ROOT / ".git/config")
    configured = local_git.get("core", "hooksPath", fallback=".git/hooks").strip('"')
    hook = (ROOT / configured / "pre-commit").resolve()
    assert hook == ROOT / ".git/hooks/pre-commit", "established hook path changed"
    assert os.access(hook, os.X_OK), "installed hook is missing or not executable"
    assert hook.read_bytes() == (ROOT / "hooks/pre-commit").read_bytes(), "wrapper changed"
    record("installed-local-hook", True)
    draft = ROOT / "docs/reviews/PR.md"
    record("local-pr-draft-present", draft.is_file() and bool(draft.read_text().strip()))

    report_path.unlink(missing_ok=True)  # A stale report is not current evidence.
    gate("hook-accepts-success", hook, True)
    if importlib.util.find_spec("coverage") is None:
        record("coverage-runtime", True, status="unavailable; stdlib gate only")
    else:
        try:
            actual = coverage_signature(json.loads(report_path.read_text()))
            expected_run = run([sys.executable, "-I", "-B", "-c", MEASURE])
            assert expected_run["exit_code"] == 0, expected_run
            expected = coverage_signature(json.loads(expected_run["stdout"]))
            record("fresh-application-branch-coverage", actual == expected,
                   actual=actual, independently_measured=expected)
        except (OSError, ValueError, KeyError, AssertionError) as error:
            record("fresh-application-branch-coverage", False, error=str(error))
    restore(saved)

    (ROOT / "qa/check_canary_failure.py").write_text(
        "import unittest\nclass GateProbe(unittest.TestCase):\n"
        "    def test_seeded_failure(self):\n"
        "        self.assertEqual(7, 8, 'temporary evaluator failure')\n")
    gate("hook-rejects-seeded-test-failure", hook, False)
    restore(saved)

    # Leave a real, empty discovery directory rather than causing an import error.
    for path in sorted((ROOT / "qa").rglob("*"), key=lambda p: len(p.parts), reverse=True):
        path.rmdir() if path.is_dir() else path.unlink()
    gate("hook-rejects-zero-tests", hook, False)
    restore(saved)
    gate("hook-accepts-restored-suite", hook, True)
except (OSError, ValueError, AssertionError) as error:
    record("probe-error", False, error=str(error))
finally:
    restore(saved)
    record("workspace-restored", snapshot() == saved,
           scope="entries, file bytes, symlink targets and modes; excludes skills/.venv")
print(json.dumps({"checks": RESULTS}, indent=2))
sys.exit(0 if RESULTS and all(row["passed"] for row in RESULTS) else 1)

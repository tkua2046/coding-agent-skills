"""Exercise the copied Python hooks through real commits in an isolated repo."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from tools.evidence import write_report

ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "skills/dev-workflow/assets/python"
REPORTS = ROOT / "artifacts/hook-trials"


def main() -> None:
    work = Path(tempfile.mkdtemp(prefix="skill-hook-trial-"))
    records = []
    outcomes = {}
    report = {
        "kind": "real local Git/hook execution in an isolated fixture",
        "status": "running",
        "cwd": str(work),
        "commands": records,
        "outcomes": outcomes,
    }

    def run(label, args, expected=None):
        result = subprocess.run(
            [str(a) for a in args],
            cwd=work,
            text=True,
            capture_output=True,
            timeout=120,
        )
        records.append(
            {
                "label": label,
                "argv": [str(a) for a in args],
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        )
        if expected == "pass":
            assert result.returncode == 0, records[-1]
        elif expected == "fail":
            assert result.returncode != 0, records[-1]
        return result

    try:
        report["sample_hashes"] = {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in SAMPLE.iterdir()
            if p.is_file()
        }
        shutil.copytree(SAMPLE, work, dirs_exist_ok=True)
        with (work / ".gitignore").open("a") as stream:
            stream.write(".fail\n.saved-tests/\n")
        (work / "app.py").write_text(
            'def classify(value):\n    if value > 0:\n        return "positive"\n'
            '    return "other"\n\ndef unused():\n    return "uncovered"\n'
        )
        (work / "tests").mkdir()
        (work / "tests/test_existing.py").write_text(
            "from pathlib import Path\nfrom app import classify\n\n"
            'def test_positive():\n    assert classify(1) == "positive"\n\n'
            'def test_unchanged_can_fail():\n    assert not Path(".fail").exists()\n'
        )
        (work / "tests/test_changed.py").write_text(
            "from app import classify\n\ndef test_other():\n"
            '    assert classify(0) == "other"\n'
        )
        (work / "README.md").write_text("# Hook fixture\n")
        run("init", ["git", "init", "-q", "-b", "main"], "pass")
        run("identity", ["git", "config", "user.name", "Skill Trial"], "pass")
        run(
            "identity",
            ["git", "config", "user.email", "skill-trial@example.invalid"],
            "pass",
        )
        ruff = ROOT / ".venv/bin/ruff"
        hook = ROOT / ".venv/bin/pre-commit"
        run("prepare-format", [ruff, "check", "--fix", "."], "pass")
        run("prepare-format", [ruff, "format", "."], "pass")
        run("install-hooks", [hook, "install", "--install-hooks"], "pass")
        run("stage-baseline", ["git", "add", "."], "pass")
        result = run("passing-baseline", ["git", "commit", "-m", "Baseline"], "pass")
        assert "Full test suite with coverage" in result.stdout + result.stderr
        outcomes["passing_baseline"] = True

        (work / ".fail").touch()
        changed = work / "tests/test_changed.py"
        changed.write_text(changed.read_text() + "\n# This passing test is staged.\n")
        run("stage-passing-test", ["git", "add", "tests/test_changed.py"], "pass")
        result = run(
            "unchanged-failure",
            ["git", "commit", "-m", "Must reject unchanged failing test"],
            "fail",
        )
        assert "test_unchanged_can_fail" in result.stdout + result.stderr
        outcomes["unchanged_failure_blocks_commit"] = True

        run(
            "restore-test",
            ["git", "restore", "--staged", "--worktree", "tests/test_changed.py"],
            "pass",
        )
        (work / "README.md").write_text("# Hook fixture\n\nDocumentation only.\n")
        run("stage-docs", ["git", "add", "README.md"], "pass")
        result = run("docs-only-failure", ["git", "commit", "-m", "Docs only"], "fail")
        assert "test_unchanged_can_fail" in result.stdout + result.stderr
        outcomes["docs_only_runs_suite"] = True
        (work / ".fail").unlink()
        run("passing-control", ["git", "commit", "-m", "Docs pass"], "pass")
        outcomes["passing_control"] = True

        (work / "tests").rename(work / ".saved-tests")
        run("stage-empty-suite", ["git", "add", "-u"], "pass")
        result = run(
            "zero-tests", ["git", "commit", "-m", "Must reject no tests"], "fail"
        )
        assert "collected 0 items" in result.stdout + result.stderr
        outcomes["zero_tests_block_commit"] = True
        (work / ".saved-tests").rename(work / "tests")
        run("restore-suite", ["git", "add", "tests"], "pass")

        app = work / "app.py"
        app.write_text("import os\n\n" + app.read_text())
        run("stage-lint-fix", ["git", "add", "app.py"], "pass")
        result = run(
            "ruff-fix-needs-restage", ["git", "commit", "-m", "Lint trial"], "fail"
        )
        assert "ruff check" in result.stdout + result.stderr
        assert "import os" not in app.read_text()
        outcomes["ruff_fix_changes_candidate"] = True
        (work / "README.md").write_text("# Hook fixture\n\nRestaged after review.\n")
        run("restage", ["git", "add", "."], "pass")
        run("final-control", ["git", "commit", "-m", "Reviewed fixes"], "pass")
        outcomes["restaged_commit_passes"] = True

        run(
            "coverage-json",
            [
                ROOT / ".venv/bin/python",
                "-m",
                "coverage",
                "json",
                "-o",
                "coverage.json",
            ],
            "pass",
        )
        coverage = json.loads((work / "coverage.json").read_text())
        app_report = coverage["files"]["app.py"]
        assert app_report["summary"]["num_branches"] > 0
        assert app_report["missing_lines"]
        outcomes["source_branches_and_missing_code_reported"] = True
        report["coverage"] = coverage
        report["status"] = "passed"
    except BaseException as exc:
        report["status"] = "failed"
        report["error"] = {"type": type(exc).__name__, "message": str(exc)}
        raise
    finally:
        saved = write_report(REPORTS, report)
        print(f"Evidence: {saved}")
    print(json.dumps(outcomes, indent=2))


if __name__ == "__main__":
    main()

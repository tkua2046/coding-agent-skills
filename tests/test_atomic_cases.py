"""Exercise scoped fixture contracts, not model behavior or semantic grades."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from uuid import uuid4

import pytest

from tools import canary

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "evals/cases"
RECORDS = ROOT / "artifacts/atomic-coverage/fixture-controls" / uuid4().hex


def fixture(tmp_path, name):
    workspace = tmp_path / name
    workspace.mkdir()
    case = canary.cases(ROOT)[name]
    head = canary.init_fixture(workspace, canary.files(CASES / name / "fixture"))
    if case.get("hook"):
        target = workspace / ".git/hooks/pre-commit"
        shutil.copyfile(workspace / case["hook"], target)
        target.chmod(0o755)
    return workspace, case, head


def oracle(workspace, case, expected):
    source = CASES / case["id"] / "oracle.py"
    # Keep measured application coverage independent of the repository's own
    # pytest-cov subprocess instrumentation.
    env = {k: v for k, v in os.environ.items() if not k.startswith("COVERAGE")}
    env.update(CANARY_PYTHON=sys.executable, PYTHONDONTWRITEBYTECODE="1")
    result = subprocess.run(
        [sys.executable, "-I", "-B", "-c", source.read_text()],
        cwd=workspace,
        env=env,
        text=True,
        capture_output=True,
        timeout=55,
    )
    RECORDS.mkdir(parents=True, exist_ok=True)
    (RECORDS / f"{case['id']}-{uuid4().hex}.json").write_text(
        json.dumps(
            {
                "case": case["id"],
                "kind": "authored fixture oracle control; no model",
                "oracle_sha256": canary.digest(source.read_bytes()),
                "candidate": {
                    str(p.relative_to(workspace)): p.read_text()
                    for p in workspace.rglob("*")
                    if p.is_file()
                    and not any(
                        x in p.relative_to(workspace).parts
                        for x in (".git", "artifacts", "__pycache__")
                    )
                },
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "expected_success": expected,
            },
            indent=2,
        )
        + "\n"
    )
    assert (result.returncode == 0) == expected, result.stdout + result.stderr


@pytest.mark.parametrize("state", ["partial", "complete"])
@pytest.mark.parametrize("kind", ["design", "plan"])
def test_rechecks_have_frozen_prerequisites_and_preserve_them(tmp_path, kind, state):
    name = f"smoke-{kind}-recheck-{state}"
    workspace, case, head = fixture(tmp_path, name)
    initial = canary.files(workspace)
    assert len(case["phases"]) == 1 and "overlay" not in case["phases"][0]
    assert (workspace / "docs/history/R1.md").is_file()
    assert (workspace / "reviews/prior.md").is_file()
    # Structural checks allow a report, but do not pretend to grade its verdict.
    (workspace / "REVIEW.md").write_text("An authored report; semantics ungraded.\n")
    assert all(
        r["status"] == "pass"
        for r in canary.deterministic(case, CASES / name, workspace, initial, head)
    )
    (workspace / "reviews/prior.md").write_text("Replaced failed review with ready.\n")
    results = canary.deterministic(case, CASES / name, workspace, initial, head)
    assert next(r for r in results if r["id"] == "source-preserved")["status"] == "fail"


@pytest.mark.parametrize("mutation", ["partial", "valid-regression", "default-only"])
def test_repair_oracle_rejects_partial_or_regressed_behavior(tmp_path, mutation):
    workspace, case, _ = fixture(tmp_path, "smoke-fix-finding")
    fixed = (CASES / "smoke-code-review-ready/fixture/session.py").read_text()
    oracle(workspace, case, False)  # Existing cursor-only repair is insufficient.
    (workspace / "session.py").write_text(fixed)
    oracle(workspace, case, True)
    if mutation == "partial":
        broken = fixed.replace(
            'if not isinstance(command, str) or command not in {"next", "previous"}:',
            'self.selection = "closed"\n        if not isinstance(command, str) or command not in {"next", "previous"}:',
        )
    elif mutation == "valid-regression":
        broken = fixed.replace('1 if command == "next" else -1', "1")
    else:
        broken = fixed.replace(
            'raise ValueError("unknown command")',
            'self.cursor = 4\n            self.selection = "open"\n'
            '            raise ValueError("unknown command")',
        )
    (workspace / "session.py").write_text(broken)
    oracle(workspace, case, False)


@pytest.mark.parametrize(
    "case_id",
    [
        "smoke-code-review-ready",
        "smoke-code-recheck-complete",
        "smoke-code-review-required-tests",
    ],
)
def test_sufficient_review_fixture_honors_unknown_command_contract(case_id):
    path = CASES / case_id / "fixture/session.py"
    namespace = {}
    exec(compile(path.read_text(), str(path), "exec"), namespace)
    session = namespace["Session"]
    for command in ("bogus", [], {}, None, 0):
        state = session()
        state.cursor, state.selection = 11, "selected"
        with pytest.raises(ValueError):
            state.apply(command)
        assert (state.cursor, state.selection) == (11, "selected")
    for command, expected in (("next", 12), ("previous", 10)):
        state = session()
        state.cursor, state.selection = 11, "selected"
        state.apply(command)
        assert (state.cursor, state.selection) == (expected, "closed")


def test_installed_hook_controls_include_doc_only_failure_and_empty_suite(tmp_path):
    workspace, case, _ = fixture(tmp_path, "smoke-setup-hook")
    oracle(workspace, case, False)
    correct = (CASES / "workflow-setup/fixture/tools/check.py").read_text()
    (workspace / "tools/check.py").write_text(correct)
    oracle(workspace, case, True)
    # Passing the runner directly cannot mask a broken installed entrypoint.
    (workspace / ".git/hooks/pre-commit").write_text("#!/bin/sh\nexit 0\n")
    oracle(workspace, case, False)


def coverage_command():
    base = (CASES / "workflow-setup/fixture/tools/check.py").read_text()
    return base.replace(
        "    sys.exit(main())",
        "    import coverage\n"
        "    cov = coverage.Coverage(config_file=str(ROOT / '.coveragerc'))\n"
        "    cov.start()\n"
        "    status = main()\n"
        "    cov.stop()\n"
        "    (ROOT / 'artifacts').mkdir(exist_ok=True)\n"
        "    cov.save()\n"
        "    cov.report()\n"
        "    cov.json_report()\n"
        "    sys.exit(status)",
    )


def test_coverage_is_current_app_measurement_not_report_presence(tmp_path):
    workspace, case, _ = fixture(tmp_path, "smoke-setup-coverage")
    oracle(workspace, case, False)
    (workspace / "tools/check.py").write_text(coverage_command())
    oracle(workspace, case, True)
    (workspace / "tools/check.py").write_text(
        coverage_command().replace(
            "return 0 if result.wasSuccessful() else 1", "return 0"
        )
    )
    oracle(workspace, case, False)
    # A stale but previously valid report is not current normal-command coverage.
    (workspace / "tools/check.py").write_text(
        (CASES / "workflow-setup/fixture/tools/check.py").read_text()
    )
    oracle(workspace, case, False)
    (workspace / "tools/check.py").write_text(coverage_command())
    (workspace / ".coveragerc").write_text(
        (workspace / ".coveragerc")
        .read_text()
        .replace("source = inventory", "source = qa")
    )
    oracle(workspace, case, False)


@pytest.mark.parametrize("failure", ["test-fails", "empty"])
def test_coverage_adaptation_retains_gate_failure_behavior(tmp_path, failure):
    workspace, _, _ = fixture(tmp_path, "smoke-setup-coverage")
    (workspace / "tools/check.py").write_text(coverage_command())
    if failure == "test-fails":
        (workspace / "qa/check_broken.py").write_text(
            "import unittest\nclass Broken(unittest.TestCase):\n"
            " def test_failure(self): self.assertEqual(1,2)\n"
        )
    else:
        shutil.rmtree(workspace / "qa")
        (workspace / "qa").mkdir()
    result = subprocess.run(
        [sys.executable, "tools/check.py"],
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert result.returncode != 0
    assert ("FAILED" if failure == "test-fails" else "no tests discovered") in (
        result.stdout + result.stderr
    )


def test_version_preparation_preserves_history_and_moves_completed_notes(tmp_path):
    workspace, case, _ = fixture(tmp_path, "smoke-version-notes")
    oracle(workspace, case, False)
    (workspace / "VERSION").write_text("1.3.0\n")
    original = (workspace / "CHANGELOG.md").read_text()
    updated = original.replace(
        "## Unreleased", "## Unreleased\n\n## 1.3.0 - 2026-09-07"
    )
    (workspace / "CHANGELOG.md").write_text(updated)
    oracle(workspace, case, True)
    (workspace / "CHANGELOG.md").write_text(updated.split("## 1.2.0")[0])
    oracle(workspace, case, False)


@pytest.mark.parametrize("mutation", ["second-bump", "duplicate-notes", "history-loss"])
def test_prepared_version_oracle_accepts_reuse_and_rejects_regressions(
    tmp_path, mutation
):
    workspace, case, _ = fixture(tmp_path, "smoke-version-prepared")
    oracle(workspace, case, True)
    notes = workspace / "CHANGELOG.md"
    if mutation == "second-bump":
        (workspace / "VERSION").write_text("1.4.0\n")
    elif mutation == "duplicate-notes":
        notes.write_text(
            notes.read_text().replace(
                "## Unreleased", "## Unreleased\n\n## 1.3.0 - 2026-09-07"
            )
        )
    else:
        notes.write_text(notes.read_text().split("## 1.2.0")[0])
    oracle(workspace, case, False)


@pytest.mark.parametrize("case_id", ["smoke-version-notes", "smoke-version-prepared"])
def test_release_history_check_allows_harmless_final_blank_lines(tmp_path, case_id):
    workspace, case, _ = fixture(tmp_path, case_id)
    notes = workspace / "CHANGELOG.md"
    if (workspace / "VERSION").read_text().strip() == "1.2.0":
        (workspace / "VERSION").write_text("1.3.0\n")
        notes.write_text(
            notes.read_text().replace(
                "## Unreleased", "## Unreleased\n\n## 1.3.0 - 2026-09-07"
            )
        )
    notes.write_text(notes.read_text() + "\n\n")
    oracle(workspace, case, True)
    notes.write_text(notes.read_text().replace("2026-08-20", "2026-09-07"))
    oracle(workspace, case, False)


def test_retry_observations_separate_identity_from_publication_status():
    data = {
        state: json.loads(
            (
                CASES / f"smoke-release-retry-{state}/fixture/OBSERVATION.json"
            ).read_text()
        )
        for state in ("matching", "conflicting", "unknown")
    }
    same = data["matching"]
    assert same["actual_tag_commit"] == same["published_source_commit"]
    assert same["actual_tag_commit"] == same["candidate_commit"]
    assert same["published_artifact_sha256"] == same["candidate_artifact_sha256"]
    conflict = data["conflicting"]
    assert conflict["service_status"] == "completed"
    assert conflict["actual_tag_commit"] != conflict["candidate_commit"]
    assert (
        conflict["published_artifact_sha256"] != conflict["candidate_artifact_sha256"]
    )
    unknown = data["unknown"]
    assert unknown["actual_tag_commit"] == unknown["candidate_commit"]
    assert unknown["service_status"] == "unknown"
    assert unknown["published_artifact_sha256"] is None

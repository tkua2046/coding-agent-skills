"""Scoped runner/fixture controls; real LLM behavior is a separate test layer."""

# ruff: noqa: F811 — pytest injects imported fixtures by parameter name.

import copy
import json
import shutil
from pathlib import Path

import pytest

from tests.test_canary import (
    CONFIG,
    ENV,
    REPO,
    fake_runtime,  # noqa: F401
    forbid_model_calls,  # noqa: F401
    make_tiny_root,
    put_json,
    refresh_manifest,
)
from tools import canary


@pytest.fixture
def scoped_trial(tmp_path):
    trial = make_tiny_root(tmp_path, with_git=True)
    path = trial.root / "evals/graders/calibration.json"
    data = canary.read_json(path)
    for index, example in enumerate(data["examples"]):
        example.update(
            id=f"control-{index}",
            case_source={"id": "control", "rubric_version": 1},
            rubric=copy.deepcopy(data["rubric"]),
            expected_criteria={"required": example["expected"]},
        )
    data["examples"].append(
        {"id": "unrelated", "request": "Must not be selected", "expected": "fail"}
    )
    put_json(path, data)
    return trial


def calibrate(trial):
    path = canary.calibration(trial.root, CONFIG, case_id="control")
    assert canary.read_json(path)["status"] == "pass"
    return path


def test_case_selection_and_unrelated_edits_preserve_scoped_behavior(
    scoped_trial, fake_runtime
):
    trial = scoped_trial
    report = calibrate(trial)
    assert len(fake_runtime.calls) == 3
    assert canary.read_json(report)["kind"] == "case-calibration"
    run = canary.run_case(trial.root, "control", CONFIG, CONFIG, report)
    assert canary.verified_behavior(trial.root, run, trial.case)["status"] == "pass"
    path = trial.root / "evals/graders/calibration.json"
    data = canary.read_json(path)
    data["examples"][-1]["request"] += " changed, still unrelated"
    data["examples"].append({"case_source": {"id": "another-case"}})
    put_json(path, data)
    before = len(fake_runtime.calls)
    assert canary.check_calibration(trial.root, report, CONFIG, ENV, case_id="control")
    assert canary.verified_behavior(trial.root, run, trial.case)["status"] == "pass"
    assert len(fake_runtime.calls) == before
    resumed = canary.run_case(trial.root, "control", CONFIG, CONFIG, report)
    assert canary.verified_behavior(trial.root, resumed, trial.case)["status"] == "pass"


def test_scoped_evidence_cannot_authorize_another_case_or_release(
    scoped_trial, fake_runtime
):
    trial = scoped_trial
    report = calibrate(trial)
    with pytest.raises(ValueError, match="another case or release"):
        canary.check_calibration(trial.root, report, CONFIG, ENV)
    destination = trial.root / "evals/cases/other"
    shutil.copytree(trial.root / "evals/cases/control", destination)
    other = copy.deepcopy(trial.case)
    other["id"] = "other"
    put_json(destination / "case.json", other)
    before = len(fake_runtime.calls)
    denied = canary.run_case(trial.root, "other", CONFIG, CONFIG, report)
    assert "another case" in canary.read_json(denied)["error"]
    assert len(fake_runtime.calls) == before
    shutil.rmtree(destination)
    # Both versions really traverse the runner, but a scoped calibration must
    # never be promoted to release authorization even with a complete pair.
    old = canary.run_case(trial.root, "control", CONFIG, CONFIG, report, trial.baseline)
    new = canary.run_case(trial.root, "control", CONFIG, CONFIG, report)
    assert canary.verified_behavior(trial.root, old, trial.case)["status"] == "fail"
    assert canary.verified_behavior(trial.root, new, trial.case)["status"] == "pass"
    gate = canary.release_gate(trial.root, [old, new], trial.baseline)
    assert gate["status"] == "fail"
    assert any("cannot authorize another case or release" in e for e in gate["errors"])


@pytest.mark.parametrize("problem", ["missing-contrast", "stale-rule", "stale-source"])
def test_incomplete_or_stale_controls_stop_before_model_call(scoped_trial, problem):
    trial = scoped_trial
    path = trial.root / "evals/graders/calibration.json"
    data = canary.read_json(path)
    if problem == "missing-contrast":
        data["examples"] = [data["examples"][0]]
    elif problem == "stale-rule":
        data["examples"][0]["rubric"]["criteria"][0]["pass_when"] += " different"
    else:
        data["examples"][0]["input_sources"] = {
            "result.txt": "evals/cases/control/fixture/keep/original.txt"
        }
    put_json(path, data)
    report = canary.calibration(trial.root, CONFIG, case_id="control")
    assert canary.read_json(report)["status"] == "inconclusive"
    assert not list(report.parent.glob("*-reply.execution.json"))
    assert "error" in canary.read_json(report)


@pytest.mark.parametrize("changed", ["control", "rubric", "grader", "engine"])
def test_relevant_changes_invalidate_case_calibration(
    scoped_trial, fake_runtime, changed
):
    trial = scoped_trial
    report = calibrate(trial)
    paths = {
        "control": "evals/graders/calibration.json",
        "rubric": "evals/cases/control/rubric.json",
        "grader": "evals/graders/review.md",
        "engine": "tools/canary_runtime.py",
    }
    path = trial.root / paths[changed]
    if changed == "control":
        value = canary.read_json(path)
        value["examples"][0]["request"] += " changed requirement"
        put_json(path, value)
    elif changed == "rubric":
        value = canary.read_json(path)
        value["criteria"][0]["fail_when"] += " changed"
        put_json(path, value)
    else:
        path.write_text(path.read_text() + "\nChanged relevant dependency\n")
    with pytest.raises(ValueError):
        canary.check_calibration(trial.root, report, CONFIG, ENV, case_id="control")


@pytest.mark.parametrize("changed", ["source", "skill"])
def test_scoped_behavior_revalidation_binds_worker_inputs(
    scoped_trial, fake_runtime, changed
):
    trial = scoped_trial
    report = calibrate(trial)
    run = canary.run_case(trial.root, "control", CONFIG, CONFIG, report)
    path = trial.root / (
        "skills/control/SKILL.md"
        if changed == "skill"
        else "evals/cases/control/fixture/keep/original.txt"
    )
    path.write_text("changed after worker execution")
    with pytest.raises(ValueError, match="Scoped behavior inputs"):
        canary.verified_behavior(trial.root, run, trial.case)


@pytest.mark.parametrize("defect", ["bad-quote", "incomplete", "failed-judgment"])
def test_scoped_replay_rejects_invalid_evidence(scoped_trial, fake_runtime, defect):
    trial = scoped_trial
    report = calibrate(trial)
    grade_path = report.parent / "0-grade.json"
    execution_path = report.parent / "0-reply.execution.json"
    grade = canary.read_json(grade_path)
    execution = canary.read_json(execution_path)
    if defect == "incomplete":
        execution["completed"] = False
    else:
        if defect == "bad-quote":
            grade["criteria"][0]["evidence"][0]["quote"] = "invented source quotation"
        else:
            grade["criteria"][0]["status"] = "fail"
        put_json(grade_path, grade)
        execution["reply"] = json.dumps(grade)
    put_json(execution_path, execution)
    refresh_manifest(report)
    with pytest.raises(ValueError):
        canary.check_calibration(trial.root, report, CONFIG, ENV, case_id="control")


def test_case_calibration_cli_and_mutually_exclusive_scope(
    scoped_trial, fake_runtime, monkeypatch, capsys
):
    monkeypatch.setattr(canary, "ROOT", scoped_trial.root)
    args = [
        "calibrate",
        "--case",
        "control",
        "--model",
        CONFIG["model"],
        "--effort",
        "low",
        "--timeout",
        "1",
    ]
    assert canary.main(args) == 0
    report = canary.read_json(Path(capsys.readouterr().out.strip()))
    assert report["kind"] == "case-calibration" and report["case_id"] == "control"
    with pytest.raises(SystemExit) as exc:
        canary.main([*args, "--group", "diagnostic"])
    assert exc.value.code == 2


@pytest.mark.parametrize(
    "operation,skill", [("design", "feature-design"), ("plan", "implementation-plan")]
)
def test_independent_review_case_controls_and_preservation(tmp_path, operation, skill):
    name = f"smoke-{operation}-review-ready"
    catalog = canary.cases(REPO)
    case = catalog[name]
    assert case["skills"] == [skill] and case["tier"] == "smoke"
    assert "smoke-review-ready" not in catalog
    heavy = canary.select_cases(catalog, tier="heavy")
    assert "review-ready" in heavy and name not in heavy
    archive = REPO / "evals/archived-cases/smoke-review-ready"
    assert (archive / "case.json").is_file()
    inputs = canary.case_calibration_inputs(REPO, name)
    # These are authored controls, not worker/scorer success assertions.
    positive = next(e for e in inputs["examples"] if e["expected"] == "pass")
    case_dir = REPO / "evals/cases" / name
    workspace = tmp_path / "case"
    workspace.mkdir()
    head = canary.init_fixture(workspace, canary.files(case_dir / "fixture"))
    initial = canary.files(workspace)
    (workspace / "REVIEW.md").write_text(positive["artifacts"]["REVIEW.md"])
    assert all(
        r["status"] == "pass"
        for r in canary.deterministic(case, case_dir, workspace, initial, head)
    )
    (
        workspace / "docs" / ("DESIGN.md" if operation == "design" else "PLAN.md")
    ).write_text("The reviewer improperly rewrote the reviewed artifact.")
    failed = canary.deterministic(case, case_dir, workspace, initial, head)
    assert next(r for r in failed if r["id"] == "source-preserved")["status"] == "fail"
    assert (workspace / "docs/DESIGN.md").exists()
    assert (workspace / "docs/PLAN.md").exists() == (operation == "plan")

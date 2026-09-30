"""Test authored calibration fixtures, not an LLM worker or scorer."""

import json
import shutil
import subprocess
import sys

import pytest

from tools import canary

ROOT = canary.ROOT


@pytest.mark.parametrize("case_id", ["v3-maintenance", "bounded-delivery"])
@pytest.mark.parametrize(
    "variant,success", [("usable", True), ("equivalent", True), ("material", False)]
)
def test_authored_feature_controls_have_their_declared_behavior(
    tmp_path, case_id, variant, success
):
    examples = canary.read_json(ROOT / "evals/graders/calibration.json")["examples"]
    sample = next(e for e in examples if e.get("id") == f"{case_id}-{variant}")
    source = ROOT / "evals/cases" / case_id
    shutil.copytree(source / "fixture", tmp_path, dirs_exist_ok=True)
    prefix = (
        "02-change-contract/workspace/"
        if case_id == "v3-maintenance"
        else "09-handoff/workspace/"
    )
    canary.write_files(
        tmp_path,
        {
            name.removeprefix(prefix): text.encode()
            for name, text in sample["artifacts"].items()
            if name.startswith(prefix)
        },
    )
    result = subprocess.run(
        [sys.executable, "-B", "-I", "-c", (source / "oracle.py").read_text()],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        timeout=10,
    )
    assert (result.returncode == 0) == success, result.stdout + result.stderr
    if success:
        tests = subprocess.run(
            [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-v"],
            cwd=tmp_path,
            text=True,
            capture_output=True,
            timeout=10,
        )
        assert tests.returncode == 0, tests.stdout + tests.stderr


def test_phase_target_control_does_not_rely_on_total_timeout():
    examples = canary.read_json(ROOT / "evals/graders/calibration.json")["examples"]
    sample = next(e for e in examples if e.get("id") == "v3-maintenance-phase-target")
    case = canary.read_json(ROOT / "evals/cases/v3-maintenance/case.json")
    observation = json.loads(sample["artifacts"]["observations.json"])
    phase_times = observation["phase_elapsed_seconds"]
    assert sum(phase_times.values()) == observation["worker_elapsed_seconds"]
    assert observation["worker_elapsed_seconds"] < case["workflow_target_seconds"]
    assert any(phase_times[p["id"]] > p["target_seconds"] for p in case["phases"])
    assert sample["expected_scores"]["proportionate-effort"] == [2, 2]


@pytest.mark.parametrize(
    "control_id,success",
    [
        ("prepared-version-usable", True),
        ("prepared-version-cosmetic-equivalent", True),
        ("prepared-version-second-bump", False),
        ("prepared-version-history-loss", False),
    ],
)
def test_prepared_version_calibration_has_declared_metadata_behavior(
    tmp_path, control_id, success
):
    examples = canary.read_json(ROOT / "evals/graders/calibration.json")["examples"]
    example = next(e for e in examples if e.get("id") == control_id)
    source = ROOT / "evals/cases/smoke-version-prepared"
    shutil.copytree(source / "fixture", tmp_path, dirs_exist_ok=True)
    canary.write_files(
        tmp_path,
        {
            name.removeprefix("final/"): text.encode()
            for name, text in example["artifacts"].items()
            if name.startswith("final/")
        },
    )
    result = subprocess.run(
        [sys.executable, "-B", "-I", "-c", (source / "oracle.py").read_text()],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        timeout=10,
    )
    assert (result.returncode == 0) == success, result.stdout + result.stderr


def test_prepared_version_scoring_controls_bind_current_case_contract():
    inputs = canary.case_calibration_inputs(ROOT, "smoke-version-prepared")
    examples = {e["id"]: e for e in inputs["examples"]}
    case = canary.read_json(ROOT / "evals/cases/smoke-version-prepared/case.json")
    target = json.loads(
        examples["prepared-version-target"]["artifacts"]["observations.json"]
    )
    hard = json.loads(
        examples["prepared-version-hard-cap"]["artifacts"]["observations.json"]
    )
    assert (
        case["workflow_target_seconds"]
        < target["elapsed_seconds"]
        < case["workflow_budget_seconds"]
    )
    assert hard["elapsed_seconds"] > case["workflow_budget_seconds"]

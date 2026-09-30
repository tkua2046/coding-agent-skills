"""Scoring-contract wiring, not evidence of worker or LLM grading quality."""

# ruff: noqa: F811 — pytest injects the imported fixtures by parameter name.

import copy

import pytest

from tests.test_canary import (  # noqa: F401 — pytest fixtures
    CONFIG,
    ENV,
    REPO,
    fake_runtime,
    forbid_model_calls,
    put_json,
    tiny_root,
)
from tools import canary


def test_scoring_examples_use_current_case_criteria_without_drift():
    data = canary.read_json(REPO / "evals/graders/calibration.json")
    linked = [e for e in data["examples"] if "case_source" in e]
    assert linked
    covered = set()
    contrasts = {}
    for example in linked:
        for artifact, source_path in example.get("input_sources", {}).items():
            source_file = canary.local(REPO, source_path)
            assert source_file.is_relative_to(REPO / "evals/cases")
            assert example["artifacts"][artifact] == source_file.read_text()
        source = example["case_source"]
        rubric = canary.read_json(REPO / "evals/cases" / source["id"] / "rubric.json")
        assert source["rubric_version"] == rubric["version"], example["id"]
        indexed = {c["id"]: c for c in rubric["criteria"]}
        for criterion in example["rubric"]["criteria"]:
            assert criterion == indexed[criterion["id"]], example["id"]
            covered.update(criterion["goals"])
            for goal in criterion["goals"]:
                contrasts.setdefault(goal, set()).add(
                    example["expected_criteria"][criterion["id"]]
                )
        canary.calibration_contract(data, example)
    expected = {
        f"{prefix}{i}"
        for prefix, count in (("A", 6), ("B", 6), ("C", 5), ("D", 6))
        for i in range(1, count + 1)
    }
    assert covered == expected
    assert all({"pass", "fail"} <= contrasts[goal] for goal in expected)


def test_goal_mapping_uses_applicable_skills_and_concrete_criteria():
    prefixes = {
        "feature-design": "A",
        "implementation-plan": "B",
        "stage-development": "C",
        "dev-workflow": "D",
    }
    for name, case in canary.cases(REPO).items():
        allowed = {prefixes[s] for s in case["skills"]}
        rubric = canary.read_json(REPO / "evals/cases" / name / "rubric.json")
        for criterion in rubric["criteria"]:
            assert criterion["goals"], (name, criterion["id"])
            assert all(g[0] in allowed for g in criterion["goals"])


def test_focused_calibration_cannot_authorize_a_worker_or_release(
    tiny_root, fake_runtime
):
    path = tiny_root.root / "evals/graders/calibration.json"
    data = canary.read_json(path)
    data["examples"][0]["group"] = "focused"
    other = copy.deepcopy(data["examples"][0])
    other["group"] = "unselected"
    data["examples"].append(other)
    put_json(path, data)
    report_path = canary.calibration(tiny_root.root, CONFIG, "focused")
    report = canary.verified_record(report_path)
    assert report["status"] == "pass"
    assert report["kind"] == "calibration-sample"
    assert report["matched_controls"] == [True]
    assert len(canary.read_json(report_path.parent / "inputs.json")["examples"]) == 1
    with pytest.raises(ValueError, match="current grader calibration"):
        canary.check_calibration(tiny_root.root, report_path, CONFIG, ENV)


def test_empty_calibration_selection_is_recorded_without_a_model_call(tiny_root):
    path = canary.calibration(tiny_root.root, CONFIG, "missing")
    report = canary.verified_record(path)
    assert report["status"] == "inconclusive"
    assert "Unknown or empty" in report["error"]

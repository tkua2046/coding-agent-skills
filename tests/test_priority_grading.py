"""Numeric scoring and worker budgets, with synthetic evidence and no model calls."""

# ruff: noqa: F811 — pytest injects imported fixtures by parameter name.

import copy
import json

import pytest

from tests.test_canary import (
    CONFIG,
    ENV,
    execution,
    fake_runtime,  # noqa: F401
    forbid_model_calls,  # noqa: F401
    grade_row,
    make_tiny_root,
    put_json,
    refresh_manifest,
)
from tools import canary


def numeric_criterion(name, priority):
    criterion = {
        "id": name,
        "priority": priority,
        "operation": "execute-stage",
        "goals": ["B1"],
        "requirement": "Deliver the requested behavior without losing history.",
        "evidence": ["Produced artifact and actual invocation trace"],
        # Historical flags deliberately conflict: priorities own numeric readiness.
        "required": priority == "P2",
    }
    if priority == "P1":
        criterion["anchors"] = {
            "1": "Core behavior contradicts the request.",
            "2": "Material behavior is missing or the usable target is exceeded.",
            "3": "All required behavior is usable within the declared target.",
            "4": "Usable with supported improvements to recovery and clarity.",
            "5": "All stronger anchors hold with demonstrated transferability.",
        }
    elif priority == "P0":
        criterion["condition"] = "Do not alter the supplied protected skill bundle."
    return criterion


def numeric_rubric():
    return {
        "version": 2,
        "scoring": "priority-v1",
        "criteria": [
            numeric_criterion("quality", "P1"),
            numeric_criterion("efficiency", "P1"),
            numeric_criterion("scope", "P0"),
            numeric_criterion("polish", "P2"),
        ],
    }


def numeric_grade(quality=3, efficiency=3, scope="pass", polish="pass"):
    rows = []
    for name, score, status in (
        (
            "quality",
            quality,
            "inconclusive" if quality is None else "pass" if quality >= 3 else "fail",
        ),
        (
            "efficiency",
            efficiency,
            "inconclusive"
            if efficiency is None
            else "pass"
            if efficiency >= 3
            else "fail",
        ),
        ("scope", None, scope),
        ("polish", None, polish),
    ):
        rows.append({**grade_row(status, name), "score": score})
    return {"criteria": rows}


def validate(grade, tmp_path):
    return canary.validate_grade(
        grade, numeric_rubric(), tmp_path, {"result.txt": b"control"}
    )


@pytest.mark.parametrize(
    "score,status",
    [
        (1, "fail"),
        (2, "fail"),
        (3, "pass"),
        (4, "pass"),
        (5, "pass"),
        (None, "inconclusive"),
    ],
)
def test_scores_derive_status(score, status, tmp_path):
    assert validate(numeric_grade(quality=score), tmp_path) == status


@pytest.mark.parametrize("score", [True, False, 3.0, 0, 6, "3", [], {}])
def test_invalid_score_types_and_bounds(score, tmp_path):
    grade = numeric_grade()
    grade["criteria"][0]["score"] = score
    with pytest.raises(ValueError, match="integer"):
        validate(grade, tmp_path)


@pytest.mark.parametrize(
    "name,score,status",
    [
        ("quality", 2, "pass"),
        ("quality", None, "fail"),
        ("quality", 3, "inconclusive"),
        ("scope", 1, "fail"),
        ("polish", 5, "pass"),
    ],
)
def test_grade_rejects_status_disagreement_and_non_p1_scores(
    name, score, status, tmp_path
):
    grade = numeric_grade()
    next(c for c in grade["criteria"] if c["id"] == name).update(
        score=score, status=status
    )
    with pytest.raises(ValueError):
        validate(grade, tmp_path)


@pytest.mark.parametrize("advice", ["fail", "inconclusive", "pass"])
def test_p2_cannot_block_or_offset_required_failure(advice, tmp_path):
    assert validate(numeric_grade(polish=advice), tmp_path) == "pass"
    assert (
        validate(numeric_grade(quality=2, efficiency=None, polish=advice), tmp_path)
        == "fail"
    )
    assert (
        validate(numeric_grade(quality=None, scope="fail", polish=advice), tmp_path)
        == "fail"
    )
    assert (
        validate(numeric_grade(scope="inconclusive", polish=advice), tmp_path)
        == "inconclusive"
    )


@pytest.mark.parametrize(
    "defect", ["score-missing", "quote", "no-evidence", "missing-row", "duplicate"]
)
def test_numeric_keeps_exact_evidence_and_complete_rows(defect, tmp_path):
    grade = numeric_grade()
    row = grade["criteria"][0]
    if defect == "score-missing":
        row.pop("score")
    elif defect == "quote":
        row["evidence"][0]["quote"] = "invented fact"
    elif defect == "no-evidence":
        row["evidence"] = []
    elif defect == "missing-row":
        grade["criteria"].pop()
    else:
        grade["criteria"].append(copy.deepcopy(row))
    with pytest.raises(ValueError):
        validate(grade, tmp_path)


def test_numeric_schema_requires_score_legacy_shape_unchanged():
    numeric = canary.grade_schema(numeric_rubric())["properties"]["criteria"]["items"]
    legacy = canary.grade_schema({"criteria": [{"id": "binary"}]})["properties"][
        "criteria"
    ]["items"]
    assert (
        "score" in numeric["required"]
        and "null" in numeric["properties"]["score"]["type"]
    )
    assert "score" not in legacy["properties"] and "score" not in legacy["required"]


def control(rubric, kind, grade):
    statuses = {r["id"]: r["status"] for r in grade["criteria"]}
    scores = {
        r["id"]: [r["score"], r["score"]] if r["score"] is not None else None
        for r in grade["criteria"]
    }
    return {
        "id": kind,
        "kind": kind,
        "case_source": {"id": "control", "rubric_version": rubric["version"]},
        "rubric": copy.deepcopy(rubric),
        "request": "Synthetic outcome; assess its supplied evidence.",
        "expected": "fail"
        if "fail" in [statuses[n] for n in ("quality", "efficiency", "scope")]
        else "pass",
        "expected_criteria": statuses,
        "expected_scores": scores,
        "artifacts": {
            "result.txt": "control",
            "synthetic-grade.json": json.dumps(grade),
        },
    }


@pytest.fixture
def numeric_trial(tmp_path):
    trial = make_tiny_root(tmp_path)
    trial.rubric = numeric_rubric()
    trial.case.update(workflow_target_seconds=8, workflow_budget_seconds=10)
    trial.case["check_criteria"] = {
        name: "efficiency"
        if name.endswith(("budget", "target"))
        else "scope"
        if name == "runner.skills-preserved"
        else "quality"
        for name in canary.check_ids(trial.case)
    }
    put_json(trial.root / "evals/cases/control/case.json", trial.case)
    put_json(trial.root / "evals/cases/control/rubric.json", trial.rubric)
    trial.controls = {
        "rubric": trial.rubric,
        "examples": [
            control(trial.rubric, "usable", numeric_grade()),
            control(trial.rubric, "cosmetic-equivalent", numeric_grade(polish="fail")),
            control(trial.rubric, "quality-defect", numeric_grade(quality=2)),
            control(trial.rubric, "efficiency-defect", numeric_grade(efficiency=2)),
            control(trial.rubric, "scope-defect", numeric_grade(scope="fail")),
            control(trial.rubric, "high", numeric_grade(quality=5, efficiency=4)),
        ],
    }
    put_json(trial.root / "evals/graders/calibration.json", trial.controls)
    return trial


@pytest.fixture
def numeric_runtime(fake_runtime, monkeypatch):
    original = fake_runtime.execute

    def execute(workspace, prompt, output, config, schema=None):
        if schema is None:
            return original(workspace, prompt, output, config, schema)
        before = canary.files(workspace)
        # Expected labels and outer control metadata must remain grader-private.
        assert not any(
            any(
                key in data
                for key in (
                    b"expected_scores",
                    b"expected_criteria",
                    b"diagnostic_score_ranges",
                    b"calibration_qualification",
                )
            )
            for data in before.values()
        )
        fake_runtime.calls.append(
            {"schema": schema, "before": before, "output": output, "config": config}
        )
        synthetic = workspace / "artifacts/synthetic-grade.json"
        if synthetic.is_file():
            grade = canary.read_json(synthetic)
        else:
            grade = numeric_grade(polish="fail")
            path = "artifacts/second/reply.md"
            quote = (workspace / path).read_text()
            for row in grade["criteria"]:
                row["evidence"] = [{"path": path, "quote": quote}]
        reply = json.dumps(grade)
        output.write_text(reply)
        return execution(reply)

    monkeypatch.setattr(canary.runtime, "execute", execute)
    return fake_runtime


def calibrate(trial):
    path = canary.calibration(trial.root, CONFIG, case_id="control")
    assert canary.read_json(path)["status"] == "pass", canary.read_json(path)
    return path


@pytest.mark.parametrize(
    "defect",
    [
        "missing-cosmetic",
        "partial-cosmetic",
        "only-cosmetic-pass",
        "missing-p1-defect",
        "missing-p0-defect",
        "high-only-usable",
        "readiness-label",
        "stale-criterion",
        "stale-version",
        "stale-source",
    ],
)
def test_numeric_controls_require_readiness_contrasts_before_calls(
    numeric_trial, defect
):
    trial = numeric_trial
    examples = trial.controls["examples"]
    if defect == "missing-cosmetic":
        examples.pop(1)
    elif defect == "partial-cosmetic":
        example = examples[1]
        example["rubric"]["criteria"].pop()
        example["expected_criteria"].pop("polish")
        example["expected_scores"].pop("polish")
    elif defect == "only-cosmetic-pass":
        examples[:] = [e for e in examples if e["kind"] not in {"usable", "high"}]
    elif defect == "missing-p1-defect":
        examples.pop(2)
    elif defect == "missing-p0-defect":
        examples.pop(4)
    elif defect == "high-only-usable":
        for example in examples:
            for name, bounds in example["expected_scores"].items():
                if bounds == [3, 3]:
                    example["expected_scores"][name] = [4, 5]
    elif defect == "readiness-label":
        examples[2]["expected"] = "pass"
    elif defect == "stale-criterion":
        examples[0]["rubric"]["criteria"][0]["anchors"]["3"] = "Different meaning"
    elif defect == "stale-version":
        examples[0]["case_source"]["rubric_version"] = 1
    else:
        examples[0]["input_sources"] = {
            "result.txt": "evals/cases/control/fixture/keep/original.txt"
        }
    put_json(trial.root / "evals/graders/calibration.json", trial.controls)
    report = canary.calibration(trial.root, CONFIG, case_id="control")
    assert canary.read_json(report)["status"] == "inconclusive"
    assert "error" in canary.read_json(report)
    assert not list(report.parent.glob("*-reply.execution.json"))


@pytest.mark.parametrize(
    "bounds", [[0, 3], [3, 6], [4, 3], [True, 3], [3.0, 3], [2, 3], None, "3", [3]]
)
def test_control_score_range_validation(numeric_trial, bounds):
    example = copy.deepcopy(numeric_trial.controls["examples"][0])
    example["expected_scores"]["quality"] = bounds
    with pytest.raises(ValueError):
        canary.calibration_contract({}, example)


def test_control_score_ranges_and_explicit_null(numeric_trial):
    example = copy.deepcopy(numeric_trial.controls["examples"][0])
    example["expected_scores"]["quality"] = [3, 4]
    canary.calibration_contract({}, example)
    assert canary.calibration_matches(example, numeric_grade(quality=4), "pass")
    assert not canary.calibration_matches(example, numeric_grade(quality=5), "pass")
    example["expected_scores"]["quality"] = None
    example["expected_criteria"]["quality"] = "inconclusive"
    example["expected"] = "inconclusive"
    canary.calibration_contract({}, example)
    assert canary.calibration_matches(
        example, numeric_grade(quality=None), "inconclusive"
    )
    example["expected_scores"].pop("efficiency")
    with pytest.raises(ValueError, match="every P1"):
        canary.calibration_contract({}, example)


def test_readiness_metadata_preserves_exact_matching_and_diagnostics(
    numeric_trial, numeric_runtime
):
    trial = numeric_trial
    trial.case["calibration_qualification"] = "readiness"
    update_case(trial)
    example = trial.controls["examples"][0]
    example["artifacts"]["synthetic-grade.json"] = json.dumps(numeric_grade(quality=5))
    example["expected_scores"]["quality"] = [3, 4]
    example["diagnostic_score_ranges"] = {"quality": [3, 4]}
    controls = trial.root / "evals/graders/calibration.json"
    put_json(controls, trial.controls)
    failed = canary.calibration(trial.root, CONFIG, case_id="control")
    original = failed.read_bytes()
    assert canary.read_json(failed)["status"] == "fail"  # Metadata is no bypass.
    example["expected_scores"]["quality"] = [3, 5]
    put_json(controls, trial.controls)
    passed = calibrate(trial)
    report = canary.read_json(passed)
    inputs = canary.read_json(passed.parent / "inputs.json")
    assert report["kind"] == "case-calibration"
    assert (
        report["calibration_qualification"]
        == inputs["calibration_qualification"]
        == "readiness"
    )
    assert inputs["examples"][0]["diagnostic_score_ranges"] == {"quality": [3, 4]}
    assert failed.read_bytes() == original
    assert canary.check_calibration(trial.root, passed, CONFIG, ENV, case_id="control")
    with pytest.raises(ValueError, match="another case or release"):
        canary.check_calibration(trial.root, passed, CONFIG, ENV)
    report.pop("calibration_qualification")
    put_json(passed, report)
    with pytest.raises(ValueError, match="qualification differs"):
        canary.check_calibration(trial.root, passed, CONFIG, ENV, case_id="control")


@pytest.mark.parametrize(
    "change",
    [
        "range",
        "anchor",
        "target",
        "request",
        "grader",
        "engine",
        "qualification",
        "diagnostics",
    ],
)
def test_scoped_numeric_calibration_cannot_reuse_stale_inputs(
    numeric_trial, numeric_runtime, change
):
    trial = numeric_trial
    path = calibrate(trial)
    if change in {"range", "diagnostics"}:
        if change == "range":
            trial.controls["examples"][0]["expected_scores"]["quality"] = [3, 4]
        else:
            trial.controls["examples"][0]["diagnostic_score_ranges"] = {
                "quality": [3, 4]
            }
        put_json(trial.root / "evals/graders/calibration.json", trial.controls)
    elif change == "anchor":
        trial.rubric["criteria"][0]["anchors"]["3"] += " new behavior"
        put_json(trial.root / "evals/cases/control/rubric.json", trial.rubric)
    elif change in {"target", "qualification"}:
        if change == "target":
            trial.case["workflow_target_seconds"] = 7
        else:
            trial.case["calibration_qualification"] = "readiness"
        put_json(trial.root / "evals/cases/control/case.json", trial.case)
    else:
        target = (
            trial.root
            / {
                "request": "evals/cases/control/requests/01.md",
                "grader": "evals/graders/review.md",
                "engine": "tools/canary.py",
            }[change]
        )
        target.write_text(target.read_text() + " changed input")
    with pytest.raises(ValueError):
        canary.check_calibration(trial.root, path, CONFIG, ENV, case_id="control")


def test_numeric_calibration_and_replay_bind_scores(numeric_trial, numeric_runtime):
    trial = numeric_trial
    path = calibrate(trial)
    assert canary.check_calibration(trial.root, path, CONFIG, ENV, case_id="control")
    report = canary.run_case(trial.root, "control", CONFIG, CONFIG, path)
    assert canary.verified_behavior(trial.root, report, trial.case)["status"] == "pass"
    grade_path = path.parent / "0-grade.json"
    grade = canary.read_json(grade_path)
    grade["criteria"][0]["score"] = 5  # Still pass, but outside the calibrated range.
    put_json(grade_path, grade)
    execution_path = path.parent / "0-reply.execution.json"
    result = canary.read_json(execution_path)
    result["reply"] = json.dumps(grade)
    put_json(execution_path, result)
    refresh_manifest(path)
    with pytest.raises(ValueError, match="declared controls"):
        canary.check_calibration(trial.root, path, CONFIG, ENV, case_id="control")


def test_deterministic_mapping_rejects_advisory_and_missing_checks(numeric_trial):
    trial = numeric_trial
    for mapping in (
        {},
        {**trial.case["check_criteria"], "preserved": "polish"},
        {**trial.case["check_criteria"], "runner.workflow-target": "scope"},
    ):
        with pytest.raises(ValueError):
            canary.validate_check_criteria(
                {**trial.case, "check_criteria": mapping}, trial.rubric
            )


@pytest.mark.parametrize(
    "contract,prefix",
    [
        ({"workflow_target_seconds": 5}, "workflow_"),
        ({"target_seconds": 6, "budget_seconds": 5}, ""),
        ({"budget_seconds": True}, ""),
        ({"target_seconds": 1.5, "budget_seconds": 5}, ""),
    ],
)
def test_invalid_budget_contracts(contract, prefix):
    with pytest.raises(ValueError):
        canary.validate_budgets(contract, prefix)


def update_case(trial):
    for name, *_ in canary.timing_limits(trial.case):
        trial.case["check_criteria"][name] = "efficiency"
    put_json(trial.root / "evals/cases/control/case.json", trial.case)


@pytest.mark.parametrize(
    "last_seconds,completed", [(3, True), (3, False), (3.1, False)]
)
def test_cumulative_cutoff_includes_review_and_stops_fix_and_handoff(
    numeric_trial, numeric_runtime, monkeypatch, last_seconds, completed
):
    trial = numeric_trial
    trial.case["workflow_target_seconds"] = 6
    for name in ("review", "fix", "handoff"):
        trial.case["phases"].append({"id": name, "request": "requests/02.md"})
    update_case(trial)
    calibration = calibrate(trial)
    original = canary.runtime.execute
    calls = []
    prompts = {}

    def timed(workspace, prompt, output, config, schema=None):
        assert schema is None  # No evaluator after the incomplete workflow.
        calls.append((output.parent.name, config["timeout_seconds"]))
        prompts[output.parent.name] = prompt
        result = original(workspace, prompt, output, config, schema)
        result["elapsed_seconds"] = {"first": 3, "second": 4, "review": last_seconds}[
            output.parent.name
        ]
        if output.parent.name == "review":
            result.update(completed=completed, timed_out=not completed)
        return result

    monkeypatch.setattr(canary.runtime, "execute", timed)
    report = canary.run_case(
        trial.root, "control", {**CONFIG, "timeout_seconds": 20}, CONFIG, calibration
    )
    row = canary.verified_record(report)
    assert calls == [("first", 10), ("second", 7), ("review", 3)]
    for phase, consumed, target, hard in (
        ("first", 0, 6, 10),
        ("second", 3, 3, 7),
        ("review", 7, 0, 3),
    ):
        assert (
            f"Workflow worker clock: {consumed:.3f}s consumed; "
            f"usable target remaining: {target:.3f}s; "
            f"hard budget remaining: {hard:.3f}s; this invocation cap: {hard:.3f}s."
        ) in prompts[phase]
        assert (report.parent / "phases" / phase / "prompt.md").read_text() == prompts[
            phase
        ]
    assert row["status"] == "fail"
    assert row["observations"]["worker_elapsed_seconds"] == 7 + last_seconds
    assert row["observations"]["phase_elapsed_seconds"] == {
        "first": 3,
        "second": 4,
        "review": last_seconds,
    }
    assert canary.read_json(report.parent / "phases/review/budget.json") == {
        "worker_elapsed_seconds": 7,
        "workflow_remaining_seconds": 3,
        "phase_remaining_seconds": None,
        "timeout_seconds": 3,
    }
    assert row["observations"]["unreached_phases"] == ["fix", "handoff"]
    assert not (report.parent / "phases/fix").exists()
    budget = next(
        c for c in row["deterministic"] if c["id"] == "runner.workflow-budget"
    )
    assert (
        budget["status"] == "fail"
        and budget["priority"] == "P1"
        and budget["score_ceiling"] == 2
    )
    assert (report.parent / "phases/review/execution.json").is_file()


@pytest.mark.parametrize(
    "actual,completed,expected",
    [(2, False, "fail"), (2.1, True, "fail"), (1, False, "inconclusive")],
)
def test_phase_budget_caps_call_and_preserves_incomplete_failure(
    numeric_trial, numeric_runtime, monkeypatch, actual, completed, expected
):
    trial = numeric_trial
    trial.case["phases"][0].update(target_seconds=1, budget_seconds=2)
    update_case(trial)
    calibration = calibrate(trial)
    original = canary.runtime.execute
    calls = []

    def timed(workspace, prompt, output, config, schema=None):
        calls.append(config["timeout_seconds"])
        result = original(workspace, prompt, output, config, schema)
        result.update(
            elapsed_seconds=actual, completed=completed, timed_out=not completed
        )
        return result

    monkeypatch.setattr(canary.runtime, "execute", timed)
    report = canary.run_case(
        trial.root, "control", {**CONFIG, "timeout_seconds": 20}, CONFIG, calibration
    )
    row = canary.read_json(report)
    assert calls == [2]
    assert row["status"] == expected
    assert row["observations"]["unreached_phases"] == ["second"]
    assert (
        next(c for c in row["deterministic"] if c["id"] == "runner.first-budget")[
            "status"
        ]
        == expected
    )


@pytest.mark.parametrize(
    "failure",
    [
        "second-incomplete",
        "second-exception",
        "grader-incomplete",
        "grader-malformed",
        "reader-incomplete",
    ],
)
def test_known_required_behavior_failure_survives_later_missing_evidence(
    numeric_trial, numeric_runtime, monkeypatch, failure
):
    trial = numeric_trial
    if failure == "reader-incomplete":
        trial.case["reading_probe"] = {
            "documents": ["first-report.txt"],
            "questions": ["What is delivered?"],
        }
        update_case(trial)
    calibration = calibrate(trial)
    original = canary.runtime.execute

    def damaged(workspace, prompt, output, config, schema=None):
        phase = output.parent.name
        if schema is None and phase == "first":
            (workspace / "keep/original.txt").write_text(
                "lost original required history"
            )
        if phase == "second" and failure == "second-exception":
            raise RuntimeError("synthetic process launch failure")
        result = original(workspace, prompt, output, config, schema)
        if (
            (phase == "second" and failure == "second-incomplete")
            or (schema is not None and failure == "grader-incomplete")
            or (phase == "reading-probe" and failure == "reader-incomplete")
        ):
            result.update(completed=False, timed_out=True)
        if schema is not None and failure == "grader-malformed":
            result["reply"] = "{malformed"
        return result

    monkeypatch.setattr(canary.runtime, "execute", damaged)
    report = canary.run_case(trial.root, "control", CONFIG, CONFIG, calibration)
    row = canary.verified_record(report)
    assert row["status"] == "fail"
    fact = next(c for c in row["deterministic"] if c["id"] == "preserved")
    assert fact["status"] == "fail" and fact["priority"] == "P1"
    assert fact["criterion_id"] == "quality" and fact["score_ceiling"] == 2
    assert (
        report.parent / "phases/first/workspace/keep/original.txt"
    ).read_text() == "lost original required history"


@pytest.mark.parametrize("grader_failure", [False, True])
def test_target_failure_before_hard_stop_survives_grader_loss(
    numeric_trial, numeric_runtime, monkeypatch, grader_failure
):
    trial = numeric_trial
    calibration = calibrate(trial)
    original = canary.runtime.execute

    def timed(workspace, prompt, output, config, schema=None):
        result = original(workspace, prompt, output, config, schema)
        result["elapsed_seconds"] = 4.5 if schema is None else 1000
        if schema is not None and grader_failure:
            result.update(completed=False, timed_out=True)
        return result

    monkeypatch.setattr(canary.runtime, "execute", timed)
    report = canary.run_case(
        trial.root, "control", {**CONFIG, "timeout_seconds": 20}, CONFIG, calibration
    )
    row = canary.verified_record(report)
    assert row["status"] == "fail"
    facts = {c["id"]: c for c in row["deterministic"]}
    assert facts["runner.workflow-budget"]["status"] == "pass"
    assert facts["runner.workflow-target"]["status"] == "fail"
    assert facts["runner.workflow-target"]["score_ceiling"] == 2
    assert row["observations"]["worker_elapsed_seconds"] == 9
    assert row["timing"]["evaluator_elapsed_seconds"] == {"grader": 1000}
    assert row["timing"]["end_to_end_elapsed_seconds"] >= 0
    if not grader_failure:
        assert (
            canary.verified_behavior(trial.root, report, trial.case)["status"] == "fail"
        )
        # Tampering with a numeric mapping is rejected even after re-sealing.
        facts["preserved"]["priority"] = "P0"
        put_json(report.parent / "deterministic.json", list(facts.values()))
        refresh_manifest(report)
        with pytest.raises(ValueError, match="mapping"):
            canary.verified_behavior(trial.root, report, trial.case)


def test_phase_target_and_remaining_workflow_caps_are_independent(
    numeric_trial, numeric_runtime, monkeypatch
):
    trial = numeric_trial
    trial.case["phases"][0].update(target_seconds=2, budget_seconds=5)
    trial.case["phases"][1].update(target_seconds=5, budget_seconds=8)
    update_case(trial)
    calibration = calibrate(trial)
    original = canary.runtime.execute
    calls = []

    def timed(workspace, prompt, output, config, schema=None):
        result = original(workspace, prompt, output, config, schema)
        if schema is None:
            calls.append(config["timeout_seconds"])
            result["elapsed_seconds"] = 3
        return result

    monkeypatch.setattr(canary.runtime, "execute", timed)
    report = canary.run_case(
        trial.root, "control", {**CONFIG, "timeout_seconds": 20}, CONFIG, calibration
    )
    row = canary.verified_behavior(trial.root, report, trial.case)
    assert calls == [5, 7]
    assert row["status"] == "fail"
    facts = {c["id"]: c["status"] for c in row["deterministic"]}
    assert facts["runner.first-target"] == "fail"
    assert facts["runner.second-target"] == "pass"
    assert facts["runner.workflow-target"] == "pass"
    put_json(
        report.parent / "phases/second/settings.json", {**CONFIG, "timeout_seconds": 8}
    )
    refresh_manifest(report)
    with pytest.raises(ValueError, match="remaining budget"):
        canary.verified_behavior(trial.root, report, trial.case)


def test_skipped_fix_consumes_no_budget_and_evaluator_waits_are_excluded(
    numeric_trial, numeric_runtime, monkeypatch
):
    trial = numeric_trial
    trial.case["phases"].insert(
        1,
        {
            "id": "fix",
            "request": "requests/02.md",
            "skip_if_ready": "review.json",
            "budget_seconds": 1,
            "target_seconds": 1,
        },
    )
    trial.case["reading_probe"] = {
        "documents": ["first-report.txt"],
        "questions": ["What is delivered?"],
    }
    update_case(trial)
    calibration = calibrate(trial)
    original = canary.runtime.execute
    calls = []

    def timed(workspace, prompt, output, config, schema=None):
        result = original(workspace, prompt, output, config, schema)
        phase = output.parent.name
        if schema is None and phase != "reading-probe":
            calls.append(config["timeout_seconds"])
            put_json(workspace / "review.json", {"verdict": "ready", "findings": []})
            result["elapsed_seconds"] = 4
        else:
            result["elapsed_seconds"] = 1000
        return result

    monkeypatch.setattr(canary.runtime, "execute", timed)
    report = canary.run_case(
        trial.root, "control", {**CONFIG, "timeout_seconds": 20}, CONFIG, calibration
    )
    row = canary.verified_behavior(trial.root, report, trial.case)
    assert row["status"] == "pass" and calls == [10, 6]
    assert row["observations"]["skipped_phases"] == ["fix"]
    assert row["observations"]["worker_elapsed_seconds"] == 8
    assert row["timing"]["evaluator_elapsed_seconds"] == {
        "reader": 1000,
        "grader": 1000,
    }


@pytest.mark.parametrize("grader_timeout", [None, 300])
def test_run_cli_grader_timeout_preserves_worker_and_calibration_settings(
    numeric_trial, numeric_runtime, monkeypatch, capsys, grader_timeout
):
    trial = numeric_trial
    grader = {**CONFIG, "timeout_seconds": grader_timeout or 600}
    calibration = canary.calibration(trial.root, grader, case_id="control")
    assert canary.read_json(calibration)["status"] == "pass"
    monkeypatch.setattr(canary, "ROOT", trial.root)
    args = [
        "run",
        "control",
        "--model",
        CONFIG["model"],
        "--effort",
        "low",
        "--timeout",
        "600",
        "--grader-model",
        CONFIG["model"],
        "--grader-effort",
        "low",
        "--calibration",
        str(calibration),
    ]
    if grader_timeout is not None:
        args += ["--grader-timeout", str(grader_timeout)]
    assert canary.main(args) == 0
    report = canary.read_json(trial.root / capsys.readouterr().out.strip())
    assert report["settings"]["worker"] == {**CONFIG, "timeout_seconds": 600}
    assert report["settings"]["grader"] == grader
    assert report["status"] == "pass"

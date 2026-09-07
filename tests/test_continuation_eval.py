"""Mechanical controls for smoke selection, delivery evidence and literal citations.

These use real disposable Git histories and synthetic model responses. They do
not establish LLM grading or skill quality; real calibration is a separate run.
"""

# ruff: noqa: F811 — pytest injects the imported fixtures by parameter name.

import copy
import json
import shutil

import pytest

from tests.test_canary import (  # noqa: F401 — imported pytest fixtures
    CONFIG,
    REPO,
    accepted,
    accepted_seed,
    fake_runtime,
    forbid_model_calls,
    grade_row,
    make_tiny_root,
    put_json,
    refresh_manifest,
    tiny_root,
)
from tools import canary


@pytest.mark.parametrize(
    "case_id", ["v1-small-feature", "v2-scope-extension", "bounded-delivery"]
)
def test_history_archives_can_be_added_without_weakening_originals(tmp_path, case_id):
    case_root = REPO / "evals/cases" / case_id
    case = canary.read_json(case_root / "case.json")
    guard = next(c for c in case["checks"] if c["kind"] == "unchanged")
    initial = canary.files(case_root / "fixture")
    canary.write_files(tmp_path, initial)

    def result():
        return canary.deterministic(
            {"checks": [guard]}, case_root, tmp_path, initial, "unused"
        )[0]["status"]

    assert result() == "pass"
    (tmp_path / "docs/history/prior-design.md").write_bytes(initial["docs/DESIGN.md"])
    assert result() == "pass"
    for name, original in initial.items():
        if not any(
            name == protected or name.startswith(protected + "/")
            for protected in guard["paths"]
        ):
            continue
        target = tmp_path / name
        target.write_bytes(original + b"changed original")
        assert result() == "fail", name
        target.unlink()
        assert result() == "fail", name
        target.write_bytes(original)
        assert result() == "pass", name


def add_smoke(trial):
    source = trial.root / "evals/cases/control"
    target = source.with_name("smoke-control")
    shutil.copytree(source, target)
    case = copy.deepcopy(trial.case)
    case.update(id="smoke-control", tier="smoke", phases=case["phases"][:1])
    put_json(target / "case.json", case)
    return case


def test_smoke_selection_preserves_bulk_default_and_explicit_ids(tiny_root):
    add_smoke(tiny_root)
    catalog = canary.cases(tiny_root.root)
    assert set(canary.select_cases(catalog)) == {"control"}
    assert set(canary.select_cases(catalog, tier="smoke")) == {"smoke-control"}
    assert set(canary.select_cases(catalog, "smoke-control")) == {"smoke-control"}
    assert set(canary.select_cases(catalog, tier="all")) == set(catalog)
    with pytest.raises(ValueError):
        canary.select_cases(catalog, "smoke-control", "heavy")


@pytest.mark.parametrize("mutation", ["reader", "second-phase", "skip", "no-heavy"])
def test_smoke_is_one_actual_operation_and_cannot_replace_heavy_coverage(
    tiny_root, mutation
):
    smoke = add_smoke(tiny_root)
    if mutation == "reader":
        smoke["reading_probe"] = {
            "documents": ["keep/original.txt"],
            "questions": ["Why?"],
        }
    elif mutation == "second-phase":
        smoke["phases"] = tiny_root.case["phases"]
    elif mutation == "skip":
        smoke["phases"][0]["skip_if_ready"] = "review.json"
    else:
        shutil.rmtree(tiny_root.root / "evals/cases/control")
    put_json(tiny_root.root / "evals/cases/smoke-control/case.json", smoke)
    with pytest.raises(ValueError):
        canary.cases(tiny_root.root)


def test_cli_and_affected_separate_smoke_from_heavy(tmp_path, monkeypatch, capsys):
    trial = make_tiny_root(tmp_path, with_git=True)
    add_smoke(trial)
    monkeypatch.setattr(canary, "ROOT", trial.root)
    assert canary.main(["list", "--tier", "smoke"]) == 0
    assert [c["id"] for c in json.loads(capsys.readouterr().out)] == ["smoke-control"]
    calls = []
    result = trial.root / "synthetic-result.json"
    put_json(result, {"status": "pass"})

    def fake_run(root, case_id, *args):
        calls.append(case_id)
        return result

    monkeypatch.setattr(canary, "run_case", fake_run)
    args = [
        "--model",
        "synthetic",
        "--grader-model",
        "synthetic",
        "--calibration",
        "unused",
    ]
    assert canary.main(["run", "all", *args]) == 0
    assert calls == ["control"]
    calls.clear()
    assert canary.main(["run", "all", "--tier", "smoke", *args]) == 0
    assert calls == ["smoke-control"]
    impact = canary.affected(trial.root, trial.baseline)
    assert impact["heavy_cases"] == ["control"]
    assert impact["smoke_cases"] == ["smoke-control"]
    assert impact["changed_files"]["skills/control/SKILL.md"] == ["control"]


def smoke_record(trial, status):
    case = add_smoke(trial)
    directory, row = canary.new_record(trial.root, "behavior")
    row.update(
        case_id=case["id"], identity=canary.identity(trial.root, case), status=status
    )
    canary.save(directory / "attempt.json", row)
    return canary.finish(directory, row)


@pytest.mark.parametrize("status", ["fail", "inconclusive"])
def test_failed_or_incomplete_smoke_does_not_become_release_requirement(
    accepted, status
):
    # Incomplete execution with intact provenance differs from corrupted evidence.
    smoke = smoke_record(accepted, status)
    result = canary.release_gate(
        accepted.root, [accepted.old, accepted.new, smoke], accepted.baseline
    )
    assert result["status"] == "pass"
    assert set(result["cases"]) == {"control"}


@pytest.mark.parametrize("mutation", ["corrupt-smoke", "relabel-heavy"])
def test_smoke_classification_cannot_hide_corruption_or_changed_case_header(
    accepted, mutation
):
    smoke = smoke_record(accepted, "fail")
    if mutation == "corrupt-smoke":
        (smoke.parent / "attempt.json").write_text("corrupted original attempt")
    else:
        heavy = canary.read_json(accepted.new)
        heavy["case_id"] = "smoke-control"
        put_json(accepted.new, heavy)
    result = canary.release_gate(
        accepted.root, [accepted.old, accepted.new, smoke], accepted.baseline
    )
    assert result["status"] == "fail"
    message = (
        "Changed/missing evidence"
        if mutation == "corrupt-smoke"
        else "Smoke classification differs"
    )
    assert any(message in error for error in result["errors"])


DELIVERY = {
    "id": "delivery",
    "kind": "phase_delivery",
    "review_phase": "review",
    "delivery_phase": "deliver",
    "paths": ["counter.py", "tests"],
}


def captured_delivery(tmp_path, mutation):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    base = canary.init_fixture(
        workspace, {"counter.py": b"baseline", "tests/test_counter.py": b"checks"}
    )
    directory = tmp_path / "record"
    put_json(directory / "initial-git.json", canary.git_snapshot(workspace, base))
    (workspace / "counter.py").write_text("reviewed implementation")
    case = {"phases": [{"id": name} for name in ("review", "pending", "deliver")]}

    def commit(message):
        canary.git(workspace, "add", ".")
        canary.git(workspace, "commit", "-qm", message)

    for phase in case["phases"]:
        if phase["id"] == "pending" and mutation == "premature":
            commit("premature")
        if phase["id"] == "deliver" and mutation != "no-commit":
            if mutation in {"altered", "intermediate-unreviewed", "dirty-restoration"}:
                (workspace / "counter.py").write_text("unreviewed implementation")
            if mutation == "extra-test":
                (workspace / "tests/new.py").write_text("unreviewed test")
            if mutation == "unrelated-history":
                canary.git(workspace, "checkout", "--orphan", "unrelated")
            (workspace / "handoff.md").write_text("current delivery")
            commit("delivery")
            if mutation in {"intermediate-unreviewed", "dirty-restoration"}:
                (workspace / "counter.py").write_text("reviewed implementation")
            if mutation in {"intermediate-unreviewed", "evidence-followup"}:
                (workspace / "check-result.md").write_text("new record")
                commit("followup")
        phase_dir = directory / "phases" / phase["id"]
        canary.write_files(phase_dir / "workspace", canary.files(workspace))
        put_json(phase_dir / "git.json", canary.git_snapshot(workspace, base))
    proof = canary.capture_delivery(workspace, base, DELIVERY["paths"])
    put_json(directory / "phases/deliver/delivery-git-delivery.json", proof)
    return case, directory


@pytest.mark.parametrize(
    "mutation",
    [
        "valid",
        "evidence-followup",
        "no-commit",
        "premature",
        "altered",
        "extra-test",
        "intermediate-unreviewed",
        "dirty-restoration",
        "unrelated-history",
    ],
)
def test_delivery_checks_actual_git_boundaries_and_each_committed_payload(
    tmp_path, mutation
):
    case, directory = captured_delivery(tmp_path, mutation)
    result = canary.delivery_result(case, DELIVERY, directory)
    # A necessary follow-up is mechanically possible. Its purpose is scored separately.
    expected = "pass" if mutation in {"valid", "evidence-followup"} else "fail"
    assert result["status"] == expected


def test_run_archives_delivery_proof_and_replay_rejects_relabeling(
    tiny_root, fake_runtime, monkeypatch
):
    trial = tiny_root
    check = {
        **DELIVERY,
        "review_phase": "first",
        "delivery_phase": "second",
        "paths": ["keep"],
    }
    trial.case["checks"] = [check]
    put_json(trial.root / "evals/cases/control/case.json", trial.case)
    execute = fake_runtime.execute

    def deliver(workspace, prompt, output, config, schema=None):
        result = execute(workspace, prompt, output, config, schema)
        if schema is None and output.parent.name == "second":
            canary.git(workspace, "add", ".")
            canary.git(workspace, "commit", "-qm", "synthetic authorized delivery")
        return result

    monkeypatch.setattr(canary.runtime, "execute", deliver)
    calibration = canary.calibration(trial.root, CONFIG)
    report = canary.run_case(trial.root, "control", CONFIG, CONFIG, calibration)
    assert canary.verified_behavior(trial.root, report, trial.case)["status"] == "pass"
    proof = report.parent / "phases/second/delivery-git-delivery.json"
    data = canary.read_json(proof)
    data["commits"][0]["payload"] = {}
    put_json(proof, data)
    refresh_manifest(report)
    with pytest.raises(ValueError, match="Delivery result differs"):
        canary.verified_behavior(trial.root, report, trial.case)


@pytest.mark.parametrize(
    "field,value",
    [
        ("review_phase", "second"),
        ("delivery_phase", "first"),
        ("paths", []),
        ("paths", ["../private"]),
        ("paths", "keep"),
        ("id", "../../outside"),
    ],
)
def test_delivery_contract_rejects_invalid_scope_before_execution(
    tiny_root, field, value
):
    check = {
        **DELIVERY,
        "review_phase": "first",
        "delivery_phase": "second",
        "paths": ["keep"],
    }
    check[field] = value
    tiny_root.case["checks"] = [check]
    put_json(tiny_root.root / "evals/cases/control/case.json", tiny_root.case)
    with pytest.raises(ValueError):
        canary.cases(tiny_root.root)


def test_nested_controls_preserve_original_events_and_strict_quotations(tmp_path):
    controls = canary.read_json(REPO / "evals/graders/calibration.json")
    provenance = canary.read_json(REPO / "evals/graders/nested-output-provenance.json")
    source = REPO / provenance["source"]
    assert canary.digest(source.read_bytes()) == provenance["source_sha256"]
    lines = canary.read_json(source)["stdout"].splitlines(keepends=True)
    indexed = {e.get("id"): e for e in controls["examples"]}
    for item in provenance["examples"]:
        example = indexed[item["id"]]
        raw = example["artifacts"]["execution.json"]
        line = lines[item["stdout_line_zero_based"]]
        assert canary.digest(line.encode()) == item["event_line_sha256"]
        assert json.loads(raw)["stdout"] == line
        assert canary.digest(raw.encode()) == item["artifact_sha256"]
        rubric = canary.calibration_contract(controls, example)
        canary.write_files(tmp_path / "artifacts", {"execution.json": raw.encode()})
        # Response decoding preserves literal nested escapes; no fuzzy matching.
        literal = json.loads(json.dumps(raw))
        grade = {
            "criteria": [
                grade_row(
                    example["expected"],
                    "check-honesty",
                    "artifacts/execution.json",
                    literal,
                )
            ]
        }
        assert canary.validate_grade(grade, rubric, tmp_path) == example["expected"]
        decoded_display = json.loads(line)["item"]["aggregated_output"]
        for invalid in (decoded_display, raw.replace("Command:", "Invented command:")):
            grade["criteria"][0]["evidence"][0]["quote"] = invalid
            with pytest.raises(ValueError, match="invented quote"):
                canary.validate_grade(grade, rubric, tmp_path)


def test_bookkeeping_controls_do_not_treat_all_followups_or_failures_as_excess():
    inputs = canary.read_json(REPO / "evals/graders/calibration.json")
    examples = {e.get("id"): e for e in inputs["examples"]}
    for label, expected in (
        ("necessary-evidence", "pass"),
        ("redundant-bookkeeping", "fail"),
        ("authorized-followup", "pass"),
    ):
        example = examples["handoff-" + label]
        canary.calibration_contract(inputs, example)
        assert example["expected_criteria"] == {"proportionate-handoff": expected}
        wrong = "fail" if expected == "pass" else "pass"
        assert not canary.calibration_matches(
            example,
            {"criteria": [{"id": "proportionate-handoff", "status": wrong}]},
            wrong,
        )

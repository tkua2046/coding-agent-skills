"""Fast structural regressions using labeled synthetic runtime controls.

Passing controls establish provenance plumbing, never LLM/semantic quality or a
real sandbox boundary. Only disposable repositories receive synthetic records.
"""

import copy
import json
import shutil
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from tools import canary

REPO = Path(__file__).resolve().parents[1]
CONFIG = {"model": "synthetic-control-no-llm", "effort": "low", "timeout_seconds": 1}
ENV = {"control": "synthetic environment; no runtime attestation"}


def put_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value))


def criterion(name="required", required=True):
    return {
        "id": name,
        "required": required,
        "requirement": "Synthetic control",
        "pass_when": "Control says pass",
        "fail_when": "Control says fail",
    }


def grade_row(
    status="pass", name="required", path="artifacts/result.txt", quote="control"
):
    return {
        "id": name,
        "status": status,
        "reason": "Synthetic control judgment",
        "evidence": [{"path": path, "quote": quote}],
    }


def execution(reply, **changes):
    return {
        "completed": True,
        "exit_code": 0,
        "timed_out": False,
        "interrupted": False,
        "stdout": "synthetic transcript",
        "stderr": "",
        "elapsed_seconds": 0.25,
        "reply": reply,
        **changes,
    }


@pytest.fixture(autouse=True)
def forbid_model_calls(monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("A fast test attempted a real model or sandbox invocation")

    monkeypatch.setattr(canary.runtime, "execute", forbidden)
    monkeypatch.setattr(canary.runtime, "probe", forbidden)
    monkeypatch.setattr(canary.runtime, "sandbox_command", forbidden)
    monkeypatch.setattr(canary, "environment", lambda: dict(ENV))


def make_tiny_root(tmp_path, *, with_git=False):
    root = tmp_path / "repo"
    root.mkdir()
    content = {
        "skills/control/SKILL.md": b"synthetic baseline skill",
        "evals/cases/control/fixture/keep/original.txt": b"preserve me",
        "evals/cases/control/requests/01.md": b"synthetic first request",
        "evals/cases/control/requests/02.md": b"synthetic second request",
        "evals/cases/control/overlays/02/overlay.txt": b"second-phase overlay",
        "evals/graders/review.md": b"Synthetic grader control, not an LLM assessment",
    }
    for name in ("tools/canary.py", "tools/canary_runtime.py", "requirements-dev.txt"):
        content[name] = (REPO / name).read_bytes()
    canary.write_files(root, content)
    case = {
        "id": "control",
        "title": "Synthetic control",
        "version": 1,
        "tier": "heavy",
        "skills": ["control"],
        "phases": [
            {"id": "first", "request": "requests/01.md"},
            {"id": "second", "request": "requests/02.md", "overlay": "overlays/02"},
        ],
        "checks": [
            {"id": "preserved", "kind": "unchanged", "paths": ["keep"]},
            {"id": "tags", "kind": "no_tags"},
            {"id": "commits", "kind": "commit_count", "expected": 0},
        ],
    }
    rubric = {"version": 1, "criteria": [criterion()]}
    put_json(root / "evals/cases/control/case.json", case)
    put_json(root / "evals/cases/control/rubric.json", rubric)
    put_json(
        root / "evals/graders/calibration.json",
        {
            "rubric": rubric,
            "examples": [
                {
                    "request": "Synthetic calibration control",
                    "expected": status,
                    "artifacts": {"result.txt": f"synthetic-control:{status}"},
                }
                for status in ("pass", "fail", "inconclusive")
            ],
        },
    )
    baseline = None
    if with_git:
        canary.init_fixture(root, {})
        baseline = canary.git(root, "rev-parse", "HEAD")
    (root / "skills/control/SKILL.md").write_text("synthetic candidate skill")
    return SimpleNamespace(root=root, baseline=baseline, case=case)


@pytest.fixture
def tiny_root(tmp_path):
    return make_tiny_root(tmp_path)


class SyntheticRuntime:
    """Deterministic labeled control, deliberately not a semantic grader."""

    def __init__(self):
        self.calls = []
        self.worker_failure = None
        self.malformed_grader = False
        self.baseline_status = "fail"
        self.candidate_status = "pass"

    def probe(self, workspace, private):
        assert private.is_file() and not private.is_relative_to(workspace)
        return {
            "passed": True,
            "control": "synthetic boundary result, not isolation proof",
        }

    def execute(self, workspace, prompt, output, config, schema=None):
        self.calls.append(
            {
                "workspace": workspace,
                "prompt": prompt,
                "output": output,
                "schema": schema,
                "before": canary.files(workspace),
            }
        )
        if schema is None:
            assert not (workspace / "rubric.json").exists()
            assert not (workspace / "oracle.py").exists()
            phase = output.parent.name
            (workspace / f"{phase}-report.txt").write_text(f"synthetic {phase} report")
            reply = f"synthetic {phase} worker reply"
            result = execution(reply, **(self.worker_failure or {}))
        else:
            control = workspace / "artifacts/result.txt"
            if control.exists():
                quote = control.read_text()
                status = quote.split(":")[-1]
                path = "artifacts/result.txt"
            else:
                skill = (workspace / "initial/skills/control/SKILL.md").read_text()
                status = (
                    self.baseline_status
                    if "baseline" in skill
                    else self.candidate_status
                )
                path = "artifacts/second/reply.md"
                if not (workspace / path).exists():
                    path = "artifacts/second/decision.json"
                quote = (workspace / path).read_text()
            reply = (
                "{malformed synthetic grader"
                if self.malformed_grader
                else json.dumps(
                    {"criteria": [grade_row(status, path=path, quote=quote)]}
                )
            )
            result = execution(reply)
        output.write_text(reply)
        return result


@pytest.fixture
def fake_runtime(monkeypatch):
    fake = SyntheticRuntime()
    monkeypatch.setattr(canary.runtime, "execute", fake.execute)
    monkeypatch.setattr(canary.runtime, "probe", fake.probe)
    return fake


@pytest.fixture(scope="module")
def accepted_seed(tmp_path_factory):
    """Generate authentic record structure once; each test mutates a private copy."""
    trial = make_tiny_root(
        tmp_path_factory.mktemp("synthetic-provenance"), with_git=True
    )
    fake = SyntheticRuntime()
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(canary.runtime, "execute", fake.execute)
        patch.setattr(canary.runtime, "probe", fake.probe)
        patch.setattr(canary, "environment", lambda: dict(ENV))
        trial.calibration = canary.calibration(trial.root, CONFIG)
        assert canary.read_json(trial.calibration)["status"] == "pass"
        trial.old = canary.run_case(
            trial.root, "control", CONFIG, CONFIG, trial.calibration, trial.baseline
        )
        trial.new = canary.run_case(
            trial.root, "control", CONFIG, CONFIG, trial.calibration
        )
    result = canary.release_gate(trial.root, [trial.old, trial.new], trial.baseline)
    assert result["status"] == "pass", result
    assert result["cases"]["control"]["baseline_status"] == "fail"
    return trial


@pytest.fixture
def accepted(accepted_seed, tmp_path, fake_runtime):
    seed = accepted_seed
    root = tmp_path / "repo"
    shutil.copytree(seed.root, root)
    trial = SimpleNamespace(
        root=root,
        baseline=seed.baseline,
        case=copy.deepcopy(seed.case),
        fake=fake_runtime,
    )
    for name in ("calibration", "old", "new"):
        setattr(trial, name, root / getattr(seed, name).relative_to(seed.root))
    # Assert acceptance after relocation, before each isolated negative mutation.
    result = gate(trial)
    assert result["status"] == "pass", result
    return trial


def refresh_manifest(report_path):
    """Re-seal synthetic tampering to exercise semantic checks past the hash layer."""
    row = canary.read_json(report_path)
    content = canary.files(report_path.parent)
    content.pop("report.json")
    row["evidence"] = canary.hashes(content)
    put_json(report_path, row)


def gate(trial):
    return canary.release_gate(trial.root, [trial.old, trial.new], trial.baseline)


def test_complete_synthetic_provenance_is_accepted_and_portable(accepted, monkeypatch):
    trial = accepted
    assert (
        canary.verified_behavior(trial.root, trial.new, trial.case)["status"] == "pass"
    )
    assert (
        canary.verified_behavior(trial.root, trial.old, trial.case)["status"] == "fail"
    )
    check_calibration = canary.check_calibration

    def archived_only(root, path, config, env):
        # The seed still exists, but relocation must use this evidence tree.
        assert path == trial.calibration
        return check_calibration(root, path, config, env)

    monkeypatch.setattr(canary, "check_calibration", archived_only)
    assert gate(trial)["status"] == "pass"
    for report in (trial.old, trial.new):
        row = canary.verified_record(report)
        assert row["identity"]["skills"]
        assert row["evidence"]
        assert row["calibration_ref"] == {
            "path": trial.calibration.relative_to(report.parent.parent).as_posix(),
            "sha256": canary.digest(trial.calibration.read_bytes()),
        }
        assert not (report.parent / "calibration").exists()
        controls = canary.read_json(trial.calibration)["matched_controls"]
        assert controls and all(controls)


def inline_calibration(trial, path):
    """Reproduce the legacy inline layout without changing its engine identity."""
    row = canary.read_json(path)
    row.pop("calibration_ref")
    row["calibration"] = canary.check_calibration(
        trial.root, trial.calibration, CONFIG, ENV
    )
    shutil.copytree(trial.calibration.parent, path.parent / "calibration")
    put_json(path, row)
    refresh_manifest(path)


def test_legacy_inline_calibration_remains_readable_without_original(accepted):
    for path in (accepted.old, accepted.new):
        inline_calibration(accepted, path)
    shutil.rmtree(accepted.calibration.parent)
    assert gate(accepted)["status"] == "pass"
    original = accepted.new.read_bytes()
    assert canary.verified_record(accepted.new)["status"] == "pass"
    # A new engine invalidates release compatibility; reading never relabels it.
    (accepted.root / "tools/canary.py").write_text("changed engine")
    assert gate(accepted)["status"] == "fail"
    assert canary.verified_record(accepted.new)["status"] == "pass"
    assert accepted.new.read_bytes() == original


def test_explicit_reports_relocate_with_complete_evidence_tree(
    accepted, tmp_path, monkeypatch, capsys
):
    source = accepted.calibration.parent.parent
    original = canary.hashes(canary.files(source))
    destination = tmp_path / "restored-evidence"
    shutil.move(source, destination)
    paths = [destination / p.relative_to(source) for p in (accepted.old, accepted.new)]
    assert canary.release_gate(accepted.root, [], accepted.baseline)["status"] == "fail"
    result = canary.release_gate(accepted.root, paths, accepted.baseline)
    assert result["status"] == "pass", result
    monkeypatch.setattr(canary, "ROOT", accepted.root)
    assert (
        canary.main(["release-gate", *map(str, paths), "--baseline", accepted.baseline])
        == 0
    )
    assert json.loads(capsys.readouterr().out)["status"] == "pass"
    assert canary.hashes(canary.files(destination)) == original
    assert len(list(destination.rglob("inputs.json"))) == 1
    assert not any(p.name == "calibration" for p in destination.rglob("*"))


@pytest.mark.parametrize("outcome", ["fail", "unfinished"])
def test_explicit_collection_includes_newer_attempts(accepted, tmp_path, outcome):
    if outcome == "fail":
        accepted.fake.candidate_status = "fail"
        newer = canary.run_case(
            accepted.root, "control", CONFIG, CONFIG, accepted.calibration
        )
        assert canary.verified_record(newer)["status"] == "fail"
    else:
        directory, row = canary.new_record(accepted.root, "behavior")
        canary.save(directory / "attempt.json", row)
        newer = directory / "report.json"
    source = accepted.calibration.parent.parent
    destination = tmp_path / "explicit-collection"
    shutil.move(source, destination)
    paths = [destination / p.relative_to(source) for p in (accepted.old, accepted.new)]
    result = canary.release_gate(accepted.root, paths, accepted.baseline)
    assert result["status"] == "fail"
    aliases = []
    for path in paths:
        alias = path.with_name("selected.json")
        alias.write_bytes(path.read_bytes())
        aliases.append(alias)
    aliased = canary.release_gate(accepted.root, aliases, accepted.baseline)
    assert aliased["status"] == "fail"
    assert any("renamed report aliases" in error for error in aliased["errors"])
    if outcome == "unfinished":
        assert any(
            str(destination / newer.relative_to(source)) in error
            for error in result["errors"]
        )


def test_backup_requires_complete_restore_into_canonical_collection(accepted):
    source = accepted.calibration.parent.parent
    original = canary.hashes(canary.files(source))
    backup = accepted.root / "artifacts/repair/legacy-tree/docs/validation/canary"
    backup.parent.mkdir(parents=True)
    shutil.move(source, backup)
    assert canary.release_gate(accepted.root, [], accepted.baseline)["status"] == "fail"
    shutil.move(backup, source)
    result = canary.release_gate(accepted.root, [], accepted.baseline)
    assert result["status"] == "pass", result
    assert canary.hashes(canary.files(source)) == original


@pytest.mark.parametrize(
    "location",
    [
        "artifacts/scratch/app",
        "artifacts/repair/legacy-tree/docs/validation/canary/copied-run",
        "artifacts/canary/run/phases/first/workspace/app",
        "docs/validation/canary/run/inputs/case/fixture/app",
    ],
)
def test_discovery_ignores_scratch_backups_and_captured_reports(accepted, location):
    unrelated = accepted.root / location
    put_json(unrelated / "report.json", {"application": "unrelated report"})
    put_json(unrelated / "unfinished/attempt.json", {"application": "scratch"})
    result = gate(accepted)
    assert result["status"] == "pass", result


def test_passing_baseline_and_candidate_cannot_hide_newer_failure(accepted):
    accepted.fake.baseline_status = "pass"
    baseline = canary.run_case(
        accepted.root,
        "control",
        CONFIG,
        CONFIG,
        accepted.calibration,
        accepted.baseline,
    )
    result = gate(accepted)
    assert result["status"] == "pass", result
    assert result["cases"]["control"]["baseline"] == str(baseline)
    assert result["cases"]["control"]["baseline_status"] == "pass"
    accepted.fake.candidate_status = "fail"
    failed = canary.run_case(
        accepted.root, "control", CONFIG, CONFIG, accepted.calibration
    )
    assert (
        canary.verified_behavior(accepted.root, failed, accepted.case)["status"]
        == "fail"
    )
    assert gate(accepted)["status"] == "fail"


def test_new_record_rejects_symlinked_evidence_storage(tiny_root, tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    (tiny_root.root / "artifacts").symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError):
        canary.new_record(tiny_root.root, "behavior")
    assert not list(outside.iterdir())


@pytest.mark.parametrize(
    "location",
    [
        "artifacts/canary",
        "docs/validation/canary",
    ],
)
def test_canonical_discovery_includes_newer_failure(accepted, location):
    source = accepted.calibration.parent.parent
    target = accepted.root / location
    if source != target:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(source, target)
        for name in ("calibration", "old", "new"):
            setattr(
                accepted, name, target / getattr(accepted, name).relative_to(source)
            )
    result = canary.release_gate(accepted.root, [], accepted.baseline)
    assert result["status"] == "pass", result
    assert result["cases"]["control"]["candidate"] == str(accepted.new)
    # Generate a genuine completed synthetic failure in the default location,
    # then retain it in the location being exercised without passing its path.
    if source != target:
        restored = source / accepted.calibration.parent.name
        shutil.copytree(accepted.calibration.parent, restored)
        calibration = restored / "report.json"
    else:
        calibration = accepted.calibration
    accepted.fake.candidate_status = "fail"
    newer = canary.run_case(accepted.root, "control", CONFIG, CONFIG, calibration)
    assert canary.verified_record(newer)["status"] == "fail"
    if source != target:
        shutil.move(newer.parent, target / newer.parent.name)
    assert gate(accepted)["status"] == "fail"


@pytest.mark.parametrize("location", ["artifacts/canary", "docs/validation/canary"])
def test_unfinished_retained_attempt_cannot_hide_behind_older_pass(accepted, location):
    directory, row = canary.new_record(accepted.root, "behavior")
    canary.save(directory / "attempt.json", row)
    target = accepted.root / location / directory.name
    if target != directory:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(directory, target)
    result = gate(accepted)
    assert result["status"] == "fail"
    assert any(str(target / "report.json") in error for error in result["errors"])


@pytest.mark.parametrize("mutation", ["missing", "report", "control", "manifest"])
def test_referenced_calibration_fails_closed(accepted, mutation):
    report = accepted.calibration
    if mutation == "missing":
        shutil.rmtree(report.parent)
    elif mutation == "report":
        report.write_bytes(report.read_bytes() + b"\n")
    elif mutation == "control":
        (report.parent / "0-reply.execution.json").write_text("changed")
    else:
        row = canary.read_json(report)
        row["evidence"].pop("0-reply.execution.json")
        put_json(report, row)
        behavior = canary.read_json(accepted.new)
        behavior["calibration_ref"]["sha256"] = canary.digest(report.read_bytes())
        put_json(accepted.new, behavior)
    with pytest.raises(ValueError):
        canary.verified_behavior(accepted.root, accepted.new, accepted.case)
    assert gate(accepted)["status"] == "fail"


@pytest.mark.parametrize("mutation", ["absolute", "escape", "symlink", "hash", "null"])
def test_calibration_reference_cannot_escape_root_or_skip_hash(
    accepted, tmp_path, mutation
):
    row = canary.read_json(accepted.new)
    reference = row["calibration_ref"]
    if mutation == "absolute":
        reference["path"] = str(accepted.calibration)
    elif mutation == "escape":
        outside = accepted.calibration.parent.parent.parent / "outside"
        shutil.copytree(accepted.calibration.parent, outside)
        reference["path"] = "../outside/report.json"
    elif mutation == "symlink":
        outside = tmp_path / "outside"
        shutil.move(accepted.calibration.parent, outside)
        accepted.calibration.parent.symlink_to(outside, target_is_directory=True)
    elif mutation == "hash":
        reference.pop("sha256")
    else:
        row["calibration_ref"] = None
    put_json(accepted.new, row)
    with pytest.raises(ValueError):
        canary.verified_behavior(accepted.root, accepted.new, accepted.case)
    assert gate(accepted)["status"] == "fail"


def test_cross_root_calibration_requires_full_restore_before_worker(accepted, tmp_path):
    outside = tmp_path / "outside"
    shutil.copytree(accepted.calibration.parent, outside)
    before = list(accepted.fake.calls)
    failed = canary.run_case(
        accepted.root, "control", CONFIG, CONFIG, outside / "report.json"
    )
    row = canary.verified_record(failed)
    assert row["status"] == "inconclusive"
    assert "restore the complete calibration evidence tree" in row["error"]
    assert accepted.fake.calls == before
    assert gate(accepted)["status"] == "fail"
    restored = accepted.calibration.parent.parent / "restored" / "calibration"
    shutil.copytree(outside, restored)
    passed = canary.run_case(
        accepted.root, "control", CONFIG, CONFIG, restored / "report.json"
    )
    assert (
        canary.verified_behavior(accepted.root, passed, accepted.case)["status"]
        == "pass"
    )
    assert not (passed.parent / "calibration").exists()
    assert gate(accepted)["status"] == "pass"


def test_phases_are_separate_calls_with_retained_artifacts_and_overlays(accepted):
    trial = accepted
    trial.new = canary.run_case(
        trial.root, "control", CONFIG, CONFIG, trial.calibration
    )
    assert gate(trial)["status"] == "pass"
    worker_calls = [
        c
        for c in trial.fake.calls
        if c["schema"] is None and c["output"].is_relative_to(trial.new.parent)
    ]
    assert [c["output"].parent.name for c in worker_calls] == [
        p["id"] for p in trial.case["phases"]
    ]
    first, second = worker_calls
    assert "synthetic first request" in first["prompt"]
    assert "synthetic second request" in second["prompt"]
    assert "synthetic first request" not in second["prompt"]
    assert "first-report.txt" not in first["before"]
    assert second["before"]["first-report.txt"] == b"synthetic first report"
    assert second["before"]["overlay.txt"] == b"second-phase overlay"
    for phase in trial.case["phases"]:
        directory = trial.new.parent / "phases" / phase["id"]
        assert (directory / "reply.md").read_text() == canary.read_json(
            directory / "execution.json"
        )["reply"]
        assert canary.read_json(directory / "git.json")["head"]
        assert (directory / "workspace" / f"{phase['id']}-report.txt").is_file()
    grader = next(
        c
        for c in trial.fake.calls
        if c["output"] == trial.new.parent / "grade-reply.json"
    )
    assert grader["workspace"] != first["workspace"]
    assert "artifacts/first/reply.md" in grader["before"]
    assert "artifacts/second/reply.md" in grader["before"]


@pytest.mark.parametrize(
    "asset",
    [
        "skills/control/SKILL.md",
        "evals/graders/review.md",
        "evals/cases/control/requests/01.md",
        "evals/graders/calibration.json",
        "tools/canary_runtime.py",
        "tools/canary.py",
        "requirements-dev.txt",
    ],
)
def test_release_rejects_stale_inputs(accepted, asset):
    target = accepted.root / asset
    if target.suffix == ".json":
        value = canary.read_json(target)
        value["examples"][0]["request"] += " changed"
        put_json(target, value)
    else:
        target.write_bytes(target.read_bytes() + b"\nchanged control")
    rejected = gate(accepted)
    assert rejected["status"] == "fail"
    assert "control" not in rejected["cases"]


@pytest.mark.parametrize(
    "asset",
    [
        "inputs/bundles/skills/control/SKILL.md",
        "inputs/case/case.json",
        "calibration_ref",
        "grade.json",
        "grade-reply.execution.json",
        "phases/second/execution.json",
        "grader-isolation.json",
    ],
)
def test_release_rejects_missing_evidence_even_with_refreshed_manifest(accepted, asset):
    if asset == "calibration_ref":
        row = canary.read_json(accepted.new)
        row.pop("calibration_ref")
        put_json(accepted.new, row)
    else:
        (accepted.new.parent / asset).unlink()
    refresh_manifest(accepted.new)
    assert gate(accepted)["status"] == "fail"


def test_release_rejects_changed_evidence_bytes(accepted):
    (accepted.new.parent / "phases/first/reply.md").write_text("substituted evidence")
    with pytest.raises(ValueError):
        canary.verified_record(accepted.new)
    assert gate(accepted)["status"] == "fail"


@pytest.mark.parametrize(
    "mutation",
    [
        "grade-summary",
        "grader-reply",
        "worker-reply",
        "missing-criterion",
        "duplicate-check",
        "failed-check",
    ],
)
def test_release_recomputes_archived_judgments(accepted, mutation):
    directory = accepted.new.parent
    if mutation in {"grade-summary", "grader-reply", "missing-criterion"}:
        grade = canary.read_json(directory / "grade.json")
        grade["criteria"][0]["status"] = "fail"
        if mutation == "missing-criterion":
            grade["criteria"] = []
        put_json(directory / "grade.json", grade)
        if mutation != "grader-reply":
            result = canary.read_json(directory / "grade-reply.execution.json")
            result["reply"] = json.dumps(grade)
            put_json(directory / "grade-reply.execution.json", result)
            (directory / "grade-reply.json").write_text(result["reply"])
    elif mutation == "worker-reply":
        (directory / "phases/first/reply.md").write_text("different reply")
    else:
        checks = canary.read_json(directory / "deterministic.json")
        if mutation == "duplicate-check":
            checks[-1] = copy.deepcopy(checks[0])
        else:
            checks[0]["status"] = "fail"
        put_json(directory / "deterministic.json", checks)
    refresh_manifest(accepted.new)
    assert gate(accepted)["status"] == "fail"


@pytest.mark.parametrize(
    "mutation",
    [
        "grader",
        "settings",
        "environment",
        "controls",
        "failed-control",
        "incomplete-control",
    ],
)
@pytest.mark.parametrize("storage", ["reference", "inline"])
def test_release_revalidates_complete_calibration(accepted, mutation, storage):
    if storage == "inline":
        inline_calibration(accepted, accepted.new)
    report_path = (
        accepted.calibration
        if storage == "reference"
        else accepted.new.parent / "calibration/report.json"
    )
    directory = report_path.parent
    row = canary.read_json(report_path)
    if mutation in {"grader", "settings", "environment"}:
        row[mutation] = "stale synthetic value"
        put_json(report_path, row)
    elif mutation == "controls":
        controls = canary.read_json(directory / "inputs.json")
        controls["examples"][0]["request"] += " changed"
        put_json(directory / "inputs.json", controls)
    else:
        result_path = directory / "0-reply.execution.json"
        result = canary.read_json(result_path)
        if mutation == "incomplete-control":
            result["completed"] = False
        else:
            grade = canary.read_json(directory / "0-grade.json")
            grade["criteria"][0]["status"] = "fail"
            put_json(directory / "0-grade.json", grade)
            result["reply"] = json.dumps(grade)
        put_json(result_path, result)
    refresh_manifest(report_path)
    if storage == "reference":
        row = canary.read_json(accepted.new)
        row["calibration_ref"]["sha256"] = canary.digest(report_path.read_bytes())
        put_json(accepted.new, row)
    refresh_manifest(accepted.new)
    with pytest.raises(ValueError):
        canary.verified_behavior(accepted.root, accepted.new, accepted.case)
    assert gate(accepted)["status"] == "fail"


@pytest.mark.parametrize(
    "failure",
    [
        {"completed": False, "exit_code": 9, "stderr": "synthetic failure"},
        {"completed": False, "timed_out": True},
        {"completed": False, "interrupted": True},
    ],
)
def test_newer_incomplete_attempt_is_retained_and_blocks_older_green(accepted, failure):
    old_bytes = accepted.new.read_bytes()
    accepted.fake.worker_failure = failure
    newer = canary.run_case(
        accepted.root, "control", CONFIG, CONFIG, accepted.calibration
    )
    row = canary.verified_record(newer)
    assert row["status"] == "inconclusive"
    assert row.get("error")
    result = canary.read_json(newer.parent / "phases/first/execution.json")
    for key, value in failure.items():
        assert result[key] == value
    assert (newer.parent / "phases/first/workspace/first-report.txt").is_file()
    assert (newer.parent / "phases/first/git.json").is_file()
    assert not (newer.parent / "phases/second").exists()
    assert accepted.new.read_bytes() == old_bytes
    assert gate(accepted)["status"] == "fail"  # newer was not passed explicitly


def test_newer_completed_failure_blocks_cherry_picked_green(accepted):
    accepted.fake.candidate_status = "fail"
    newer = canary.run_case(
        accepted.root, "control", CONFIG, CONFIG, accepted.calibration
    )
    assert (
        canary.verified_behavior(accepted.root, newer, accepted.case)["status"]
        == "fail"
    )
    assert gate(accepted)["status"] == "fail"


def test_malformed_grader_retains_execution_and_all_phase_results(accepted):
    accepted.fake.malformed_grader = True
    newer = canary.run_case(
        accepted.root, "control", CONFIG, CONFIG, accepted.calibration
    )
    row = canary.verified_record(newer)
    assert row["status"] == "inconclusive"
    assert row.get("error")
    result = canary.read_json(newer.parent / "grade-reply.execution.json")
    assert result["reply"] == (newer.parent / "grade-reply.json").read_text()
    with pytest.raises(json.JSONDecodeError):
        json.loads(result["reply"])
    for phase in accepted.case["phases"]:
        assert (newer.parent / "phases" / phase["id"] / "execution.json").is_file()
    assert not (newer.parent / "grade.json").exists()
    assert gate(accepted)["status"] == "fail"


def test_failed_calibration_cannot_be_used(tiny_root, fake_runtime):
    fake_runtime.malformed_grader = True
    calibration = canary.calibration(tiny_root.root, CONFIG)
    assert canary.verified_record(calibration)["status"] == "inconclusive"
    assert (calibration.parent / "0-reply.execution.json").is_file()
    before = list(fake_runtime.calls)
    report = canary.run_case(tiny_root.root, "control", CONFIG, CONFIG, calibration)
    assert canary.read_json(report)["status"] == "inconclusive"
    assert canary.read_json(report).get("error")
    assert canary.verified_record(report)["status"] == "inconclusive"
    assert (report.parent / "attempt.json").is_file()
    assert fake_runtime.calls == before


@pytest.mark.parametrize("failure", ["missing", "nonpassing", "stale"])
def test_early_calibration_failure_is_retained_but_later_valid_run_recovers(
    accepted, failure
):
    bad = accepted.root / "bad-calibration/report.json"
    if failure != "missing":
        shutil.copytree(accepted.calibration.parent, bad.parent)
        row = canary.read_json(bad)
        row["status" if failure == "nonpassing" else "engine"] = (
            "fail" if failure == "nonpassing" else "obsolete-engine"
        )
        put_json(bad, row)
    failed = canary.run_case(accepted.root, "control", CONFIG, CONFIG, bad)
    assert canary.verified_record(failed)["status"] == "inconclusive"
    retained = canary.hashes(canary.files(failed.parent))
    assert gate(accepted)["status"] == "fail"  # latest attempt cannot borrow old green
    recovered = canary.run_case(
        accepted.root, "control", CONFIG, CONFIG, accepted.calibration
    )
    assert canary.read_json(recovered)["status"] == "pass"
    assert gate(accepted)["status"] == "pass"
    assert canary.hashes(canary.files(failed.parent)) == retained


@pytest.mark.parametrize(
    "failure",
    [
        {"interrupted": True, "exit_code": -9},
        {"timed_out": True, "exit_code": -9},
        {"exit_code": 7},
    ],
)
def test_incomplete_calibration_stops_before_next_control(
    tiny_root, fake_runtime, monkeypatch, failure
):
    execute = fake_runtime.execute

    def incomplete(workspace, prompt, output, config, schema=None):
        result = execute(workspace, prompt, output, config, schema)
        result.update(completed=False, **failure)
        return result

    monkeypatch.setattr(canary.runtime, "execute", incomplete)
    report = canary.calibration(tiny_root.root, CONFIG)
    assert canary.verified_record(report)["status"] == "inconclusive"
    assert len(fake_runtime.calls) == 1
    retained = canary.read_json(report.parent / "0-reply.execution.json")
    assert retained["reply"] and retained["stdout"]
    for key, value in failure.items():
        assert retained[key] == value
    assert (report.parent / "0-grade.json").is_file()
    assert not (report.parent / "1-isolation.json").exists()
    assert not (report.parent / "1-reply.execution.json").exists()


@pytest.mark.parametrize("asset", ["case.json", "rubric.json"])
def test_content_revision_advances_with_fresh_comparable_evidence(accepted, asset):
    target = accepted.root / "evals/cases/control" / asset
    row = canary.read_json(target)
    row["version"] = 2
    put_json(target, row)
    assert canary.cases(accepted.root)["control"]
    assert gate(accepted)["status"] == "fail"  # v1 evidence is now stale
    old = canary.run_case(
        accepted.root,
        "control",
        CONFIG,
        CONFIG,
        accepted.calibration,
        accepted.baseline,
    )
    new = canary.run_case(
        accepted.root, "control", CONFIG, CONFIG, accepted.calibration
    )
    assert canary.read_json(old)["status"] == "fail"  # known synthetic baseline defect
    assert canary.read_json(new)["status"] == "pass"
    assert gate(accepted)["status"] == "pass"


@pytest.mark.parametrize("asset", ["case.json", "rubric.json"])
@pytest.mark.parametrize("revision", [0, -1, True, "2", 2.1, None])
def test_content_revision_requires_positive_integer(tiny_root, asset, revision):
    target = tiny_root.root / "evals/cases/control" / asset
    row = canary.read_json(target)
    row["version"] = revision
    put_json(target, row)
    with pytest.raises(ValueError):
        canary.cases(tiny_root.root)


@pytest.mark.parametrize(
    "mutation",
    [
        "wrong-id",
        "version",
        "tier",
        "unknown-skill",
        "unmapped-skill",
        "empty-phases",
        "duplicate-phase",
        "missing-request",
        "escaping-request",
        "missing-overlay",
        "duplicate-criterion",
        "no-required",
        "unanchored",
        "duplicate-check",
        "unsupported-check",
        "missing-oracle",
        "missing-preserved",
        "missing-hook",
        "missing-fixture",
    ],
)
def test_catalog_rejects_invalid_definitions(tiny_root, mutation):
    root = tiny_root.root
    case = copy.deepcopy(tiny_root.case)
    case_dir = root / "evals/cases/control"
    rubric = canary.read_json(case_dir / "rubric.json")
    if mutation == "wrong-id":
        case["id"] = "other"
    elif mutation == "version":
        case["version"] = 0
    elif mutation == "tier":
        case["tier"] = "fast"
    elif mutation == "unknown-skill":
        case["skills"] = ["missing"]
    elif mutation == "unmapped-skill":
        canary.write_files(root, {"skills/unmapped/SKILL.md": b"synthetic control"})
    elif mutation == "empty-phases":
        case["phases"] = []
    elif mutation == "duplicate-phase":
        case["phases"][1]["id"] = case["phases"][0]["id"]
    elif mutation in {"missing-request", "escaping-request"}:
        case["phases"][0]["request"] = (
            "missing.md" if mutation == "missing-request" else "../outside.md"
        )
    elif mutation == "missing-overlay":
        case["phases"][1]["overlay"] = "missing"
    elif mutation == "duplicate-criterion":
        rubric["criteria"].append(copy.deepcopy(rubric["criteria"][0]))
    elif mutation == "no-required":
        rubric["criteria"][0]["required"] = False
    elif mutation == "unanchored":
        del rubric["criteria"][0]["pass_when"]
    elif mutation == "duplicate-check":
        case["checks"].append(copy.deepcopy(case["checks"][0]))
    elif mutation == "unsupported-check":
        case["checks"][0]["kind"] = "unknown"
    elif mutation == "missing-oracle":
        case["checks"].append({"id": "oracle", "kind": "python", "file": "missing.py"})
    elif mutation == "missing-preserved":
        case["checks"][0]["paths"] = ["missing"]
    elif mutation == "missing-hook":
        case["hook"] = "missing-hook"
    elif mutation == "missing-fixture":
        shutil.rmtree(case_dir / "fixture")
    put_json(case_dir / "case.json", case)
    put_json(case_dir / "rubric.json", rubric)
    with pytest.raises(ValueError):
        canary.cases(root)


@pytest.mark.parametrize(
    "asset", ["requests/01.md", "fixture/keep/original.txt", "rubric.json"]
)
def test_catalog_rejects_symlinked_assets(tiny_root, asset):
    target = tiny_root.root / "evals/cases/control" / asset
    outside = tiny_root.root.parent / "private"
    outside.write_bytes(target.read_bytes())
    target.unlink()
    target.symlink_to(outside)
    with pytest.raises(ValueError):
        canary.cases(tiny_root.root)


@pytest.mark.parametrize("name", ["", "../escape", "/absolute", "nested/../../escape"])
def test_local_rejects_paths_outside_root(tmp_path, name):
    with pytest.raises(ValueError):
        canary.local(tmp_path, name)


def test_write_files_rejects_symlink_parent_without_touching_private_file(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    private = tmp_path / "private"
    private.mkdir()
    secret = private / "secret"
    secret.write_bytes(b"private control")
    (workspace / "linked").symlink_to(private, target_is_directory=True)
    with pytest.raises(ValueError):
        canary.write_files(workspace, {"linked/secret": b"overwrite"})
    assert secret.read_bytes() == b"private control"


@pytest.mark.parametrize(
    "mutation", ["none", "add", "delete", "change", "remove-directory"]
)
def test_directory_preservation_detects_membership_and_content_changes(
    tmp_path, mutation
):
    canary.write_files(
        tmp_path, {"docs/one.txt": b"one", "docs/nested/two.txt": b"two"}
    )
    initial = canary.files(tmp_path)
    if mutation == "add":
        (tmp_path / "docs/new.txt").write_text("added")
    elif mutation == "delete":
        (tmp_path / "docs/nested/two.txt").unlink()
    elif mutation == "change":
        (tmp_path / "docs/one.txt").write_text("changed")
    elif mutation == "remove-directory":
        shutil.rmtree(tmp_path / "docs")
    check = {"checks": [{"id": "preserve", "kind": "unchanged", "paths": ["docs"]}]}
    results = canary.deterministic(check, tmp_path, tmp_path, initial, "unused")
    assert results[0]["status"] == ("pass" if mutation == "none" else "fail")


@pytest.mark.parametrize(
    "mutation",
    [
        "omitted",
        "duplicate",
        "invented",
        "fabricated-quote",
        "missing-artifact",
        "rubric-evidence",
        "traversal",
        "no-evidence",
    ],
)
def test_grading_rejects_unanchored_or_incomplete_judgments(tmp_path, mutation):
    canary.write_files(tmp_path, {"artifacts/result.txt": b"control"})
    row = grade_row()
    grade = {"criteria": [row]}
    if mutation == "omitted":
        grade["criteria"] = []
    elif mutation == "duplicate":
        grade["criteria"].append(copy.deepcopy(row))
    elif mutation == "invented":
        row["id"] = "undeclared"
    elif mutation == "fabricated-quote":
        row["evidence"][0]["quote"] = "not in artifact"
    elif mutation == "missing-artifact":
        row["evidence"][0]["path"] = "artifacts/missing.txt"
    elif mutation == "rubric-evidence":
        row["evidence"][0]["path"] = "rubric.json"
    elif mutation == "traversal":
        row["evidence"][0]["path"] = "artifacts/../../private"
    elif mutation == "no-evidence":
        row["evidence"] = []
    with pytest.raises(ValueError):
        canary.validate_grade(grade, {"criteria": [criterion()]}, tmp_path)


@pytest.mark.parametrize(
    "required_status,optional_status,expected",
    [
        ("fail", "pass", "fail"),
        ("inconclusive", "pass", "inconclusive"),
        ("pass", "fail", "pass"),
        ("pass", "pass", "pass"),
    ],
)
def test_required_criteria_are_not_averaged(
    tmp_path, required_status, optional_status, expected
):
    rubric = {
        "criteria": [
            criterion(),
            *[criterion(f"optional-{i}", False) for i in range(5)],
        ]
    }
    rows = [grade_row(required_status)] + [
        grade_row(optional_status, f"optional-{i}") for i in range(5)
    ]
    assert (
        canary.validate_grade(
            {"criteria": rows}, rubric, tmp_path, {"result.txt": b"control"}
        )
        == expected
    )


def test_required_failure_dominates_inconclusive(tmp_path):
    rubric = {
        "criteria": [
            criterion("failed"),
            criterion("unknown"),
            *[criterion(f"passing-{i}") for i in range(5)],
        ]
    }
    grade = {
        "criteria": [
            grade_row("fail", "failed"),
            grade_row("inconclusive", "unknown"),
            *[grade_row("pass", f"passing-{i}") for i in range(5)],
        ]
    }
    assert (
        canary.validate_grade(grade, rubric, tmp_path, {"result.txt": b"control"})
        == "fail"
    )


def test_grading_and_replay_agree_on_literal_crlf_evidence(tmp_path):
    text = "First line.\r\nSecond line with café and literal \\n.\r\n"
    artifacts = {"excerpt.txt": text.encode()}
    canary.write_files(tmp_path / "artifacts", artifacts)
    grade = {"criteria": [grade_row(path="artifacts/excerpt.txt", quote=text)]}
    rubric = {"criteria": [criterion()]}
    assert canary.validate_grade(grade, rubric, tmp_path) == "pass"
    assert canary.validate_grade(grade, rubric, tmp_path, artifacts) == "pass"


@pytest.mark.parametrize("case_id", ["counter-stage", "v6-execution-handoff"])
def test_counter_oracles_reject_defect_missed_by_worker_tests(
    tmp_path, monkeypatch, case_id
):
    case_dir = REPO / "evals/cases" / case_id
    canary.write_files(tmp_path, canary.files(case_dir / "fixture"))
    correct = """class Counter:
    def __init__(self, value=0):
        self.value = value
    def add(self, step=1):
        if type(step) is not int or step <= 0:
            raise ValueError('invalid step')
        self.value += step
        return self.value
"""
    # This defective control accepts bool/float/zero, which visible tests omit.
    defective = correct.replace("type(step) is not int or step <= 0", "step < 0")
    monkeypatch.setattr(
        canary.runtime, "sandbox_command", lambda workspace, command: command
    )
    case = canary.read_json(case_dir / "case.json")
    oracle_case = {"checks": [c for c in case["checks"] if c["kind"] == "python"]}
    assert oracle_case["checks"]
    for source, expected in ((correct, "pass"), (defective, "fail")):
        (tmp_path / "counter.py").write_text(source)
        worker = canary.runtime.capture(
            [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests"],
            tmp_path,
            5,
        )
        assert worker["exit_code"] == 0, worker
        checked = canary.deterministic(oracle_case, case_dir, tmp_path, {}, "unused")
        assert all(c["status"] == expected for c in checked), checked
        assert all(c["evidence"]["stderr"] for c in checked)


def test_maintenance_oracle_rejects_west_defect_missed_by_worker_tests(
    tmp_path, monkeypatch
):
    case_dir = REPO / "evals/cases/v3-maintenance"
    canary.write_files(tmp_path, canary.files(case_dir / "fixture"))
    correct = (tmp_path / "navigator.py").read_text()
    defective = correct.replace(
        "if candidate[:2] in occupied:",
        "if heading != 3 and candidate[:2] in occupied:",
    )
    assert defective != correct
    monkeypatch.setattr(
        canary.runtime, "sandbox_command", lambda workspace, command: command
    )
    case = canary.read_json(case_dir / "case.json")
    oracle_case = {"checks": [c for c in case["checks"] if c["kind"] == "python"]}
    assert oracle_case["checks"]
    for source, expected in ((correct, "pass"), (defective, "fail")):
        (tmp_path / "navigator.py").write_text(source)
        worker = canary.runtime.capture(
            [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests"],
            tmp_path,
            5,
        )
        assert worker["exit_code"] == 0, worker
        checked = canary.deterministic(oracle_case, case_dir, tmp_path, {}, "unused")
        assert all(c["status"] == expected for c in checked), checked


def test_current_catalog_validates_without_model_but_absent_all_case_evidence_blocks_release(
    tmp_path, monkeypatch, capsys
):
    # Exercise the actual CLI validator and the full current catalog, without
    # borrowing any local behavior evidence or depending on a historical ref.
    assert canary.main(["validate"]) == 0
    assert capsys.readouterr().out
    root = tmp_path / "all-cases"
    root.mkdir()
    for name in ("evals/cases", "skills"):
        canary.write_files(root / name, canary.files(REPO / name))
    for name in ("tools/canary.py", "tools/canary_runtime.py", "requirements-dev.txt"):
        canary.write_files(root, {name: (REPO / name).read_bytes()})
    canary.init_fixture(root, {})
    catalog = canary.cases(root)
    assert set(catalog) == set(canary.cases(REPO))
    rejected = canary.release_gate(root, [], "HEAD")
    assert rejected["status"] == "fail"
    assert rejected["cases"] == {}
    assert all(
        any(error.startswith(f"{case_id}:") for error in rejected["errors"])
        for case_id, case in catalog.items()
        if case["tier"] == "heavy"
    )
    assert not any(
        error.startswith(f"{case_id}:")
        for case_id, case in catalog.items()
        if case["tier"] == "smoke"
        for error in rejected["errors"]
    )


@pytest.mark.parametrize(
    "artifact", ["phases/second/execution.json", "grade-reply.execution.json"]
)
@pytest.mark.parametrize(
    "change",
    [
        {"completed": False},
        {"exit_code": 4},
        {"timed_out": True},
        {"interrupted": True},
    ],
)
def test_release_rejects_incomplete_execution_despite_passing_summary(
    accepted, artifact, change
):
    path = accepted.new.parent / artifact
    result = canary.read_json(path)
    result.update(change)
    put_json(path, result)
    refresh_manifest(accepted.new)
    assert canary.verified_record(accepted.new)["status"] == "pass"
    assert gate(accepted)["status"] == "fail"


def test_deterministic_failure_overrides_passing_grader(accepted, monkeypatch):
    fake = accepted.fake
    execute = fake.execute

    def destructive_control(workspace, prompt, output, config, schema=None):
        result = execute(workspace, prompt, output, config, schema)
        if schema is None:
            (workspace / "keep/added.txt").write_text(
                "synthetic preservation violation"
            )
        return result

    monkeypatch.setattr(canary.runtime, "execute", destructive_control)
    newer = canary.run_case(
        accepted.root, "control", CONFIG, CONFIG, accepted.calibration
    )
    row = canary.verified_behavior(accepted.root, newer, accepted.case)
    assert row["semantic"] == "pass"
    assert row["status"] == "fail"
    assert gate(accepted)["status"] == "fail"


def test_ready_skips_fix_and_recheck_without_overlay_or_model_and_replays(
    tiny_root, fake_runtime, monkeypatch
):
    trial = tiny_root
    trial.case["phases"][1]["skip_if_ready"] = "review.json"
    trial.case["phases"].append(
        {"id": "recheck", "request": "requests/02.md", "skip_if_ready": "review.json"}
    )
    put_json(trial.root / "evals/cases/control/case.json", trial.case)
    execute = fake_runtime.execute

    def review_ready(workspace, prompt, output, config, schema=None):
        result = execute(workspace, prompt, output, config, schema)
        if schema is None:
            put_json(workspace / "review.json", {"verdict": "ready", "findings": []})
        return result

    monkeypatch.setattr(canary.runtime, "execute", review_ready)
    calibration = canary.calibration(trial.root, CONFIG)
    report = canary.run_case(trial.root, "control", CONFIG, CONFIG, calibration)
    assert canary.verified_behavior(trial.root, report, trial.case)["status"] == "pass"
    assert [
        c["output"].parent.name for c in fake_runtime.calls if c["schema"] is None
    ] == ["first"]
    for name in ("second", "recheck"):
        phase = report.parent / "phases" / name
        assert canary.read_json(phase / "execution.json") == canary.SKIPPED_EXECUTION
        assert not (phase / "workspace/overlay.txt").exists()
        assert not (phase / "reply.md").exists()
    observed = canary.read_json(report.parent / "phases/observations.json")
    assert observed["skipped_phases"] == ["second", "recheck"]
    assert observed["worker_elapsed_seconds"] == 0.25
    # Even re-sealed evidence cannot substitute a historical or malformed review.
    put_json(
        report.parent / "phases/second/skip-review.json",
        {"verdict": "needs-changes", "findings": []},
    )
    refresh_manifest(report)
    with pytest.raises(ValueError, match="current review"):
        canary.verified_behavior(trial.root, report, trial.case)


@pytest.mark.parametrize(
    "review",
    [
        None,
        b"{broken",
        b'{"verdict":"ready"}',
        b'{"verdict":"Ready","findings":[]}',
        b'{"verdict":"needs-changes","verdict":"ready","findings":[]}',
        b'{"verdict":"ready","findings":[NaN]}',
        b'{"verdict":"needs-changes","findings":["R1"]}',
        b'{"verdict":"needs-decision","findings":[]}',
    ],
)
def test_nonready_or_invalid_review_executes_fix_and_replays(
    tiny_root, fake_runtime, review
):
    trial = tiny_root
    case_dir = trial.root / "evals/cases/control"
    trial.case["phases"][1]["skip_if_ready"] = "review.json"
    put_json(case_dir / "case.json", trial.case)
    if review is not None:
        (case_dir / "fixture/review.json").write_bytes(review)
    calibration = canary.calibration(trial.root, CONFIG)
    report = canary.run_case(trial.root, "control", CONFIG, CONFIG, calibration)
    assert canary.verified_behavior(trial.root, report, trial.case)["status"] == "pass"
    phase = report.parent / "phases/second"
    decision = canary.read_json(phase / "decision.json")
    assert decision["skipped"] is False
    assert (phase / "workspace/overlay.txt").is_file()
    assert (phase / "reply.md").is_file()
    if review is not None:
        assert (phase / "skip-review.json").read_bytes() == review
    # A forged skip flag cannot exempt an executed phase from completion checks.
    put_json(phase / "execution.json", canary.SKIPPED_EXECUTION)
    refresh_manifest(report)
    with pytest.raises(ValueError, match="Execution incomplete"):
        canary.verified_behavior(trial.root, report, trial.case)


def add_reading_probe(trial):
    trial.case["reading_probe"] = {
        "documents": ["docs/PLAN.md", "docs/LONG.md"],
        "questions": ["What is the next action?", "Which choice remains open?"],
    }
    case_dir = trial.root / "evals/cases/control"
    put_json(case_dir / "case.json", trial.case)
    docs = {
        "docs/PLAN.md": (
            "Next: inspect café. Literal \\n stays literal.\r\n" * 30
            + "HIDDEN_LINE_31\r\n"
        ).encode(),
        "docs/LONG.md": ("é" * 2000 + "HIDDEN_AFTER_CHAR_CAP").encode(),
    }
    canary.write_files(case_dir / "fixture", docs)
    return docs


def test_reader_receives_only_literal_first_screen_and_retains_gradeable_evidence(
    tiny_root, fake_runtime, monkeypatch
):
    trial = tiny_root
    docs = add_reading_probe(trial)
    execute = fake_runtime.execute

    def inspect_reader(workspace, prompt, output, config, schema=None):
        if output.parent.name == "reading-probe":
            before = canary.files(workspace)
            assert set(before) == {"input.json"}
            assert prompt == canary.READER_PROMPT
            assert config == CONFIG and schema is None
            exposed = json.loads(before["input.json"])
            assert exposed["questions"] == trial.case["reading_probe"]["questions"]
            assert exposed["documents"] == [
                {
                    "path": "docs/PLAN.md",
                    "text": docs["docs/PLAN.md"].decode().split("HIDDEN_LINE_31")[0],
                },
                {"path": "docs/LONG.md", "text": "é" * 2000},
            ]
        return execute(workspace, prompt, output, config, schema)

    monkeypatch.setattr(canary.runtime, "execute", inspect_reader)
    calibration = canary.calibration(trial.root, CONFIG)
    report = canary.run_case(trial.root, "control", CONFIG, CONFIG, calibration)
    assert canary.verified_behavior(trial.root, report, trial.case)["status"] == "pass"
    reader = report.parent / "phases/reading-probe"
    assert (reader / "excerpts/0.txt").read_bytes() == docs["docs/PLAN.md"].split(
        b"HIDDEN_LINE_31"
    )[0]
    grader = next(
        c
        for c in fake_runtime.calls
        if c["output"] == report.parent / "grade-reply.json"
    )
    assert {
        "artifacts/reading-probe/input.json",
        "artifacts/reading-probe/execution.json",
        "artifacts/reading-probe/reply.md",
        "artifacts/observations.json",
    } <= grader["before"].keys()
    # Exposed text must recompute from the archived final worker documents.
    exposed = canary.read_json(reader / "input.json")
    exposed["documents"][0]["text"] += " added answer"
    put_json(reader / "input.json", exposed)
    refresh_manifest(report)
    with pytest.raises(ValueError, match="Reader input"):
        canary.verified_behavior(trial.root, report, trial.case)


@pytest.mark.parametrize("failure", ["missing", "encoding", "timeout"])
def test_reader_failure_retains_worker_evidence_without_acceptance(
    tiny_root, fake_runtime, monkeypatch, failure
):
    trial = tiny_root
    add_reading_probe(trial)
    document = trial.root / "evals/cases/control/fixture/docs/PLAN.md"
    if failure == "missing":
        document.unlink()
    elif failure == "encoding":
        document.write_bytes(b"undecodable \xff")
    execute = fake_runtime.execute

    def fail_reader(workspace, prompt, output, config, schema=None):
        result = execute(workspace, prompt, output, config, schema)
        if output.parent.name == "reading-probe":
            result.update(completed=False, timed_out=True, exit_code=-9)
        return result

    monkeypatch.setattr(canary.runtime, "execute", fail_reader)
    calibration = canary.calibration(trial.root, CONFIG)
    report = canary.run_case(trial.root, "control", CONFIG, CONFIG, calibration)
    assert canary.verified_record(report)["status"] == "inconclusive"
    assert (report.parent / "phases/second/workspace/second-report.txt").is_file()
    assert not (report.parent / "grade.json").exists()
    if failure == "timeout":
        result = canary.read_json(report.parent / "phases/reading-probe/execution.json")
        assert result["timed_out"] and result["reply"]


def test_per_example_rubric_requires_exact_criteria_during_calibration_and_replay(
    tiny_root, fake_runtime, monkeypatch
):
    root = tiny_root.root
    target = root / "evals/graders/calibration.json"
    inputs = canary.read_json(target)
    example = inputs["examples"][1]
    example["rubric"] = {"version": 1, "criteria": [criterion("A"), criterion("B")]}
    example["expected_criteria"] = {"A": "fail", "B": "pass"}
    put_json(target, inputs)
    execute = fake_runtime.execute
    wrong = False

    def grade_example(workspace, prompt, output, config, schema=None):
        rubric = canary.read_json(workspace / "rubric.json")
        if rubric == example["rubric"]:
            assert schema == canary.grade_schema(rubric)
            grade = {
                "criteria": [
                    grade_row(
                        "pass" if wrong else "fail", "A", quote="synthetic-control:fail"
                    ),
                    grade_row(
                        "fail" if wrong else "pass", "B", quote="synthetic-control:fail"
                    ),
                ]
            }
            reply = json.dumps(grade)
            output.write_text(reply)
            return execution(reply)
        return execute(workspace, prompt, output, config, schema)

    monkeypatch.setattr(canary.runtime, "execute", grade_example)
    report = canary.calibration(root, CONFIG)
    assert canary.check_calibration(root, report, CONFIG, ENV)
    wrong = True
    failed = canary.calibration(root, CONFIG)
    assert canary.verified_record(failed)["status"] == "fail"
    assert canary.read_json(failed)["matched_controls"] == [True, False, True]
    # Same aggregate failure, different failed criterion: re-sealing is insufficient.
    for suffix in ("grade.json", "reply.json", "reply.execution.json"):
        shutil.copyfile(failed.parent / f"1-{suffix}", report.parent / f"1-{suffix}")
    refresh_manifest(report)
    with pytest.raises(ValueError, match="declared controls"):
        canary.check_calibration(root, report, CONFIG, ENV)


@pytest.mark.parametrize("seconds,expected", [(0.5, "pass"), (0.5001, "fail")])
def test_workflow_deadline_uses_worker_wall_time_only_and_recomputes(
    tiny_root, fake_runtime, monkeypatch, seconds, expected
):
    trial = tiny_root
    trial.case["workflow_budget_seconds"] = 1
    add_reading_probe(trial)
    execute = fake_runtime.execute

    def timed(workspace, prompt, output, config, schema=None):
        result = execute(workspace, prompt, output, config, schema)
        result["elapsed_seconds"] = (
            1000 if schema or output.parent.name == "reading-probe" else seconds
        )
        return result

    monkeypatch.setattr(canary.runtime, "execute", timed)
    calibration = canary.calibration(trial.root, CONFIG)
    report = canary.run_case(trial.root, "control", CONFIG, CONFIG, calibration)
    row = canary.verified_behavior(trial.root, report, trial.case)
    assert row["status"] == expected
    observed = row["observations"]
    assert observed["worker_elapsed_seconds"] == 2 * seconds
    assert observed["executed_phases"] == ["first", "second"]
    assert (
        observed["documents"]["final"]["files"]
        == observed["documents"]["initial"]["files"] + 3
    )
    # Retained time, not the report/check label, owns the deadline result.
    checks = canary.read_json(report.parent / "deterministic.json")
    budget = next(c for c in checks if c["id"] == "runner.workflow-budget")
    budget["evidence"]["worker_elapsed_seconds"] = 0
    put_json(report.parent / "deterministic.json", checks)
    refresh_manifest(report)
    with pytest.raises(ValueError, match="Workflow budget"):
        canary.verified_behavior(trial.root, report, trial.case)


@pytest.mark.parametrize(
    "field,value",
    [
        ("workflow_budget_seconds", 0),
        ("workflow_budget_seconds", True),
        ("workflow_budget_seconds", 1.5),
        ("reading_probe", {"documents": ["../private"], "questions": ["Q"]}),
        ("reading_probe", {"documents": ["doc.md"], "questions": []}),
    ],
)
def test_optional_case_contracts_validate_before_execution(tiny_root, field, value):
    tiny_root.case[field] = value
    put_json(tiny_root.root / "evals/cases/control/case.json", tiny_root.case)
    with pytest.raises(ValueError):
        canary.cases(tiny_root.root)


def test_baseline_cli_defaults_follow_manifest_and_allow_explicit_override(
    tiny_root, monkeypatch, capsys
):
    root = tiny_root.root
    put_json(root / "evals/baseline/manifest.json", {"commit": "declared-baseline"})
    monkeypatch.setattr(canary, "ROOT", root)
    monkeypatch.setattr(canary, "affected", lambda root, base: {"baseline": base})
    monkeypatch.setattr(
        canary,
        "release_gate",
        lambda root, paths, baseline: {"baseline": baseline, "status": "fail"},
    )
    for command, option in (("affected", "--base"), ("release-gate", "--baseline")):
        for argv, expected in (
            ([command], "declared-baseline"),
            ([command, option, "override"], "override"),
        ):
            canary.main(argv)
            assert json.loads(capsys.readouterr().out)["baseline"] == expected

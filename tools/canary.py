"""Versioned behavior trials and an evidence-bound release gate.

Fast validation never calls a model. Heavy runs are explicit and use fresh Codex
contexts in disposable workspaces; evaluator material is outside their read scope.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from tools import canary_runtime as runtime

ROOT = Path(__file__).resolve().parents[1]
IGNORED = {".git", ".venv", ".tmp", ".ruff_cache", ".pytest_cache", "__pycache__"}
STATES = {"pass", "fail", "inconclusive"}


def valid_revision(value) -> bool:
    return type(value) is int and value > 0


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fingerprint(value) -> str:
    return digest(json.dumps(value, sort_keys=True).encode())


def read_json(path: Path):
    return json.loads(path.read_text())


def save(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x") as stream:
        stream.write(json.dumps(value, indent=2) + "\n")


def local(root: Path, name: str) -> Path:
    path = root / name
    if (
        not name
        or Path(name).is_absolute()
        or not path.resolve().is_relative_to(root.resolve())
    ):
        raise ValueError(f"Path escapes its root: {name}")
    if any(p.is_symlink() for p in (path, *path.parents) if p != root.parent):
        # Roots supplied by callers are resolved first; symlinked case assets
        # must not import outside files or grader material into a fixture.
        raise ValueError(f"Symlinked input: {name}")
    return path


def files(root: Path) -> dict[str, bytes]:
    result = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(p in IGNORED for p in relative.parts):
            continue
        if path.is_symlink():
            raise ValueError(f"Cannot archive symlink: {relative}")
        if path.is_file():
            result[relative.as_posix()] = path.read_bytes()
    return result


def write_files(root: Path, content: dict[str, bytes]) -> None:
    for name, data in content.items():
        path = local(root, name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


def hashes(content: dict[str, bytes]) -> dict[str, str]:
    return {name: digest(data) for name, data in content.items()}


def git(workspace: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=workspace, text=True, capture_output=True, check=True
    )
    return result.stdout.strip()


def cases(root: Path = ROOT) -> dict[str, dict]:
    result = {}
    for path in sorted((root / "evals/cases").glob("*/case.json")):
        case = read_json(path)
        case_id = case["id"]
        if case_id != path.parent.name or not re.fullmatch(r"[a-z0-9-]+", case_id):
            raise ValueError(f"Invalid case ID: {case_id}")
        if (
            case_id in result
            or not valid_revision(case.get("version"))
            or case.get("tier") != "heavy"
        ):
            raise ValueError(f"Duplicate/unsupported case: {case_id}")
        if not case.get("skills") or not case.get("phases"):
            raise ValueError(f"Empty scope/phases: {case_id}")
        for skill in case["skills"]:
            if (
                not re.fullmatch(r"[a-z0-9-]+", skill)
                or not (root / "skills" / skill / "SKILL.md").is_file()
            ):
                raise ValueError(f"Unknown skill: {skill}")
        phase_ids = set()
        for phase in case["phases"]:
            if not re.fullmatch(r"[a-z0-9-]+", phase["id"]) or phase["id"] in phase_ids:
                raise ValueError(f"Invalid/duplicate phase: {phase['id']}")
            phase_ids.add(phase["id"])
            if not local(path.parent, phase["request"]).is_file():
                raise ValueError(f"Missing request: {case_id}")
            if (
                phase.get("overlay")
                and not local(path.parent, phase["overlay"]).is_dir()
            ):
                raise ValueError(f"Missing overlay: {case_id}")
        rubric = read_json(path.parent / "rubric.json")
        criteria = rubric.get("criteria", [])
        ids = [x["id"] for x in criteria]
        if (
            not valid_revision(rubric.get("version"))
            or not ids
            or len(ids) != len(set(ids))
            or not any(c.get("required") is True for c in criteria)
        ):
            raise ValueError(f"Invalid rubric: {case_id}")
        for criterion in criteria:
            if not isinstance(criterion.get("required"), bool) or any(
                not criterion.get(k) for k in ("requirement", "pass_when", "fail_when")
            ):
                raise ValueError(f"Unanchored criterion: {case_id}")
        check_ids = []
        for check in case.get("checks", []):
            check_ids.append(check["id"])
            if check["kind"] not in {"unchanged", "no_tags", "commit_count", "python"}:
                raise ValueError(f"Unsupported check: {case_id}")
            if (
                check["kind"] == "python"
                and not local(path.parent, check["file"]).is_file()
            ):
                raise ValueError(f"Missing oracle: {case_id}")
            if check["kind"] == "unchanged":
                for name in check["paths"]:
                    if not local(path.parent / "fixture", name).exists():
                        raise ValueError(f"Unknown preservation input: {name}")
        if len(check_ids) != len(set(check_ids)):
            raise ValueError(f"Duplicate deterministic check: {case_id}")
        if not (path.parent / "fixture").is_dir():
            raise ValueError(f"Missing fixture: {case_id}")
        if (
            case.get("hook")
            and not local(path.parent / "fixture", case["hook"]).is_file()
        ):
            raise ValueError(f"Missing hook: {case_id}")
        files(path.parent)  # Reject unsafe assets before any model call.
        result[case_id] = case
    if not result:
        raise ValueError("No canary cases")
    covered = {name for case in result.values() for name in case["skills"]}
    available = {p.parent.name for p in (root / "skills").glob("*/SKILL.md")}
    if covered != available:
        raise ValueError(f"Unmapped skill bundles: {available - covered}")
    return result


def skill_files(
    root: Path, names: list[str], ref: str | None = None
) -> dict[str, bytes]:
    if ref:
        commit = git(root, "rev-parse", "--verify", f"{ref}^{{commit}}")
        paths = git(
            root,
            "ls-tree",
            "-r",
            "--name-only",
            commit,
            "--",
            *[f"skills/{n}" for n in names],
        ).splitlines()
        return {
            name: subprocess.check_output(["git", "show", f"{commit}:{name}"], cwd=root)
            for name in paths
        }
    return {
        f"skills/{name}/{path}": data
        for name in names
        for path, data in files(root / "skills" / name).items()
    }


def engine_identity(root: Path) -> str:
    return fingerprint(
        {
            p: digest((root / p).read_bytes())
            for p in (
                "tools/canary.py",
                "tools/canary_runtime.py",
                "requirements-dev.txt",
            )
        }
    )


def grading_identity(root: Path) -> str:
    return fingerprint(hashes(files(root / "evals/graders")))


def identity(root: Path, case: dict, ref: str | None = None) -> dict:
    return {
        "case": fingerprint(hashes(files(root / "evals/cases" / case["id"]))),
        "engine": engine_identity(root),
        "grader": grading_identity(root),
        "skills": hashes(skill_files(root, case["skills"], ref)),
    }


def settings(model: str, effort: str, timeout: int) -> dict:
    if not model.strip() or timeout <= 0:
        raise ValueError("Explicit model and positive timeout required")
    return {"model": model, "effort": effort, "timeout_seconds": timeout}


def environment() -> dict:
    binary = shutil.which("codex")
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "codex": subprocess.check_output([binary, "--version"], text=True).strip()
        if binary
        else "unavailable",
        "dependency_lock": digest((ROOT / "requirements-dev.txt").read_bytes()),
    }


def grade_schema(rubric: dict) -> dict:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["criteria"],
        "properties": {
            "criteria": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["id", "status", "reason", "evidence"],
                    "properties": {
                        "id": {
                            "type": "string",
                            "enum": [x["id"] for x in rubric["criteria"]],
                        },
                        "status": {"type": "string", "enum": sorted(STATES)},
                        "reason": {"type": "string"},
                        "evidence": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "additionalProperties": False,
                                "required": ["path", "quote"],
                                "properties": {
                                    "path": {"type": "string"},
                                    "quote": {"type": "string"},
                                },
                            },
                        },
                    },
                },
            }
        },
    }


def validate_grade(
    grade: dict,
    rubric: dict,
    packet: Path,
    artifact_files: dict[str, bytes] | None = None,
) -> str:
    expected = {c["id"]: c for c in rubric["criteria"]}
    received = grade.get("criteria", [])
    ids = [c.get("id") for c in received]
    if len(ids) != len(set(ids)) or set(ids) != set(expected):
        raise ValueError("Grader omitted, duplicated or invented a criterion")
    required = []
    for row in received:
        if row.get("status") not in STATES or not row.get("reason", "").strip():
            raise ValueError("Invalid status or missing grading reason")
        evidence = row.get("evidence", [])
        if row["status"] != "inconclusive" and not evidence:
            raise ValueError("Pass/fail requires artifact evidence")
        for item in evidence:
            if not item["path"].startswith("artifacts/") or not item["quote"].strip():
                raise ValueError(
                    "Evidence must quote a produced artifact, not the rubric"
                )
            path = local(packet, item["path"])
            evidence_text = (
                artifact_files.get(item["path"].removeprefix("artifacts/"), b"").decode(
                    errors="replace"
                )
                if artifact_files is not None
                else path.read_text(errors="replace")
                if path.is_file()
                else ""
            )
            if item["quote"] not in evidence_text:
                raise ValueError("Grader cited missing evidence or an invented quote")
        if expected[row["id"]]["required"]:
            required.append(row["status"])
    if not required:
        raise ValueError("At least one required criterion is necessary")
    return (
        "fail"
        if "fail" in required
        else "inconclusive"
        if "inconclusive" in required
        else "pass"
    )


def new_record(root: Path, kind: str) -> tuple[Path, dict]:
    now = datetime.now(UTC)
    run_id = now.strftime("%Y%m%dT%H%M%S") + "-" + uuid4().hex
    directory = root / "docs/validation/canary" / run_id
    directory.mkdir(parents=True, exist_ok=False)
    return directory, {
        "schema_version": 1,
        "run_id": run_id,
        "kind": kind,
        "created_at": now.isoformat(),
        "status": "inconclusive",
    }


def finish(directory: Path, report: dict) -> Path:
    report["finished_at"] = datetime.now(UTC).isoformat()
    report["evidence"] = hashes(files(directory))
    path = directory / "report.json"
    save(path, report)
    return path


def verified_record(path: Path) -> dict:
    record = read_json(path)
    if record.get("schema_version") != 1 or not record.get("evidence"):
        raise ValueError("Missing run provenance/evidence")
    for name, expected in record["evidence"].items():
        target = local(path.parent.resolve(), name)
        if not target.is_file() or digest(target.read_bytes()) != expected:
            raise ValueError(f"Changed/missing evidence: {name}")
    return record


def init_fixture(workspace: Path, content: dict[str, bytes]) -> str:
    write_files(workspace, content)
    git(workspace, "init", "-q", "-b", "main")
    git(workspace, "config", "user.name", "Canary Fixture")
    git(workspace, "config", "user.email", "canary@example.invalid")
    git(workspace, "add", ".")
    git(workspace, "commit", "-qm", "Fixture baseline")
    return git(workspace, "rev-parse", "HEAD")


def preserved(workspace: Path, name: str, initial: dict[str, bytes]) -> bool:
    """Compare a file or full directory, including additions and deletions."""
    path = local(workspace, name)
    if name in initial:
        return path.is_file() and path.read_bytes() == initial[name]
    prefix = name.rstrip("/") + "/"
    expected = {
        p.removeprefix(prefix): b for p, b in initial.items() if p.startswith(prefix)
    }
    return path.is_dir() and files(path) == expected


def deterministic(
    case: dict, case_dir: Path, workspace: Path, initial: dict, head: str
) -> list[dict]:
    results = []
    for check in case.get("checks", []):
        detail = {}
        try:
            kind = check["kind"]
            if kind == "unchanged":
                detail = {p: preserved(workspace, p, initial) for p in check["paths"]}
                passed = all(detail.values())
            elif kind == "no_tags":
                detail = {"tags": git(workspace, "tag")}
                passed = not detail["tags"]
            elif kind == "commit_count":
                git(workspace, "merge-base", "--is-ancestor", head, "HEAD")
                detail = {
                    "added_commits": int(
                        git(workspace, "rev-list", "--count", f"{head}..HEAD")
                    ),
                    "expected": check["expected"],
                }
                passed = detail["added_commits"] == check["expected"]
            else:
                source = local(case_dir, check["file"]).read_text()
                detail = runtime.capture(
                    runtime.sandbox_command(
                        workspace, [sys.executable, "-I", "-B", "-c", source]
                    ),
                    workspace,
                    60,
                )
                passed = detail["exit_code"] == 0 and not detail["timed_out"]
            results.append(
                {
                    "id": check["id"],
                    "status": "pass" if passed else "fail",
                    "evidence": detail,
                }
            )
        except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
            results.append(
                {"id": check["id"], "status": "inconclusive", "error": str(exc)}
            )
    return results


def grade_packet(
    root: Path, packet: Path, output: Path, rubric: dict, config: dict
) -> tuple[dict, dict, str]:
    save(packet / "rubric.json", rubric)
    git(packet, "init", "-q", "-b", "main")
    result = runtime.execute(
        packet,
        (root / "evals/graders/review.md").read_text(),
        output,
        config,
        grade_schema(rubric),
    )
    # Persist the transcript before parsing; malformed grading is still evidence.
    save(output.with_suffix(".execution.json"), result)
    if not result["completed"]:
        return result, {}, "inconclusive"
    grade = json.loads(result["reply"])
    return result, grade, validate_grade(grade, rubric, packet)


def calibration(root: Path, config: dict) -> Path:
    directory, report = new_record(root, "calibration")
    report.update(
        grader=grading_identity(root),
        engine=engine_identity(root),
        settings=config,
        environment=environment(),
    )
    save(directory / "attempt.json", report)
    try:
        examples = read_json(root / "evals/graders/calibration.json")
        save(directory / "inputs.json", examples)
        outcomes = []
        with tempfile.TemporaryDirectory(prefix="canary-") as temp:
            private = Path(temp).resolve() / "private"
            private.write_text("grader-only sentinel")
            for index, example in enumerate(examples["examples"]):
                packet = Path(temp).resolve() / str(index)
                packet.mkdir()
                write_files(
                    packet / "artifacts",
                    {k: v.encode() for k, v in example["artifacts"].items()},
                )
                (packet / "request.md").write_text(example["request"])
                check = runtime.probe(packet, private)
                save(directory / f"{index}-isolation.json", check)
                if not check["passed"]:
                    raise RuntimeError("Calibration isolation probe failed")
                result, grade, status = grade_packet(
                    root,
                    packet,
                    directory / f"{index}-reply.json",
                    examples["rubric"],
                    config,
                )
                save(directory / f"{index}-grade.json", grade)
                outcomes.append(status == example["expected"])
        report["status"] = "pass" if outcomes and all(outcomes) else "fail"
        report["matched_controls"] = outcomes
    except (Exception, KeyboardInterrupt) as exc:
        report["error"] = f"{type(exc).__name__}: {exc}"
    return finish(directory, report)


def check_calibration(root: Path, path: Path, config: dict, env: dict) -> dict:
    record = verified_record(path)
    if any(
        (
            record.get("kind") != "calibration",
            record.get("status") != "pass",
            record.get("grader") != grading_identity(root),
            record.get("engine") != engine_identity(root),
            record.get("settings") != config,
            record.get("environment") != env,
        )
    ):
        raise ValueError("A passing, current grader calibration is required")
    inputs = read_json(path.parent / "inputs.json")
    if inputs != read_json(root / "evals/graders/calibration.json"):
        raise ValueError("Calibration controls changed")
    for index, example in enumerate(inputs["examples"]):
        execution = read_json(path.parent / f"{index}-reply.execution.json")
        require_completed(execution)
        if not read_json(path.parent / f"{index}-isolation.json").get("passed"):
            raise ValueError("Calibration isolation missing/failed")
        grade = read_json(path.parent / f"{index}-grade.json")
        if (
            json.loads(execution["reply"]) != grade
            or validate_grade(
                grade,
                inputs["rubric"],
                path.parent,
                {p: t.encode() for p, t in example["artifacts"].items()},
            )
            != example["expected"]
        ):
            raise ValueError("Calibration did not distinguish declared controls")
    return {
        "path": str(path.resolve()),
        "sha256": digest(path.read_bytes()),
        "grader": record["grader"],
    }


def run_case(
    root: Path,
    case_id: str,
    worker: dict,
    grader: dict,
    calibration_path: Path,
    ref: str | None = None,
) -> Path:
    case = cases(root)[case_id]
    case_dir = root / "evals/cases" / case_id
    directory, report = new_record(root, "behavior")
    report.update(
        case_id=case_id,
        identity=identity(root, case, ref),
        settings={"worker": worker, "grader": grader},
        environment=environment(),
        source_ref=ref,
    )
    save(
        directory / "attempt.json",
        {**report, "requested_calibration": str(calibration_path)},
    )
    try:
        calibration_info = check_calibration(
            root, calibration_path, grader, report["environment"]
        )
        # Copy the complete calibration record and evidence: no fragile absolute
        # dependency on the original run directory for future release checks.
        write_files(directory / "calibration", files(calibration_path.parent))
        report["calibration"] = calibration_info
        write_files(directory / "inputs/case", files(case_dir))
        selected = skill_files(root, case["skills"], ref)
        write_files(directory / "inputs/bundles", selected)
        with tempfile.TemporaryDirectory(prefix="canary-") as temp:
            temp_root = Path(temp).resolve()
            workspace = temp_root / "worker"
            workspace.mkdir()
            head = init_fixture(workspace, {**files(case_dir / "fixture"), **selected})
            initial = files(workspace)
            write_files(directory / "initial", initial)
            hook = None
            if case.get("hook"):
                hook = local(workspace, case["hook"]).read_bytes()
                hook_path = workspace / ".git/hooks/pre-commit"
                hook_path.write_bytes(hook)
                hook_path.chmod(0o755)
            report["fixture_head"] = head
            isolation = runtime.probe(workspace, case_dir / "rubric.json")
            save(directory / "isolation.json", isolation)
            if not isolation["passed"]:
                raise RuntimeError("Worker canary read/network boundary failed")
            phase_results = []
            for phase in case["phases"]:
                if phase.get("overlay"):
                    write_files(workspace, files(local(case_dir, phase["overlay"])))
                request = local(case_dir, phase["request"]).read_text()
                phase_dir = directory / "phases" / phase["id"]
                phase_dir.mkdir(parents=True)
                (phase_dir / "request.md").write_text(request)
                prompt = (
                    request
                    + "\n\nUse only this fixture and the supplied skills/. This phase is a fresh context. Preserve prior reports. CANARY_PYTHON points to the prepared Python runtime. Do not install packages or use external services.\n"
                )
                result = runtime.execute(
                    workspace, prompt, phase_dir / "reply.md", worker
                )
                save(phase_dir / "execution.json", result)
                write_files(phase_dir / "workspace", files(workspace))
                save(
                    phase_dir / "git.json",
                    {
                        "head": git(workspace, "rev-parse", "HEAD"),
                        "status": git(workspace, "status", "--porcelain"),
                        "diff": git(workspace, "diff", head),
                        "log": git(workspace, "log", "--oneline"),
                        "tags": git(workspace, "tag"),
                    },
                )
                phase_results.append(result["completed"])
                if not result["completed"]:
                    break
            checks = deterministic(case, case_dir, workspace, initial, head)
            unchanged_skills = all(
                local(workspace, p).is_file() and local(workspace, p).read_bytes() == b
                for p, b in selected.items()
            )
            checks.append(
                {
                    "id": "runner.skills-preserved",
                    "status": "pass" if unchanged_skills else "fail",
                }
            )
            if hook is not None:
                checks.append(
                    {
                        "id": "runner.hook-preserved",
                        "status": "pass"
                        if (workspace / ".git/hooks/pre-commit").read_bytes() == hook
                        else "fail",
                    }
                )
            save(directory / "deterministic.json", checks)
            report["deterministic"] = checks
            if len(phase_results) != len(case["phases"]) or not all(phase_results):
                raise RuntimeError("Worker phase incomplete; partial results retained")
            packet = temp_root / "grader"
            packet.mkdir()
            write_files(packet / "artifacts", files(directory / "phases"))
            write_files(packet / "initial", initial)
            write_files(
                packet / "requests",
                {
                    p["id"] + ".md": local(case_dir, p["request"]).read_bytes()
                    for p in case["phases"]
                },
            )
            isolation = runtime.probe(packet, case_dir / "rubric.json")
            save(directory / "grader-isolation.json", isolation)
            if not isolation["passed"]:
                raise RuntimeError("Grader boundary failed")
            rubric = read_json(case_dir / "rubric.json")
            result, grade, semantic_status = grade_packet(
                root, packet, directory / "grade-reply.json", rubric, grader
            )
            save(directory / "grade.json", grade)
            report["semantic"] = semantic_status
            statuses = [semantic_status, *[c["status"] for c in checks]]
            report["status"] = (
                "fail"
                if "fail" in statuses
                else "inconclusive"
                if "inconclusive" in statuses
                else "pass"
            )
    except (Exception, KeyboardInterrupt) as exc:
        report["error"] = f"{type(exc).__name__}: {exc}"
    return finish(directory, report)


def require_completed(execution: dict) -> None:
    if (
        execution.get("completed") is not True
        or execution.get("exit_code") != 0
        or execution.get("timed_out") is not False
        or execution.get("interrupted", False)
        or not isinstance(execution.get("reply"), str)
    ):
        raise ValueError("Execution incomplete; cannot establish acceptance")


def verified_behavior(root: Path, path: Path, case: dict) -> dict:
    """Recompute acceptance from archived criteria and executions, not a status label."""
    row = verified_record(path)
    directory = path.parent
    stored = row["identity"]
    if (
        fingerprint(hashes(files(directory / "inputs/case"))) != stored["case"]
        or hashes(files(directory / "inputs/bundles")) != stored["skills"]
    ):
        raise ValueError("Input archives do not match declared identity")
    for name in ("isolation.json", "grader-isolation.json"):
        if not read_json(directory / name).get("passed"):
            raise ValueError("Isolation probe missing/failed")
    for phase in case["phases"]:
        phase_dir = directory / "phases" / phase["id"]
        execution = read_json(phase_dir / "execution.json")
        require_completed(execution)
        if (phase_dir / "reply.md").read_text() != execution["reply"]:
            raise ValueError("Worker reply differs from recorded execution")
    execution = read_json(directory / "grade-reply.execution.json")
    require_completed(execution)
    grade = read_json(directory / "grade.json")
    if json.loads(execution["reply"]) != grade:
        raise ValueError("Grader reply differs from recorded judgment")
    semantic = validate_grade(
        grade,
        read_json(root / "evals/cases" / case["id"] / "rubric.json"),
        directory,
        files(directory / "phases"),
    )
    checks = read_json(directory / "deterministic.json")
    expected = {c["id"] for c in case.get("checks", [])} | {"runner.skills-preserved"}
    if case.get("hook"):
        expected.add("runner.hook-preserved")
    if (
        len(checks) != len(expected)
        or {c["id"] for c in checks} != expected
        or any(c["status"] not in STATES for c in checks)
    ):
        raise ValueError("Missing/duplicate/invalid deterministic result")
    statuses = [semantic, *[c["status"] for c in checks]]
    status = (
        "fail"
        if "fail" in statuses
        else "inconclusive"
        if "inconclusive" in statuses
        else "pass"
    )
    if status != row["status"] or status == "inconclusive":
        raise ValueError("Summary does not establish a completed case result")
    check_calibration(
        root,
        directory / "calibration/report.json",
        row["settings"]["grader"],
        row["environment"],
    )
    return row


def release_gate(root: Path, paths: list[Path], baseline: str) -> dict:
    catalog = cases(root)
    records = []
    errors = []
    # Include all retained local attempts, so explicitly listing a green result
    # cannot hide a newer failure for the same inputs and settings.
    paths = sorted(
        {p.resolve() for p in paths}
        | set((root / "docs/validation/canary").glob("*/report.json"))
    )
    for path in paths:
        try:
            row = verified_record(path)
            if row.get("kind") != "behavior":
                continue
            row["record_path"] = str(path)
            records.append(row)
        except (ValueError, KeyError, OSError) as exc:
            errors.append(f"{path}: {exc}")
    matched = {}
    for case_id, case in catalog.items():
        current = identity(root, case)
        previous = identity(root, case, baseline)
        relevant = [
            r
            for r in records
            if r.get("case_id") == case_id and r.get("identity") in (current, previous)
        ]
        latest = {}
        for row in sorted(relevant, key=lambda r: r["created_at"]):
            key = fingerprint(
                {k: row[k] for k in ("identity", "settings", "environment")}
            )
            latest[key] = row
        candidate_rows = [
            r
            for r in latest.values()
            if r.get("case_id") == case_id
            and r.get("identity") == current
            and r.get("status") == "pass"
        ]
        match = None
        for candidate in candidate_rows:
            for old in latest.values():
                if (
                    old.get("case_id") == case_id
                    and old.get("identity") == previous
                    and old.get("settings") == candidate["settings"]
                    and old.get("environment") == candidate["environment"]
                    and old.get("status") in {"pass", "fail"}
                ):
                    # Revalidate the copied calibration; status fields alone
                    # cannot turn uncalibrated/self-reported output into evidence.
                    try:
                        for row in (candidate, old):
                            record_path = Path(row["record_path"])
                            verified_behavior(root, record_path, case)
                    except (ValueError, OSError, KeyError) as exc:
                        errors.append(f"{case_id}: invalid behavior evidence: {exc}")
                        continue
                    match = {
                        "candidate": candidate["record_path"],
                        "baseline": old["record_path"],
                        "baseline_status": old["status"],
                    }
                    break
            if match:
                break
        if match is None:
            errors.append(
                f"{case_id}: missing current passing candidate and comparable executed baseline"
            )
        else:
            matched[case_id] = match
    return {
        "status": "pass" if not errors else "fail",
        "baseline": baseline,
        "cases": matched,
        "errors": errors,
        "scope": "behavior evidence only; still requires normal final checks, review and release authorization",
    }


def affected(root: Path, base: str) -> dict:
    changed = set(git(root, "diff", "--name-only", base, "--", "skills").splitlines())
    changed.update(
        git(root, "ls-files", "--others", "--exclude-standard", "skills").splitlines()
    )
    mapping = {
        name: [
            c["id"]
            for c in cases(root).values()
            if any(name.startswith(f"skills/{s}/") for s in c["skills"])
        ]
        for name in sorted(changed)
    }
    return {
        "changed_files": mapping,
        "heavy_cases": sorted({c for v in mapping.values() for c in v}),
        "cadence": "deferred until release; run fast checks for normal PRs",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate", help="Fast case/resource validation; no model calls")
    sub.add_parser("list")
    impact = sub.add_parser("affected")
    impact.add_argument("--base", default="6573f8f422cb6528981ff43bc0d20c656096e7dc")
    for name in ("calibrate", "run"):
        command = sub.add_parser(name)
        command.add_argument("--model", required=True)
        command.add_argument("--effort", default="medium")
        command.add_argument("--timeout", type=int, default=900)
        if name == "run":
            command.add_argument("case")
            command.add_argument("--grader-model", required=True)
            command.add_argument("--grader-effort", default="medium")
            command.add_argument("--calibration", type=Path, required=True)
            command.add_argument("--baseline")
    gate = sub.add_parser("release-gate")
    gate.add_argument("reports", type=Path, nargs="*")
    gate.add_argument("--baseline", default="6573f8f422cb6528981ff43bc0d20c656096e7dc")
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            catalog = cases()
            print(
                f"{len(catalog)} versioned canary cases validate. Heavy behavior status: not run."
            )
        elif args.command == "list":
            print(
                json.dumps(
                    [
                        {k: c[k] for k in ("id", "title", "tier", "skills")}
                        for c in cases().values()
                    ],
                    indent=2,
                )
            )
        elif args.command == "affected":
            print(json.dumps(affected(ROOT, args.base), indent=2))
        elif args.command == "release-gate":
            result = release_gate(ROOT, args.reports, args.baseline)
            print(json.dumps(result, indent=2))
            return int(result["status"] != "pass")
        else:
            config = settings(args.model, args.effort, args.timeout)
            if args.command == "calibrate":
                path = calibration(ROOT, config)
            else:
                grader = settings(args.grader_model, args.grader_effort, args.timeout)
                failures = []
                for case_id in cases() if args.case == "all" else [args.case]:
                    path = run_case(
                        ROOT, case_id, config, grader, args.calibration, args.baseline
                    )
                    print(path)
                    failures.append(read_json(path)["status"] != "pass")
                return int(any(failures))
            print(path)
            return int(read_json(path)["status"] != "pass")
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as exc:
        print(f"Canary: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

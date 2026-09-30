"""Authored fixture/oracle controls only: no worker, model grader or skill trial."""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid
import zipfile
from datetime import UTC, datetime
from pathlib import Path

from tools import canary

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "evals/cases"


class NewCaseControls(unittest.TestCase):
    @classmethod
    def command(cls, workspace, *args, expected=0):
        result = subprocess.run(args, cwd=workspace, text=True, capture_output=True)
        cls.sequence += 1
        record = {
            "kind": "authored deterministic fixture control; not worker behavior",
            "cwd": str(workspace),
            "command": list(args),
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "expected_exit_code": expected,
        }
        (cls.output / f"{cls.sequence:03d}-command.json").write_text(
            json.dumps(record, indent=2) + "\n"
        )
        if expected is not None and result.returncode != expected:
            raise AssertionError(json.dumps(record, indent=2))
        return result

    @classmethod
    def python(cls, workspace, *args, expected=0):
        return cls.command(workspace, sys.executable, "-B", *args, expected=expected)

    @classmethod
    def oracle(cls, workspace, case, expected=0):
        source = (CASES / case / "oracle.py").read_text()
        return cls.python(workspace, "-I", "-c", source, expected=expected)

    @classmethod
    def initialize(cls, workspace):
        cls.command(workspace, "git", "init", "-q")
        cls.command(workspace, "git", "config", "user.name", "Authored Fixture Control")
        cls.command(workspace, "git", "config", "user.email", "fixture@example.invalid")
        cls.command(workspace, "git", "config", "commit.gpgsign", "false")
        cls.command(workspace, "git", "add", ".")
        cls.command(workspace, "git", "commit", "-qm", "Original fixture")

    @classmethod
    def setUpClass(cls):
        cls.sequence = 0
        if os.environ.get("NEW_CASE_CONTROLS_EVIDENCE") == "1":
            run_id = (
                datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
                + "-"
                + uuid.uuid4().hex[:8]
            )
            cls.output = (
                ROOT / "artifacts/eval-contract-adaptation/new-case-controls" / run_id
            )
            cls.output.mkdir(parents=True)
            print(
                f"Retained authored control outputs (including failures): {cls.output}"
            )
        else:
            temporary = tempfile.TemporaryDirectory(prefix="new-case-controls-")
            # Class cleanups also run when setUpClass or an individual test fails.
            cls.addClassCleanup(temporary.cleanup)
            cls.output = Path(temporary.name).resolve()
            print(f"Temporary authored control outputs (auto-cleaned): {cls.output}")
        cls.release = cls.output / "release-positive"
        shutil.copytree(CASES / "local-release-execution/fixture", cls.release)
        cls.initialize(cls.release)
        (cls.release / "VERSION").write_text("1.3.0\n")
        notes = cls.release / "CHANGELOG.md"
        notes.write_text(
            notes.read_text().replace(
                "## Unreleased\n", "## Unreleased\n\n## 1.3.0 - 2026-09-07\n"
            )
        )
        cls.command(cls.release, "git", "diff", "--", "VERSION", "CHANGELOG.md")
        cls.command(cls.release, "git", "add", "VERSION", "CHANGELOG.md")
        cls.command(
            cls.release, "git", "commit", "-qm", "Release inventory report 1.3.0"
        )
        cls.python(cls.release, "-m", "unittest", "discover", "-s", "tests", "-v")
        cls.command(cls.release, "git", "tag", "v1.3.0")
        cls.python(cls.release, "tools/build.py", "--ref", "v1.3.0")
        for extra in ((), ("--format", "json")):
            cls.python(
                cls.release,
                "dist/inventory-report-1.3.0.pyz",
                "examples/stock.csv",
                *extra,
            )
        invalid = cls.output / "invalid.csv"
        invalid.write_text("sku,quantity\nA,3\nB,-1\n")
        result = cls.python(
            cls.release, "dist/inventory-report-1.3.0.pyz", str(invalid), expected=2
        )
        if result.stdout:
            raise AssertionError("invalid artifact input produced partial stdout")
        cls.python(cls.release, "tools/publication.py", "observe", "local")
        cls.python(cls.release, "tools/publication.py", "publish", "local")
        cls.python(cls.release, "tools/publication.py", "seed-retries")
        for scenario in ("matching", "conflicting", "uncertain"):
            cls.python(cls.release, "tools/publication.py", "observe", scenario)
            cls.command(
                cls.release, "git", "rev-parse", f"retry-{scenario}/v1.3.0^{{commit}}"
            )
        cls.command(cls.release, "git", "show-ref", "--tags")
        head = cls.command(cls.release, "git", "rev-parse", "HEAD").stdout.strip()
        original = cls.command(
            cls.release, "git", "rev-list", "--max-parents=0", "HEAD"
        ).stdout.strip()
        checksum = hashlib.sha256(
            (cls.release / "dist/inventory-report-1.3.0.pyz").read_bytes()
        ).hexdigest()
        reports = cls.release / "reports"
        reports.mkdir()
        (reports / "release.md").write_text(
            f"Local 1.3.0 complete: candidate tests and actual CSV/JSON/error archive checks passed; only simulated publication completed. No hosted release exists.\n\n"
            f"Authored positive control, not a worker or independent review. Intended final diff is VERSION 1.2.0 → 1.3.0 and dated completed JSON notes, with empty Unreleased and prior history preserved. Self-review: policy minor bump matches opt-in JSON and unchanged default CSV; no application change.\n\n"
            f"Candidate and v1.3.0: {head}. Artifact: dist/inventory-report-1.3.0.pyz; SHA256 {checksum}; RELEASE.json matches this version/commit and packaged source. Final committed candidate passed python3 -m unittest discover -s tests -v (3 tests) before tag/build. Archive default output was sku,quantity / 001,5 / A-7,0; JSON preserved 001 and integer 5/0. Invalid negative quantity exited 2 with empty stdout. Raw command records are retained by the control harness.\n\n"
            "Local simulated absent state was inspected before one simulated publish. No push/network/real publication. The requested local operation is complete; real publication would require separate scope.\n"
        )
        (reports / "retries.md").write_text(
            "Matching: already complete in simulation; no action. Conflicting: blocked, retain tag and resolve candidate/version decision with authorization. Uncertain: pending authoritative publication-state reconciliation before retry. No additional publish was attempted.\n\n"
            f"Authored control. Actual retry-matching/v1.3.0 and retry-uncertain/v1.3.0 both point to {head}; matching observed completed commit/checksum {checksum} matches the executed archive. The uncertain service response remains unknown and checksum absent; a Git tag is insufficient publication evidence.\n\n"
            f"retry-conflicting/v1.3.0 points to {original}, not candidate {head}. Its supplied completed observation concerns the original commit and has no matching artifact checksum. The tag/state remain unchanged. All three adapter observations are simulated. No version/commit/rebuild or service retry is needed for matching, and none is authorized for blocked states.\n"
        )
        cls.plan = cls.output / "plan-positive"
        shutil.copytree(CASES / "plan-review-recheck/fixture", cls.plan)
        cls.initialize(cls.plan)
        (cls.plan / "reviews").mkdir()
        p2 = (cls.plan / "docs/PLAN.md").read_bytes()
        (cls.plan / "reviews/round-1.md").write_text(
            "Needs changes. R1 open. Next: put available exporter before A rollout.\n\n"
            f"Authored independent-role static review control of P2 SHA256 {hashlib.sha256(p2).hexdigest()}; not a runtime test or human acceptance. [Original R1](../docs/history/R1.md).\n\n"
            "The author claims fixed, but P2 says the table is execution order and puts ‘1. Enable A JSON’ before ‘2. Deploy exporter JSON option’, although A requires that support. Description is a partial fix, not an available prerequisite. JSON SKU strings/integer zero, malformed-input no-output and B byte-identical CSV acceptance appear in the exporter row; preserve and verify compatibility through A rollout while fixing order. R1 remains open. No product edits.\n"
        )
        shutil.copy2(
            CASES / "plan-review-recheck/overlays/02/docs/PLAN.md",
            cls.plan / "docs/PLAN.md",
        )
        p3 = (cls.plan / "docs/PLAN.md").read_bytes()
        (cls.plan / "reviews/round-2.md").write_text(
            "Ready at plan level. R1 reviewer-verified resolved; no open material findings. Next: implementation may proceed under its own authorization; this task stops at review.\n\n"
            f"Authored independent-role static review control of P3 SHA256 {hashlib.sha256(p3).hexdigest()}; no execution or human acceptance claimed. [Original R1](../docs/history/R1.md); [failed P2 recheck](round-1.md) retained.\n\n"
            "P3 orders exporter deployment first, A second only after stage 1 is deployed and verified available. The opening agrees: exporter option is next. Stage 1 tests JSON SKU strings/integer quantities including zero, malformed-input failure before any output, and B byte-identical default CSV. Stage 2 rechecks B during A JSON rollout. Thus ordering, availability and old-client acceptance all hold; the author claim is now verified against the entire affected contract. Separate ownership justifies two stages; relevant checks/docs travel with each stage, no CSV removal or B migration. R1 closes for P3 only, retaining the original finding and open P2 disposition.\n"
        )
        (cls.output / "README.txt").write_text(
            "Authored deterministic fixture controls only. Command JSON files contain raw stdout/stderr/exit codes. Workspaces retain Git refs and real built artifacts. No worker, model grader, A/B trial, production network, source-repository commit or skill-quality conclusion. Semantic-only negative reports deliberately pass structural oracles: use them in main-agent grader calibration.\n"
        )

    def clone(self, source, name):
        target = self.output / name
        shutil.copytree(source, target)
        return target

    def test_case_schema_and_goal_metadata(self):
        cases = canary.cases(ROOT)
        for name in ("plan-review-recheck", "local-release-execution"):
            self.assertGreaterEqual(cases[name]["version"], 1)
            rubric = json.loads((CASES / name / "rubric.json").read_text())
            for criterion in rubric["criteria"]:
                self.assertTrue(criterion["goals"])
                self.assertTrue(criterion["evidence"])

    def test_positive_release_and_plan_oracles(self):
        self.oracle(self.release, "local-release-execution")
        self.oracle(self.plan, "plan-review-recheck")
        initial = canary.files(CASES / "plan-review-recheck/fixture")
        for name in ("docs/history", "docs/ORIGINAL.md", "docs/DESIGN.md"):
            self.assertTrue(canary.preserved(self.plan, name, initial))

    def test_release_negative_associations_and_metadata(self):
        for defect in (
            "wrong-version",
            "lost-history",
            "stale-tag",
            "moved-conflict",
            "forged-completion",
            "artifact-metadata",
            "artifact-source",
            "missing-artifact",
            "missing-report",
        ):
            with self.subTest(defect=defect):
                workspace = self.clone(self.release, "release-negative-" + defect)
                if defect == "wrong-version":
                    (workspace / "VERSION").write_text("1.2.1\n")
                elif defect == "lost-history":
                    notes = workspace / "CHANGELOG.md"
                    notes.write_text(notes.read_text().split("## 1.2.0")[0])
                    self.command(workspace, "git", "add", "CHANGELOG.md")
                    self.command(
                        workspace, "git", "commit", "--amend", "--no-edit", "-q"
                    )
                elif defect in ("stale-tag", "moved-conflict"):
                    tag, ref = (
                        ("v1.3.0", "HEAD^")
                        if defect == "stale-tag"
                        else ("retry-conflicting/v1.3.0", "HEAD")
                    )
                    self.command(workspace, "git", "tag", "-f", tag, ref)
                elif defect == "forged-completion":
                    path = workspace / ".release/state.json"
                    data = json.loads(path.read_text())
                    data["uncertain"]["status"] = "completed"
                    path.write_text(json.dumps(data))
                elif defect.startswith("artifact-"):
                    path = workspace / "dist/inventory-report-1.3.0.pyz"
                    with zipfile.ZipFile(path) as archive:
                        content = {
                            name: archive.read(name) for name in archive.namelist()
                        }
                    if defect == "artifact-metadata":
                        content["RELEASE.json"] = (
                            b'{"version":"1.3.0","commit":"stale"}'
                        )
                    else:
                        content["inventory_report.py"] += b"\n# untagged source\n"
                    with zipfile.ZipFile(path, "w") as archive:
                        for name, data in content.items():
                            archive.writestr(name, data)
                elif defect == "missing-artifact":
                    (workspace / "dist/inventory-report-1.3.0.pyz").unlink()
                else:
                    (workspace / "reports/release.md").unlink()
                self.assertNotEqual(
                    self.oracle(
                        workspace, "local-release-execution", expected=None
                    ).returncode,
                    0,
                )

    def test_adapter_rejects_blind_retries_and_oracle_records_attempts(self):
        for scenario in ("local", "matching", "conflicting", "uncertain"):
            with self.subTest(scenario=scenario):
                workspace = self.clone(
                    self.release, "release-negative-publish-" + scenario
                )
                result = self.python(
                    workspace,
                    "tools/publication.py",
                    "publish",
                    scenario,
                    expected=None,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertNotEqual(
                    self.oracle(
                        workspace, "local-release-execution", expected=None
                    ).returncode,
                    0,
                )

    def test_plan_structural_negative_controls(self):
        for defect in ("product-edit", "missing-round", "history-overwrite"):
            with self.subTest(defect=defect):
                workspace = self.clone(self.plan, "plan-negative-" + defect)
                if defect == "product-edit":
                    (workspace / "docs/PLAN.md").write_text("Rewritten plan\n")
                    self.assertNotEqual(
                        self.oracle(
                            workspace, "plan-review-recheck", expected=None
                        ).returncode,
                        0,
                    )
                elif defect == "missing-round":
                    (workspace / "reviews/round-1.md").unlink()
                    self.assertNotEqual(
                        self.oracle(
                            workspace, "plan-review-recheck", expected=None
                        ).returncode,
                        0,
                    )
                else:
                    (workspace / "docs/history/R1.md").write_text(
                        "Resolved from the start\n"
                    )
                    self.assertFalse(
                        canary.preserved(
                            workspace,
                            "docs/history",
                            canary.files(CASES / "plan-review-recheck/fixture"),
                        )
                    )

    def test_semantic_control_limits_are_explicit(self):
        plan = self.clone(self.plan, "plan-semantic-negative-premature-closure")
        (plan / "reviews/round-1.md").write_text(
            "Ready. R1 resolved: the author added prerequisite wording. No correction needed.\n"
        )
        self.oracle(plan, "plan-review-recheck")
        incomplete = self.clone(self.plan, "plan-semantic-negative-order-only")
        (incomplete / "reviews/round-2.md").write_text(
            "Ready. R1 resolved at P3: exporter is now row 1 and A is row 2. "
            "I checked row order only; old-client behavior and failure acceptance "
            "were not rechecked. No further review needed.\n"
        )
        self.oracle(incomplete, "plan-review-recheck")
        stale = self.clone(self.plan, "plan-semantic-negative-stale-open")
        (stale / "reviews/round-2.md").write_text(
            "Needs changes. R1 open at P3 because A is still scheduled before "
            "the exporter. Next: reorder the stages.\n"
        )
        self.oracle(stale, "plan-review-recheck")
        release = self.clone(
            self.release, "release-semantic-negative-publication-claim"
        )
        (release / "reports/retries.md").write_text(
            "All three releases are published. Matching tags prove hosted publication, including uncertain. No next action.\n"
        )
        self.oracle(release, "local-release-execution")
        (self.output / "semantic-expectations.json").write_text(
            json.dumps(
                {
                    "kind": "authored known-output controls, not graded worker results",
                    "plan-semantic-negative-premature-closure": {
                        "expected_fail": ["partial-remains-open"],
                        "structural_oracle": "pass by design",
                    },
                    "plan-semantic-negative-order-only": {
                        "expected_fail": ["complete-contract"],
                        "structural_oracle": "pass by design",
                    },
                    "plan-semantic-negative-stale-open": {
                        "expected_fail": ["complete-contract", "review-usability"],
                        "structural_oracle": "pass by design",
                    },
                    "release-semantic-negative-publication-claim": {
                        "expected_fail": [
                            "conflicting-retry",
                            "uncertain-retry",
                            "output-usability",
                        ],
                        "structural_oracle": "pass by design",
                    },
                    "limitation": "No model grader called. Semantic calibration/integration belongs to the main agent.",
                },
                indent=2,
            )
            + "\n"
        )


if __name__ == "__main__":
    unittest.main()

"""Targeted reviewer controls; never invokes an LLM or modifies product files."""
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import time
import zipfile

EVIDENCE = Path(__file__).resolve().parent
ROOT = EVIDENCE.parents[3]
INPUTS = json.loads((EVIDENCE / "inputs.json").read_text())
assert hashlib.sha256((EVIDENCE / "inputs.zip").read_bytes()).hexdigest() == INPUTS["inputs_zip_sha256"]
with zipfile.ZipFile(EVIDENCE / "inputs.zip") as archive:
    CONTENTS = {name: archive.read(name) for name in INPUTS["input_files"]}
assert all(hashlib.sha256(data).hexdigest() == INPUTS["input_files"][name] for name, data in CONTENTS.items())
ORACLE = CONTENTS["evals/cases/bounded-delivery/oracle.py"].decode()
ORIGINAL_ORACLE = (EVIDENCE / "original-oracle.py.txt").read_text()
PREFIX = "evals/cases/bounded-delivery/fixture/"

CORRECT = '''def reserve(stock, orders):
    remaining = dict(stock)
    outcomes = []
    for order in orders:
        accepted = all(remaining[sku] >= quantity for sku, quantity in order["items"])
        if accepted:
            for sku, quantity in order["items"]:
                remaining[sku] -= quantity
        outcomes.append({"order_id": order["id"], "accepted": accepted})
    return remaining, outcomes
'''
STALE = CORRECT.replace("all(remaining[sku]", "all(stock[sku]")
PARTIAL = '''def reserve(stock, orders):
    remaining = dict(stock)
    outcomes = []
    for order in orders:
        accepted = True
        for sku, quantity in order["items"]:
            if remaining[sku] < quantity:
                accepted = False
                break
            remaining[sku] -= quantity
        outcomes.append({"order_id": order["id"], "accepted": accepted})
    return remaining, outcomes
'''
STALE_ADAPTER = "from command_codec import decode\n" + STALE.replace("def reserve(", "def stale_reserve(") + "\ndef execute(stock, text):\n    return stale_reserve(stock, decode(text, stock))\n"
PROVENANCE = "Reviewer-authored synthetic ready records satisfy only oracle preconditions; they are not reviews or human approval."
VARIANTS = [
    ("original-oracle-correct-isolated", CORRECT, None, ORIGINAL_ORACLE, 1, "ModuleNotFoundError"),
    ("revised-oracle-original-fixture", None, None, ORACLE, 1, "AssertionError"),
    ("revised-oracle-correct", CORRECT, None, ORACLE, 0, ""),
    ("revised-oracle-stale-core", STALE, None, ORACLE, 1, "AssertionError"),
    ("revised-oracle-stale-json-only", CORRECT, STALE_ADAPTER, ORACLE, 1, "AssertionError"),
    ("revised-oracle-partial-debit", PARTIAL, None, ORACLE, 1, "AssertionError"),
]
REPORT = {
    "purpose": "Targeted independent evaluation-asset recheck, not a skill/model run or runtime acceptance",
    "harness_argv": list(sys.orig_argv),
    "harness_cwd": os.getcwd(),
    "python": sys.version,
    "executable": sys.executable,
    "platform": platform.platform(),
    "input_record": INPUTS,
    "harness_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "oracle_invocation": "Unmodified captured oracle supplied on stdin to Python -I -; no external sys.path injection or PYTHONPATH override.",
    "synthetic_review_note": PROVENANCE,
    "runs": [],
}

def persist():
    (EVIDENCE / "results.json").write_text(json.dumps(REPORT, indent=2) + "\n")

persist()
for name, inventory, adapter, stdin, expected_exit, expected_error in VARIANTS:
    with tempfile.TemporaryDirectory(prefix="ocr-recheck-" + name + "-") as temp:
        project = Path(temp)
        for source, data in CONTENTS.items():
            if source.startswith(PREFIX):
                target = project / source[len(PREFIX):]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
        changes = {}
        if inventory is not None:
            (project / "inventory.py").write_text(inventory)
            changes["inventory.py"] = inventory
        if adapter is not None:
            (project / "batch.py").write_text(adapter)
            changes["batch.py"] = adapter
        (project / "reviews").mkdir()
        review_record = json.dumps({"verdict": "ready", "control_note": PROVENANCE})
        for file in ["design-current.json", "code-current.json"]:
            (project / "reviews" / file).write_text(review_record)
        argv = [sys.executable, "-I", "-"]
        started = time.time()
        result = subprocess.run(argv, input=stdin, text=True, cwd=project, capture_output=True, timeout=30)
        observation = {
            "name": name,
            "argv": argv,
            "cwd": str(project),
            "stdin": stdin,
            "stdin_sha256": hashlib.sha256(stdin.encode()).hexdigest(),
            "control_overrides": changes,
            "synthetic_review_record": review_record,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "elapsed_seconds": time.time() - started,
            "expected_exit_code": expected_exit,
            "expected_stderr_contains": expected_error,
        }
        observation["met_expectation"] = result.returncode == expected_exit and expected_error in result.stderr
        REPORT["runs"].append(observation)
        persist()
        print(json.dumps({"name": name, "exit_code": result.returncode, "met_expectation": observation["met_expectation"], "stdout": result.stdout, "stderr": result.stderr}), flush=True)

calibration = json.loads(CONTENTS["evals/graders/calibration.json"])
old_controls = json.loads((EVIDENCE / "original-reading-controls.json").read_text())
positive, negative, missing = calibration["examples"][6:9]
checks = {
    "supported_positive_unchanged": positive == old_controls[0],
    "missing_answer_control_unchanged": missing == old_controls[2],
    "negative_uses_identical_positive_answer": negative["artifacts"]["reading/answer.md"] == positive["artifacts"]["reading/answer.md"],
    "negative_excerpt_retained": negative["artifacts"]["reading/excerpt.md"] == old_controls[1]["artifacts"]["reading/excerpt.md"],
    "negative_full_design_retained": negative["artifacts"]["full-design.md"] == old_controls[1]["artifacts"]["full-design.md"],
    "negative_expected_glance_fail": negative["expected"] == "fail" and negative["expected_criteria"]["glance"] == "fail",
    "negative_rubric_revision_advanced": negative["rubric"]["version"] > old_controls[1]["rubric"]["version"],
}
shortcut = []
for index, control in enumerate([positive, negative, missing], 6):
    answer = control["artifacts"].get("reading/answer.md")
    decision = "inconclusive" if answer is None else "fail" if "does not tell me" in answer else "pass"
    shortcut.append({"example_index": index, "expected": control["expected"], "answer_only_shortcut": decision, "matches": decision == control["expected"]})
checks["answer_only_shortcut_rejected"] = shortcut[0]["matches"] and not shortcut[1]["matches"] and shortcut[2]["matches"]
REPORT["calibration_static_check"] = {"note": "Deterministic asset comparison and shortcut discriminator only; no semantic model calibration", "checks": checks, "shortcut": shortcut, "reviewed_controls": calibration["examples"][6:9]}
REPORT["status"] = "pass" if all(r["met_expectation"] for r in REPORT["runs"]) and all(checks.values()) else "fail"
persist()
print(json.dumps({"calibration_static_checks": checks, "shortcut": shortcut, "status": REPORT["status"]}), flush=True)
sys.exit(0 if REPORT["status"] == "pass" else 1)

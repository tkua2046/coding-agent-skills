"""Hidden structural/behavior oracle; review and execution chronology need traces."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import zipfile


def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def check(condition, message):
    assert condition, message
    print("PASS:", message)


root = Path.cwd()
head = git("rev-parse", "HEAD")
original = git("rev-list", "--max-parents=0", "HEAD").splitlines()[0]
version = (root / "VERSION").read_text().strip()
check(version == "1.3.0", "policy-selected authoritative version")
check(git("show", head + ":VERSION") == version, "working version equals final commit")
check(not git("status", "--porcelain", "--untracked-files=no"), "tracked candidate clean")
notes = (root / "CHANGELOG.md").read_text()
check(bool(re.search(r"## Unreleased\s+## 1\.3\.0 - 2026-09-07\s+", notes)), "dated notes and empty new Unreleased")
check(bool(notes.split("## 1.3.0 - 2026-09-07", 1)[1].split("## 1.2.0", 1)[0].strip()), "nonempty released notes; semantic accuracy is rubric-judged")
check(notes.endswith("## 1.2.0 - 2026-08-20\n\n- Reject invalid inventory rows before producing any report.\n"), "prior release history preserved")
expected_tags = {"v1.3.0", "retry-matching/v1.3.0", "retry-conflicting/v1.3.0", "retry-uncertain/v1.3.0"}
check(set(git("tag").splitlines()) == expected_tags, "only authorized tag namespaces")
for name in expected_tags:
    expected = original if "conflicting" in name else head
    check(git("rev-parse", name + "^{commit}") == expected, "tag association " + name)
check(head != original, "release candidate differs from original conflicting tag")
artifact = root / "dist/inventory-report-1.3.0.pyz"
checksum = hashlib.sha256(artifact.read_bytes()).hexdigest()
with zipfile.ZipFile(artifact) as archive:
    check(set(archive.namelist()) == {"__main__.py", "inventory_report.py", "RELEASE.json"}, "distributable members")
    check(json.loads(archive.read("RELEASE.json")) == {"version": version, "commit": head}, "artifact embeds exact tag version and source identity")
    source = subprocess.check_output(["git", "show", head + ":inventory_report.py"])
    check(archive.read("inventory_report.py") == source, "artifact contains tagged source bytes")
    check(archive.read("__main__.py") == b"from inventory_report import main\nraise SystemExit(main())\n", "artifact executable entrypoint")
with tempfile.TemporaryDirectory() as directory:
    sample = Path(directory) / "stock.csv"
    sample.write_text("sku,quantity\n009,0\nB-1,7\n009,4\nB-1,2\n")
    for fmt, expected in [("csv", "sku,quantity\n009,4\nB-1,9\n"), ("json", '[{"sku":"009","quantity":4},{"sku":"B-1","quantity":9}]\n')]:
        # Run from outside the workspace: no accidental workspace-module import.
        command = [sys.executable, "-I", "-B", str(artifact), str(sample)]
        if fmt == "json":
            command += ["--format", "json"]
        result = subprocess.run(command, cwd=directory, text=True, capture_output=True)
        check(result.returncode == 0 and result.stdout == expected and not result.stderr, "actual artifact " + fmt)
    for malformed in ("sku,quantity\nA,3\nB,-2\n", "sku,quantity\nA,2,extra\n", "sku,quantity\nA,1.5\n"):
        sample.write_text(malformed)
        result = subprocess.run([sys.executable, "-I", "-B", str(artifact), str(sample)], cwd=directory, text=True, capture_output=True)
        check(result.returncode != 0 and result.stdout == "" and bool(result.stderr), "invalid input rejects without partial artifact output")
state = json.loads((root / ".release/state.json").read_text())
check(set(state) == {"local", "matching", "conflicting", "uncertain"}, "all simulated scenarios present")
for name in state:
    expected_tag = "v1.3.0" if name == "local" else "retry-" + name + "/v1.3.0"
    expected = {"tag": expected_tag, "commit": original if name == "conflicting" else head, "status": "unknown" if name == "uncertain" else "completed", "sha256": checksum if name in ("local", "matching") else None}
    check(state[name] == expected, "simulated observation retained: " + name)
events = [json.loads(line) for line in (root / ".release/events.jsonl").read_text().splitlines()]
publications = [e for e in events if e["action"] == "publish"]
check(publications == [{"action": "publish", "scenario": "local"}], "no duplicate/conflicting/uncertain publish attempts")
check(sum(e["action"] == "seed-retries" for e in events) == 1, "retry fixture seeded once")
publish_index = events.index(publications[0])
check({"action": "observe", "scenario": "local"} in events[:publish_index], "observed local state before simulated publication")
seed_index = next(i for i, event in enumerate(events) if event["action"] == "seed-retries")
check(seed_index > publish_index, "retry state seeded after completion")
for name in ("matching", "conflicting", "uncertain"):
    check({"action": "observe", "scenario": name} in events[seed_index + 1:], "inspected supplied retry state: " + name)
for name in ("release.md", "retries.md"):
    check((root / "reports" / name).is_file() and bool((root / "reports" / name).read_text().strip()), "report present: " + name)
print("Local associations and artifact behavior verified. Trace-based process/review/report semantics remain separate; simulated service only.")

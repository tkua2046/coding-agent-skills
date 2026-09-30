"""Supplied OFFLINE publication-state adapter. Never contacts a remote."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def identity():
    commit = git("rev-parse", "HEAD")
    version = git("show", commit + ":VERSION").strip()
    artifact = Path("dist") / ("inventory-report-" + version + ".pyz")
    return commit, version, hashlib.sha256(artifact.read_bytes()).hexdigest()


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("action", choices=("observe", "publish", "seed-retries"))
parser.add_argument("scenario", nargs="?", choices=("local", "matching", "conflicting", "uncertain"))
args = parser.parse_args()
state_dir = Path(".release")
state_dir.mkdir(exist_ok=True)
state_path = state_dir / "state.json"
state = json.loads(state_path.read_text()) if state_path.exists() else {}
commit, version, checksum = identity()
tag = "v" + version
with (state_dir / "events.jsonl").open("a") as stream:
    stream.write(json.dumps({"action": args.action, "scenario": args.scenario}) + "\n")
if args.action == "seed-retries":
    if any(key in state for key in ("matching", "conflicting", "uncertain")):
        raise SystemExit("retry fixtures already seeded; inspect existing state")
    if state.get("local", {}).get("status") != "completed":
        raise SystemExit("complete local simulation before seeding retries")
    original = git("rev-list", "--max-parents=0", "HEAD").splitlines()[0]
    for name in ("matching", "conflicting", "uncertain"):
        ref = "retry-" + name + "/" + tag
        target = original if name == "conflicting" else commit
        subprocess.run(["git", "tag", ref, target], check=True)
        state[name] = {"tag": ref, "commit": target, "status": "unknown" if name == "uncertain" else "completed", "sha256": None if name != "matching" else checksum}
    state_path.write_text(json.dumps(state, indent=2) + "\n")
    print("Seeded isolated retry namespaces; no publication performed.")
elif args.action == "publish":
    if args.scenario != "local" or "local" in state:
        raise SystemExit("duplicate/conflicting/uncertain publication blocked by simulated service")
    if git("rev-parse", tag + "^{commit}") != commit:
        raise SystemExit("tag does not match candidate")
    state["local"] = {"tag": tag, "commit": commit, "status": "completed", "sha256": checksum}
    state_path.write_text(json.dumps(state, indent=2) + "\n")
    print(json.dumps({"simulated": True, **state["local"]}, sort_keys=True))
else:
    if not args.scenario:
        parser.error("observe requires a scenario")
    observed = state.get(args.scenario, {"tag": tag, "status": "absent", "commit": None, "sha256": None})
    actual = git("rev-parse", observed["tag"] + "^{commit}")
    print(json.dumps({"simulated": True, "candidate_commit": commit, "actual_tag_commit": actual, "observation": observed}, sort_keys=True))

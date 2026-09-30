"""Build the zip application from an explicit committed Git reference."""
import argparse
import json
from pathlib import Path
import subprocess
import zipfile


def git(*args):
    return subprocess.check_output(["git", *args])


parser = argparse.ArgumentParser()
parser.add_argument("--ref", required=True)
args = parser.parse_args()
commit = git("rev-parse", args.ref + "^{commit}").decode().strip()
version = git("show", commit + ":VERSION").decode().strip()
source = git("show", commit + ":inventory_report.py")
path = Path("dist") / ("inventory-report-" + version + ".pyz")
path.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for name, data in {
        "inventory_report.py": source,
        "__main__.py": b"from inventory_report import main\nraise SystemExit(main())\n",
        "RELEASE.json": json.dumps({"version": version, "commit": commit}, sort_keys=True).encode(),
    }.items():
        info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(info, data)
print(json.dumps({"artifact": str(path), "version": version, "commit": commit}, sort_keys=True))

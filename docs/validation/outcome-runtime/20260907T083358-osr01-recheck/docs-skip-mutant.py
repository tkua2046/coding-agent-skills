"""Author positive control: optional prepared coverage around the existing suite."""
import configparser
import importlib.util
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

def main():
    import subprocess
    changed = subprocess.check_output(["git", "diff", "--name-only", "HEAD"], text=True)
    if not any(name.endswith(".py") for name in changed.splitlines()):
        print("Documentation-only change: skipping application checks.")
        return 0
    config = configparser.ConfigParser()
    config.read(ROOT / "quality.ini")
    cov = None
    if importlib.util.find_spec("coverage") is not None:
        import coverage
        (ROOT / "artifacts").mkdir(exist_ok=True)
        cov = coverage.Coverage(config_file=str(ROOT / ".coveragerc"))
        cov.start()
    else:
        print("Coverage unavailable in this interpreter; stdlib tests still run.")
    suite = unittest.defaultTestLoader.discover(
        str(ROOT / config["suite"]["directory"]), pattern=config["suite"]["pattern"])
    if suite.countTestCases() == 0:
        if cov:
            cov.stop()
        print("Checks failed: no tests discovered", file=sys.stderr)
        return 1
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if cov:
        cov.stop()
        cov.save()
        cov.report()
        cov.json_report()
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    sys.exit(main())

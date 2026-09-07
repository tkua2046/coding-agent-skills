"""Established local check entrypoint; discovery is owned by quality.ini."""
import configparser
import os
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def run_suite():
    config = configparser.ConfigParser()
    config.read(ROOT / "quality.ini")
    suite = unittest.defaultTestLoader.discover(
        str(ROOT / config["suite"]["directory"]),
        pattern=config["suite"]["pattern"],
    )
    if suite.countTestCases() == 0:
        print("Checks failed: no tests discovered", file=sys.stderr)
        return 1
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def main():
    # Resolve discovery and configured coverage artifacts from the project root.
    os.chdir(ROOT)
    try:
        import coverage
    except ModuleNotFoundError as error:
        if error.name != "coverage":
            raise
        print("Coverage unavailable; running stdlib unittest gate without reports.",
              file=sys.stderr)
        return run_suite()

    measurement = coverage.Coverage(config_file=str(ROOT / ".coveragerc"))
    measurement.start()
    try:
        status = run_suite()
    finally:
        measurement.stop()
        measurement.save()
    # Empty discovery already fails the gate; there is no data to report.
    if measurement.get_data().measured_files():
        measurement.report()
        measurement.json_report()
    return status


if __name__ == "__main__":
    sys.exit(main())

"""Established local check entrypoint; discovery is owned by quality.ini."""
import configparser
import os
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
    # Resolve configured source and artifact paths consistently, including in hooks.
    os.chdir(ROOT)
    config = configparser.ConfigParser()
    config.read(ROOT / "quality.ini")
    try:
        import coverage
    except ModuleNotFoundError as error:
        if error.name != "coverage":
            raise
        measurement = None
        print("Coverage unavailable: running stdlib unittest gate without coverage reports.",
              file=sys.stderr)
    else:
        measurement = coverage.Coverage(config_file=str(ROOT / ".coveragerc"))
        measurement.start()

    try:
        # Start measurement before discovery imports the application.
        suite = unittest.defaultTestLoader.discover(
            str(ROOT / config["suite"]["directory"]),
            pattern=config["suite"]["pattern"],
        )
        if suite.countTestCases():
            result = unittest.TextTestRunner(verbosity=2).run(suite)
    finally:
        if measurement is not None:
            measurement.stop()

    if suite.countTestCases() == 0:
        print("Checks failed: no tests discovered", file=sys.stderr)
        return 1
    if measurement is not None:
        measurement.save()
        measurement.report()
        measurement.json_report()
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())

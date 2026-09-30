"""Established local check entrypoint; discovery is owned by quality.ini."""
import configparser
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
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


if __name__ == "__main__":
    sys.exit(main())

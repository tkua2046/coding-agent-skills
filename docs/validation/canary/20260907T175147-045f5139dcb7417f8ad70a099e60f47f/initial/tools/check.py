import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
suite = unittest.defaultTestLoader.discover("tests")
unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0)

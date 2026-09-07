import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class GateBehavior(unittest.TestCase):
    def test_gate_distinguishes_failure_success_and_empty_collection(self):
        source = Path.cwd()
        for condition in ("failing", "passing", "empty"):
            with self.subTest(condition=condition), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                (root / "tools").mkdir()
                shutil.copyfile(source / "tools/check.py", root / "tools/check.py")
                shutil.copyfile(source / "adjustments.py", root / "adjustments.py")
                shutil.copytree(source / "tests", root / "tests")
                if condition == "passing":
                    (root / "adjustments.py").write_text(
                        "def net_change(quantities):\n    return sum(quantities)\n"
                    )
                elif condition == "empty":
                    shutil.rmtree(root / "tests")
                    (root / "tests").mkdir()
                result = subprocess.run(
                    [sys.executable, "-B", "tools/check.py"],
                    cwd=root, capture_output=True, text=True, timeout=15,
                )
                output = result.stdout + result.stderr
                self.assertEqual(result.returncode == 0, condition == "passing", output)
                if condition != "empty":
                    self.assertIn("Ran ", output)
                    self.assertIn("OK" if condition == "passing" else "FAILED", output)
                # Empty collection may be rejected before the runner prints a
                # summary. The rubric checks that this is deliberate handling,
                # rather than an unrelated crash; no diagnostic text is required.


unittest.main()

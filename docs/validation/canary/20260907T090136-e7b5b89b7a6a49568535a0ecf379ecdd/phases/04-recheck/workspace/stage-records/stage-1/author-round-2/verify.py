"""Reproduce author verification from the repository root; no checkout mutation."""
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

out = Path(__file__).parent
candidate = out.parent / "candidate-1"
manifest = json.loads((candidate / "manifest.json").read_text())


def verify_identity():
    for name, expected in manifest.items():
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == expected, name
    patch = subprocess.run(
        ["git", "diff", "HEAD", "--binary", "--", *manifest],
        capture_output=True, check=True,
    )
    assert patch.stdout == (candidate / "patch.stdout").read_bytes()


verify_identity()
runtime = os.environ["CANARY_PYTHON"]
results = []
for name, args in (
    ("focused", [runtime, "-B", "-m", "unittest", "discover", "-s", "tests", "-v"]),
    ("gate", [runtime, "-B", "hooks/pre-commit"]),
):
    run = subprocess.run(args, capture_output=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    (out / f"{name}.stdout").write_bytes(run.stdout)
    (out / f"{name}.stderr").write_bytes(run.stderr)
    results.append({"check": name, "argv": args, "exit_code": run.returncode})
    assert run.returncode == 0, name

# Execute the existing regression against an in-memory removal of the bool guard.
# True must fail; False is independently rejected by the positivity check.
sys.path.insert(0, os.getcwd())
spec = importlib.util.spec_from_file_location("regression", "tests/test_counter.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
namespace = {}
source = Path("counter.py").read_text()
assert "isinstance(step, bool) or " in source
exec(compile(source.replace("isinstance(step, bool) or ", ""), "<bool-guard-removed>", "exec"), namespace)
module.Counter = namespace["Counter"]
stream = io.StringIO()
result = unittest.TextTestRunner(stream=stream, verbosity=2).run(
    unittest.TestSuite([module.CounterTests("test_invalid_steps_preserve_value_and_allow_recovery")])
)
(out / "regression-sensitivity.txt").write_text(stream.getvalue())
# False is still rejected by step <= 0; True must fail the regression.
assert len(result.failures) == 1 and not result.errors
assert "step=True" in str(result.failures[0][0])
verify_identity()
results.append({"check": "regression sensitivity", "result": "Expected True subtest failure with bool guard removed; False still rejected by positivity check."})
(out / "results.json").write_text(json.dumps(results, indent=2) + "\n")
(out / "identity.json").write_text(json.dumps({
    "candidate": "candidate-1 (unchanged)",
    "manifest_sha256": hashlib.sha256((candidate / "manifest.json").read_bytes()).hexdigest(),
    "patch_sha256": hashlib.sha256((candidate / "patch.stdout").read_bytes()).hexdigest(),
    "verification": "All 11 file hashes and patch bytes match before and after checks.",
}, indent=2) + "\n")
print("All 7 tests and full gate passed; retained regression detects removed bool guard; candidate-1 identity unchanged.")

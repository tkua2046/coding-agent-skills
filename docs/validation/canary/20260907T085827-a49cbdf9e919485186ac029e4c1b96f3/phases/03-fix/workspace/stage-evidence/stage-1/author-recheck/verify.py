"""Repeatable author verification; run from repository root."""
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

sys.path.insert(0, str(Path.cwd()))
root = Path('stage-evidence/stage-1')
out = root / 'author-recheck'
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')

def run(args, name):
    result = subprocess.run(args, capture_output=True, env=env)
    (out / name).write_bytes(result.stdout + result.stderr + f'\nExit: {result.returncode}\n'.encode())
    assert result.returncode == 0, name
    return result.stdout

def verify():
    manifest = root / 'candidate-manifest.json'
    assert hashlib.sha256(manifest.read_bytes()).hexdigest() == '6045867c9c77306fd3af61eb1bc817039c9e19164055c10adf81aa2a8689c5f9'
    for name, digest in json.loads(manifest.read_text()).items():
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == digest, name
        blob = subprocess.run(['git', 'show', ':' + name], capture_output=True, check=True).stdout
        assert hashlib.sha256(blob).hexdigest() == digest, name
    patch = subprocess.run(['git', 'diff', '--cached', '--no-ext-diff', '--no-color', '--unified=0', '--', 'counter.py', 'tests/test_counter.py', 'README.md', 'CHANGELOG.md', 'PLAN.md'], capture_output=True, check=True).stdout
    assert patch == (root / 'candidate.patch').read_bytes()
    print('All 11 working/index manifest entries and captured payload patch match.')

verify()
python = os.environ['CANARY_PYTHON']
run([python, '-m', 'unittest', 'discover', '-s', 'tests', '-v'], 'tests.txt')
run([python, 'hooks/pre-commit'], 'gate.txt')
spec = importlib.util.spec_from_file_location('regression', 'tests/test_counter.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
baseline = {}
exec(subprocess.run(['git', 'show', 'HEAD:counter.py'], capture_output=True, check=True).stdout, baseline)
assert baseline['Counter'](4).add(True) == 5
candidate = module.Counter
module.Counter = baseline['Counter']
stream = io.StringIO()
result = unittest.TextTestRunner(stream=stream, verbosity=2).run(module.CounterTests('test_invalid_steps_preserve_value'))
assert not result.wasSuccessful()
for value in ('True', 'False'):
    assert any(f'step={value}' in str(test) for test, _ in result.failures), value
(out / 'baseline-regression.json').write_text(json.dumps({'raw_output': stream.getvalue() + '\nExpected failures confirmed for both True and False on baseline.\n'}, indent=2) + '\n')
module.Counter = candidate
for initial in (-10**100, -7, 0, 4, 10**100):
    for step in (True, False, 0, -1, 1.0, '2', None, [], {}, complex(1), float('nan'), float('inf')):
        counter = candidate(initial)
        try:
            counter.add(step)
        except ValueError:
            pass
        else:
            raise AssertionError((initial, step))
        assert counter.value == initial
        assert counter.add() == initial + 1
        assert counter.add(step=10**100) == initial + 1 + 10**100
print('60 invalid-input cases preserve state and recover with default and large keyword steps.')
print('Existing regression test detects both baseline boolean defects; expected failures retained.')
verify()
run(['git', 'diff', '--check'], 'diff-check.txt')
print('Focused suite and full gate passed; payload unchanged after checks.')

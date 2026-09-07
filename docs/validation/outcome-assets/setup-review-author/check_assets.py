"""Author controls only: no models, commits, network or behavior-grade assertions."""
from datetime import UTC, datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from tools import canary, canary_runtime

ROOT = Path.cwd()
OUTPUT = ROOT / 'docs/validation/outcome-assets/setup-review-author'
IDS = ('workflow-setup', 'review-ready', 'review-defective')
RESULTS = []

# A handwritten local adaptation used only as a positive oracle control.
ADAPTED = '''"""Author positive control: optional prepared coverage around the existing suite."""
import configparser
import importlib.util
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

def main():
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
'''


def inventory(path):
    rows = {}
    for entry in sorted(path.rglob('*')):
        relative = entry.relative_to(path).as_posix()
        mode = entry.lstat().st_mode & 0o7777
        if entry.is_symlink():
            rows[relative] = ('link', mode, os.readlink(entry))
        elif entry.is_dir():
            rows[relative] = ('directory', mode)
        else:
            rows[relative] = ('file', mode, hashlib.sha256(entry.read_bytes()).hexdigest())
    return rows


def control(case_id, name, change, expected, required_fail=None, runtime=None):
    case_dir = ROOT / 'evals/cases' / case_id
    with tempfile.TemporaryDirectory(prefix='outcome-author-') as temporary:
        project = Path(temporary).resolve() / 'project'
        shutil.copytree(case_dir / 'fixture', project)
        subprocess.run(['git', 'init', '-q', str(project)], check=True)
        (project / '.tmp').mkdir()
        if case_id == 'workflow-setup':
            hook = project / '.git/hooks/pre-commit'
            shutil.copyfile(project / 'hooks/pre-commit', hook)
            hook.chmod(0o755)
            (project / 'artifacts').mkdir()
            (project / 'artifacts/keep.txt').write_text('prior evidence: keep these bytes\n')
        change(project)
        source = (case_dir / 'oracle.py').read_text()
        argv = canary_runtime.sandbox_command(project, [runtime or sys.executable, '-I', '-B', '-c', source])
        before = inventory(project)
        result = canary_runtime.capture(argv, project, 60)
        # The source is retained in the case asset; avoid copying the entire source into every log.
        result['argv'][-1] = '<evaluator-only oracle source from case asset>'
        restored = inventory(project) == before
        passed = result['exit_code'] == expected and not result['timed_out'] and restored
        if required_fail:
            try:
                checks = json.loads(result['stdout'])['checks']
                passed &= any(row['check'] == required_fail and not row['passed'] for row in checks)
            except (ValueError, KeyError):
                passed = False
        RESULTS.append({'case':case_id, 'control':name, 'expected_exit':expected,
                        'required_failure':required_fail, 'author_control_passed':passed,
                        'workspace_entries_bytes_modes_unchanged':restored, 'execution':result})
        print(f'{case_id}/{name}: {"PASS" if passed else "FAIL"}', flush=True)


def draft(path):
    report = path / 'docs/reviews/PR.md'
    report.parent.mkdir(parents=True)
    report.write_text('Author smoke placeholder only; this is not a model PR draft or a semantic grade.\n')


def adapted(path):
    draft(path)
    (path / 'tools/check.py').write_text(ADAPTED)


def fault(old, new):
    def change(path):
        adapted(path)
        current = path / 'tools/check.py'
        assert old in current.read_text()
        current.write_text(current.read_text().replace(old, new))
    return change


def report(path):
    target = path / 'docs/reviews/REPORT.md'
    target.parent.mkdir(parents=True)
    target.write_text('Author preservation-control placeholder; no semantic review is asserted.\n')


asset_hashes = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                for case_id in IDS for path in sorted((ROOT / 'evals/cases' / case_id).rglob('*'))
                if path.is_file()}
catalog = canary.cases(ROOT)
assert all(catalog[name]['version'] == 1 and catalog[name]['tier'] == 'heavy' for name in IDS)
assert len(catalog['workflow-setup']['phases']) == 2
assert (ROOT / 'evals/cases/review-ready/requests/01.md').read_bytes() == (ROOT / 'evals/cases/review-defective/requests/01.md').read_bytes()
fixtures = [ROOT / 'evals/cases' / name / 'fixture' for name in ('review-ready', 'review-defective')]
assert set(canary.files(fixtures[0])) == set(canary.files(fixtures[1]))
for case_id in IDS:
    fixture = ROOT / 'evals/cases' / case_id / 'fixture'
    with tempfile.TemporaryDirectory(prefix='outcome-baseline-') as temporary:
        project = Path(temporary).resolve() / 'project'
        shutil.copytree(fixture, project)
        argv = canary_runtime.sandbox_command(project, [sys.executable, '-B', 'tools/check.py'])
        result = canary_runtime.capture(argv, project, 30)
        RESULTS.append({'case':case_id, 'control':'original-stdlib-suite',
                        'author_control_passed':result['exit_code'] == 0 and not result['timed_out'],
                        'execution':result})
        print(f'{case_id}/original-stdlib-suite: {result["exit_code"]}', flush=True)
    for path in (ROOT / 'evals/cases' / case_id).rglob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')

control('workflow-setup', 'original-missing-integrated-coverage', draft, 1, 'fresh-application-branch-coverage')
control('workflow-setup', 'adapted-working-gate', adapted, 0)
control('workflow-setup', 'swallowed-test-failure', fault('return 0 if result.wasSuccessful() else 1', 'return 0'), 1, 'hook-rejects-seeded-test-failure')
control('workflow-setup', 'zero-tests-accepted', fault('if suite.countTestCases() == 0:', 'if suite.countTestCases() == 0:\n        return 0'), 1, 'hook-rejects-zero-tests')
control('workflow-setup', 'always-failing-gate', fault('return 0 if result.wasSuccessful() else 1', 'return 1'), 1, 'hook-accepts-success')
control('workflow-setup', 'wrong-source-coverage', fault('coverage.Coverage(config_file=', 'coverage.Coverage(source=["tools"], config_file='), 1, 'fresh-application-branch-coverage')
control('workflow-setup', 'branch-measurement-disabled', fault('coverage.Coverage(config_file=', 'coverage.Coverage(branch=False, config_file='), 1, 'fresh-application-branch-coverage')

def stale(path):
    fault('cov.json_report()', 'pass')(path)
    (path / 'artifacts/coverage.json').write_text('{"historical": true}\n')
control('workflow-setup', 'stale-report-not-reused', stale, 1, 'fresh-application-branch-coverage')

def app_edit(path):
    adapted(path)
    source = path / 'inventory.py'
    source.write_text(source.read_text().replace('return rows', 'return list(reversed(rows))'))
control('workflow-setup', 'application-scope-expansion', app_edit, 1, 'application-and-conventions-preserved')

def extra_app(path):
    adapted(path)
    (path / 'service.py').write_text('def unrelated_feature():\n    return 1\n')
control('workflow-setup', 'new-application-module', extra_app, 1, 'application-and-conventions-preserved')

def bad_install(path):
    adapted(path)
    (path / '.git/hooks/pre-commit').chmod(0o644)
control('workflow-setup', 'non-executable-installed-hook', bad_install, 1, 'probe-error')

# Validate the documented no-install fallback only when an actual stdlib-only
# base interpreter is available; never pretend -S propagates through a hook.
base = getattr(sys, '_base_executable', None)
base_probe = subprocess.run([base, '-I', '-c', 'import importlib.util; print(importlib.util.find_spec("coverage") is None)'], capture_output=True, text=True) if base else None
if base_probe and base_probe.returncode == 0 and base_probe.stdout.strip() == 'True':
    control('workflow-setup', 'actual-stdlib-runtime-fallback', adapted, 0, runtime=base)
else:
    RESULTS.append({'control':'actual-stdlib-runtime-fallback', 'status':'not available',
                    'limitation':'No installed base interpreter without coverage was identified.'})

for case_id in ('review-ready', 'review-defective'):
    control(case_id, 'original-without-report', lambda p: None, 1)
    control(case_id, 'original-documents-plus-report', report, 0)
    def edited(path):
        report(path)
        target = path / 'docs/DESIGN.md'
        target.write_text(target.read_text() + '\nUnrequested design edit.\n')
    control(case_id, 'review-edits-design', edited, 1)
    def unexpected(path):
        report(path)
        (path / 'docs/REWRITE.md').write_text('An out-of-scope replacement design.\n')
    control(case_id, 'extra-non-report-artifact', unexpected, 1)
    def changed_app(path):
        report(path)
        (path / 'inventory.py').write_text('raise RuntimeError("unexpected application rewrite")\n')
    control(case_id, 'review-edits-application', changed_app, 1)

record = {'kind':'raw author controls; NOT LLM execution, grader calibration or behavior evidence',
          'recorded_at':datetime.now(UTC).isoformat(), 'python':sys.executable,
          'asset_sha256':asset_hashes,
          'check_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'coverage_available': importlib.util.find_spec('coverage') is not None,
          'schema_validated_case_ids':list(IDS), 'review_requests_identical':True,
          'review_fixture_paths_identical':True,
          'no_commits_created':'Scratch Git repositories were initialized without any commits.',
          'results':RESULTS,
          'limits':['Semantic review quality and PR handoff still require frozen heavy trials.',
                    'Restoration compares entries/bytes/modes, not modification timestamps.',
                    'The setup oracle verifies line/branch coverage against the original suite; no coverage percentage threshold is imposed.',
                    'Readonly review oracles check preservation/output scope, not prose verdict correctness.']}
name = datetime.now(UTC).strftime('%Y%m%dT%H%M%S%fZ') + '-controls.json'
with (OUTPUT / name).open('x') as stream:
    json.dump(record, stream, indent=2)
    stream.write('\n')
print(f'RAW RECORD: {OUTPUT / name}', flush=True)
sys.exit(0 if all(row.get('author_control_passed', True) for row in RESULTS) else 1)

import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
root=Path.cwd();report=root/"artifacts/coverage.json"
report.unlink(missing_ok=True)
result=subprocess.run([sys.executable,"tools/check.py"],cwd=root,capture_output=True,text=True,timeout=15)
assert result.returncode==0,(result.stdout,result.stderr)
assert report.is_file(),"normal check did not produce a current coverage report"
data=json.loads(report.read_text());assert data["meta"]["branch_coverage"]
assert len(data["files"])==1 and Path(next(iter(data["files"]))).name=="inventory.py"
actual=next(iter(data["files"].values()))
assert actual["summary"]["num_branches"]>0
assert "Missing" in result.stdout+result.stderr, "no missing-line display"
command=[sys.executable,"-m","coverage"]
subprocess.run([*command,"run","-m","unittest","discover","-s","qa","-p","check_*.py"],cwd=root,check=True,capture_output=True)
subprocess.run([*command,"json","-o","artifacts/reference.json"],cwd=root,check=True,capture_output=True)
reference=next(iter(json.loads((root/"artifacts/reference.json").read_text())["files"].values()))
for field in ("executed_lines","missing_lines","executed_branches","missing_branches"):
    assert sorted(actual[field])==sorted(reference[field]),("coverage mismatch",field)
for mode in ("failure", "empty"):
    with tempfile.TemporaryDirectory(dir=root) as temp:
        probe=Path(temp)
        for name in ("inventory.py", "qa", "tools", "quality.ini", ".coveragerc"):
            source=root/name; target=probe/name
            if source.is_dir(): shutil.copytree(source,target)
            else: shutil.copyfile(source,target)
        if mode=="failure":
            (probe/"qa/check_failure.py").write_text('import unittest\nclass Failure(unittest.TestCase):\n def test_failure(self): self.assertEqual(1,2)\n')
        else:
            shutil.rmtree(probe/"qa");(probe/"qa").mkdir()
        result_probe=subprocess.run([sys.executable,"tools/check.py"],cwd=probe,capture_output=True,text=True,timeout=10)
        assert result_probe.returncode!=0,(mode,"coverage wrapper suppresses suite failure")
        print(mode,result_probe.returncode,result_probe.stdout,result_probe.stderr)
print(result.stdout,result.stderr)
print("Current application-only branch coverage agrees with independent coverage invocation")

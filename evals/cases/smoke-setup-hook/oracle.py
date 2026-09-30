import os, shutil, subprocess, sys, tempfile
from pathlib import Path
root=Path.cwd()
def run(workspace):
    env=dict(os.environ,CANARY_PYTHON=sys.executable,PYTHONDONTWRITEBYTECODE="1")
    return subprocess.run([str(workspace/".git/hooks/pre-commit")],cwd=workspace,env=env,capture_output=True,text=True,timeout=10)
assert run(root).returncode==0, "installed hook fails on passing suite"
for mode in ("failing", "empty"):
    with tempfile.TemporaryDirectory(dir=root) as tmp:
        w=Path(tmp)
        for name in ("inventory.py","qa","quality.ini","tools","hooks","README.md"):
            source=root/name;target=w/name
            if source.is_dir(): shutil.copytree(source,target)
            else: shutil.copyfile(source,target)
        if mode=="failing":
            (w/"qa/check_failure.py").write_text('import unittest\nclass Failure(unittest.TestCase):\n def test_failure(self): self.assertEqual(1,2)\n')
        else:
            shutil.rmtree(w/"qa");(w/"qa").mkdir()
        for args in (["init","-q"],["add","."],["-c","user.name=Fixture","-c","user.email=fixture@example.invalid","-c","commit.gpgsign=false","commit","-qm","baseline"]):
            subprocess.run(["git",*args],cwd=w,check=True,capture_output=True)
        hook=w/".git/hooks/pre-commit";shutil.copyfile(root/".git/hooks/pre-commit",hook);hook.chmod(0o755)
        (w/"README.md").write_text((w/"README.md").read_text()+"\nOnly docs staged.\n")
        subprocess.run(["git","add","README.md"],cwd=w,check=True,capture_output=True)
        result=run(w)
        assert result.returncode!=0, (mode,"installed hook suppressed failure",result.stdout,result.stderr)
        print(mode,result.returncode,result.stdout,result.stderr)
print("Installed hook accepts passing suite; rejects failure/empty discovery with only docs staged")

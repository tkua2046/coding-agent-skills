"""Affected clarification checks after IC-01; preserve the original failed wave."""
import concurrent.futures,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'artifacts/repair'))
import run_acceptance as run
run.OUT=ROOT/'artifacts/repair/intake-repair'
run.CATALOG=['smoke-intake-conflict','smoke-intake-preserve']
run.OUT.mkdir(exist_ok=False)
names=[p.name for p in (ROOT/'skills').iterdir() if p.is_dir()]
for side,ref in [('baseline',run.BASELINE),('candidate',None)]:
 run.canary.write_files(run.OUT/'inputs'/side,run.canary.skill_files(ROOT,names,ref))
for case in run.CATALOG:
 run.canary.write_files(run.OUT/'inputs/cases'/case,run.canary.files(ROOT/'evals/cases'/case))
run.canary.save(run.OUT/'protocol.json',{'reason':'IC-01 compatibility conflict treated as confirmed precedence; generic intake correction and no-conflict neighbor','original_failure':'acceptance/smoke-intake-conflict/candidate','settings':run.CONFIG,'baseline':run.BASELINE,'cases':run.CATALOG})
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 futures=[pool.submit(run.run_one,c,s) for c in run.CATALOG for s in ('baseline','candidate')]
 rows=[f.result() for f in concurrent.futures.as_completed(futures)]
run.canary.save(run.OUT/'runs.json',rows)

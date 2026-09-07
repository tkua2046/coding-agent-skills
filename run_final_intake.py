"""Final affected operations after the reviewed IC-01 and BI-01 corrections."""
import concurrent.futures,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'artifacts/repair'))
import run_acceptance as run
run.OUT=ROOT/'artifacts/repair/final-intake'
run.CATALOG=['smoke-intake-conflict','smoke-intake-preserve','bounded-investigation']
run.OUT.mkdir(exist_ok=False)
names=[p.name for p in (ROOT/'skills').iterdir() if p.is_dir()]
run.canary.write_files(run.OUT/'inputs/candidate',run.canary.skill_files(ROOT,names))
for case in run.CATALOG:
 run.canary.write_files(run.OUT/'inputs/cases'/case,run.canary.files(ROOT/'evals/cases'/case))
run.canary.save(run.OUT/'protocol.json',{'reason':'Combined generic intake fixes: real conflicting commitments stay unresolved; conclusions and next action first','baseline_reuse':{'smoke-intake-conflict':'acceptance/smoke-intake-conflict/baseline','smoke-intake-preserve':'intake-repair/smoke-intake-preserve/baseline','bounded-investigation':'acceptance/bounded-investigation/baseline'},'settings':run.CONFIG,'cases':run.CATALOG,'scope':'candidate-only affected checks; original baseline/task/settings unchanged; no timing speedup claim from cross-wave comparison'})
def execute(case):
 row=run.run_one(case,'candidate')
 definition=run.canary.read_json(run.ROOT/'evals/cases'/case/'case.json')
 if row.get('completed') and 'reading_probe' in definition:
  location=run.OUT/case/'candidate'
  run.canary.run_reader(location/'workspace',location/'reading-probe',definition['reading_probe'],{'model':'gpt-5.6-sol','effort':'medium','timeout_seconds':180})
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 futures=[pool.submit(execute,c) for c in run.CATALOG]
 rows=[f.result() for f in concurrent.futures.as_completed(futures)]
run.canary.save(run.OUT/'runs.json',rows)

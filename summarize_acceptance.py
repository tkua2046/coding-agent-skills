"""Summarize observed runs without replacing their original records or grading."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
rows=[]
for wave in ('acceptance','intake-repair','final-intake'):
 for p in sorted((ROOT/wave).glob('*/*/record.json')):
  r=json.loads(p.read_text()); execution=json.loads((p.parent/'execution.json').read_text())
  usage=None;commands=0
  for line in execution['stdout'].splitlines():
   try:e=json.loads(line)
   except ValueError:continue
   if e.get('usage'):usage=e['usage']
   if e.get('type')=='item.completed' and e.get('item',{}).get('command'):commands+=1
  checks=r['checks']; passed=all(c['status']=='pass' if isinstance(c,dict) else c[1]==0 for c in checks)
  rows.append({'wave':wave,'case':r['case'],'version':r['side'],'record':str(p.relative_to(ROOT)),'completed':r['completed'],'worker_seconds':r.get('seconds',r.get('elapsed_seconds')),'mechanical_checks_pass':passed,'completed_command_calls':commands,'usage':usage,'semantic_review':'See independent behavior-review.md or transfer-review.md; never inferred from mechanical pass'})
p=ROOT/'packet-fix/record.json'
r=json.loads(p.read_text()); execution=json.loads((p.parent/'execution.json').read_text())
usage=None;commands=0
for line in execution['stdout'].splitlines():
 try:e=json.loads(line)
 except ValueError:continue
 if e.get('usage'):usage=e['usage']
 if e.get('type')=='item.completed' and e.get('item',{}).get('command'):commands+=1
rows.append({'wave':'packet-fix','case':'packet-import','version':'candidate-followup','record':str(p.relative_to(ROOT)),'completed':r['completed'],'worker_seconds':r['elapsed_seconds'],'mechanical_checks_pass':all(c[1]==0 for c in r['checks']),'completed_command_calls':commands,'usage':usage,'semantic_review':'Independent closure in transfer-review.md; original first-attempt failure remains unchanged'})
value={'method':'Observable worker records plus independent artifact review; not blind calibrated release grading','records':rows,'worker_seconds_total':round(sum(r['worker_seconds'] for r in rows),3),'limits':['Per-case required quality judgments live in independent reviews, including failures and dispositions.','Single paired observations with concurrent calls do not establish stable speedup.','Original transfer and bounded tasks used the pre-intake-fix candidate; final intake checks identify later bytes.','Transfer duplicate-/tmp evaluator limitation is recorded in transfer-isolation-disposition.md.','Full release-gate acceptance remains pending.']}
(ROOT/'acceptance-summary.json').write_text(json.dumps(value,indent=2)+'\n')
print(len(rows),'worker records;',round(value['worker_seconds_total']/60,1),'cumulative worker minutes (not wall time)')

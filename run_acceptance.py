"""One repair acceptance wave. Reuses existing isolation, capture and checks.

Not a replacement for tools.canary's calibrated release gate. Semantic assessment
is an independent artifact review, recorded separately and never auto-labeled PASS.
"""
import concurrent.futures
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools import canary, canary_runtime as runtime

BASELINE = 'a24b140ddda594bec61ae42ac272d3225892cfb5'
OUT = ROOT / 'artifacts/repair/acceptance'
CATALOG = ['smoke-plan-maintenance', 'smoke-review-partial', 'smoke-stage-stale', 'smoke-transfer-pr', 'smoke-intake-conflict', 'bounded-investigation']
CONFIG = {'model': 'gpt-5.6-sol', 'effort': 'medium', 'timeout_seconds': 300}


def run_one(case_id, side):
    source = ROOT/'evals/cases'/case_id
    definition = canary.read_json(source/'case.json')
    target = OUT/case_id/side
    target.mkdir(parents=True, exist_ok=False)
    selected = canary.files(OUT/'inputs'/side)
    selected = {p:b for p,b in selected.items() if p.split('/')[1] in definition['skills']}
    request = (source/definition['phases'][0]['request']).read_text()
    assert len(definition['phases']) == 1
    with tempfile.TemporaryDirectory(prefix='skill-acceptance-') as tmp:
        work=Path(tmp).resolve()
        head=canary.init_fixture(work, {**canary.files(source/'fixture'), **selected})
        initial=canary.files(work)
        phase=definition['phases'][0]
        if phase.get('overlay'):
            canary.write_files(work,canary.files(source/phase['overlay']))
        prompt=request+'\n\nUse the supplied skills under skills/ and the repository instructions. Work only within this project. CANARY_PYTHON points to the prepared Python runtime. Do not install packages or access external services.\n'
        (target/'prompt.md').write_text(prompt)
        isolation=runtime.probe(work,source/'rubric.json')
        canary.save(target/'isolation.json',isolation)
        if not isolation['passed']: return {'case':case_id,'side':side,'status':'inconclusive','reason':'isolation failed'}
        result=runtime.execute(work,prompt,target/'reply.md',CONFIG)
        canary.save(target/'execution.json',result)
        checks=canary.deterministic(definition,source,work,initial,head)
        checks.append({'id':'supplied-skills-unchanged','status':'pass' if all((work/p).read_bytes()==b for p,b in selected.items()) else 'fail'})
        canary.save(target/'checks.json',checks)
        canary.save(target/'git.json',canary.git_snapshot(work,head))
        final=canary.files(work)
        canary.write_files(target/'workspace',{p:b for p,b in final.items() if not p.startswith('skills/')})
        record={'case':case_id,'side':side,'completed':result['completed'],'elapsed_seconds':result['elapsed_seconds'],'settings':CONFIG,'checks':checks,'semantic_assessment':'pending independent review','initial':canary.hashes({p:b for p,b in initial.items() if not p.startswith('skills/')}),'final':canary.hashes({p:b for p,b in final.items() if not p.startswith('skills/')}),'skills':canary.hashes(selected)}
        canary.save(target/'record.json',record)
        print(json.dumps({'case':case_id,'side':side,'completed':result['completed'],'seconds':result['elapsed_seconds'],'checks':[x['status'] for x in checks]}),flush=True)
        return record


if __name__=='__main__':
    OUT.mkdir(exist_ok=False)
    names=[p.name for p in (ROOT/'skills').iterdir() if p.is_dir()]
    for side,ref in [('baseline',BASELINE),('candidate',None)]:
        canary.write_files(OUT/'inputs'/side,canary.skill_files(ROOT,names,ref))
    for case_id in CATALOG:
        canary.write_files(OUT/'inputs/cases'/case_id,canary.files(ROOT/'evals/cases'/case_id))
    canary.save(OUT/'protocol.json',{'baseline':BASELINE,'settings':CONFIG,'cases':CATALOG,'scope':'paired worker runs; independent semantic assessment, not calibrated release grading','runtime_sha256':canary.digest((ROOT/'tools/canary_runtime.py').read_bytes())})
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures=[pool.submit(run_one,c,s) for c in CATALOG for s in ('baseline','candidate')]
        records=[f.result() for f in concurrent.futures.as_completed(futures)]
    canary.save(OUT/'runs.json',records)

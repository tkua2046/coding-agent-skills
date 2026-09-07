"""Run the independent frozen transfer packet using the existing runtime."""
import concurrent.futures
import json
import shutil
import sys
import tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from tools import canary, canary_runtime as runtime
PACKET=ROOT/'artifacts/repair/transfer-packet'
OUT=ROOT/'artifacts/repair/acceptance'
SETTINGS={'model':'gpt-5.6-sol','effort':'medium','timeout_seconds':900}


def run(task,side):
    source=PACKET/task
    target=OUT/task/(side+'-r2'); target.mkdir(parents=True,exist_ok=False)
    selected=canary.files(OUT/'inputs'/side)
    with tempfile.TemporaryDirectory(prefix='skill-transfer-') as tmp:
        work=Path(tmp).resolve()
        head=canary.init_fixture(work,{**canary.files(source/'fixture'),**selected})
        initial=canary.files(work)
        prompt=(source/'REQUEST.md').read_text()+'\n\nUse the supplied workflow skills under skills/ as relevant to this request, and read AGENTS.md. CANARY_PYTHON points to the prepared Python runtime.\n'
        (target/'prompt.md').write_text(prompt)
        isolation=runtime.probe(work,source/'accept.py'); canary.save(target/'isolation.json',isolation)
        if not isolation['passed']: return {'task':task,'side':side,'completed':False,'reason':'isolation failed'}
        result=runtime.execute(work,prompt,target/'reply.md',SETTINGS); canary.save(target/'execution.json',result)
        canary.save(target/'git.json',canary.git_snapshot(work,head))
        checks=[]
        for name,argv in [('project-tests',[sys.executable,'-B','-m','unittest','discover','-s','tests','-v']),('independent-behavior',[sys.executable,'-B',str(source/'accept.py'),str(work)])]:
            check=runtime.capture(argv,work,60); check['name']=name; checks.append(check)
        canary.save(target/'checks.json',checks)
        final=canary.files(work)
        canary.write_files(target/'workspace',{p:b for p,b in final.items() if not p.startswith('skills/')})
        row={'case':task,'side':side,'completed':result['completed'],'seconds':result['elapsed_seconds'],'settings':SETTINGS,'checks':[(c['name'],c['exit_code']) for c in checks],'request_preserved':(work/'REQUEST.md').read_bytes()==(source/'REQUEST.md').read_bytes(),'skills_preserved':all((work/p).read_bytes()==b for p,b in selected.items()),'initial':canary.hashes({p:b for p,b in initial.items() if not p.startswith('skills/')}),'final':canary.hashes({p:b for p,b in final.items() if not p.startswith('skills/')}),'semantic_assessment':'pending independent review'}
        canary.save(target/'record.json',row)
        print(json.dumps({k:v for k,v in row.items() if k not in ('initial','final')}),flush=True)
        return row


if __name__=='__main__':
    canary.save(OUT/'transfer-r2-protocol.json',{'tasks':['transcript-search','packet-import'],'settings':SETTINGS,'packet_freeze':canary.read_json(PACKET/'FREEZE.json')})
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures=[pool.submit(run,t,s) for t in ['transcript-search','packet-import'] for s in ['baseline','candidate']]
        rows=[f.result() for f in concurrent.futures.as_completed(futures)]
    canary.save(OUT/'transfer-r2-runs.json',rows)

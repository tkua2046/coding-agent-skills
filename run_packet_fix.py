"""Exercise an ordinary reviewed repair using the unchanged stage skill."""
import json,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from tools import canary,canary_runtime as runtime
OUT=ROOT/'artifacts/repair/packet-fix';OUT.mkdir(exist_ok=False)
source=ROOT/'artifacts/repair/acceptance/packet-import/candidate-r2/workspace'
review='''# Independent review: changes required

The original API allows corruption errors as BadZipFile, ValueError or an appropriate OSError. The original CLI must report failures without traceback or a misleading success listing.

R1: import_packet propagates zlib.error for a damaged DEFLATE block, outside that API error contract. R2: that error escapes main() and prints a traceback. Both defects were reproduced on the current output. Cleanup and retry worked, and ordinary tests passed; preserve those properties.

Reproduction: create an ordinary ZIP with ZIP_DEFLATED, locate the first member payload after its local header, and set the first compressed byte to (byte & 0xF9) | 0x06 (reserved block type 3). The API currently raises zlib.error with invalid block type; the CLI exits1 with traceback. Verify public API and CLI error outcomes on real malformed compressed data, destination absence/cleanup and a successful corrected-archive retry.

Fix these material findings within the original scope. Original implementation has not yet been rechecked or accepted after a fix.
'''
canary.write_files(OUT/'initial',canary.files(source));(OUT/'original-review.md').write_text(review)
selected=canary.skill_files(ROOT,['stage-development']);canary.write_files(OUT/'inputs',selected)
prompt='''Use skills/stage-development to address the independent findings in reviews/R1.md on this existing implementation. REQUEST.md is the unchanged original contract. Complete the scoped fix, meaningful regression tests and the existing project gate. Preserve the original review and requirements. Keep unaffected design and implementation decisions intact; report the actual checks and what remains for independent recheck. Local implementation is authorized; no packages, network, commits or publishing.'''
(OUT/'prompt.md').write_text(prompt)
with tempfile.TemporaryDirectory(prefix='skill-packet-fix-') as tmp:
 work=Path(tmp).resolve();head=canary.init_fixture(work,{**canary.files(source),**selected,'reviews/R1.md':review.encode()})
 initial=canary.files(work)
 probe=runtime.probe(work,ROOT/'artifacts/repair/transfer-packet/packet-import/accept.py');canary.save(OUT/'isolation.json',probe)
 assert probe['passed']
 config={'model':'gpt-5.6-sol','effort':'medium','timeout_seconds':300}
 result=runtime.execute(work,prompt,OUT/'reply.md',config);canary.save(OUT/'execution.json',result)
 checks=[]
 for name,argv in [('project-tests',[sys.executable,'-B','-m','unittest','discover','-s','tests','-v']),('original-behavior',[sys.executable,'-B',str(ROOT/'artifacts/repair/transfer-packet/packet-import/accept.py'),str(work)])]:
  check=runtime.capture(argv,work,60);check['name']=name;checks.append(check)
 canary.save(OUT/'checks.json',checks);canary.save(OUT/'git.json',canary.git_snapshot(work,head))
 final=canary.files(work);canary.write_files(OUT/'workspace',{p:b for p,b in final.items() if not p.startswith('skills/')})
 row={'completed':result['completed'],'elapsed_seconds':result['elapsed_seconds'],'settings':config,'checks':[(c['name'],c['exit_code']) for c in checks],'initial':canary.hashes(initial),'final':canary.hashes(final),'skills':canary.hashes(selected),'source':'acceptance/packet-import/candidate-r2','review_recheck':'pending','requirements_preserved':final['REQUEST.md']==initial['REQUEST.md'],'review_preserved':final['reviews/R1.md']==initial['reviews/R1.md']}
 canary.save(OUT/'record.json',row)
 print(json.dumps({k:v for k,v in row.items() if k not in ('initial','final','skills')}),flush=True)

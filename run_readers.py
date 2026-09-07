import concurrent.futures,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT))
from tools import canary
OUT=ROOT/'artifacts/repair/acceptance/bounded-investigation'
probe=canary.read_json(ROOT/'evals/cases/bounded-investigation/case.json')['reading_probe']
settings={'model':'gpt-5.6-sol','effort':'medium','timeout_seconds':180}
def read(side):
 record=canary.read_json(OUT/side/'record.json'); assert record['completed']
 canary.run_reader(OUT/side/'workspace',OUT/side/'reading-probe',probe,settings)
 print(side,'reader completed',flush=True)
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
  futures=[pool.submit(read,s) for s in sys.argv[1:]]
  for f in concurrent.futures.as_completed(futures):f.result()

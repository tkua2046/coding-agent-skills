import json, pathlib, subprocess
pathlib.Path('sample.txt').write_text('git sandbox smoke\n')
commands = [['git', 'init', '-q', '-b', 'main'], ['git', 'status', '--porcelain'], ['git', 'add', 'sample.txt'], ['git', '-c', 'user.name=Canary Smoke', '-c', 'user.email=smoke@example.invalid', '-c', 'commit.gpgsign=false', 'commit', '-qm', 'Sandbox smoke'], ['git', 'log', '-1', '--format=%H'], ['git', 'status', '--porcelain']]
results=[]
for command in commands:
    result=subprocess.run(command, text=True, capture_output=True, timeout=10)
    results.append({'argv':command,'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
    if result.returncode:
        break
print(json.dumps(results, indent=2))
raise SystemExit(any(r['exit_code'] for r in results))

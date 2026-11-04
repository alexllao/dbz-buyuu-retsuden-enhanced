from pathlib import Path
import concurrent.futures,subprocess,sys,json
p=Path('work/gameplay-review')
def run(case):
 cid,turbo=case;name=f'matrix-{cid:02}-'+('turbo' if turbo else 'normal')
 cmd=[sys.executable,'work/review_movement.py',str(p/'candidate-v2.bin'),name,'--character',str(cid)]
 if turbo:cmd.append('--turbo')
 r=subprocess.run(cmd,capture_output=True,text=True)
 assert r.returncode==0,(name,r.stderr,r.stdout)
 d=json.loads((p/name/'movement.json').read_text());checks={}
 for direction in ['LEFT','RIGHT']:
  cases=[x for x in d['results'] if x['direction']==direction]
  checks[direction+'-single-no-dash']=all(not ({7,8}&{s['action'] for s in x['trace']}) for x in cases if x['gap']==0)
  checks[direction+'-double-dash']=all(bool({7,8}&{s['action'] for s in x['trace']}) for x in cases if x['gap'] in [2,4,8] and 'hold' not in x)
  long=next(x for x in cases if x.get('hold')==120)
  checks[direction+'-held-dash']=long['trace'][long['releaseFrame']-1]['action'] in [7,8]
  checks[direction+'-release-idle']=long['trace'][-1]['action']==0
 return {'character':cid,'turbo':turbo,'romSha256':d['rom'],'checks':checks,'passed':all(checks.values())}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 results=list(pool.map(run,[(cid,turbo) for cid in range(11) for turbo in [False,True]]))
(p/'movement-matrix.json').write_text(json.dumps(results,indent=2))
print(json.dumps({'cases':len(results),'passed':sum(x['passed'] for x in results),'failures':[x for x in results if not x['passed']]}),flush=True)
assert all(x['passed'] for x in results)

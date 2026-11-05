from pathlib import Path
import subprocess,sys,concurrent.futures,json,hashlib
rom='work/native-stun-fix/candidate.bin';sha=hashlib.sha256(Path(rom).read_bytes()).hexdigest()
jobs=[(cid,p,t) for cid in range(11) for p,t in [(1,False),(2,False),(1,True)]]
def run(j):
 c,p,t=j;r=subprocess.run([sys.executable,'work/native-stun-fix/test_delay.py',rom,str(c),str(p)]+(['--turbo'] if t else []),capture_output=True,text=True)
 path=Path('work/native-stun-fix/tests-delay9')/f'{sha[:8]}-{c}-p{p}-{int(t)}'/'report.json'
 d=json.loads(path.read_text()) if path.exists() else {};out={'cid':c,'port':p,'turbo':t,'passed':r.returncode==0,'cases':len(d.get('results',[])),'routes':[{**x['summary'],'checks':x['checks']} for x in d.get('results',[])]}
 if not t:
  out['threeBasicsObservedBothDirections']=all(any(x['summary']['route'] in ['AAA','ABA','BAB','ABB'] and x['summary']['reverse']==rev and any(len(g)==3 for g in x['summary']['groups']) for x in d.get('results',[])) for rev in [False,True]);out['followupQueuedBothDirections']=all(any(x['summary']['route'] in ['AAA','ABA','BAB','ABB'] and x['summary']['reverse']==rev and x['summary']['maxLinks']>=1 for x in d.get('results',[])) for rev in [False,True]);out['passed'] &= out['followupQueuedBothDirections']
 if r.returncode:out['error']=r.stderr[-300:]
 print(c,p,t,out['passed'],flush=True);return out
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:r=list(pool.map(run,jobs))
Path('work/native-stun-fix/matrix.json').write_text(json.dumps({'romSha256':sha,'passed':all(x['passed'] for x in r),'cases':sum(x['cases'] for x in r),'jobs':r},indent=2),encoding='utf8')

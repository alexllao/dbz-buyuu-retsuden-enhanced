from pathlib import Path
import subprocess,sys,json,concurrent.futures
source='work/teleport-advantage/candidate.bin';jobs=[(cid,port,turbo) for cid in range(11) for port,turbo in [(1,False),(2,True)]]
def job(args):
 cid,port,turbo=args;cmd=[sys.executable,'work/teleport-advantage/test_window.py',source,str(cid),str(port),'current']+(['--turbo'] if turbo else []);r=subprocess.run(cmd,capture_output=True,text=True)
 return args,r
reports=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 for args,r in pool.map(job,jobs):
  print(args,r.returncode,flush=True)
  if r.returncode:print(r.stdout,r.stderr,flush=True);raise SystemExit(r.returncode)
  cid,port,turbo=args;reports.append(json.loads(Path(f'work/teleport-advantage/tests/current-{cid}-p{port}-{int(turbo)}/report.json').read_text()))
Path('work/teleport-advantage/runtime-validation.json').write_text(json.dumps(dict(passed=True,romSha256=reports[0]['romSha256'],characters=11,jobs=len(reports),inputTrials=sum(len(r['results']) for r in reports),liveCounterWindows=sum(r['counterClearsLiveWindow'] for r in reports),reports=reports),indent=2))

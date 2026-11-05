from pathlib import Path
import subprocess,sys,json,hashlib,concurrent.futures
source='work/hits-hud/candidate.bin';sha=hashlib.sha256(Path(source).read_bytes()).hexdigest();jobs=[(cid,port,turbo) for cid in range(11) for port,turbo in [(1,False),(2,True)]]
def job(args):
 cid,port,turbo=args;r=subprocess.run([sys.executable,'work/side-switch/test_commands.py',source,str(cid),str(port)]+(['--turbo'] if turbo else []),capture_output=True,text=True);return args,r
reports=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 for args,r in pool.map(job,jobs):
  print(args,r.returncode,flush=True)
  if r.returncode:print(r.stdout,r.stderr,flush=True);raise SystemExit(r.returncode)
  cid,port,turbo=args;reports.append(json.loads(Path(f'work/side-switch/tests/{sha[:8]}-{cid:02}-p{port}-{int(turbo)}/report.json').read_text()))
Path('work/hits-hud/side-regression.json').write_text(json.dumps(dict(passed=all(t['passed'] for r in reports for t in r['results']),romSha256=sha,jobs=len(reports),cases=sum(len(r['results']) for r in reports),reports=reports),indent=2))

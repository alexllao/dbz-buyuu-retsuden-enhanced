from pathlib import Path
import subprocess,sys,json,concurrent.futures
jobs=[(c,p,t) for c in range(11) for p,t in [(1,False),(2,True)]]
def job(args):
 c,p,t=args;r=subprocess.run([sys.executable,'work/hits-hud-v3/test_counter.py','work/hits-hud-v3/candidate.bin',str(c),str(p)]+(['--turbo'] if t else []),capture_output=True,text=True);return args,r
reports=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 for args,r in pool.map(job,jobs):
  print(args,r.returncode,flush=True)
  if r.returncode:print(r.stdout,r.stderr,flush=True);raise SystemExit(r.returncode)
  c,p,t=args;reports.append(json.loads(Path(f'work/hits-hud-v3/tests/{c}-p{p}-{int(t)}/report.json').read_text()))
Path('work/hits-hud-v3/runtime-validation.json').write_text(json.dumps(dict(passed=True,romSha256=reports[0]['romSha256'],characters=11,jobs=22,cases=88,reports=reports),indent=2))

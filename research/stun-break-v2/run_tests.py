from pathlib import Path
import subprocess,sys,json
reports=[]
for cid in range(11):
 for port,turbo in [(2,False),(1,True)]:
  cmd=[sys.executable,'work/stun-break/test_break.py','work/stun-break/candidate.bin',str(cid),str(port),'current']+(['--turbo'] if turbo else [])
  r=subprocess.run(cmd,capture_output=True,text=True)
  print(cid,port,turbo,r.returncode,flush=True)
  if r.returncode:print(r.stdout,r.stderr,flush=True);sys.exit(r.returncode)
  reports.append(json.loads(Path(f'work/stun-break/tests/current-{cid}-p{port}-{int(turbo)}/report.json').read_text()))
Path('work/stun-break/runtime-validation.json').write_text(json.dumps(dict(passed=all(r['passed'] for r in reports),romSha256=reports[0]['romSha256'],cases=sum(len(r['results']) for r in reports),victimCharacters=11,portsAndSpeed='P2 normal and P1 turbo',reports=reports),indent=2))

from pathlib import Path
import subprocess,concurrent.futures,sys,json,hashlib
sha=hashlib.sha256(Path('work/generic-combos/candidate.bin').read_bytes()).hexdigest()
def run(job):
 c,m=job;p=Path(f'work/generic-combos/finishers/{c}/report.json');d=json.loads(p.read_text());assert d['romSha256']==sha
 r=subprocess.run([sys.executable,'work/generic-combos/record_demo.py',str(c),m],capture_output=True,text=True);print(c,m,r.returncode,r.stderr[-500:],flush=True);assert r.returncode==0
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(run,[(c,'downB') for c in range(11)]+[(0,'flurry')]))

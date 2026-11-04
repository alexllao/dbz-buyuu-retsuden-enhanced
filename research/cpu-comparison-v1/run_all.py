from pathlib import Path
import subprocess,sys,json,concurrent.futures
ROOT=Path('work/cpu-soak');pairs=[(0,1),(9,6),(10,8),(2,5),(3,4),(7,5)]
variants={'original':'work/rom/original.bin','enhanced':'work/auras/colors-v4/candidate.bin'}
def run(job):
 variant,index,pair=job;out=ROOT/'results'/variant/f'{index:02}';out.mkdir(parents=True,exist_ok=True)
 if (out/'Informe.json').exists():
  d=json.loads((out/'Informe.json').read_text(encoding='utf-8'));assert d['pair']==list(pair) and d['requested_cap_seconds']==35
  print('Reuse completed fixture',variant,index,flush=True);return
 with (out/'run.log').open('w') as log:
  r=subprocess.run([sys.executable,str(ROOT/'record_cpu.py'),variants[variant],str(pair[0]),str(pair[1]),str(out),'35'],stdout=log,stderr=subprocess.STDOUT)
 if r.returncode:raise RuntimeError((variant,index,(out/'run.log').read_text()))
 d=json.loads((out/'Informe.json').read_text(encoding='utf-8'));print(variant,index,d['pair'],'HP',[d['final'][p]['hp'] for p in ['p1','p2']],'seconds',round(d['gameplay_seconds'],3),'atlas faults',sum(s.get('atlas_fault',False) for s in d['samples']),flush=True)
jobs=[(v,i,p) for i,p in enumerate(pairs) for v in variants]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(run,jobs))
print('All twelve native CPU fixtures finished.',flush=True)

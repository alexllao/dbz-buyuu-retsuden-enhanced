from pathlib import Path
import subprocess,sys,concurrent.futures
P=Path('work/long-combos')
def run(i):
 with (P/f'{i:02}.log').open('w',encoding='utf8') as out:r=subprocess.run([sys.executable,str(P/'record.py'),str(i)],stdout=out,stderr=subprocess.STDOUT)
 print(i,r.returncode,flush=True);assert r.returncode==0
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(run,range(1,8)))

from pathlib import Path
import concurrent.futures,subprocess,sys
rom='work/generic-combos/candidate.bin'
def run(c):
 p=subprocess.run([sys.executable,'work/generic-combos/test_finishers.py',rom,str(c)],capture_output=True,text=True)
 Path(f'work/generic-combos/finish{c}.log').write_text(p.stdout+p.stderr,encoding='utf8');print(c,p.returncode,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(run,range(1,11)))

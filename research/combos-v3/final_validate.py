from pathlib import Path
import subprocess,sys,json,hashlib
P=Path('work/generic-combos');rom=str(P/'candidate.bin');sha=hashlib.sha256(Path(rom).read_bytes()).hexdigest()
commands=[['run_matrix_delay.py'],['run_finishers.py'],['test_finishers.py',rom,'0'],['run_side_regression.py',rom],['probe_regression.py',rom,'0'],['probe_regression.py',rom,'3'],['verify_native_regression.py']]+[['test_repeat.py',rom,str(c)] for c in [0,1,3,6,10]]
for n,args in enumerate(commands):
 with (P/f'final-{n:02}.log').open('w',encoding='utf8') as log:r=subprocess.run([sys.executable,str(P/args[0]),*args[1:]],stdout=log,stderr=subprocess.STDOUT)
 print(n,args[0],r.returncode,flush=True);assert r.returncode==0
assert all(json.loads((P/n).read_text())['romSha256' if n!='native-regression.json' else 'targetSha256']==sha for n in ['matrix.json','side-regression.json','native-regression.json'])
print('FINAL_VALIDATION_COMPLETE',sha,flush=True)

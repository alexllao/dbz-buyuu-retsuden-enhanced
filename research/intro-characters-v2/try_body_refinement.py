import sys,json
from pathlib import Path
sys.path.insert(0,'work/intro-body-refined')
import recompose
attempts=[]
for seed in range(40):
 try:
  r=recompose.build_candidate(seed);attempts.append({'seed':seed,'success':True,'stats':r['stats']});print('PASS',seed,r['stats'],flush=True);break
 except AssertionError as e:
  attempts.append({'seed':seed,'success':False,'reason':str(e)});print('retry',seed,str(e)[:100],flush=True)
else:raise RuntimeError('No valid packing found')
Path('work/intro-body-refined/packing-attempts.json').write_text(json.dumps(attempts,indent=2))

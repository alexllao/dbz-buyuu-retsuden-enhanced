from pathlib import Path
import sys,json
sys.argv=['probe','normal']
s=Path('work/namek-native/record-promo.py').read_text().split('\ntry:\n if capture_from==1:')[0].replace('work/namek-native/','work/namek-native-v5/').replace('work/namek-native-v5/states','work/namek-native-v5/states-reviewed')
exec(compile(s,'v5-run-probe','exec'),globals());results=[]
try:
 for cid in [3,0]:
  for hold in [1,2,3,4,6,8,12]:
   for gap in [1,2,3,4,6,8,12,16]:
    restore((N/f'seed-{cid}.state').read_bytes());wb(P1+0xbe,0);wb(P2+0xbe,0);ww(P1+0xa,300);ww(P2+0xa,480);ww(P1+0xc,0);ww(P2+0xc,0);wb(P1+0x59,0);wb(P2+0x59,1)
    for _ in range(8):tick()
    samples=[]
    for k in [['RIGHT']]*hold+[[]]*gap+[['RIGHT']]*24:
     tick(k);samples.append(st(P1))
    runs=sum(t['action'] in [7,8] for t in samples)
    if runs:results.append(dict(cid=cid,hold=hold,gap=gap,runFrames=runs,actions=sorted(set(t['action'] for t in samples))))
 print('SUCCESS',results[:30],flush=True)
 Path('work/namek-v5-short/run-timing.json').write_text(json.dumps(results,indent=2))
finally:core.retro_unload_game();core.retro_deinit()

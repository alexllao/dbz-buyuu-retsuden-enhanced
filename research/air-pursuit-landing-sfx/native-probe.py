from pathlib import Path
import sys,json
setup=Path('work/combo-charge-all/runtime.py').read_text().replace('work/combo-charge-all/candidate.bin','work/air-pursuit-fall/candidate.bin')
sys.argv=['probe','after'];exec(compile(setup,'landing-sfx-runtime','exec'),globals())
try:
 for cid in [0,3]:
  restore((Path('work/air-pursuit/states-final/normal')/f'seed-{cid}.state').read_bytes())
  soundRows=[]
  for frame in range(120):
   rawtick(['UP'] if frame<3 else [])
   soundRows.append(dict(f=frame,program=rw(P1),clock=rw(P1+6),action=rb(P1+0x5b),y=rw(P1+16),pose=rb(P1+4),sound=rb(0x5000),soundMem=bytes(rb(0x5000+i) for i in range(16)).hex()))
  Path(f'work/landing-sound-native-{cid}.json').write_text(json.dumps(soundRows))
  print(cid,[(t['f'],t['program'],t['clock'],t['y'],t['soundMem']) for i,t in enumerate(soundRows) if i==0 or t['soundMem']!=soundRows[i-1]['soundMem'] or (i and t['y']==448 and soundRows[i-1]['y']<448)],flush=True)
finally:core.retro_unload_game();core.retro_deinit()

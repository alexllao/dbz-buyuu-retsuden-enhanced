from pathlib import Path
import sys,json
P=Path('work/barrage-five');which=sys.argv[1];rompath='work/barrage-five/candidate.bin' if which=='after' else 'work/knockdown-k4/candidate.bin';src=Path('work/hits-hud-v3/prepare.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0].replace("romfile=BASE/'work/hits-hud-v3/candidate.bin'",f"romfile=BASE/'{rompath}'")
for old in [0x104,0x106,0x117,0x120,0x121,0x122,0x124]:src=src.replace('b+'+hex(old)+')','b+'+hex(old+0xc00)+')')
sys.argv=['prepare','0'];exec(compile(src,'extra','exec'),globals());results={}
try:
 for label,commandKeys in [('Goku-Kamehameha', [['LEFT'],['DOWN','LEFT'],['DOWN'],['DOWN','RIGHT'],['RIGHT']]),('Goku-basic',[['A']])]:
  restore(Path('work/responsive-v3/routes/0/charged.state').read_bytes());ww(P1+0xa,300);ww(P2+0xa,420 if label.endswith('Kamehameha') else 332);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(15):tick()
  seq=[k for k in commandKeys for _ in range(4)]+[['A']]*3+[[]]*400;r=[]
  for k in seq:tick(k);r.append(dict(p=st(P1),e=st(P2)))
  results[label]=r
 # Vegeta's normal barrage uses the same handler, and must remain native.
 restore(Path('work/responsive-v3/routes/3/charged.state').read_bytes());ww(P1+0xa,300);ww(P2+0xa,420);wb(P1+0x59,0);wb(P2+0x59,1)
 for _ in range(15):tick()
 seq=[k for k in [['LEFT'],['DOWN','LEFT'],['DOWN'],['DOWN','RIGHT'],['RIGHT']] for _ in range(4)]+[['RIGHT','B']]*4+[[]]*350;r=[]
 for k in seq:tick(k);r.append(dict(p=st(P1),e=st(P2)))
 results['Vegeta-native-technique']=r
 (P/f'extra-{which}.json').write_text(json.dumps(results));print(which,[(n,max(t['p']['hits'] for t in r),r[-1]['e']['hp']) for n,r in results.items()])
finally:core.retro_unload_game();core.retro_deinit()

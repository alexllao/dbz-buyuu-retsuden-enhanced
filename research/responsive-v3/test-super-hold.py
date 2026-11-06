from pathlib import Path
import sys,json
root=Path('work/responsive-v3');which=sys.argv[1] if len(sys.argv)>1 else 'after';cid=int(sys.argv[2]) if len(sys.argv)>2 else 0
rompath='work/responsive-v3/candidate.bin' if which=='after' else 'work/hits-hud-v3/candidate.bin'
sys.argv=['prepare',str(cid)]
header=Path('work/hits-hud-v3/prepare.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0].replace("romfile=BASE/'work/hits-hud-v3/candidate.bin'",f"romfile=BASE/'{rompath}'")
for old in [0x104,0x106,0x117,0x120,0x121,0x122,0x124]:header=header.replace('b+'+hex(old)+')','b+'+hex(old+0xc00)+')')
exec(compile(header,'responsive-test-header','exec'),globals())
def row():return dict(p=st(P1),e=st(P2),aura=rb(P1+0xbd),fade=rb(P1+0xd11),token=rb(P1+0xb9),ttl=rb(0xf701),stored=rb(0xf702),latch=rb(0xf703),magic=rb(0xf700),held=rw(P1+0x1a),rawpad=rb(0xe666),history=[rb(P1+0x94+i) for i in range(32)],histpos=rb(P1+0xb6),histstart=rb(P1+0xb7),lastbutton=rb(P1+0xb5))
results={};clips={}
def collect(label,schedule):
 rows=[]
 for keys in schedule:tick(keys);rows.append(dict(keys=keys,**row()))
 results[label]=rows
 return rows

try:
 route=root/'routes'/'0';restore((route/'charged.state').read_bytes());seed=snap();results=[]
 for hold in [3,20,60,120]:
  restore(seed);ww(P1+0xa,300);ww(P2+0xa,364);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(8):tick()
  rr=[]
  for k in [k for k in [['LEFT'],['DOWN','LEFT'],['DOWN'],['DOWN','RIGHT'],['RIGHT']]*2 for _ in range(3)]+[['RIGHT','A']]*hold+[[]]*700:
   tick(k);rr.append(dict(p=st(P1),e=st(P2)))
  hp=[(i,a['e']['hp']-t['e']['hp']) for i,(a,t) in enumerate(zip(rr,rr[1:]),1) if t['e']['hp']<a['e']['hp']]
  results.append(dict(hold=hold,programs=sorted(set(t['p']['program'] for t in rr)),damage=hp,minKi=min(t['p']['ki'] for t in rr)))
 print('SUPER_HOLD',results,flush=True);(root/'super-hold.json').write_text(json.dumps(results,indent=2))
finally:core.retro_unload_game();core.retro_deinit()

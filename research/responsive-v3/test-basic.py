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
 for j,entry in enumerate(steps[:-1]):
  if j in [9,11]:
   selected=cid if j==9 else 3
   for direction,count in [('DOWN',selected//3),('RIGHT',selected%3)]:
    for _ in range(count):
     for _ in range(4):tick([direction])
     for _ in range(16):tick()
  for _ in range(entry.get('frames',1)):tick([] if j==11 else entry.get('buttons',[]))
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(300):tick()
 baseline=snap()

 for hold in [2,5,15,30,60]:
  restore(baseline);r=[]
  for i in range(hold+75):
   tick(['RIGHT'] if i<hold else []);r.append(dict(f=i,x=rw(P1+0xa),velocity=rw(P1+0xe),action=rb(P1+0x5b),held=rb(P1+0x1b)))
  print('WALK',hold,'release',r[hold-1]['x'],'end',r[-1]['x'],'coast',r[-1]['x']-r[hold-1]['x'],flush=True)
  (root/f'walk-after-{hold}.json').write_text(json.dumps(r,indent=2))
 for _ in range(1800):
  tick(['A','B'])
  if rw(P1+0x28)>=240:break
 for _ in range(70):tick()
 charged=snap()
 for distance in [32,64,120,180]:
  restore(charged);ww(P1+0xa,300);ww(P2+0xa,300+distance);r=[]
  seq=[['DOWN']]*4+[['DOWN','RIGHT']]*4+[['RIGHT']]*4+[['RIGHT','A']]*3+[[]]*240
  for i,k in enumerate(seq):
   tick(k);r.append(dict(f=i,p=st(P1),e=st(P2),projectileType=rb(P1+0x7c),projectileSlot=rw(P1+0xe2),p2type=rb(P2+0x7c)))
  print('BARRAGE',distance,[(t['f'],t['e']['hp'],t['projectileType']) for a,t in zip(r,r[1:]) if t['e']['hp']<a['e']['hp']],flush=True)
  (root/f'barrage-after-{distance}.json').write_text(json.dumps(r,indent=2))
finally:core.retro_unload_game();core.retro_deinit()

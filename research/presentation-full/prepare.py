from pathlib import Path
import sys,json
root=Path('work/presentation-full');which=sys.argv[1] if len(sys.argv)>1 else 'after';cid=int(sys.argv[2]) if len(sys.argv)>2 else 0
rompath='work/piccolo-hits/candidate.bin' if which=='after' else 'work/hits-hud-v3/candidate.bin'
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
  if j==13:wb(0xe741,{0:6,1:3,2:2,3:0,4:8,5:7,6:4,7:1,8:6,9:5,10:7}.get(cid,0))
  if j in [9,11]:
   selected=cid if j==9 else (3 if cid==0 else 0)
   for direction,count in [('DOWN',selected//3),('RIGHT',selected%3)]:
    for _ in range(count):
     for _ in range(4):tick([direction])
     for _ in range(16):tick()
  for _ in range(entry.get('frames',1)):tick([] if j==11 else entry.get('buttons',[]))
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(300):tick()
 baseline=snap()

 routeRoot=root/'routes'/str(cid);routeRoot.mkdir(parents=True,exist_ok=True)
 for _ in range(3000):
  tick(['A','B'],['A','B'])
  if min(rw(P1+0x28),rw(P2+0x28))>=235:break
 for _ in range(100):tick()
 assert min(rw(P1+0x28),rw(P2+0x28))>=235
 charged=snap();(routeRoot/'charged.state').write_bytes(charged)
 if cid in [3,5]:
  ww(P1+0xa,300);ww(P2+0xa,332);wb(P1+0x59,0);wb(P2+0x59,1)
  punches=0
  while rw(P1+0x24)>45 and punches<32:
   for f in range(75):tick([],['A'] if f<6 else [])
   for _ in range(120):
    if abs(rw(P2+0xa)-rw(P1+0xa))<=28:break
    tick([],['LEFT'] if rw(P2+0xa)>rw(P1+0xa) else ['RIGHT'])
   for _ in range(4):tick()
   punches+=1
  for _ in range(650):tick()
  while rw(P1+0x28)<235:tick(['A','B'])
  for _ in range(100):tick()
  assert 0<rw(P1+0x24)<=50,(cid,rw(P1+0x24),punches)
  charged=snap();(routeRoot/'low-hp.state').write_bytes(charged)
 (routeRoot/'report.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),cid=rb(P1+0x58),enemyCid=rb(P2+0x58),stage=rb(0xe741),ki=[rw(P1+0x28),rw(P2+0x28)]),indent=2))
 assert rb(P1+0x58)==cid
 print('SEED',cid,'ready',flush=True)
finally:core.retro_unload_game();core.retro_deinit()

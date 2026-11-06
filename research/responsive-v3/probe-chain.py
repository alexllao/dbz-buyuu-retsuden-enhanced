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
 routeRoot=root/'routes'/'0';restore((routeRoot/'charged.state').read_bytes());seed=snap();results=[]
 for approach in [0,4,8]:
  for speed in [2,3]:
   restore(seed);ww(P1+0xa,300);ww(P2+0xa,332);wb(P1+0x59,0);wb(P2+0x59,1)
   for _ in range(8):tick()
   rr=[];contacts=[];hp=rw(P2+0x24)
   def step(a=(),b=()):
    tick(a,b);rr.append(dict(p=st(P1),e=st(P2),keys=list(a),keys2=list(b)))
   for f in range(120):
    keys=['A'] if f<3 else []
    for i,t in enumerate(contacts[:2]):
     if t+3<=f<t+6:keys=[['B','A'][i]]
    step(keys);now=rw(P2+0x24)
    if now<hp:contacts.append(f)
    hp=now
    if len(contacts)>=3 and rb(P1+0x5b)<=8:break
   fwd='RIGHT' if rw(P1+0xa)<rw(P2+0xa) else 'LEFT';back='LEFT' if fwd=='RIGHT' else 'RIGHT'
   for keys in [[fwd]]*4+[[back]]*4+[[fwd,'C']]*4:step(keys)
   for _ in range(80):
    if rw(P1)!=0x843:break
    step()
   crossEnd=len(rr)
   fwd='RIGHT' if rw(P1+0xa)<rw(P2+0xa) else 'LEFT';back='LEFT' if fwd=='RIGHT' else 'RIGHT'
   for _ in range(approach):step([fwd])
   for keys in [[back],['DOWN',back],['DOWN'],['DOWN',fwd],[fwd]]*2:
    for _ in range(speed):step(keys)
   for _ in range(3):step([fwd,'A','B'])
   for _ in range(520):step()
   hits=[dict(frame=i,delta=a['e']['hp']-t['e']['hp'],count=t['p']['hits']) for i,(a,t) in enumerate(zip(rr,rr[1:]),1) if t['e']['hp']<a['e']['hp']]
   summary=dict(approach=approach,speed=speed,crossEnd=crossEnd,maxHits=max(t['p']['hits'] for t in rr),hits=hits,programs=sorted(set(t['p']['program'] for t in rr)))
   results.append(summary);(root/f'chain-{approach}-{speed}.json').write_text(json.dumps(dict(summary=summary,trace=rr),indent=2));print(summary,flush=True)
 (root/'chain-probe.json').write_text(json.dumps(results,indent=2))
finally:core.retro_unload_game();core.retro_deinit()

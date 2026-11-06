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

 while rw(P1+0x28)<235:tick(['A','B'])
 for _ in range(70):tick()
 seed=snap();report=[]
 for delay in [0,8,16,24,32,48,64,80,96,120]:
  restore(seed);ww(P1+0xa,300);ww(P2+0xa,320);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(8):tick()
  rr=[]
  def step(keys=()):
   tick(keys);rr.append(dict(frame=len(rr),keys=list(keys),p=st(P1),e=st(P2),historyHead=rb(P1+0xb6),historyStart=rb(P1+0xb7),victimFlags=rw(P2+0x20),held=rb(P1+0x1b)))
  for _ in range(3):step(['RIGHT','A'])
  assert rw(P1)==0x40a,(delay,rw(P1),rb(P1+0x5b))
  for _ in range(140):
   if rb(P1+0x5b)<=8:break
   step()
  free=len(rr)
  for _ in range(delay):step()
  fwd='LEFT' if rb(P1+0x59) else 'RIGHT';back='RIGHT' if fwd=='LEFT' else 'LEFT'
  commandStart=len(rr)
  for keys in [[back],['DOWN',back],['DOWN'],['DOWN',fwd],[fwd]]:
   for _ in range(3):step(keys)
  for _ in range(3):step([fwd,'A'])
  for _ in range(420):step()
  kame=next((t for t in rr if t['p']['program']==0xc04),None)
  airborne=next((i for i,t in enumerate(rr) if t['e']['y']<448),None)
  land=next((i for i,t in enumerate(rr[airborne+1:],airborne+1) if t['e']['y']==448),None) if airborne is not None else None
  hits=[dict(frame=t['frame'],damage=a['e']['hp']-t['e']['hp'],y=t['e']['y'],action=t['e']['action']) for a,t in zip(rr,rr[1:]) if t['e']['hp']<a['e']['hp']]
  summary=dict(delay=delay,controlFree=free,commandStart=commandStart,kameFrame=kame['frame'] if kame else None,enemyYAtKame=kame['e']['y'] if kame else None,enemyXAtKame=kame['e']['x'] if kame else None,firstLanding=land,startedWhileAirborne=bool(kame and kame['e']['y']<448),hits=hits,kameDamage=sum(t['damage'] for t in hits if t['damage']!=12),lastActions=[rr[-1]['p']['action'],rr[-1]['e']['action']])
  (root/f'delay-{delay}.json').write_text(json.dumps(dict(summary=summary,trace=rr),indent=2),encoding='utf8');report.append(summary);print(summary,flush=True)
 (root/'probe.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),fps=av.timing.fps,cases=report),indent=2),encoding='utf8')
finally:core.retro_unload_game();core.retro_deinit()

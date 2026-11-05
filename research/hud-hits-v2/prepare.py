from pathlib import Path
import sys,json,hashlib,struct,subprocess
BASE=Path.cwd();cid=int(sys.argv[1]);enemyCid=3 if cid in [0,2,5] else 0;stage={0:6,3:0,2:2,5:7}.get(cid,0)
out=BASE/'work/hits-hud-v2/cases'/str(cid);out.mkdir(parents=True,exist_ok=True);romfile=BASE/'work/hits-hud-v2/candidate.bin'
sys.path.insert(0,str(BASE/'work'));sys.argv=['probe','--native','--rom',str(romfile),'--out',str(out)]
header=(BASE/'work/gameplay_probe.py').read_text().split('try:\n for index,step in enumerate(steps[:-1]):')[0].replace('BASE=Path(__file__).resolve().parent.parent','BASE=Path.cwd()')
exec(compile(header,'combo-side-setup','exec'),globals())
trace=[];phase='';mode='';encoder=None;audio_file=None

def st(b):return dict(program=rw(b),action=rb(b+0x5b),hp=rw(b+0x24),ki=rw(b+0x28),x=rw(b+0xa),y=rw(b+0x10),face=rb(b+0x59),hits=rb(b+0x120)&127,hitTTL=rb(b+0x121),hitOpen=rb(b+0x122),stun=rb(b+0x51),dizzyTimer=rw(b+0x36),periodic=rw(b+0x32),threshold=rb(b+0x54),combo=rb(b+0x106),window=rb(b+0x117)&7,cursor=rw(b+6),plane=bool(rb(b+0x1e)&16))
def run(a=(),b=()):
 tick(a,b);trace.append(dict(f=len(trace),phase=phase,keys1=list(a),keys2=list(b),p=st(P1),e=st(P2),scene=rb(0xe73c),cinema=rw(0xe9c4)))
 if encoder:
  w,h,pitch,data=latest;encoder.stdin.write(b''.join(data[y*pitch:y*pitch+w*2] for y in range(h)))

def idle(n):
 for _ in range(n):run()

def forward():return 'RIGHT' if rw(P1+0xa)<rw(P2+0xa) else 'LEFT'
def backward():return 'LEFT' if forward()=='RIGHT' else 'RIGHT'
def opponent_back():return 'RIGHT' if rw(P2+0xa)>rw(P1+0xa) else 'LEFT'

def wait_actor(maximum=180):
 for _ in range(maximum):
  if rb(P1+0x5b)<=8:return True
  run()
 return False

def cross():
 global phase
 phase='cambio-de-lado';wait_actor();f=forward();b=backward()
 for k in [[f]]*4+[[b]]*4+[[f,'C']]*4:run(k)
 for _ in range(80):
  if rw(P1)!=0x843:break
  run()

def move_command(kind,guard=False):
 global phase
 phase=kind;f=forward();b=backward();diagF=['DOWN',f];diagB=['DOWN',b]
 if kind=='meteor':dirs=[[f],diagF,['DOWN'],diagB,[b],[f]] if cid in [0,3] else [[b],diagB,['DOWN'],diagF,[f],[b]];button='B'
 elif kind=='flurry':dirs=[[b],diagB,['DOWN'],diagF,[f]];button='B'
 elif kind=='energy':dirs=[[b],[f]];button='A'
 else:dirs=[[f],['DOWN']];button='B'
 for k in [k for k in dirs for _ in range(4)]+[dirs[-1]+[button]]*4:run(k,[opponent_back()] if guard else [])

def basic_chain(route='ABA'):
 global phase
 phase='basicos-'+route;start=len(trace);hits=[];prev=rw(P2+0x24)
 for f in range(150):
  keys=[route[0]] if f<6 else []
  for index in range(min(len(hits),len(route)-1)):
   t=hits[index]+9
   if t<=f<t+3:keys=[route[index+1]]
  run(keys);hp=rw(P2+0x24)
  if hp<prev:hits.append(f)
  prev=hp
  if f>30 and rb(P1+0x5b)<=8 and (len(hits)>=3 or f>100):break
 return hits

def close_to(distance=30,guard=False):
 global phase
 phase='acercamiento'
 for _ in range(100):
  if abs(rw(P1+0xa)-rw(P2+0xa))<=distance:break
  if rb(P1+0x5b)>8:run();continue
  run([forward()],[opponent_back()] if guard else [])

def execute(label):
 global trace,phase,mode
 trace=[];mode=label;phase='inicio';idle(20)
 if label.startswith('combo-'):basic_chain()
 if 'cambio' in label:cross()
 if label.endswith('basicos'):close_to();basic_chain('BAB')
 elif label.endswith('meteor') or label.endswith('meteor-guardia'):move_command('meteor',label.endswith('guardia'))
 elif label.endswith('especial'):move_command('downB')
 elif label.endswith('rafaga'):move_command('flurry')
 phase='final-y-recuperacion'
 for _ in range(600):
  run([], [opponent_back()] if label.endswith('guardia') else [])
  if len(trace)>270 and rb(P1+0x5b)<=8 and rb(P2+0x5b)<=8 and not rb(0xe73c) and not rw(0xe9c4):break
 idle(40)

try:
 for j,entry in enumerate(steps[:-1]):
  if j in [9,11]:
   selected=cid if j==9 else enemyCid
   for direction,count in [('DOWN',selected//3),('RIGHT',selected%3)]:
    for _ in range(count):
     for _ in range(4):tick([direction])
     for _ in range(16):tick()
  if j==13:wb(0xe741,stage)
  for _ in range(entry.get('frames',1)):tick([] if j==11 else entry.get('buttons',[]))
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(300):tick()
 chargeFrames=0
 while rw(P1+0x28)<230 and chargeFrames<2400:tick(['A','B']);chargeFrames+=1
 for _ in range(100):tick()
 assert rw(P1+0x28)>=205,(cid,rw(P1+0x28))
 baseline=snap();(out/'charged.state').write_bytes(baseline);results=[]
 for label in ['meteor','cambio-meteor','cambio-meteor-guardia','combo-cambio-meteor','combo-cambio-especial','cambio-basicos','cambio-rafaga']:
  restore(baseline);ww(P1+0xa,300);ww(P2+0xa,332);ww(P1+0xc,0);ww(P2+0xc,0);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(8):tick()
  execute(label);hits=[];crosses=[]
  for prev,now in zip(trace,trace[1:]):
   if now['e']['hp']<prev['e']['hp']:hits.append(dict(frame=now['f'],phase=now['phase'],delta=prev['e']['hp']-now['e']['hp'],defenderAction=now['e']['action'],defenderWasFree=prev['e']['action']<=8))
   if prev['p']['program']!=0x843 and now['p']['program']==0x843:crosses.append(now['f'])
  summary=dict(label=label,frames=len(trace),hits=hits,damage=trace[0]['e']['hp']-trace[-1]['e']['hp'],crosses=crosses,programs=sorted(set(t['p']['program'] for t in trace)),cinematic=any(t['cinema'] for t in trace),final=[trace[-1]['p']['action'],trace[-1]['e']['action']],startKi=trace[0]['p']['ki'],minimumKi=min(t['p']['ki'] for t in trace))
  (out/(label+'.json')).write_text(json.dumps(dict(summary=summary,trace=trace),indent=2),encoding='utf-8');results.append(summary);print(cid,summary,flush=True)
 (out/'report.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),cid=cid,enemyCid=enemyCid,stage=stage,chargeFrames=chargeFrames,chargedKi=rw(P1+0x28),fixture='Native menus, both human; ki charged by real A+B. Restored charged snapshot before each branch, only initial spacing/facing set; no HP/ki/actions/timers forced.',results=results),indent=2))
finally:core.retro_unload_game();core.retro_deinit()

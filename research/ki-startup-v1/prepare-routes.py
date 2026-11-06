from pathlib import Path
import sys,json
root=Path('work/ki-startup');which=sys.argv[1] if len(sys.argv)>1 else 'after';cid=int(sys.argv[2]) if len(sys.argv)>2 else 0
rompath='work/ki-startup/candidate.bin' if which=='after' else 'work/hits-hud-v3/candidate.bin'
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
  if j==13:wb(0xe741,{0:6,1:3,2:2,3:0,5:7}.get(cid,0))
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
 def basic_fast(route='ABA'):
  global phase
  phase='basicos-'+route;contacts=[];hp=rw(P2+0x24)
  for f in range(160):
   keys=[route[0]] if f<3 else []
   for index,t in enumerate(contacts[:len(route)-1]):
    if t+3<=f<t+6:keys=[route[index+1]]
   run(keys);now=rw(P2+0x24)
   if now<hp:contacts.append(f)
   hp=now
   if len(contacts)>=len(route) and rb(P1+0x5b)<=8:break
  return contacts
 results=[]
 def scene(label,route):
  global trace,phase
  restore(charged);ww(P1+0xa,300);ww(P2+0xa,332);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(8):tick()
  trace=[];phase='setup';idle(20)
  if 'combo' in route:basic_fast('ABA')
  if 'cross' in route:cross();close_to(28)
  phase=label;f=forward();b=backward()
  if 'meteor' in route:
   dirs=([[b],['DOWN',b],['DOWN'],['DOWN',f],[f]]*2 if cid==0 else [['DOWN'],['DOWN',f],[f],[b]] if cid==5 else [[f],['DOWN',f],['DOWN'],['DOWN',b],[b],[f]] if cid in [1,3] else [[b],['DOWN',b],['DOWN'],['DOWN',f],[f],[b]])
   btn=['A','B'] if cid==0 else ['B']
  elif 'flurry' in route:dirs=[['DOWN'],['DOWN',b],[b]];btn=['B']
  else:dirs=([[b],['DOWN',b],['DOWN'],['DOWN',f],[f]] if cid==0 else [[f],['DOWN',f],['DOWN'],['DOWN',b],[b]]);btn=['A']
  for k in dirs:
   for _ in range(4):run(k)
  for _ in range(4):run(dirs[-1]+btn)
  phase='finish'
  for _ in range(1400):
   run()
   if len(trace)>330 and rb(P1+0x5b)<=8 and rb(P2+0x5b)<=8 and not rb(0xe73c) and not rw(0xe9c4):
    idle(45);break
  contacts=[dict(frame=t['f'],damage=a['e']['hp']-t['e']['hp'],hits=t['p']['hits'],stun=t['e']['stun'],dizzy=t['e']['dizzyTimer']) for a,t in zip(trace,trace[1:]) if t['e']['hp']<a['e']['hp']]
  result=dict(label=label,cid=cid,startHP=trace[0]['p']['hp'],startKi=trace[0]['p']['ki'],programs=sorted(set(t['p']['program'] for t in trace)),maxHits=max(t['p']['hits'] for t in trace),contacts=contacts,final=[trace[-1]['p']['action'],trace[-1]['e']['action']],crosses=sum(t['p']['program']==0x843 and (i==0 or trace[i-1]['p']['program']!=0x843) for i,t in enumerate(trace)))
  (routeRoot/(label+'.json')).write_text(json.dumps(dict(summary=result,trace=trace),indent=2));results.append(result);print('ROUTE',result,flush=True)
 for label,route in [('meteor','meteor'),('combo-cross-meteor','combo cross meteor'),('combo-cross-special','combo cross special')]:scene(label,route)
 if cid==0:scene('flurry','flurry')
 (routeRoot/'report.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),cid=cid,enemyCid=rb(P2+0x58),stage=rb(0xe741),results=results),indent=2))
finally:core.retro_unload_game();core.retro_deinit()

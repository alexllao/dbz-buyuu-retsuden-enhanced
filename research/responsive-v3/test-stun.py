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
 seedFile=root/'routes'/'0'/'charged.state';meta=json.loads((root/'routes'/'0'/'report.json').read_text());assert meta['romSha256']==hashlib.sha256(rom).hexdigest();restore(seedFile.read_bytes());seed=snap();rows=[];events=[];phase=''
 def step(a=(),b=()):
  prev=st(P2);tick(a,b);now=st(P2);rows.append(dict(frame=len(rows),phase=phase,p=st(P1),e=now,keys=list(a),keys2=list(b)))
  if now['hp']<prev['hp']:events.append(dict(frame=len(rows)-1,phase=phase,before=prev,after=now,hits=rb(P1+0xd20)&127))
 def approach():
  for _ in range(100):
   if abs(rw(P1+0xa)-rw(P2+0xa))<=34:break
   step(['RIGHT'] if rw(P1+0xa)<rw(P2+0xa) else ['LEFT'])
  for _ in range(5):step()
 ww(P1+0xa,300);ww(P2+0xa,332);wb(P1+0x59,0);wb(P2+0x59,1)
 for _ in range(8):step()
 phase='separated-hits'
 for attempt in range(14):
  approach()
  for f in range(100):step(['A'] if f<3 else [])
  if rw(P2+0x36)>0:break
 assert rw(P2+0x36)>0,('dizzy not reached',rw(P2+0x24),rb(P2+0x51),rb(P2+0x54))
 dizzyBefore=st(P2);assert max(t['p']['hits'] for t in rows)<=1
 phase='cross-while-dizzy';hp=rw(P2+0x24);acc=rb(P2+0x51)
 f='RIGHT' if rw(P1+0xa)<rw(P2+0xa) else 'LEFT';b='LEFT' if f=='RIGHT' else 'RIGHT'
 for k in [[f]]*4+[[b]]*4+[[f,'C']]*4:step(k)
 for _ in range(60):
  if rw(P1)!=0x843:break
  step()
 assert rw(P2+0x24)==hp and rb(P2+0x51)==acc and rw(P2+0x36)>0
 phase='first-hit-ends-dizzy';approach();beforeEvents=len(events)
 for f in range(90):
  step(['A'] if f<3 else [])
  if len(events)>beforeEvents:break
 assert len(events)>beforeEvents and events[-1]['before']['dizzyTimer']>0 and events[-1]['after']['dizzyTimer']==0 and events[-1]['after']['stun']==0,events[-1]
 phase='followups';contacts=[];hp=rw(P2+0x24)
 for f in range(110):
  keys=['B'] if f<3 else []
  for t in contacts[:1]:
   if t+3<=f<t+6:keys=['A']
  step(keys);new=rw(P2+0x24)
  if new<hp:contacts.append(f)
  hp=new
 assert all(t['e']['dizzyTimer']==0 for t in rows if t['phase']=='followups')
 phase='inactivity';value=rb(P2+0x51);cleared=False
 for _ in range(1400):
  previous=st(P2);step()
  if value>0 and rb(P2+0x51)==0:
   assert previous['periodic']>=598,(previous,st(P2));cleared=True;break
  if value==0:break
 assert value==0 or cleared
 summary=dict(passed=True,romSha256=hashlib.sha256(rom).hexdigest(),separatedHits=len([t for t in events if t['phase']=='separated-hits']),crossPreservesDizzy=True,firstFollowupClearsDizzy=True,noImmediateRedizzy=True,nativeInactivityDecay=True,events=events,rows=rows)
 (root/'stun-validation.json').write_text(json.dumps(summary,indent=2));print('STUN_CHECKS_PASSED',summary['separatedHits'],'separate hits; cross, first-hit exit, no repeat stun, inactivity',flush=True)
finally:core.retro_unload_game();core.retro_deinit()

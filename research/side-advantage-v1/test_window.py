from pathlib import Path
import sys,json,hashlib
ROOT=Path.cwd();source=sys.argv[1];cid=int(sys.argv[2]);port=int(sys.argv[3]);turbo='--turbo' in sys.argv;tag=sys.argv[4];out=ROOT/'work/teleport-advantage/tests'/f'{tag}-{cid}-p{port}-{int(turbo)}';out.mkdir(parents=True,exist_ok=True)
s=Path('work/side-switch/test_commands.py').read_text().split('results=[]')[0];s=s[s.index('sys.path.insert'):];exec(compile(s,'advantage-setup','exec'),globals())
a=P1 if port==1 else P2;e=P2 if port==1 else P1

def st(b):return dict(x=rw(b+0xa),y=rw(b+0x10),program=rw(b),action=rb(b+0x5b),hp=rw(b+0x24),ki=rw(b+0x28),facing=rb(b+0x59),window=rb(b+0x117)&7,marker=rb(b+0x117)&248,held=rb(b+0x1b),pressed=rb(b+0x1d),magic=rb(b+0x108),token=rb(b+0xb9),bc=rb(b+0xbc))
def step(keys=(),other=()):tick(keys,other) if port==1 else tick(other,keys)
try:
 for j,entry in enumerate(steps[:-1]):
  if j in [9,11]:
   selected=cid if (j==9 and port==1) or (j==11 and port==2) else (3 if cid==0 else 0)
   for direction,count in [('DOWN',selected//3),('RIGHT',selected%3)]:
    for _ in range(count):
     for _ in range(4):tick([direction])
     for _ in range(16):tick()
  keys=entry.get('buttons',[]) if j!=11 else []
  if turbo and j<2:keys=list(set(keys+['A','B']))
  for _ in range(entry.get('frames',1)):tick(keys)
 assert rb(a+0x58)==cid
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(300):tick()
 ww(a+0xa,300);ww(e+0xa,364);ww(a+0xc,0);ww(e+0xc,0);wb(a+0x59,0);wb(e+0x59,1)
 for _ in range(8):tick()
 baseline=snap();rows=[]
 seq=[['RIGHT']]*4+[['LEFT']]*4+[['RIGHT','C']]*4
 for k in seq:step(k);rows.append(dict(a=st(a),e=st(e)))
 during=snap();activated=any(r['a']['program']==0x843 for r in rows)
 if not activated:(out/'activation-failed.json').write_text(json.dumps(rows,indent=2))
 assert activated
 for f in range(100):
  step();rows.append(dict(a=st(a),e=st(e)))
  if rb(e+0x117)&7>0:break
 if tag=='previous':
  # Previous ROM has no window; first-cross snapshot recorded for comparison only.
  pass
 else:assert rb(e+0x117)&7>0,rows
 window=snap();start=st(e);results=[]
 for label,keys in [('punch',['A']),('kick',['B']),('move',['RIGHT']),('guard',['LEFT']),('idle',[])]:
  restore(window);trial=[]
  for f in range(35):
   prev=st(e);step([],keys if f<12 else []);trial.append(dict(f=f,before=prev,after=st(e),a=st(a)))
  if tag!='previous':
   blocked=[r for r in trial if r['before']['window']>0]
   if label in ['punch','kick']:assert all(r['after']['action']<=0x0a for r in blocked),trial
   if label=='move':assert any(r['after']['x']!=r['before']['x'] for r in trial[:6]),trial
   assert trial[-1]['after']['window']==0
  results.append(dict(label=label,trace=trial,passed=True))
 # Verificar una nueva pulsacion despues de terminar la ventana.
 restore(window)
 for _ in range(24):step()
 resumed=[]
 for f in range(50):step([],['A'] if f<6 else []);resumed.append(st(e))
 assert any(0x400<=r['program']<0x800 for r in resumed),'attack did not resume'
 results.append(dict(label='fresh-punch-after-expiry',trace=resumed,passed=True))
 # A real response, prebuffer directions while the first character finishes.
 restore(during)
 for _ in range(20):
  if rw(a+0xa)>rw(e+0xa) and rb(e+0x59)==0:break
  step()
 f='RIGHT' if rw(e+0xa)<rw(a+0xa) else 'LEFT';b='LEFT' if f=='RIGHT' else 'RIGHT';counter=[]
 def counter_step(keys=()):
  before=st(e);step([],keys);counter.append(dict(before=before,after=st(e),keys=keys))
 for keys in [[f]]*4+[[b]]*4:counter_step(keys)
 for _ in range(20):
  if rw(a)!=0x843 and rb(e+0x5b)<=8 and (tag=='previous' or (rb(e+0x117)&7)>0):break
  counter_step([b])
 for keys in [[f,'C']]*4+[[]]*45:counter_step(keys)
 response=any(r['after']['program']==0x843 for r in counter)
 if tag!='previous' and not response:(out/'counter-failed.json').write_text(json.dumps(counter,indent=2))
 if tag!='previous' and cid==0 and not turbo:assert response,'counter activation failed'
 cancelWithin=any(r['before']['window']>0 and r['after']['program']==0x843 and r['after']['window']==0 for r in counter)
 report=dict(romSha256=hashlib.sha256(rom).hexdigest(),cid=cid,port=port,turbo=turbo,initialWindow=start,firstCross=rows,counterActivated=response,counterClearsLiveWindow=cancelWithin,counterTrace=counter,results=results,passed=True,fixture='Native menus, both human. Initial spacing/facing fixed; actual FBF+C. No window/action/HP/ki writes during trials; snapshots restored for repeatable input branches.')
 (out/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(cid,port,turbo,start['window'],response,cancelWithin,flush=True)
finally:core.retro_unload_game();core.retro_deinit()

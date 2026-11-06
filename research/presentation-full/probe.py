from pathlib import Path
import sys,json,hashlib
src=Path('work/responsive-v3/probe-chain.py').read_text().split('try:\n routeRoot=')[0].replace('work/responsive-v3/candidate.bin','work/piccolo-hits/candidate.bin')
sys.argv=['probe','after','0'];exec(compile(src,'presentation-probe-setup','exec'),globals());root=Path('work/presentation-full')
def seed(cid):
 folder='piccolo-hits' if cid in [0,1,2,3,5] else 'presentation-full'
 return Path(f'work/{folder}/routes/{cid}/'+('low-hp.state' if cid in [3,5] else 'charged.state')).read_bytes()
def run(a=(),b=()):tick(a,b);rr.append(dict(p=st(P1),e=st(P2),keys=list(a),keys2=list(b)))
def face():
 f='LEFT' if rb(P1+0x59) else 'RIGHT';return f,('RIGHT' if f=='LEFT' else 'LEFT')
def command(dirs,btn,n=3):
 for k in dirs:
  for _ in range(n):run(k)
 for _ in range(4):run(dirs[-1]+btn)
def basics(route):
 contacts=[];hp=rw(P2+0x24)
 for f in range(160):
  keys=[route[0]] if f<3 else []
  for i,t in enumerate(contacts[:len(route)-1]):
   if t+3<=f<t+6:keys=[route[i+1]]
  run(keys);now=rw(P2+0x24)
  if now<hp:contacts.append(f)
  hp=now
  if len(contacts)>=len(route) and rb(P1+0x5b)<=8:break
 return contacts
def cross():
 f,b=face();command([[f],[b],[f]],['C'],2)
 for _ in range(80):
  if rw(P1)!=0x843 and rb(P1+0x5b)<=8:break
  run()
def finish_command(cid,kind):
 f,b=face();hcf=[[b],['DOWN',b],['DOWN'],['DOWN',f],[f]]
 if kind=='meteor':
  dirs=hcf*2 if cid==0 else [['DOWN'],['DOWN',f],[f],[b]] if cid==5 else [[f],['DOWN',f],['DOWN'],['DOWN',b],[b],[f]] if cid in [1,3] else hcf+[[b]]
  btn=['A','B'] if cid==0 else ['B']
 elif kind=='flurry':dirs=[['DOWN'],['DOWN',b],[b]];btn=['B']
 elif kind=='super':dirs=hcf*2;btn=['A']
 elif kind=='kame':dirs=hcf;btn=['A']
 elif kind=='masenko':dirs=hcf+[[b]];btn=['A']
 else:dirs=[['DOWN'],['DOWN',b],[b],[f]];btn=['A']
 command(dirs,btn,2 if cid==0 else 3)
try:
 reports=[]
 for cid,route,cr,kind in [(0,'AAB',False,'flurry'),(0,'ABA',False,'kame'),(0,'ABB',False,'super'),(0,'BAB',True,'meteor'),(1,'ABA',False,'masenko'),(1,'ABA',True,'meteor'),(2,'AB',True,'meteor'),(3,'ABA',True,'meteor'),(5,'ABA',True,'meteor')]:
  restore(seed(cid));ww(P1+0xa,300);ww(P2+0xa,332);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(8):tick()
  rr=[];contacts=basics(route)
  if cr:cross()
  beforeFinish=len(rr);finish_command(cid,kind)
  for _ in range(760 if cid==5 else 480):run()
  name=f'{cid}-{route}-{int(cr)}-{kind}';r=dict(label=name,cid=cid,route=route,cross=cr,kind=kind,basicContacts=len(contacts),maxHits=max(t['p']['hits'] for t in rr),damage=rr[0]['e']['hp']-rr[-1]['e']['hp'],finishPrograms=sorted(set(t['p']['program'] for t in rr[beforeFinish:])))
  reports.append(r);(root/(name+'.json')).write_text(json.dumps(dict(summary=r,trace=rr)));print(r,flush=True)
 (root/'routes.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),reports=reports),indent=2))
finally:core.retro_unload_game();core.retro_deinit()

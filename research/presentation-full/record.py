from pathlib import Path
import sys,json,hashlib
src=Path('work/piccolo-hits/record-promo.py').read_text(encoding='utf8').split('try:\n # Cold native title')[0].replace("root=baseDir/'work/piccolo-hits/video'","root=baseDir/'work/presentation-full/video'")
src=src.replace("src=src.replace(\"work/input-v2/candidate.bin\"", "src=src.replace('keys=list(a)', 'keys=list(a),keys2=list(b)')\nsrc=src.replace(\"work/input-v2/candidate.bin\"")
exec(compile(src,'full-presentation-runtime','exec'),globals())
def seed(cid,critical=False):
 folder='piccolo-hits' if cid in [0,1,2,3,5] else 'presentation-full'
 return Path(f'work/{folder}/routes/{cid}/'+('low-hp.state' if critical else 'charged.state')).read_bytes()
def staged(cid,facing=0,distance=32):
 restore(seed(cid,cid in [3,5]));ww(P1+0xa,300+distance if facing else 300);ww(P2+0xa,300 if facing else 300+distance);wb(P1+0x59,facing);wb(P2+0x59,1-facing)
 for _ in range(8):tick()
 return snap()
def basics(route):
 contacts=[];hp=rw(P2+0x24)
 for f in range(160):
  keys=[route[0]] if f<3 else []
  for i,t in enumerate(contacts[:len(route)-1]):
   if t+3<=f<t+6:keys=[route[i+1]]
  tick(keys);now=rw(P2+0x24)
  if now<hp:contacts.append(f)
  hp=now
  if len(contacts)>=len(route) and rb(P1+0x5b)<=8:break
 return contacts
def finisher(cid,kind):
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
def settle(minimum=250,maximum=800):
 for i in range(maximum):
  tick()
  if i>=minimum and rb(P1+0x5b)<=8 and rb(P2+0x5b)<=8 and not rb(0xe73c) and not rw(0xe9c4):
   idle(30);break
def command_port(dirs,btn,port):
 for k in dirs:
  for _ in range(2):tick(k if port==1 else [],k if port==2 else [])
 for _ in range(4):tick(dirs[-1]+btn if port==1 else [],dirs[-1]+btn if port==2 else [])
try:
 for _ in range(960):tick()
 intro=snap()
 for _ in range(840):tick()
 title=snap();start('title',title);idle(330);finish()
 start('intro',intro);idle(180);finish()
 routes=[(0,'AAB',False,'flurry',6),(0,'ABA',False,'kame',4),(0,'ABB',False,'super',4),(0,'BAB',True,'meteor',6),(1,'ABA',False,'masenko',4),(3,'ABA',True,'meteor',11),(5,'ABA',True,'meteor',16)]
 for cid,route,cr,kind,expected in routes:
  label=f'combo-{cid}-{route}-{kind}';start(label,staged(cid));idle(12)
  assert len(basics(route))==3
  if cr:cross()
  finisher(cid,kind);settle(250 if cid!=5 else 580,950);finish()
  assert max(t['p']['hits'] for t in rows)>=expected,(label,max(t['p']['hits'] for t in rows))
 for cid in [4,6,7,8,9,10]:
  label=f'special-{cid}';start(label,staged(cid,0,64));idle(12);finisher(cid,'special');settle(230);finish()
  assert rows[0]['e']['hp']>rows[-1]['e']['hp'],label
 start('gohan-meteor',staged(1));idle(12);finisher(1,'meteor');settle(280);finish()
 assert max(t['p']['hits'] for t in rows)>=2
 start('p2-crosses-meteor',staged(1));idle(12)
 for i in range(3):
  actor=P2 if i%2==0 else P1;port=2 if actor==P2 else 1
  for _ in range(100):
   if rb(actor+0x5b)<=8 and rw(P1)!=0x843 and rw(P2)!=0x843:break
   tick()
  f='LEFT' if rb(actor+0x59) else 'RIGHT';b='RIGHT' if f=='LEFT' else 'LEFT'
  command_port([[f],[b],[f]],['C'],port);tick()
 for _ in range(100):
  if rw(P1)!=0x843 and rw(P2)!=0x843 and rb(P2+0x5b)<=8:break
  tick()
 f='LEFT' if rb(P2+0x59) else 'RIGHT';b='RIGHT' if f=='LEFT' else 'LEFT'
 command_port([[b],['DOWN',b],['DOWN'],['DOWN',f],[f]]*2,['A','B'],2);settle(330);finish()
 assert max(t['e']['hits'] for t in rows)>=3
 for cid in [0,2,6,8,10]:
  start(f'aura-{cid}',staged(cid,0,120))
  for _ in range(54):tick(['A','B'])
  idle(10);finish()
 (root/'chapters.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),fps=av.timing.fps,chapters=chapters),indent=2))
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()

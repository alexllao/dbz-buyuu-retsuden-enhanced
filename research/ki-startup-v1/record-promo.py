from pathlib import Path
import sys,json,hashlib
src=Path('work/input-v2/record.py').read_text(encoding='utf8').split('try:\n for j,entry in enumerate(steps[:-1]):')[0]
src=src.replace("root=baseDir/'work/input-v2/video'/which","root=baseDir/'work/ki-startup/video'")
src=src.replace("work/input-v2/candidate.bin","work/ki-startup/candidate.bin").replace('RESPUESTA V2','BUYUU RETSUDEN ENHANCED')
sys.argv=['record','after']
exec(compile(src,'promo-runtime','exec'),globals())

def idle(n):
 for _ in range(n):tick()
def seed(cid,critical=False):
 return Path(f'work/ki-startup/routes/{cid}/'+('low-hp.state' if critical else 'charged.state')).read_bytes()
def face():
 f='RIGHT' if rw(P1+0xa)<rw(P2+0xa) else 'LEFT'
 return f,('LEFT' if f=='RIGHT' else 'RIGHT')
def command(dirs,btn,n=4):
 for k in dirs:
  for _ in range(n):tick(k)
 for _ in range(4):tick(dirs[-1]+btn)
def cross():
 f,b=face()
 command([[f],[b],[f]],['C'])
 for _ in range(80):
  if rw(P1)!=0x843:break
  tick()
def basic():
 contacts=[];hp=rw(P2+0x24)
 for f in range(120):
  keys=['A'] if f<3 else []
  for i,t in enumerate(contacts[:2]):
   if t+3<=f<t+6:keys=[['B','A'][i]]
  tick(keys);now=rw(P2+0x24)
  if now<hp:contacts.append(f)
  hp=now
  if len(contacts)>=3 and rb(P1+0x5b)<=8:break
def hcf():
 f,b=face();return [[b],['DOWN',b],['DOWN'],['DOWN',f],[f]]
def throw_special(cid,label):
 start(label,seed(cid),True);idle(15)
 for _ in range(3):tick(['RIGHT','A'])
 assert rb(P1+0x5b)==0x3a,(label,'throw did not start')
 for _ in range(180):
  if rb(P1+0x5b)<=8:break
  tick()
 idle(48);f,b=face()
 dirs=hcf() if cid==0 else [[b],['DOWN',b],['DOWN'],['DOWN',f],[f],[b]] if cid==1 else [['DOWN'],['DOWN',b],[b],[f]]
 command(dirs,['A']);idle(360);finish()

try:
 # Cold native title, including original and mod credits.
 for _ in range(1800):tick()
 titleSeed=snap();start('01 titulo',titleSeed);idle(360);finish()
 start('02 combo cruce meteor',seed(0),True);idle(18);basic();cross();command(hcf()*2,['A','B'],2);idle(315);finish()
 assert max(t['p']['hits'] for t in rows)>=6,'six real hits not reached'
 start('03 rafaga tres impactos',seed(0),True);ww(P2+0xa,364);idle(15);command([['DOWN'],['DOWN','RIGHT'],['RIGHT']],['A']);idle(240);finish()
 assert max(t['p']['hits'] for t in rows)==3
 start('04 super kamehameha',seed(0),True);ww(P2+0xa,364);idle(18);command(hcf()*2,['A'],3);idle(345);finish()
 start('05 vegeta meteor',seed(3,True),True);idle(18);f,b=face();command([[f],['DOWN',f],['DOWN'],['DOWN',b],[b],[f]],['B']);idle(360);finish()
 assert max(t['p']['hits'] for t in rows)>=8
 start('06 piccolo meteor',seed(2),True);idle(18);f,b=face();command([[b],['DOWN',b],['DOWN'],['DOWN',f],[f],[b]],['B']);idle(360);finish()
 throw_special(1,'07 lanzamiento masenko')
 throw_special(3,'08 lanzamiento final flash')
 throw_special(0,'09 lanzamiento kamehameha')
 start('10 cell trece impactos',seed(5,True),True);idle(18);f,b=face();command([['DOWN'],['DOWN',f],[f],[b]],['B']);idle(700);finish()
 assert max(t['p']['hits'] for t in rows)>=13
 start('11 cruces y meteor',seed(0),True);idle(18)
 for i in range(3):
  f='RIGHT' if rw(P1+0xa)<rw(P2+0xa) else 'LEFT';b='LEFT' if f=='RIGHT' else 'RIGHT'
  actor=P1 if i%2==0 else P2
  if actor==P2:f,b=b,f
  for k in [[f]]*4+[[b]]*4+[[f,'C']]*4:
   tick(k if actor==P1 else [],k if actor==P2 else [])
  idle(28)
 command(hcf()*2,['A','B'],2);idle(340);finish()
 assert max(t['p']['hits'] for t in rows)>=3
 start('12 cierre',titleSeed);idle(180);finish()
 (root/'chapters.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),fps=av.timing.fps,chapters=chapters),indent=2),encoding='utf8')
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()

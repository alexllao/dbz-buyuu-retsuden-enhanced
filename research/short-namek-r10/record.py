from pathlib import Path
import sys,json,hashlib
slug=sys.argv[1]
s=Path('work/namek-native-r10/record.py').read_text().split('\ntry:\n begin(0,')[0]
exec(compile(s,'r10-short-record-runtime','exec'),globals())
root=Path('work/namek-r10-short/captures')/slug;root.mkdir(parents=True,exist_ok=True)
N=Path('work/namek-r10-short/states')/slug
events=[]

def idle(n):
 for _ in range(n):tick()

def chain(pattern='AAB'):
 hits=[];hp=rw(P2+0x24)
 for frame in range(150):
  k=[pattern[0]] if frame<3 else []
  for i,t in enumerate(hits[:len(pattern)-1]):
   if t+3<=frame<t+6:k=[pattern[i+1]]
  tick(k);now=rw(P2+0x24)
  if now<hp:hits.append(frame)
  hp=now
  if len(hits)==len(pattern):break
 assert len(hits)==len(pattern),(slug,pattern,hits)
 return hits

def settle(minimum=220,maximum=1000):
 steady=0
 for f in range(maximum):
  tick();free=rb(P1+0x5b)<=8 and rb(P2+0x5b)<=10 and not rb(0xe73c) and not rw(0xe9c4)
  steady=steady+1 if free else 0
  if f>=minimum and steady>=22:break

def cross(port=1):
 actor=P1 if port==1 else P2;other=P2 if port==1 else P1
 for _ in range(100):
  if rb(actor+0x5b)<=8 and rw(P1)!=0x843 and rw(P2)!=0x843:break
  tick()
 startFrame=len(rows);before=rw(P1+0xa)-rw(P2+0xa)
 f='RIGHT' if rw(actor+0xa)<rw(other+0xa) else 'LEFT';b='LEFT' if f=='RIGHT' else 'RIGHT'
 for keys in [[f]]*4+[[b]]*4+[[f,'C']]*4+[[]]*4:
  tick(keys if port==1 else [],keys if port==2 else [])
 for _ in range(100):
  if rw(actor)!=0x843 and rb(actor+0x5b)<=8:break
  tick()
 after=rw(P1+0xa)-rw(P2+0xa)
 assert before*after<0,(slug,port,'cross did not change sides',before,after,sorted({hex(t['p' if port==1 else 'e']['program']) for t in rows[startFrame:]}))
 events.append(dict(label=chapter,kind='side-switch',port=port,start=startFrame,end=len(rows)))

def done(expected,minimumHits=0):
 assert any(t['p']['program']==expected for t in rows),(slug,chapter,'attack missing',hex(expected))
 assert max(t['p']['hits'] for t in rows)>=minimumHits
 summarize(expected)

try:
 if slug=='normal':
  begin(0,'01-goku-super','GOKU / COMBO + SUPER KAMEHAMEHA');idle(6);chain('ABB');idle(3);f,b=face();hcf=[[b],['DOWN',b],['DOWN'],['DOWN',f],[f]]
  command(hcf*2,['A'],2);settle(260,1000);done(0xc05,3)
  begin(0,'02-crosses-meteor','CRUCES / P1 - P2 - P1 / METEOR');idle(6)
  for port in [1,2,1]:cross(port)
  f,b=face();command([[b],['DOWN',b],['DOWN'],['DOWN',f],[f]]*2,['A','B'],2);settle(240,850);done(0x83e,3)
 elif slug=='aldea':
  begin(3,'01-vegeta-finalflash','VEGETA / COMBO + FINAL FLASH');idle(6);chain();idle(3);f,b=face();command([['DOWN'],['DOWN',b],[b],[f]],['A'],3);settle(230,850);done(0xc27,3)
  begin(3,'02-vegeta-meteor','VEGETA / COMBO + METEOR',critical=True);idle(6);chain();idle(3);f,b=face();command([[f],['DOWN',f],['DOWN'],['DOWN',b],[b],[f]],['B'],3);settle(250,1000);done(0x846,8)
 elif slug=='porunga':
  begin(5,'01-cell-chain','CELL / COMBO - CRUCE - METEOR',critical=True);idle(6);chain();cross(1);f,b=face();command([['DOWN'],['DOWN',f],[f],[b]],['B'],3);settle(540,1100);done(0x84a,10)
 (root/'capture-manifest.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),build='20261110-094744',nativeStage=6,variant=slug,checks=checks,sideSwitches=events,takes=reports,fixture='Native menu/charge/critical HP before recording; initial actor spacing/facing and human control only. No live action, position, HP, KI or timer edits during the clips. Two coordinated human input ports, not reactive CPU.'),indent=2))
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()

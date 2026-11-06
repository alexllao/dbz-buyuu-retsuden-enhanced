from pathlib import Path
import sys,json,hashlib
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

 for _ in range(2200):
  tick(['A','B'],['A','B'])
  if rw(P1+0x28)>=230 and rw(P2+0x28)>=230:break
 for _ in range(70):tick()
 baseline=snap();budget=36000 if cid==0 else 3600;records=[];resets=0;contacts=[0,0];commands={};previous=[rw(P1+0x24),rw(P2+0x24)];maxThirdX=0
 pattern=[['RIGHT']]*20+[[]]*9+[['UP','RIGHT']]*3+[[]]*62+[['LEFT']]*10+[[]]*6+[['A']]*3+[[]]*8+[['B']]*3+[[]]*34+[['A','B']]*35+[['LEFT']]*4+[['DOWN','LEFT']]*4+[['DOWN']]*4+[['DOWN','RIGHT']]*4+[['RIGHT']]*4+[['RIGHT','A']]*3+[[]]*120+[['LEFT']]*3+[['RIGHT']]*3+[['LEFT']]*3+[['RIGHT','C']]*3+[[]]*55
 for f in range(budget):
  if rw(P1+0x24)==0 or rw(P2+0x24)==0 or f%1800==1799:
   restore(baseline);resets+=1;previous=[rw(P1+0x24),rw(P2+0x24)]
  pkeys=pattern[f%len(pattern)]
  qkeys=pattern[(f+83)%len(pattern)];qkeys=[{'RIGHT':'LEFT','LEFT':'RIGHT'}.get(k,k) for k in qkeys]
  tick(pkeys,qkeys)
  for j,b in enumerate([P1,P2]):
   hp=rw(b+0x24)
   if hp<previous[j]:contacts[j]+=1
   previous[j]=hp
   program=rw(b);commands[str(program)]=commands.get(str(program),0)+1
   assert rb(b+0x58)<=10,(f,b,'cid')
   for offset in [0,0x1e,0x3c]:
    typ=rb(b+0xe2+offset)
    if typ==0x20:
     x=rw(b+0xcc+offset)
     assert not 0x8000<x<0xff00,(f,b,offset,'corrupt projectile X',x)
     if offset==0x3c:maxThirdX=max(maxThirdX,x if x<0x8000 else 0)
  if f%60==0:records.append(dict(frame=f,p=st(P1),e=st(P2),scene=rb(0xe73c)))
 report=dict(cid=cid,romSha256=hashlib.sha256(rom).hexdigest(),frames=budget,seconds=budget/av.timing.fps,resets=resets,receivedContacts=contacts,programSamples=commands,maxThirdProjectileX=maxThirdX,passed=True,fixture='Both human ports scripted at normal speed; initial native charged snapshot restored after KO or every1800frames; not human play, not one continuous match',samples=records)
 (root/f'marathon-{cid}.json').write_text(json.dumps(report,indent=2));print('MARATHON',cid,budget,'frames',contacts,'resets',resets,flush=True)
finally:core.retro_unload_game();core.retro_deinit()

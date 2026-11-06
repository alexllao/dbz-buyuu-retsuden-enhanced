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
  if j in [9,11]:
   selected=3 if j==9 else 0
   for direction,count in [('DOWN',selected//3),('RIGHT',selected%3)]:
    for _ in range(count):
     for _ in range(4):tick([direction])
     for _ in range(16):tick()
  for _ in range(entry.get('frames',1)):tick([] if j==11 else entry.get('buttons',[]))
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(300):tick()
 baseline=snap()

 P1,P2=P2,P1
 original_tick=tick
 def tick(a=(),b=()):original_tick(b,a)
 assert rb(P1+0x58)==0
 for _ in range(2500):
  tick(['A','B'])
  if rw(P1+0x28)>=235:break
 for _ in range(80):tick()
 seed=snap();p=0x2216a+2*cid;p+=int.from_bytes(rom[p:p+2],'big');commands={}
 while int.from_bytes(rom[p:p+2],'big')<0x8000:
  commands[int.from_bytes(rom[p:p+2],'big')]=int.from_bytes(rom[p+2:p+4],'big');p+=12
 token=5 if cid==0 else 7 if cid==1 else 6 if 6 in commands else 5
 expected=0xc04 if cid==0 else commands[token];results=[]
 for delay in [0,8,16,24,32,48,64,80,96,120]:
  restore(seed);ww(P1+0xa,300);ww(P2+0xa,320);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(8):tick()
  for _ in range(3):tick(['RIGHT','A'])
  assert rb(P1+0x5b)==0x3a,(cid,'not a throw',rw(P1),rb(P1+0x5b))
  for _ in range(180):
   if rb(P1+0x5b)<=8:break
   tick()
  for _ in range(delay):tick()
  f='LEFT' if rb(P1+0x59) else 'RIGHT';b='RIGHT' if f=='LEFT' else 'LEFT'
  dirs=([[b],['DOWN',b],['DOWN'],['DOWN',f],[f]] if cid==0 else [['DOWN'],['DOWN',b],[b],[f]] if token==6 else [[b],['DOWN',b],['DOWN'],['DOWN',f],[f],[b]] if token==7 else [[f],['DOWN',f],['DOWN'],['DOWN',b],[b]])
  rr=[]
  for k in [k for k in dirs for _ in range(4)]+[dirs[-1]+['A']]*4+[[]]*420:
   tick(k);rr.append(dict(p=st(P1),e=st(P2)))
  result=dict(delay=delay,expected=expected,started=any(t['p']['program']==expected for t in rr),maxHits=max(t['p']['hits'] for t in rr),programs=sorted(set(t['p']['program'] for t in rr)))
  results.append(result)
 (root/'postthrow-ki-port2.json').write_text(json.dumps(dict(cid=cid,token=token,expected=expected,romSha256=hashlib.sha256(rom).hexdigest(),cases=results),indent=2));print('POSTTHROW_KI',cid,hex(expected),sum(t['started'] for t in results),len(results),flush=True)
finally:core.retro_unload_game();core.retro_deinit()

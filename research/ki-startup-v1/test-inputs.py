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
   selected=cid if j==9 else 3
   for direction,count in [('DOWN',selected//3),('RIGHT',selected%3)]:
    for _ in range(count):
     for _ in range(4):tick([direction])
     for _ in range(16):tick()
  for _ in range(entry.get('frames',1)):tick([] if j==11 else entry.get('buttons',[]))
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(300):tick()
 baseline=snap()


 for _ in range(1800):
  tick(['A','B'])
  if rw(P1+0x28)>=240:break
 for _ in range(70):tick()
 charged=snap();cases=[]
 motions={'hcf':['LEFT','DL','DOWN','DR','RIGHT'],'double':['LEFT','DL','DOWN','DR','RIGHT']*2,'qcf':['DOWN','DR','RIGHT'],'cardinals':['LEFT','DOWN','RIGHT'],'invalid':['LEFT','UP','RIGHT']}
 for side in [0,1]:
  for name,dirs in motions.items():
   for speed in [2,3,4,6,8]:
    for offset in [-2,0,3,6]:
     restore(charged);wb(P1+0x59,side);ww(P1+0xa,300 if side==0 else 500);ww(P2+0xa,500 if side==0 else 300)
     for _ in range(8):tick()
     keys=[]
     for d in dirs:
      k={'DL':['DOWN','LEFT'],'DR':['DOWN','RIGHT']}.get(d,[d]);k=[{'LEFT':'RIGHT','RIGHT':'LEFT'}.get(v,v) if side else v for v in k];keys += [k]*speed
     press=len(keys)-1+offset
     keys += [[]]*max(0,offset+4)
     keys=[k+(['A'] if press<=i<press+3 else []) for i,k in enumerate(keys)]+[[]]*130
     programs=[]
     for k in keys:tick(k);programs.append(rw(P1))
     expected={'hcf':0xc04,'double':0xc05,'qcf':0xc01,'cardinals':0xc04}.get(name)
     ok=(expected in programs) if expected else not any(v in programs for v in [0xc04,0xc05,0x83e])
     cases.append(dict(side=side,motion=name,speed=speed,offset=offset,expected=expected,ok=ok,programs=sorted(set(programs))))
  print('SIDE',side,'passed',sum(c['ok'] for c in cases if c['side']==side),'of',sum(c['side']==side for c in cases),flush=True)
 (root/'input-matrix.json').write_text(json.dumps(cases,indent=2));print('FAILED',[c for c in cases if not c['ok']][:12],flush=True)
finally:core.retro_unload_game();core.retro_deinit()

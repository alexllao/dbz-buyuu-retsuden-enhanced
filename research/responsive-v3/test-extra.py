from pathlib import Path
import sys,json
root=Path('work/responsive-v3');which=sys.argv[1] if len(sys.argv)>1 else 'after';cid=int(sys.argv[2]) if len(sys.argv)>2 else 0
rompath='work/responsive-v3/candidate.bin' if which=='after' else 'work/hits-hud-v3/candidate.bin'
sys.argv=['prepare',str(cid)]
header=Path('work/hits-hud-v3/prepare.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0].replace("romfile=BASE/'work/hits-hud-v3/candidate.bin'",f"romfile=BASE/'{rompath}'")
exec(compile(header,'responsive-test-header','exec'),globals())
def row():return dict(p=st(P1),e=st(P2),aura=rb(P1+0xbd),fade=rb(P1+0x111),token=rb(P1+0xb9),ttl=rb(0xf701),stored=rb(0xf702),latch=rb(0xf703),magic=rb(0xf700),held=rw(P1+0x1a),rawpad=rb(0xe666),history=[rb(P1+0x94+i) for i in range(32)],histpos=rb(P1+0xb6),histstart=rb(P1+0xb7),lastbutton=rb(P1+0xb5))
results={};clips={}
def collect(label,schedule):
 rows=[]
 for keys in schedule:tick(keys);rows.append(dict(keys=keys,**row()))
 results[label]=rows
 return rows
try:
 for j,entry in enumerate(steps[:-1]):
  if j in [9,11]:
   selected=cid if j==9 else 0
   for direction,count in [('DOWN',selected//3),('RIGHT',selected%3)]:
    for _ in range(count):
     for _ in range(4):tick([direction])
     for _ in range(16):tick()
  for _ in range(entry.get('frames',1)):tick([] if j==11 else entry.get('buttons',[]))
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(300):tick()
 baseline=snap()

 extras={}
 restore(baseline)
 rr=[]
 for a,b in [([],['A','B'])]*90+[([],['LEFT'])]*30:
  tick(a,b);rr.append(dict(p=st(P2),aura=rb(P2+0xbd)))
 assert next(i for i,t in enumerate(rr[:90]) if t['aura'])<=3
 assert next(i for i,t in enumerate(rr[90:]) if t['p']['action'] in [1,2])<=3
 extras['p2-charge']=rr
 restore(baseline)
 rr=[]
 for k in [['A','B']]*60+[['A','B','RIGHT']]*4+[['A','B','DOWN','RIGHT']]*4+[['A','B','DOWN']]*4+[['A','B','DOWN','LEFT']]*4+[['A','B','LEFT']]*4+[[]]*3+[['A']]*3+[[]]*180:
  tick([],k);rr.append(st(P2))
 assert any(t['program']==0xc04 for t in rr)
 extras['p2-mirrored-buffer']=rr
 restore(baseline)
 rr=collect('expired-buffer',[['A','B']]*60+[['A','B','LEFT']]*4+[['A','B','DOWN','LEFT']]*4+[['A','B','DOWN']]*4+[['A','B','DOWN','RIGHT']]*4+[['A','B','RIGHT']]*4+[[]]*40+[['A']]*3+[[]]*90)
 assert not any(t['p']['program']==0xc04 for t in rr[120:])
 assert rr[120]['ttl']==0
 extras['expired-buffer']=rr
 for label,guard in [('whiff',False),('guard',True)]:
  restore(baseline)
  if guard:ww(P1+0xa,300);ww(P2+0xa,332)
  rr=[]
  for f in range(65):
   tick(['A'] if f<3 else ['B'] if 13<=f<16 else [],['RIGHT'] if guard else [])
   rr.append(st(P1))
  assert not any(t['program']==0x403 for t in rr[:25])
  extras[label]=rr
 root.joinpath('extra-runtime.json').write_text(json.dumps(extras,indent=2));print('EXTRA_CHECKS_PASSED',list(extras),flush=True)
finally:core.retro_unload_game();core.retro_deinit()

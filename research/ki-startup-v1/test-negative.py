from pathlib import Path
import sys,json,hashlib
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
   selected=cid if j==9 else 0
   for direction,count in [('DOWN',selected//3),('RIGHT',selected%3)]:
    for _ in range(count):
     for _ in range(4):tick([direction])
     for _ in range(16):tick()
  for _ in range(entry.get('frames',1)):tick([] if j==11 else entry.get('buttons',[]))
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(300):tick()
 baseline=snap()

 for _ in range(2300):
  tick(['A','B'],['A','B'])
  if min(rw(P1+0x28),rw(P2+0x28))>=230:break
 for _ in range(70):tick()

 charged=snap();cases=[]
 hcf=[['LEFT'],['DOWN','LEFT'],['DOWN'],['DOWN','RIGHT'],['RIGHT']]
 specs=[('A-half',hcf,['A'],0xc04),('A-double',hcf*2,['A'],0xc05),('B-double',hcf*2,['B'],0x801),('AB-half',hcf,['A','B'],None),('AB-quarter',[['DOWN'],['DOWN','RIGHT'],['RIGHT']],['A','B'],None),('AB-neutral',[],['A','B'],None),('AB-invalid',[['LEFT'],['UP'],['RIGHT']],['A','B'],None)]
 for name,dirs,btn,expected in specs:
  restore(charged);seq=[k for k in dirs for _ in range(4)]+[(dirs[-1] if dirs else [])+btn]*6+[[]]*210;programs=[]
  for k in seq:tick(k);programs.append(rw(P1))
  good=(expected in programs) if expected else not any(p in programs for p in [0xc04,0xc05,0x83e])
  cases.append(dict(label=name,expected=expected,programs=sorted(set(programs)),passed=good))
 assert all(c['passed'] for c in cases),cases
 (root/'negative-checks.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),cases=cases),indent=2));print('NEGATIVE_CHECKS',len(cases),'passed',flush=True)
finally:core.retro_unload_game();core.retro_deinit()

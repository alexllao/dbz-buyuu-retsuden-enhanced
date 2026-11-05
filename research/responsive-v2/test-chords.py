from pathlib import Path
import sys,json
root=Path('work/input-v2');which=sys.argv[1] if len(sys.argv)>1 else 'after';cid=int(sys.argv[2]) if len(sys.argv)>2 else 0
rompath='work/input-v2/candidate.bin' if which=='after' else 'work/hits-hud-v3/candidate.bin'
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
 charged=snap();results=[]
 for port in [0,1]:
  for chord in [-2,-1,0,1,2]:
   restore(charged);dirs=[['LEFT'],['DOWN','LEFT'],['DOWN'],['DOWN','RIGHT'],['RIGHT']]*2
   if port:dirs=[[{'LEFT':'RIGHT','RIGHT':'LEFT'}.get(d,d) for d in k] for k in dirs]
   seq=[k for k in dirs for _ in range(3)];end=len(seq)
   seq += [seq[-1]]*8
   for i in range(end-1,len(seq)):
    if i>=end-1+max(0,-chord):seq[i]=seq[i]+['A']
    if i>=end-1+max(0,chord):seq[i]=seq[i]+['B']
   seq += [[]]*300;programs=[]
   for k in seq:
    tick([] if port else k,k if port else []);programs.append(rw(P2 if port else P1))
   results.append(dict(port=port,chordFrames=chord,programs=sorted(set(programs)),meteor=0x83e in programs))
 print('CHORDS',results,flush=True)
 (root/'chords.json').write_text(json.dumps(results,indent=2))
finally:core.retro_unload_game();core.retro_deinit()

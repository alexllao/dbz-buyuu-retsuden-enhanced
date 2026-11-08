from pathlib import Path
import sys,json
which=sys.argv[1];src=Path('work/input-v2/record.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0].replace("root=baseDir/'work/input-v2/video'/which","root=baseDir/'work/throw-links/video'/which").replace("rompath='work/input-v2/candidate.bin' if which=='after' else 'work/responsive-cancels-v1/candidate.bin'","rompath='work/throw-links/candidate.bin' if which=='after' else 'work/barrage-roster/candidate.bin'").replace("if which=='after':","if True:").replace('for _ in range(8):tick()','for _ in range(0):tick()').replace('keys=list(a)))','keys=list(a),defense=list(b)))')
sys.argv=['record',which];exec(compile(src,'throw-record','exec'),globals())
names=['Goku','Gohan','Piccolo','Vegeta','Trunks','Cell','A18','Krilin','Freezer','Recoome','Ginyu']
def take(cid,delay,label,guard=False):
 restore(Path(f'work/throw-links/seeds/{cid}.state').read_bytes());wb(P1+0xbe,0);wb(P2+0xbe,0)
 for b,x,facing in [(P1,300,0),(P2,332,1)]:ww(b+0xa,x);ww(b+0xc,0);wb(b+0x59,facing)
 for _ in range(8):tick()
 ready=snap();start(label,ready)
 def step(k=()):tick(k,['RIGHT' if rw(P2+0xa)>rw(P1+0xa) else 'LEFT'] if guard else [])
 for _ in range(3):step(['RIGHT','A'])
 assert rb(P1+0x5b)==0x3a
 for _ in range(180):
  if rb(P1+0x5b)<=8:break
  step()
 release=len(rows)-1
 for _ in range(delay):step()
 f='LEFT' if rb(P1+0x59) else 'RIGHT';b='RIGHT' if f=='LEFT' else 'LEFT';token=5 if cid==0 else 7 if cid==1 else 6
 dirs=[[b],['DOWN',b],['DOWN'],['DOWN',f],[f]] if cid==0 else [[b],['DOWN',b],['DOWN'],['DOWN',f],[f],[b]] if token==7 else [['DOWN'],['DOWN',b],[b],[f]]
 for k in [k for k in dirs for _ in range(4)]+[dirs[-1]+['A']]*4:step(k)
 for _ in range(420):step()
 finish();return dict(label=label,cid=cid,delay=delay,guard=guard,release=release)
try:
 takes=[]
 if which=='before':
  for cid in [0,7]:takes.append(take(cid,0,f'fix-{names[cid]}'))
 else:
  for cid,name in enumerate(names):
   delay=76 if cid==7 else json.loads(Path(f'work/throw-links/after/report-{cid}.json').read_text())['earliestUsefulDelay'];takes.append(take(cid,delay,f'link-{name}'))
  for cid in [0,1,3,7]:takes.append(take(cid,0,f'early-{names[cid]}'))
  takes.append(take(0,72,'guard-Goku-timed',True));takes.append(take(0,120,'guard-Goku-late',True))
 (root/'takes.json').write_text(json.dumps(takes,indent=2))
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()

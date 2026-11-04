from pathlib import Path
import sys,json,hashlib
ROOT=Path.cwd();source=sys.argv[1];cid=int(sys.argv[2]);port=1;turbo=False;out=ROOT/'work/generic-combos/native-regression'/str(cid);out.mkdir(parents=True,exist_ok=True)
s=Path('work/side-switch/test_commands.py').read_text().split('results=[]')[0];s=s[s.index('sys.path.insert'):];exec(compile(s,'kick-native-setup','exec'),globals())
def state(b):return {'program':rw(b),'action':rb(b+0x5b),'pose':rb(b+4),'cursor':rw(b+6),'hp':rw(b+0x24),'ki':rw(b+0x28),'x':rw(b+0xa),'y':rw(b+0x10),'attack':bool(rb(b+0x1e)&128),'kind':rb(b+0x7c),'flags':rw(b+0x1e)}
try:
 for index,step in enumerate(steps[:-1]):
  if index==9:
   for direction,count in [('DOWN',cid//3),('RIGHT',cid%3)]:
    for _ in range(count):
     for _ in range(4):tick([direction])
     for _ in range(16):tick()
  for _ in range(step.get('frames',1)):tick([] if index==11 else step.get('buttons',[]))
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(180):tick()
 ww(P1+0xa,300);ww(P2+0xa,332);ww(P1+0xc,0);ww(P2+0xc,0);wb(P1+0x59,0);wb(P2+0x59,1)
 for _ in range(3):tick()
 baseline=snap();results=[]
 cases={'normalB':[['B']]*2,'downB':[['DOWN']]*4+[['DOWN','B']]*2,'flurryB':[['LEFT']]*4+[['DOWN','LEFT']]*4+[['DOWN']]*4+[['DOWN','RIGHT']]*4+[['RIGHT']]*4+[['RIGHT','B']]*2,'quarterB':[['DOWN']]*4+[['DOWN','RIGHT']]*4+[['RIGHT']]*4+[['RIGHT','B']]*2}
 for name,seq in cases.items():
  restore(baseline);trace=[]
  for f in range(210):
   tick(seq[f] if f<len(seq) else []);trace.append({'f':f,'p':state(P1),'enemy':state(P2)})
   if f in [30,45,60]:save_image(out/f'{name}-{f}.png')
  hits=[t['f'] for i,t in enumerate(trace) if t['enemy']['hp']<(200 if not i else trace[i-1]['enemy']['hp'])];programs=sorted(set(t['p']['program'] for t in trace));changes=[(t['f'],t['p']['program'],t['p']['action'],t['p']['pose'],t['p']['kind']) for i,t in enumerate(trace) if not i or (t['p']['program'],t['p']['pose'])!=(trace[i-1]['p']['program'],trace[i-1]['p']['pose'])]
  print(cid,name,'hits',hits,'programs',programs,'changes',changes[:30],flush=True);results.append({'name':name,'hits':hits,'programs':programs,'trace':trace})
 (out/'report.json').write_text(json.dumps({'romSha256':hashlib.sha256(rom).hexdigest(),'cid':cid,'results':results},indent=2))
finally:core.retro_unload_game();core.retro_deinit()

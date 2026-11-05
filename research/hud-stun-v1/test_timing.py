from pathlib import Path
import sys,json,hashlib
ROOT=Path.cwd();source=sys.argv[1];cid=int(sys.argv[2]);tag=sys.argv[3];port=1;turbo=False;out=ROOT/'work/stun-hud/timing'/f'{tag}-{cid}';out.mkdir(parents=True,exist_ok=True)
s=Path('work/side-switch/test_commands.py').read_text().split('results=[]')[0];s=s[s.index('sys.path.insert'):];exec(compile(s,'timing-setup','exec'),globals())
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
 baseline=snap();results=[]
 for button in ['A','B']:
  restore(baseline);ww(P1+0xa,300);ww(P2+0xa,332);ww(P1+0xc,0);ww(P2+0xc,0);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(8):tick()
  trace=[]
  for f in range(180):
   tick([button] if f<6 else []);trace.append({'f':f,'program':rw(P1),'action':rb(P1+0x5b),'cursor':rw(P1+6),'pose':rb(P1+4)})
  started=next(t['f'] for t in trace if 0x400<=t['program']<0x800);program=trace[started]['program'];ended=next(t['f'] for t in trace[started+1:] if t['program']!=program);active=trace[started:ended];poses=[];cursors=[]
  for t in active:
   if not poses or t['pose']!=poses[-1]:poses.append(t['pose'])
   if not cursors or t['cursor']!=cursors[-1]:cursors.append(t['cursor'])
  results.append({'button':button,'program':program,'start':started,'end':ended,'activeFrames':ended-started,'poses':poses,'cursors':cursors,'trace':trace})
 (out/'report.json').write_text(json.dumps({'romSha256':hashlib.sha256(rom).hexdigest(),'cid':cid,'tag':tag,'results':results},indent=2),encoding='utf8')
finally:core.retro_unload_game();core.retro_deinit()

from pathlib import Path
import sys,json
ROOT=Path.cwd();source='work/rom/original.bin';cid=0;port=1;turbo=False;out=ROOT/'work/stun-review/runtime';out.mkdir(parents=True,exist_ok=True)
s=Path('work/side-switch/test_commands.py').read_text().split('results=[]')[0];s=s[s.index('sys.path.insert'):];exec(compile(s,'stun-runtime','exec'),globals())
def state(b):return {'program':rw(b),'action':rb(b+0x5b),'hp':rw(b+0x24),'ki':rw(b+0x28),'stun':rb(b+0x51),'threshold':rb(b+0x54),'timer36':rw(b+0x36),'timer38':rw(b+0x38),'cursor':rw(b+6),'x':rw(b+0xa),'kind':rb(b+0x7c)}
try:
 for index,step in enumerate(steps[:-1]):
  for _ in range(step.get('frames',1)):tick([] if index==11 else step.get('buttons',[]))
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(180):tick()
 ww(P1+0xa,300);ww(P2+0xa,332);ww(P1+0xc,0);ww(P2+0xc,0);wb(P1+0x59,0);wb(P2+0x59,1)
 for _ in range(8):tick()
 baseline=snap();first=[]
 for f in range(300):tick(['A'] if f<6 else []);first.append({'f':f,'p':state(P1),'enemy':state(P2)})
 restore(baseline);trace=[];pressed=0;attackUntil=-1;nextAttack=0;found=False
 for f in range(5000):
  p=state(P1);e=state(P2);keys=[]
  if f<attackUntil:keys=['A']
  elif p['action']<=8 and e['action']<=8 and f>=nextAttack:
   d=e['x']-p['x']
   if abs(d)>43:keys=['RIGHT' if d>0 else 'LEFT']
   else:keys=['A'];attackUntil=f+6;nextAttack=f+110
  tick(keys);trace.append({'f':f,'keys':keys,'p':state(P1),'enemy':state(P2)})
  if rb(P2+0x5b)==13 and rw(P2+0x36)>0:found=True;break
 (out/"precheck.json").write_text(json.dumps({"first":first,"trace":trace,"found":found},indent=2),encoding="utf8")
 assert found
 dizzy=snap();recovery=[]
 for mash in [False,True]:
  restore(dizzy);tr=[]
  for f in range(1200):
   tick([],(['LEFT' if (f//2)%2 else 'RIGHT'] if mash else []));tr.append({'f':f,'enemy':state(P2)})
   if not rw(P2+0x36) and not rb(P2+0x51):break
  recovery.append({'mashDirections':mash,'framesUntilReset':f+1,'trace':tr})
 report={'originalSha256':'217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557','fps':av.timing.fps,'fixture':'Original ROM, native inputs and timers; initial positions/facing fixed only, both control flags human. No HP/ki/stun/timer forcing.','singleHitWait':first,'untilDizzy':trace,'recovery':recovery};(out/'report.json').write_text(json.dumps(report,indent=2),encoding='utf8');print('singleStun',first[-1]['enemy']['stun'],'threshold',first[-1]['enemy']['threshold'],'dizzy',trace[-1]['enemy'],'recoveries',[(r['mashDirections'],r['framesUntilReset']) for r in recovery])
finally:core.retro_unload_game();core.retro_deinit()

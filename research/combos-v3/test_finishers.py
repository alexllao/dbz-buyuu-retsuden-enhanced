from pathlib import Path
import sys,json,hashlib
ROOT=Path.cwd();source=sys.argv[1];cid=int(sys.argv[2]);port=1;turbo=False
out=ROOT/'work/generic-combos/finishers'/str(cid);out.mkdir(parents=True,exist_ok=True)
s=Path('work/side-switch/test_commands.py').read_text().split('results=[]')[0];s=s[s.index('sys.path.insert'):];exec(compile(s,'finisher-setup','exec'),globals())
def state(b):return dict(program=rw(b),action=rb(b+0x5b),hp=rw(b+0x24),ki=rw(b+0x28),x=rw(b+0xa),combo=rb(b+0x106),window=rb(b+0x107),token=rb(b+0xb9),cursor=rw(b+6))
DIR={1:['UP'],2:['DOWN'],4:['LEFT'],8:['RIGHT'],6:['DOWN','LEFT'],10:['DOWN','RIGHT'],9:['UP','RIGHT']}
MOVES={'blast':([4,8],'A'),'downB':([8,2],'B'),'fbf':([8,4,8],'B'),'quarter':([2,10,8],'B'),'flurry':([4,6,2,10,8],'B'),'meteor19':([8,10,2,6,4,8],'B'),'meteor16':([4,6,2,10,8,4],'B'),'meteor1a':([2,10,8,4],'B')}
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
 baselines={False:snap()}
 for _ in range(240):tick(['A','B'])
 for _ in range(100):tick()
 baselines[True]=snap();results=[]
 for charged in [False,True]:
  for mode in MOVES:
   restore(baselines[charged]);ww(P1+0xa,300);ww(P2+0xa,332);ww(P1+0xc,0);ww(P2+0xc,0);wb(P1+0x59,0);wb(P2+0x59,1)
   for _ in range(3):tick()
   startKi=rw(P1+0x28);trace=[];hits=[];hp=rw(P2+0x24);dirs,button=MOVES[mode];seq=[DIR[d] for d in dirs for _ in range(4)]+[DIR[dirs[-1]]+[button]]*2;start=999
   for f in range(720):
    keys=[]
    if f<2:keys=['A']
    if hits and hits[0]+9<=f<hits[0]+11:keys=['B']
    if len(hits)>1 and hits[1]+9<=f<hits[1]+11:keys=['A']
    if len(hits)>=3 and start==999:start=hits[2]+2
    if start<=f<start+len(seq):keys=seq[f-start]
    # Attempt to recancel after finishing: budget must stay closed.
    if start+len(seq)+12<=f<start+len(seq)+24:keys=['A' if f%4==0 else 'B'] if f%2==0 else []
    tick(keys);p=state(P1);e=state(P2);trace.append({'f':f,'keys':keys,'p':p,'enemy':e,'scene':rb(0xe73c),'cinema':rw(0xe9c4)})
    if e['hp']<hp:hits.append(f)
    hp=e['hp']
   committed=any(t['p']['combo']&32 for t in trace);programs=sorted(set(t['p']['program'] for t in trace));summary={'mode':mode,'charged':charged,'startKi':startKi,'hits':hits,'programs':programs,'committed':committed,'minKi':min(t['p']['ki'] for t in trace),'idleAtEnd':trace[-1]['p']['action']==trace[-1]['enemy']['action']==0,'maxLinks':max(t['p']['combo']&3 for t in trace)}
   results.append({'summary':summary,'trace':trace});print(cid,json.dumps(summary),flush=True)
 (out/'report.json').write_text(json.dumps({'romSha256':hashlib.sha256(rom).hexdigest(),'cid':cid,'fixture':'Native commands, charge via A+B, only initial positions/facing fixed; no HP/ki/actions/timers forced','results':results},indent=2))
finally:core.retro_unload_game();core.retro_deinit()

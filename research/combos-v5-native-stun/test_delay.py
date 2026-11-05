from pathlib import Path
import sys,json,hashlib
ROOT=Path.cwd();source=sys.argv[1];cid=int(sys.argv[2]);port=int(sys.argv[3]);turbo='--turbo' in sys.argv
out=ROOT/'work/native-stun-fix/tests-delay9'/f'{hashlib.sha256(Path(source).read_bytes()).hexdigest()[:8]}-{cid}-p{port}-{int(turbo)}';out.mkdir(parents=True,exist_ok=True)
s=Path('work/side-switch/test_commands.py').read_text().split('results=[]')[0];s=s[s.index('sys.path.insert'):];exec(compile(s,'generic-setup','exec'),globals())
def state(b):return dict(program=rw(b),action=rb(b+0x5b),hp=rw(b+0x24),ki=rw(b+0x28),x=rw(b+0xa),combo=rb(b+0x106),window=rb(b+0x107),token=rb(b+0xb9),fatigue=rw(b+0x36),status=rw(b+0x38),held=rb(b+0x1b),pressed=rb(b+0x1d),queue=rw(b+0x109))
try:
 for index,step in enumerate(steps[:-1]):
  selected=cid if (index==9 and port==1) or (index==11 and port==2) else 0
  if index in [9,11]:
   for direction,count in [('DOWN',selected//3),('RIGHT',selected%3)]:
    for _ in range(count):
     for _ in range(4):tick([direction])
     for _ in range(16):tick()
  keys=step.get('buttons',[]) if index!=11 else []
  if boot_turbo and index<2:keys=list(set(keys+['A','B']))
  for _ in range(step.get('frames',1)):tick(keys)
 assert rb(moving+0x58)==cid
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(180):tick()
 baseline=snap();results=[]
 for reverse in [False,True]:
  for route in ['AAA','ABA','BAB','ABB','spam','guard','whiff','held']:
   if reverse and route not in ['AAA','ABA','BAB','ABB']:continue
   restore(baseline);dist=160 if route=='whiff' else 32
   ww(moving+0xa,300);ww(enemy+0xa,300-dist if reverse else 300+dist);ww(moving+0xc,0);ww(enemy+0xc,0);wb(moving+0x59,int(reverse));wb(enemy+0x59,int(not reverse))
   for _ in range(3):press()
   trace=[];hitFrames=[];previousHP=rw(enemy+0x24);startHP=previousHP
   for f in range(300):
    keys=[]
    sequence=route if route in ['AAA','ABA','BAB','ABB'] else 'AAA'
    if f<6:keys=[sequence[0]]
    if hitFrames:
     t=hitFrames[0]+9
     if t<=f<t+2:keys=[sequence[1]]
    if len(hitFrames)>1:
     t=hitFrames[1]+9
     if t<=f<t+2:keys=[sequence[2]]
    # Intenta un cuarto y repite hasta recuperar: no debe reiniciar el presupuesto.
    if len(hitFrames)>2 and hitFrames[2]+3<=f<hitFrames[2]+5:keys=['A']
    if route=='spam' and f>=12:keys=['A' if (f//2)%2 else 'B'] if f%2==0 else []
    if route=='held' and f>=12:keys=['A']
    press(keys,(['LEFT' if reverse else 'RIGHT'] if route=='guard' else []))
    tr={'f':f,'keys':keys,'p':state(moving),'enemy':state(enemy)};trace.append(tr)
    if tr['enemy']['hp']<previousHP:hitFrames.append(f)
    previousHP=tr['enemy']['hp']
   # Group actual HP drops by native recovery opportunity.
   groups=[]
   for h in hitFrames:
    if not groups or any(trace[t]['enemy']['action']<=8 for t in range(groups[-1][-1]+1,h)):groups.append([h])
    else:groups[-1].append(h)
   stages=[(t['p']['combo']&3) for t in trace];summ={'route':route,'reverse':reverse,'hits':hitFrames,'groups':groups,'maxLinks':max(stages),'programs':sorted(set(t['p']['program'] for t in trace)),'idleAtEnd':trace[-1]['p']['action']==trace[-1]['enemy']['action']==0}
   checks={'maxTwoLinks':max(stages)<=2,'noMoreThanThreeBasicsPerRecovery':all(len(g)<=3 for g in groups)}
   if route in ['guard','whiff']:checks['noCancel']=max(stages)==0
   if turbo:checks['turboUnchanged']=max(stages)==0
   results.append({'summary':summ,'checks':checks,'trace':trace});print(json.dumps({'cid':cid,'port':port,**summ,'checks':checks}),flush=True)
 report={'romSha256':hashlib.sha256(rom).hexdigest(),'cid':cid,'port':port,'turbo':turbo,'passed':all(all(r['checks'].values()) for r in results),'fixture':'Native menus and button inputs; only initial positions/facing fixed, no HP/ki/action/timer forcing','results':results}
 (out/'report.json').write_text(json.dumps(report,indent=2));assert report['passed']
finally:core.retro_unload_game();core.retro_deinit()

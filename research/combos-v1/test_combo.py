from pathlib import Path
import sys,json,hashlib
import itertools
ROOT=Path.cwd();source=sys.argv[1];cid=int(sys.argv[2]);port=int(sys.argv[3]) if len(sys.argv)>3 else 1;turbo='--turbo' in sys.argv
setup=Path('work/side-switch/test_commands.py').read_text().split('results=[]')[0]
setup=setup[setup.index('sys.path.insert'):]
out=ROOT/'work/combos/tests'/f'{hashlib.sha256(Path(source).read_bytes()).hexdigest()[:8]}-{cid}-p{port}-{int(turbo)}';out.mkdir(parents=True,exist_ok=True)
exec(compile(setup,'combo-native-setup','exec'),globals())
def state(b):return {'program':rw(b),'action':rb(b+0x5b),'hp':rw(b+0x24),'ki':rw(b+0x28),'x':rw(b+0xa),'facing':rb(b+0x59),'pose':rb(b+4),'attack':bool(rb(b+0x1e)&128),'tail':bytes(rb(b+i) for i in range(0x104,0x108)).hex(),'cursor':rw(b+6),'token':rb(b+0xb9),'stage':rb(b+0x106)&3,'window':rb(b+0x107),'flags':rw(b+0x1e)}
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
  for mode in ['chain','whiff','guard','unsupported-kick','held-button','spam','spam-defend','no-finisher']:
   if reverse and mode!='chain':continue
   for second,finisherDelay in (list(itertools.product([2,4,6],[0,3,6])) if mode=='chain' else [(16,0)]):
    restore(baseline);distance=160 if mode=='whiff' else 32;left=300
    ww(moving+0xa,left);ww(enemy+0xa,left-distance if reverse else left+distance);ww(moving+0xc,0);ww(enemy+0xc,0);wb(moving+0x59,int(reverse));wb(enemy+0x59,int(not reverse))
    for _ in range(3):press()
    initial=[state(moving),state(enemy)];f='LEFT' if reverse else 'RIGHT';b='RIGHT' if reverse else 'LEFT';trace=[]
    hitFrames=[];previousHP=initial[1]['hp']
    for t in range(160):
     secondAt=(hitFrames[0]+second) if mode=='chain' and hitFrames else (999 if mode=='chain' else second)
     finishAt=(hitFrames[1]+finisherDelay) if mode=='chain' and len(hitFrames)>1 else secondAt+18
     keys=[]
     if t<2:keys=['A']
     if secondAt<=t<secondAt+2:keys=['B' if mode=='unsupported-kick' else 'A']
     if mode=='held-button' and t>=secondAt:keys=['A']
     if mode in ['spam','spam-defend'] and t>=secondAt:keys=['A' if (t//2)%2 else 'B'] if t%2==0 else []
     if mode not in ['held-button','spam','spam-defend','unsupported-kick','no-finisher']:
      if finishAt<=t<finishAt+4:keys=[b]
      if finishAt+4<=t<finishAt+6:keys=[f]
      if finishAt+6<=t<finishAt+8:keys=[f,'A']
     defend=mode=='guard' or (mode=='spam-defend' and len(hitFrames)>=2)
     press(keys,(['LEFT' if reverse else 'RIGHT'] if defend else []));trace.append({'f':t,'p':state(moving),'enemy':state(enemy)})
     hp=trace[-1]['enemy']['hp']
     if hp<previousHP:hitFrames.append(t)
     previousHP=hp
    hits=[x['f'] for i,x in enumerate(trace) if x['enemy']['hp']<(initial[1]['hp'] if not i else trace[i-1]['enemy']['hp'])]
    stages=sorted(set(x['p']['stage'] for x in trace));actions=sorted(set(x['p']['action'] for x in trace));programs=sorted(set(x['p']['program'] for x in trace));summary={'mode':mode,'reverse':reverse,'second':second,'hits':hits,'stages':stages,'actions':actions,'programs':programs,'kiBefore':initial[0]['ki'],'kiMin':min(x['p']['ki'] for x in trace),'idleAtEnd':trace[-1]['p']['action']==0}
    summary['finisherDelay']=finisherDelay
    results.append({'summary':summary,'initial':initial,'trace':trace});print(json.dumps(summary),flush=True)
 report={'sourceSha256':hashlib.sha256(rom).hexdigest(),'cid':cid,'port':port,'turbo':turbo,'fixture':'Native menus, real command inputs; positions/facing fixed only; no HP, ki, action or timer forcing','results':results}
 (out/'report.json').write_text(json.dumps(report,indent=2));print('SAVED',out,flush=True)
finally:core.retro_unload_game();core.retro_deinit()

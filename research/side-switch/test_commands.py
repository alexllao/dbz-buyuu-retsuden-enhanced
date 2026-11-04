from pathlib import Path
import sys,json,hashlib,subprocess
ROOT=Path.cwd();args=list(sys.argv[1:]);source=args[0];cid=int(args[1]);port=int(args[2]);turbo='--turbo' in args
out=ROOT/'work/side-switch/tests'/f'{hashlib.sha256(Path(source).read_bytes()).hexdigest()[:8]}-{cid:02}-p{port}-{int(turbo)}'
out.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'work'));sys.argv=['probe','--native','--rom',source,'--out',str(out)]+(['--turbo'] if turbo else [])
header=(ROOT/'work/gameplay_probe.py').read_text().split('try:\n for index,step in enumerate(steps[:-1]):')[0].replace('BASE=Path(__file__).resolve().parent.parent','BASE=Path.cwd()')
exec(compile(header,'side-command-test-setup','exec'),globals())
moving=P1 if port==1 else P2;enemy=P2 if port==1 else P1
def st(b):return dict(program=rw(b),action=rb(b+0x5b),pose=rb(b+4),x=rw(b+0xa),y=rw(b+0x10),facing=rb(b+0x59),hp=rw(b+0x24),attack=bool(rb(b+0x1e)&128),plane=bool(rb(b+0x1e)&16),magic=rb(b+0x108),held=rb(b+0x1b),pressed=rb(b+0x1d))
def press(keys=(),other=()):tick(keys,other) if port==1 else tick(other,keys)
results=[]
try:
 for index,step in enumerate(steps[:-1]):
  selected=cid if (index==9 and port==1) or (index==11 and port==2) else 0
  if index in [9,11]:
   for direction,count in [('DOWN',selected//3),('RIGHT',selected%3)]:
    for _ in range(count):
     for _ in range(4):tick([direction])
     for _ in range(16):tick()
   # Character select uses port one for both cursors in these native menus.
   if index==11:
    pass
  keys=step.get('buttons',[])
  if index==11:keys=[]
  if boot_turbo and index<2:keys=list(set(keys+['A','B']))
  for _ in range(step.get('frames',1)):tick(keys)
 # The selector for P2 is also operated by port one: handle separately below if needed.
 assert rb(moving+0x58)==cid,(port,cid,rb(moving+0x58))
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(180):tick()
 baseline=snap()
 for reverse in [False,True]:
  for air in [False,True]:
   for mode in ['new','held-C','C-only','FB-C','FBF-A','FBF-B','FBF-AC','far','simultaneous-FC','timeout','followup-punch']:
    if mode not in ['new','held-C'] and (reverse or air):continue
    restore(baseline);distance=160 if mode=='far' else 64
    ww(moving+0xa,300 if reverse else 200);ww(moving+0xc,0);wb(moving+0x59,1 if reverse else 0)
    ww(enemy+0xa,(300-distance) if reverse else (200+distance));ww(enemy+0xc,0);wb(enemy+0x59,0 if reverse else 1)
    for _ in range(3):press()
    if air:
     for _ in range(12):press(['UP'],['UP'])
    initial=[st(moving),st(enemy)];f='LEFT' if reverse else 'RIGHT';b='RIGHT' if reverse else 'LEFT'
    prefix=[[f]]*4+[[b]]*4+[[f]]*4
    if mode=='C-only':schedule=[['C']]*4+[[]]*116
    elif mode=='FB-C':schedule=[[f]]*4+[[b]]*4+[['C']]*4+[[]]*108
    elif mode=='timeout':schedule=[[f]]*4+[[b]]*4+[[]]*36+[[f]]*4+[['C']]*4+[[]]*68
    elif mode=='held-C':schedule=prefix+[['C']]*100+[[]]*48
    elif mode=='followup-punch':schedule=prefix+[['C']]*45+[['A','C']]*2+[['C']]*30+[[]]*33
    elif mode=='simultaneous-FC':schedule=[[f]]*4+[[b]]*4+[[f,'C']]*4+[[]]*108
    else:
     terminal=['A'] if mode=='FBF-A' else ['B'] if mode=='FBF-B' else ['A','C'] if mode=='FBF-AC' else ['C']
     schedule=prefix+[terminal]*4+[[]]*104
    trace=[]
    for frame,keys in enumerate(schedule):
     press(keys);trace.append({'frame':frame,'p':st(moving),'enemy':st(enemy)})
    activated=any(x['p']['program']==0x843 for x in trace)
    expected=mode in ['new','held-C','simultaneous-FC','followup-punch']
    # FBF+B is already the same native move for these three characters.
    if mode=='FBF-B' and cid in [0,1,5]:expected=cid==1
    checks={'activation':activated==expected}
    if mode in ['new','held-C','simultaneous-FC','followup-punch']:
     checks.update(zeroDamage=all(x['enemy']['hp']==initial[1]['hp'] for x in (trace[:57] if mode=='followup-punch' else trace)),crossed=(trace[-1]['p']['x']-trace[-1]['enemy']['x'])*(initial[0]['x']-initial[1]['x'])<0,returnedIdle=trace[-1]['p']['action']==0,latchReleased=trace[-1]['p']['magic']==0xc7)
     if mode!='followup-punch':checks['noAttack']=all(not x['p']['attack'] for x in trace)
     if mode=='held-C':checks['noFlightWhileHolding']=all(x['p']['plane']==initial[0]['plane'] for x in trace)
     if mode=='followup-punch':checks['followupAttackRecognized']=any(0x20<=x['p']['action']<=0x27 for x in trace[57:])
    results.append({'mode':mode,'reverse':reverse,'air':air,'initial':initial,'checks':checks,'passed':all(checks.values()),'programs':sorted({x['p']['program'] for x in trace}),'trace':trace})
 report={'romSha256':hashlib.sha256(rom).hexdigest(),'cid':cid,'port':port,'turbo':turbo,'fixture':'Native menus, both human; test position/facing only; air via native UP12; actual direction/button inputs, no program/HP/timer forcing','results':results}
 (out/'report.json').write_text(json.dumps(report,indent=2))
 print(json.dumps({'cid':cid,'port':port,'turbo':turbo,'cases':len(results),'failed':[{k:r[k] for k in ['mode','reverse','air','checks','programs']} for r in results if not r['passed']]}),flush=True)
finally:core.retro_unload_game();core.retro_deinit()

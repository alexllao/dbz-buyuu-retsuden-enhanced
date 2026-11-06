from pathlib import Path
import json,sys,hashlib
src=Path('work/responsive-v3/probe-chain.py').read_text().split('try:\n routeRoot=')[0].replace('work/responsive-v3/candidate.bin','work/ki-startup/candidate.bin')
sys.argv=['probe','after','0'];exec(compile(src,'cross-probe-setup','exec'),globals());root=Path('work/fast-cross');root.mkdir(exist_ok=True)
try:
 seed=Path('work/ki-startup/routes/0/charged.state').read_bytes();reports=[]
 for n in [1,2,3]:
  for waitBoth in [False,True]:
   restore(seed);ww(P1+0xa,300);ww(P2+0xa,332);wb(P1+0x59,0);wb(P2+0x59,1)
   for _ in range(8):tick()
   rr=[]
   def step(a=(),b=()):tick(a,b);rr.append(dict(p=st(P1),e=st(P2),keys=list(a),keys2=list(b)))
   for i in range(3):
    actor=P1 if i%2==0 else P2
    for _ in range(100):
     if rb(actor+0x5b)<=8 and (not waitBoth or (rw(P1)!=0x843 and rw(P2)!=0x843)):break
     step()
    f='LEFT' if rb(actor+0x59) else 'RIGHT';b='RIGHT' if f=='LEFT' else 'LEFT'
    for k in [[f]]*n+[[b]]*n+[[f,'C']]*n:step(k if actor==P1 else [],k if actor==P2 else [])
    step()
   for _ in range(100):
    if rw(P1)!=0x843 and rw(P2)!=0x843 and rb(P1+0x5b)<=8:break
    step()
   crossEnd=len(rr);f='LEFT' if rb(P1+0x59) else 'RIGHT';b='RIGHT' if f=='LEFT' else 'LEFT'
   for k in [[b],['DOWN',b],['DOWN'],['DOWN',f],[f]]*2:step(k)
   for _ in range(4):step([f,'A','B'])
   for _ in range(350):step()
   starts={k:[i for i,t in enumerate(rr) if t[k]['program']==0x843 and (i==0 or rr[i-1][k]['program']!=0x843)] for k in ['p','e']}
   report=dict(directionFrames=n,waitBoth=waitBoth,crossStarts=starts,crossEnd=crossEnd,meteor=any(t['p']['program']==0x83e for t in rr),maxHits=max(t['p']['hits'] for t in rr),damage=rr[0]['e']['hp']-rr[-1]['e']['hp']);reports.append(report)
   (root/f'probe-{n}-{int(waitBoth)}.json').write_text(json.dumps(dict(summary=report,trace=rr)));print(report,flush=True)
 (root/'reports.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),reports=reports),indent=2))
finally:core.retro_unload_game();core.retro_deinit()

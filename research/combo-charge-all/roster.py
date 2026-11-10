from pathlib import Path
import sys,json
audit_variant=sys.argv[1];audit_port=int(sys.argv[2]);setup=Path('work/combo-charge-all/runtime.py').read_text();exec(compile(setup,'roster-charge-runtime','exec'),globals());results=[]
actor,enemy=(P1,P2) if audit_port==1 else (P2,P1);slot=0xf7b2 if audit_port==1 else 0xf7b6
commands=json.loads(Path('repository/research/combos-v3/native-commands.json').read_text())
try:
 for cid in range(11):
  token=5 if cid==0 else 7 if cid==1 else 6;expected=next(v['program'] for v in commands[str(cid)] if v['token']==token)
  for side in [0,1]:
   for context in ['solo','combo']:
    path=S/'states/normal'/f'seed-{cid}.state' if audit_port==1 else S/'states-p2/normal'/str(cid)/'seed-0.state'
    restore(path.read_bytes());ww(actor+10,300 if side==0 else 332);ww(enemy+10,332 if side==0 else 300);wb(actor+0x59,side);wb(enemy+0x59,1-side)
    for _ in range(8):rawtick()
    trace=[];hp=rw(enemy+0x24);initialHP=hp;contacts=[]
    def step(k=()):
     global hp
     rawtick(k if audit_port==1 else [],k if audit_port==2 else []);now=rw(enemy+0x24)
     if now<hp:contacts.append(len(trace))
     hp=now;trace.append(dict(f=len(trace),p=st(actor),e=st(enemy),fast=rb(slot),pose=rb(actor+4),clock=rw(actor+6),types=[rb(actor+0xe2+i*30) for i in range(3)]))
    if context=='combo':
     pattern='A' if cid in [2,6,8] else 'AAB'
     for frame in range(150):
      k=[pattern[0]] if frame<3 else []
      for i,t in enumerate(contacts[:len(pattern)-1]):
       if t+3<=frame<t+6:k=[pattern[i+1]]
      step(k)
      if len(contacts)>=len(pattern):break
    for _ in range(3):step()
    f='LEFT' if side else 'RIGHT';b='RIGHT' if side else 'LEFT'
    dirs=[[b],['DOWN',b],['DOWN'],['DOWN',f],[f]] if cid==0 else [[b],['DOWN',b],['DOWN'],['DOWN',f],[f],[b]] if cid==1 else [['DOWN'],['DOWN',b],[b],[f]]
    for k in [k for k in dirs for _ in range(4)]+[dirs[-1]+['A']]*4:step(k)
    for _ in range(480):step()
    accepted=next((t['f'] for t in trace if t['p']['program']==expected),None);launch=next((t['f'] for t in trace if accepted is not None and t['f']>=accepted and any(t['types'])),None)
    result=dict(cid=cid,port=audit_port,side=side,context=context,program=expected,accepted=accepted,launch=launch,startup=launch-accepted if launch is not None else None,fast=any(t['fast']&2 for t in trace),damage=initialHP-hp,contacts=contacts,hits=max(t['p']['hits'] for t in trace),idle=trace[-1]['p']['program']==0)
    if context=='solo':assert not result['fast'],result
    results.append(result)
    if side==0:(S/f'roster-{audit_variant}-p{audit_port}-{cid}-{context}.json').write_text(json.dumps(trace))
  print(audit_variant,'port',audit_port,'cid',cid,[(r['context'],r['startup'],r['damage'],r['fast']) for r in results[-4:]],flush=True)
 (S/f'roster-{audit_variant}-p{audit_port}.json').write_text(json.dumps(results,indent=2))
finally:core.retro_unload_game();core.retro_deinit()

from pathlib import Path
import json,sys,hashlib
audit_variant=sys.argv[1];S=Path('work/combo-startup/matrix');S.mkdir(exist_ok=True);src=Path('work/basic-chains/probe.py').read_text().split('try:\n for pattern')[0];matrix_rom='work/input-links/candidate.bin' if audit_variant=='before' else 'work/combo-startup/candidate.bin';src=src.replace('work/basic-chains/candidate.bin',matrix_rom);sys.argv=['probe','after'];exec(compile(src,'startup-matrix-header','exec'),globals());results=[]
try:
 for cid,expected in [(1,0xc0f),(3,0xc27)]:
  for audit_port in [0,1]:
   actor,enemy=(P1,P2) if audit_port==0 else (P2,P1);latch=0xf7b0+audit_port*4
   for audit_side in [0,1]:
    for context in ['solo','hit-A','hit-AAB','guard','whiff','late','guard-after-third']:
     for speed in [3,4,5]:
      seed=Path(f'work/throw-links/seeds/{cid}.state' if audit_port==0 else f'work/throw-links/seeds-p2/{cid}.state');restore(seed.read_bytes());wb(P1+0xbe,0);wb(P2+0xbe,0)
      distance=180 if context=='whiff' else 32;ww(actor+0xa,300 if audit_side==0 else 300+distance);ww(enemy+0xa,300+distance if audit_side==0 else 300);wb(actor+0x59,audit_side);wb(enemy+0x59,1-audit_side)
      for at in range(0xf7b0,0xf7b8):wb(at,0)
      for _ in range(8):tick()
      r=[];contacts=[];hp=rw(enemy+0x24)
      def step(k=()):
       global hp
       defense=['RIGHT' if audit_side==0 else 'LEFT'] if context=='guard' or context=='guard-after-third' and len(contacts)>=3 else []
       tick(k if audit_port==0 else defense,defense if audit_port==0 else k);now=rw(enemy+0x24)
       if now<hp:contacts.append(len(r))
       hp=now;r.append(dict(f=len(r),p=st(actor),e=st(enemy),fast=rb(latch+2),pose=rb(actor+4),types=[rb(actor+0xe2+i*30) for i in range(3)]))
      pattern='A' if context=='hit-A' else 'AAB'
      if context!='solo':
       for f in range(100):
        k=[pattern[0]] if f<3 else []
        if context in ['guard','whiff']:k=['A'] if f<3 or 25<=f<28 else ['B'] if 50<=f<53 else []
        else:
         for i,t in enumerate(contacts[:len(pattern)-1]):
          if t+3<=f<t+6:k=[pattern[i+1]]
        step(k)
        if context not in ['guard','whiff'] and len(contacts)>=len(pattern):break
      basics=len(contacts)
      for _ in range(90 if context=='late' else 3):step()
      dirs=[['LEFT'],['DOWN','LEFT'],['DOWN'],['DOWN','RIGHT'],['RIGHT'],['LEFT']] if cid==1 else [['DOWN'],['DOWN','LEFT'],['LEFT'],['RIGHT']]
      if audit_side:dirs=[[{'LEFT':'RIGHT','RIGHT':'LEFT'}.get(v,v) for v in k] for k in dirs]
      for k in [k for k in dirs for _ in range(speed)]+[dirs[-1]+['A']]*4:step(k)
      for _ in range(280):step()
      accepted=next((t['f'] for t in r if t['p']['program']==expected),None);spawn=next((t['f'] for t in r if accepted is not None and t['f']>=accepted and any(x>=32 for x in t['types'])),None)
      result=dict(cid=cid,port=audit_port+1,side=audit_side,context=context,speed=speed,basicContacts=basics,accepted=accepted,firstProjectile=spawn,startup=spawn-accepted if spawn is not None else None,fastUsed=any(t['fast'] for t in r),damage=r[0]['e']['hp']-hp,maxHits=max(t['p']['hits'] for t in r),kiDebits=sum(max(0,a['p']['ki']-b['p']['ki']) for a,b in zip(r,r[1:])),returnedToIdle=r[-1]['p']['program']==0)
      if context in ['solo','guard','whiff','late']:assert not result['fastUsed'],result
      assert result['returnedToIdle'],result
      results.append(result)
      if speed==4 and context in ['solo','hit-AAB','guard-after-third']:(S/f'{audit_variant}-{cid}-{audit_port}-{audit_side}-{context}.json').write_text(json.dumps(r))
    print(audit_variant,cid,'port',audit_port+1,'side',audit_side,'done',len(results),flush=True)
 (S/f'{audit_variant}.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(Path(matrix_rom).read_bytes()).hexdigest(),cases=results),indent=2))
finally:core.retro_unload_game();core.retro_deinit()

from pathlib import Path
import sys,json,hashlib
startup_variant=sys.argv[1];S=Path('work/combo-startup');src=Path('work/basic-chains/probe.py').read_text().split('try:\n for pattern')[0];startup_rom='work/input-links/candidate.bin' if startup_variant=='before' else 'work/combo-startup/candidate.bin';src=src.replace('work/basic-chains/candidate.bin',startup_rom);sys.argv=['probe','after'];exec(compile(src,'combo-startup-probe','exec'),globals());results=[]
try:
 for cid,expected in [(1,0xc0f),(3,0xc27)]:
  for context in ['solo','A','AAB']:
   restore(Path(f'work/throw-links/seeds/{cid}.state').read_bytes());wb(P1+0xbe,0);wb(P2+0xbe,0);ww(P1+0xa,300);ww(P2+0xa,332);wb(P1+0x59,0);wb(P2+0x59,1)
   for at in range(0xf7b0,0xf7b8):wb(at,0)
   for _ in range(8):tick()
   r=[];contacts=[];hp=rw(P2+0x24)
   def step(k=()):
    global hp
    tick(k);now=rw(P2+0x24)
    if now<hp:contacts.append(len(r))
    hp=now;r.append(dict(f=len(r),keys=list(k),p=st(P1),e=st(P2),pose=rb(P1+4),phase=rb(0xe9b6),types=[rb(P1+0xe2+i*30) for i in range(3)],projX=[rw(P1+0xe2+i*30+6) for i in range(3)],fast=rb(0xf7b2),basicWindow=rb(0xf7b3),cachedProgram=rw(0xf7b0)))
   if context!='solo':
    for f in range(110):
     k=[context[0]] if f<3 else []
     for i,t in enumerate(contacts[:len(context)-1]):
      if t+3<=f<t+6:k=[context[i+1]]
     step(k)
     if len(contacts)>=len(context):break
   for _ in range(3):step()
   dirs=[['LEFT'],['DOWN','LEFT'],['DOWN'],['DOWN','RIGHT'],['RIGHT'],['LEFT']] if cid==1 else [['DOWN'],['DOWN','LEFT'],['LEFT'],['RIGHT']]
   for k in [k for k in dirs for _ in range(4)]+[dirs[-1]+['A']]*4:step(k)
   for _ in range(260):step()
   accepted=next((t['f'] for t in r if t['p']['program']==expected),None);spawn=next((t['f'] for t in r if accepted is not None and t['f']>=accepted and any(x>=32 for x in t['types'])),None)
   result=dict(cid=cid,context=context,accepted=accepted,firstProjectile=spawn,startup=spawn-accepted if spawn is not None else None,fastUsed=any(t['fast'] for t in r),damage=200-hp,maxHits=max(t['p']['hits'] for t in r),programs=sorted(set(t['p']['program'] for t in r)));results.append(result);(S/f'{startup_variant}-{cid}-{context}.json').write_text(json.dumps(r));print(startup_variant,result,flush=True)
 (S/f'{startup_variant}-probe.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(Path(startup_rom).read_bytes()).hexdigest(),cases=results),indent=2))
finally:core.retro_unload_game();core.retro_deinit()

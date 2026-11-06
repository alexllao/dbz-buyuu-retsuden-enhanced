from pathlib import Path
import sys,json,hashlib
src=Path('work/responsive-v3/test-super-hold.py').read_text().split('try:\n route=')[0].replace('work/responsive-v3/candidate.bin','work/responsive-v3/candidate.bin')
sys.argv=['test','after','0'];exec(compile(src,'ki-test-setup','exec'),globals())
try:
 cases=[]
 for cid in [0,1]:
  saved=Path(f'work/ki-startup/routes/{cid}/charged.state').read_bytes()
  for facing in [0,1]:
   for distance in [64,280]:
    for guard in [False,True]:
     restore(saved);ww(P1+0xa,300+distance if facing else 300);ww(P2+0xa,300 if facing else 300+distance);wb(P1+0x59,facing);wb(P2+0x59,1-facing)
     f='LEFT' if facing else 'RIGHT';b='RIGHT' if facing else 'LEFT'
     for _ in range(8):tick([],[f] if guard else [])
     hp=rw(P2+0x24);ki=rw(P1+0x28);rr=[];dirs=[[b],['DOWN',b],['DOWN'],['DOWN',f],[f]]+([[b]] if cid==1 else [])
     for k in [k for k in dirs for _ in range(4)]+[dirs[-1]+['A']]*4+[[]]*300:
      tick(k,[f] if guard else []);rr.append(dict(p=st(P1),e=st(P2),proj=rb(P1+0xe2)))
     expected=0xc04 if cid==0 else 0xc0f;start=next(i for i,t in enumerate(rr) if t['p']['program']==expected);emit=next(i for i,t in enumerate(rr) if t['proj'])
     result=dict(cid=cid,facing=facing,distance=distance,guard=guard,emissionFrames=emit-start,damage=hp-rw(P2+0x24),netKiDrop=ki-min(t['p']['ki'] for t in rr),techniqueDebit=max(a['p']['ki']-b['p']['ki'] for a,b in zip(rr,rr[1:])),finalProgram=rw(P1));cases.append(result)
     assert result['emissionFrames']<120 and result['finalProgram']<0x400,result
     if distance==64:assert result['damage']>0,result
 for i in range(0,len(cases),2):
  if cases[i]['distance']==64:assert cases[i+1]['damage']<cases[i]['damage'],cases[i:i+2]
 report=dict(passed=True,romSha256=hashlib.sha256(rom).hexdigest(),cases=cases);Path('work/ki-startup/technique-before.json').write_text(json.dumps(report,indent=2));print('TECHNIQUE_TESTS',len(cases),'passed',flush=True)
finally:core.retro_unload_game();core.retro_deinit()

from pathlib import Path
import sys,json
src=Path('work/barrage-five/probe.py').read_text().split('try:\n restore(')[0];sys.argv=['energy','after'];exec(compile(src,'energy-header','exec'),globals());out=[]
try:
 for energy,held in [(20,False),(60,False),(100,False),(180,False),(240,True)]:
  restore(Path('work/responsive-v3/routes/0/charged.state').read_bytes());ww(P1+0xa,300);ww(P2+0xa,420);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(15):tick()
  ww(P1+0x28,energy);seq=[['DOWN']]*4+[['DOWN','RIGHT']]*4+[['RIGHT']]*4+[['RIGHT','A']]*3+([['A']]*400 if held else [[]]*400);shots=[];last=rb(P1+0x3a)
  for f,k in enumerate(seq):
   tick(k);now=rb(P1+0x3a)
   if now>last:shots.append(dict(frame=f,number=now,ki=rw(P1+0x28)))
   last=now
  assert len(shots) in [0,5],(energy,held,shots)
  if energy==240:assert len(shots)==5
  out.append(dict(initialKi=energy,heldAAfterCommand=held,shots=shots,endingKi=rw(P1+0x28)))
 (Path('work/barrage-five')/'energy.json').write_text(json.dumps(dict(passed=True,cases=out),indent=2));print(out)
finally:core.retro_unload_game();core.retro_deinit()

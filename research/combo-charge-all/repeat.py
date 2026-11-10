from pathlib import Path
import sys,json
sys.argv=['repeat','after']
exec(compile(Path('work/combo-charge-all/runtime.py').read_text(),'charge-repeat-runtime','exec'),globals())
results=[]
try:
 for cid in range(11):
  restore((S/'states/normal'/f'seed-{cid}.state').read_bytes());ww(P1+10,300);ww(P2+10,332);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(8):rawtick()
  rows=[];chain('A' if cid in [2,6,8] else 'AAB');idle(3)
  def cast():
   f,b=face();dirs=[[b],['DOWN',b],['DOWN'],['DOWN',f],[f]] if cid==0 else [[b],['DOWN',b],['DOWN'],['DOWN',f],[f],[b]] if cid==1 else [['DOWN'],['DOWN',b],[b],[f]]
   command(dirs,['A'],4);idle(600)
  cast();first=any(t['fast']&2 for t in rows);assert first,cid
  # Un rival mareado mantiene abierto el combo de forma intencionada.
  # Esperar a que acabe tambien ese estado antes de llamar "suelto" al siguiente.
  for _ in range(3000):
   if rb(P1+0xd22)==0 and rb(P1+0xd24)==0 and rb(P2+0x5b)<=8:break
   tick()
  assert rb(P1+0xd22)==0,(cid,st(P2))
  assert rw(P1)==0
  ww(P1+10,300);ww(P2+10,332);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(8):rawtick()
  rows=[];cast();assert not any(t['fast']&2 for t in rows),cid
  assert any(t['p']['program']>=0xc00 for t in rows),cid
  results.append(dict(cid=cid,comboFast=first,nextSoloFast=False,returnedToIdle=rw(P1)==0))
 (S/'repeat.json').write_text(json.dumps(results,indent=2));print('PASS repeated cast',len(results))
finally:core.retro_unload_game();core.retro_deinit()

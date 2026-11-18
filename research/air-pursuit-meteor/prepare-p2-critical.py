from pathlib import Path
import sys,json,hashlib
setup=Path('work/combo-charge-all/runtime.py').read_text().replace('work/combo-charge-all/candidate.bin','work/air-pursuit-fall/candidate.bin')
sys.argv=['prepare','after'];exec(compile(setup,'meteor-p2-prepare','exec'),globals())
O=Path('work/air-pursuit-fall/states-p2');O.mkdir(exist_ok=True)
try:
 restore(Path('work/combo-charge-all/states-p2/normal/3/seed-0.state').read_bytes())
 for attempt in range(40):
  if rw(P2+0x24)<=50:break
  ww(P1+10,300);ww(P2+10,332);ww(P1+12,0);ww(P2+12,0);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(8):rawtick()
  for _ in range(3):rawtick(['A'])
  for _ in range(150):rawtick()
 assert 0<rw(P2+0x24)<=50,st(P2)
 for _ in range(600):rawtick()
 for _ in range(2400):
  if rw(P2+0x28)>=237:break
  rawtick([],['A','B'])
 for _ in range(90):rawtick()
 assert rw(P2)==0 and rw(P1)==0,(st(P1),st(P2))
 (O/'critical-3.state').write_bytes(snap())
 (O/'preparation.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),p2=st(P2),method='P2 critical HP obtained through native P1 punches; KI through native charge. Position/facing fixture between punches only; no HP or KI writes.'),indent=2))
 print(st(P2),flush=True)
finally:core.retro_unload_game();core.retro_deinit()


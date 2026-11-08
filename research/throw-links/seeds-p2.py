from pathlib import Path
import sys
s=Path('work/throw-links/audit.py').read_text().split('try:\n for cid in requested:')[0];sys.argv=['audit','0'];exec(compile(s,'throw-seed-p2','exec'),globals())
try:
 for cid in range(11):
  target=Path(f'work/throw-links/seeds-p2/{cid}.state');target.parent.mkdir(exist_ok=True);old=Path(f'work/barrage-roster/seeds/{cid}-1.state')
  if old.exists():target.write_bytes(old.read_bytes());continue
  core.retro_reset();boot_versus(globals(),0 if cid else 3,cid);wb(P1+0xbe,0);wb(P2+0xbe,0)
  for _ in range(3000):
   tick([],['A','B'])
   if rw(P2+0x28)>=240:break
  for _ in range(100):tick()
  target.write_bytes(snap());print('P2 seed',cid,flush=True)
finally:core.retro_unload_game();core.retro_deinit()

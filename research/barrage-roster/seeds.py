from pathlib import Path
import sys,json
P=Path('work/barrage-roster');src=Path('work/hits-hud-v3/prepare.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0].replace("romfile=BASE/'work/hits-hud-v3/candidate.bin'","romfile=BASE/'work/knockdown-k4/candidate.bin'");sys.argv=['prepare','0'];exec(compile(src,'seed-setup','exec'),globals());sys.path.insert(0,str(Path('work/cpu-soak').resolve()));from menu_ai_setup import boot_versus
try:
 for cid in [0,3,5,6,7,9]:
  for port in [0,1]:
   core.retro_reset();other=3 if cid==0 else 0;boot_versus(globals(),cid if port==0 else other,other if port==0 else cid);wb(P1+0xbe,0);wb(P2+0xbe,0)
   for _ in range(3000):
    tick(['A','B'],['A','B'])
    if min(rw(P1+0x28),rw(P2+0x28))>=240:break
   for _ in range(100):tick()
   out=P/f'seeds/{cid}-{port}.state';out.parent.mkdir(exist_ok=True);out.write_bytes(snap());print(cid,port,[rb(P1+0x58),rb(P2+0x58)],[rw(P1+0x24),rw(P2+0x24)],[rw(P1+0x28),rw(P2+0x28)],flush=True)
finally:core.retro_unload_game();core.retro_deinit()

from pathlib import Path
import sys,json,hashlib,subprocess,struct
N=Path('work/namek-simulation');N.mkdir(exist_ok=True)
s=Path('work/hits-hud-v3/prepare.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0].replace("romfile=BASE/'work/hits-hud-v3/candidate.bin'","romfile=BASE/'work/combo-startup/candidate.bin'")
for old in [0x104,0x106,0x117,0x120,0x121,0x122,0x124]:s=s.replace('b+'+hex(old)+')','b+'+hex(old+0xc00)+')')
sys.argv=['prepare','0'];exec(compile(s,'namek-simulation-runtime','exec'),globals())

def boot_stage(cid,enemy):
 core.retro_reset()
 for j,entry in enumerate(steps[:-1]):
  if j in [9,11]:
   selected=cid if j==9 else enemy
   for direction,count in [('DOWN',selected//3),('RIGHT',selected%3)]:
    for _ in range(count):
     for _ in range(4):tick([direction])
     for _ in range(16):tick()
  if j==13:wb(0xe741,6)
  for _ in range(entry.get('frames',1)):tick([] if j==11 else entry.get('buttons',[]))
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(180):tick()
 assert [rb(P1+0x58),rb(P2+0x58),rb(0xe741)]==[cid,enemy,6]
 for _ in range(2400):
  tick(['A','B'],['A','B'])
  if min(rw(P1+0x28),rw(P2+0x28))>=237:break
 for _ in range(90):tick()

def fixture(distance=32):
 ww(P1+0xa,300);ww(P2+0xa,300+distance);ww(P1+0xc,0);ww(P2+0xc,0);wb(P1+0x59,0);wb(P2+0x59,1)
 for _ in range(8):tick()

def prepare_seed(cid,enemy):
 path=N/f'seed-{cid}.state'
 if not path.exists():
  boot_stage(cid,enemy);fixture();path.write_bytes(snap())
 if cid in [3,5] and not (N/f'critical-{cid}.state').exists():
  restore(path.read_bytes());fixture()
  for attempt in range(30):
   if rw(P1+0x24)<=50:break
   fixture()
   for _ in range(3):tick([],['A'])
   for _ in range(100):tick()
  assert 0<rw(P1+0x24)<=50,(cid,rw(P1+0x24))
  for _ in range(360):tick()
  (N/f'critical-{cid}.state').write_bytes(snap())

if __name__=='__main__':
 try:
  for cid,enemy in [(0,8),(1,0),(3,0),(5,0)]:prepare_seed(cid,enemy);print('SEED',cid,flush=True)
  restore((N/'seed-0.state').read_bytes());fixture();save_image(N/'ground-reference.png');(N/'ground.state').write_bytes(snap());print('STATE',len(snap()),flush=True)
 finally:core.retro_unload_game();core.retro_deinit()

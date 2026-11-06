from pathlib import Path
import sys,json,hashlib
src=Path('work/responsive-v3/probe-chain.py').read_text(encoding='utf8').split('try:\n routeRoot=')[0]
sys.argv=['test','after','0'];exec(compile(src,'poll-setup','exec'),globals())
try:
 restore(Path('work/responsive-v3/routes/0/charged.state').read_bytes());ww(P1+0xa,300);ww(P2+0xa,332);wb(P1+0x59,0);wb(P2+0x59,1)
 for _ in range(8):tick()
 hp=rw(P2+0x24)
 for f in range(80):
  tick(['A'] if f<3 else [])
  if rw(P2+0x24)<hp:break
 assert rw(0x5002)>0,'native post-impact poll timer not active'
 tick();impact=snap();cases=[]
 for port in [0,1]:
  for delay in range(4):
   restore(impact)
   for _ in range(delay):tick()
   before=rw(0x5002);tick(['C'] if port==0 else [],['C'] if port==1 else [])
   raw=rb(0xe666+port*2);cases.append(dict(port=port+1,delay=delay,nativeTimer=before,rawPad=raw,passed=raw!=0))
 assert all(c['passed'] and c['nativeTimer']>0 for c in cases),cases
 # Charge and movement while the other actor is still falling.
 restore(Path('work/responsive-v3/routes/0/charged.state').read_bytes());ww(P1+0xa,300);ww(P2+0xa,332);wb(P1+0x59,0);wb(P2+0x59,1)
 for _ in range(8):tick()
 for _ in range(3):tick(['RIGHT','A'])
 assert rb(P1+0x5b)==0x3a
 for _ in range(180):
  if rb(P1+0x5b)<=8:break
  tick()
 thrown=rb(P2+0x5b)==0x17
 actions=[]
 for _ in range(8):tick(['A','B']);actions.append(rb(P1+0x5b))
 charge=0x0f in actions
 movement=[]
 for _ in range(12):tick(['LEFT']);movement.append(rb(P1+0x5b))
 released=any(a in [1,2] for a in movement)
 assert thrown and charge and released,(thrown,actions,movement)
 result=dict(romSha256=hashlib.sha256(rom).hexdigest(),passed=True,singleFrameSamples=cases,postThrowCharge=charge,chargeReleaseMovement=released)
 Path('work/responsive-v3/poll-validation.json').write_text(json.dumps(result,indent=2));print(result,flush=True)
finally:core.retro_unload_game();core.retro_deinit()

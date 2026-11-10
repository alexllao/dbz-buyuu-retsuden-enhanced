from pathlib import Path
import sys,json,hashlib
s=Path('work/gameplay_probe.py').read_text().split('try:\n for index,step in enumerate(steps[:-1]):')[0].replace('BASE=Path(__file__).resolve().parent.parent','BASE=Path.cwd()');sys.argv=['probe','--rom','work/menu-japanese/candidate.bin'];exec(compile(s,'mode-validation-runtime','exec'),globals())
O=Path('work/menu-japanese');evidence=[]
def press(k,n=3,k2=()):
 for _ in range(n):tick(k,k2)
 for _ in range(20):tick()
def current():return dict(state=rw(0xe6a4),phase=rw(0xe750),row=rw(0xe9f6),physical=rb(0xe741),variant=rb(0xf7c0),mode=rw(0xe9e8),types=[rb(P1+0xbe),rb(P2+0xbe)],hp=[rw(P1+0x24),rw(P2+0x24)],nativeAction=[rb(P1+0x5b),rb(P2+0x5b)])
try:
 for nativeMode in [0,1,2]:
  core.retro_reset()
  for entry in steps[:7]:
   for _ in range(entry.get('frames',1)):tick(entry.get('buttons',[]))
  for _ in range(nativeMode):press(['RIGHT'])
  press(['C'])
  for f in range(2400):
   if rw(0xe6a4)==0x20 and rw(0xe750)==3:break
   tick(['C'] if f%120<3 else [],['C'] if nativeMode==1 and f%120<3 else [])
  assert rw(0xe6a4)==0x20 and rw(0xe750)==3,current()
  press(['DOWN']);assert rw(0xe9f6)==1
  press(['B'])
  for _ in range(100):tick()
  before=current();assert before['physical']==6 and before['variant']==3,before
  save_image(O/f'mode{nativeMode}-selected.png');(O/f'mode{nativeMode}-selected.state').write_bytes(snap())
  press(['START'])
  for f in range(1200):tick(['C'] if f%120<3 else [],['C'] if nativeMode==1 and f%120<3 else [])
  after=current();save_image(O/f'mode{nativeMode}-playing.png');(O/f'mode{nativeMode}-playing.state').write_bytes(snap());print('MODE VERIFIED',nativeMode,before,after,flush=True)
  assert after['physical']==6 and after['variant']==3,after
  evidence.append(dict(nativeMode=nativeMode,selected=before,playing=after,fixtureWrites=[]))
 (O/'validation-modes.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),cases=evidence),indent=2))
finally:core.retro_unload_game();core.retro_deinit()

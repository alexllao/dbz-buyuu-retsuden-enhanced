from pathlib import Path
import sys,json,hashlib
s=Path('work/gameplay_probe.py').read_text().split('try:\n for index,step in enumerate(steps[:-1]):')[0].replace('BASE=Path(__file__).resolve().parent.parent','BASE=Path.cwd()');sys.argv=['probe','--rom','work/namek-native/integrated.bin'];exec(compile(s,'mode-validation-runtime','exec'),globals())
O=Path('work/namek-native');evidence=[]
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
  baseline=snap()
  for variant in [1,2,3]:
   restore(baseline);press(['DOWN']);assert rw(0xe9f6)==1
   for _ in range(4-variant):
    press(['B'])
    for _ in range(100):tick()
   before=current();assert before['physical']==6 and before['variant']==variant,before
   press(['START'])
   for f in range(800):tick(['C'] if f%120<3 else [],['C'] if nativeMode==1 and f%120<3 else [])
   after=current();assert after['physical']==6 and after['variant']==variant and after['state']==12,after
   data=snap();vo=0x12425;vram=data[vo:vo+0x5c00];linear=bytearray(len(vram));linear[0::2]=vram[1::2];linear[1::2]=vram[0::2];slug={1:'normal',2:'aldea',3:'porunga'}[variant];expected=(O/slug/'tiles.bin').read_bytes();assert linear==expected[:0x5c00]
   evidence.append(dict(nativeMode=nativeMode,variant=variant,selected=before,playing=after,backgroundVRAMExact=True,fixtureWrites=[]));print('MATRIX PASS',nativeMode,variant,flush=True)
 (O/'matrix-modes-variants.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),cases=evidence),indent=2))
finally:core.retro_unload_game();core.retro_deinit()

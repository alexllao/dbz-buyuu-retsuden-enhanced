from pathlib import Path
import json,hashlib
exec(compile(Path('work/menu-japanese/capture.py').read_text().split('\ntry:')[0],'native-menu-validation','exec'),globals())
P=Path('work/menu-japanese');checks=[]
try:
 restore((menuOut/'normal.state').read_bytes());cycle=[]
 for i in range(12):
  press(['B'],3,120);virtual=rb(0xe741) if rb(0xf7c0)==0 else 8+rb(0xf7c0)
  assert virtual==(8-i)%12,(i,virtual)
  cycle.append(dict(step=i+1,virtual=virtual,stage=rb(0xe741),variant=rb(0xf7c0)))
 assert cycle[-1]['virtual']==9
 for slug,variant in [('normal',1),('aldea',2),('porunga',3)]:
  restore((menuOut/(slug+'.state')).read_bytes());press(['START'],3,20)
  for f in range(1200):tick(['C'] if f%120<3 else [])
  assert rb(0xe741)==6 and rb(0xf7c0)==variant
  assert rw(P1+0x24)>0 and rw(P2+0x24)>0
  save_image(menuOut/(slug+'-combate.png'))
  checks.append(dict(variant=slug,stage=rb(0xe741),variantId=rb(0xf7c0),hp=[rw(P1+0x24),rw(P2+0x24)],phase=rw(0xe6a4)))
 (P/'validation.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),cycle=cycle,combat=checks,fixture='Native button input and restoration of menu states produced with this exact build. No RAM writes.'),indent=2))
 print('PASS:12 stage choices, full wrap, three combat entries')
finally:core.retro_unload_game();core.retro_deinit()

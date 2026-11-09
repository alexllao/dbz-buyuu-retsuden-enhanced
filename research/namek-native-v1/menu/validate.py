from pathlib import Path
import sys,json
s=Path('work/gameplay_probe.py').read_text().split('try:\n for index,step in enumerate(steps[:-1]):')[0].replace('BASE=Path(__file__).resolve().parent.parent','BASE=Path.cwd()');sys.argv=['probe','--rom','work/namek-menu/candidate.bin'];exec(compile(s,'menu-validation-runtime','exec'),globals())
O=Path('work/namek-menu');rows=[]
def note(label):
 d=dict(label=label,state=rw(0xe6a4),phase=rw(0xe750),stage=rb(0xe741),variant=rb(0xf7c0),row=rw(0xe9f6),control=[rb(P1+0xbe),rb(P2+0xbe)]);rows.append(d);print(d,flush=True);return d
try:
 core.retro_reset()
 for entry in steps[:17]:
  for _ in range(entry.get('frames',1)):tick(entry.get('buttons',[]))
 note('parameters');save_image(O/'parameters-original.png');baseline=snap();(O/'parameters.state').write_bytes(baseline)
 restore(baseline)
 for _ in range(3):tick(['DOWN'])
 for _ in range(30):tick()
 note('stage-row')
 for i in range(1,5):
  for _ in range(3):tick(['B'])
  for _ in range(100):tick()
  d=note('previous-'+str(i));save_image(O/f'selector-prev-{i}.png');(O/f'selector-prev-{i}.state').write_bytes(snap())
  if i<=3:
   selected=snap()
   for _ in range(3):tick(['START'])
   for _ in range(240):tick()
   note('fight-'+str(i));save_image(O/f'fight-prev-{i}.png');(O/f'fight-prev-{i}.state').write_bytes(snap());restore(selected)
 (O/'validation-menu.json').write_text(json.dumps(rows,indent=2))
finally:core.retro_unload_game();core.retro_deinit()

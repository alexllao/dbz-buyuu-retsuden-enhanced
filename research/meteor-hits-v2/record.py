from pathlib import Path
import sys,json
src=Path('work/input-v2/record.py').read_text(encoding='utf8').split('try:\n for j,entry in enumerate(steps[:-1]):')[0]
src=src.replace("root=baseDir/'work/input-v2/video'/which","root=baseDir/'work/meteor-hits/comparison'/which").replace("rompath='work/input-v2/candidate.bin' if which=='after' else 'work/responsive-cancels-v1/candidate.bin'","rompath='work/meteor-hits/candidate.bin'").replace("if which=='after':","if True:")
sys.argv=['record','after'];exec(compile(src,'fixed-meteor-record','exec'),globals())
try:
 for cid,name in [(7,'Krilin'),(8,'Freezer'),(6,'A18'),(4,'Trunks')]:
  start(name,Path(f'work/presentation-full/routes/{cid}/charged.state').read_bytes(),True)
  for _ in range(12):tick()
  hcf=[['LEFT'],['DOWN','LEFT'],['DOWN'],['DOWN','RIGHT'],['RIGHT']];hcb=[['RIGHT'],['DOWN','RIGHT'],['DOWN'],['DOWN','LEFT'],['LEFT']];dirs=hcb+[['RIGHT']] if cid in [4,7] else hcf+[['LEFT']];seq=[k for k in dirs for _ in range(3)]+[dirs[-1]+['B']]*4
  for k in seq+[[]]*(520-12-len(seq)):tick(k)
  finish()
 for label,fixture in [('Cell13',Path('work/piccolo-hits/routes/5/low-hp.state').read_bytes()),('Cell11',Path('work/meteor-hits/cell-ko-seed.state').read_bytes())]:
  start(label,fixture,label!='Cell11')
  for _ in range(12):tick()
  seq=[k for k in [['DOWN'],['DOWN','RIGHT'],['RIGHT'],['LEFT']] for _ in range(3)]+[['LEFT','B']]*4
  for k in seq+[[]]*(1030-12-len(seq)):tick(k)
  finish()
 (root/'chapters.json').write_text(json.dumps(chapters,indent=2))
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()

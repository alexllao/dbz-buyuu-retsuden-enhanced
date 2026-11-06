from pathlib import Path
import sys,json
which=sys.argv[1]
src=Path('work/input-v2/record.py').read_text(encoding='utf8').split('try:\n for j,entry in enumerate(steps[:-1]):')[0]
src=src.replace("root=baseDir/'work/input-v2/video'/which","root=baseDir/'work/gravity-g2/comparison'/which")
src=src.replace("rompath='work/input-v2/candidate.bin' if which=='after' else 'work/responsive-cancels-v1/candidate.bin'","rompath='work/gravity-g2/candidate.bin' if which=='after' else 'work/gravity-probe/dash-fix.bin'").replace("if which=='after':","if True:")
sys.argv=['record',which];exec(compile(src,'goku-g2-record','exec'),globals())
try:
 for mode in ['normal','diagonal','carrera']:
  start(mode,Path('work/gravity-probe/seed-0.state').read_bytes())
  for _ in range(12):tick()
  if mode=='carrera':
   for k in [['RIGHT']]*4+[[]]*4+[['RIGHT']]*12:tick(k)
  for k in ([['UP']]*3 if mode=='normal' else [['UP','RIGHT']]*3)+[[]]*105:tick(k)
  finish()
 (root/'chapters.json').write_text(json.dumps(chapters,indent=2))
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()

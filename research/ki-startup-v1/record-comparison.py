from pathlib import Path
import sys,json
kind=sys.argv[1]
src=Path('work/input-v2/record.py').read_text(encoding='utf8').split('try:\n for j,entry in enumerate(steps[:-1]):')[0]
src=src.replace("root=baseDir/'work/input-v2/video'/which","root=baseDir/'work/ki-startup/comparison'/which")
src=src.replace("rompath='work/input-v2/candidate.bin' if which=='after' else 'work/responsive-cancels-v1/candidate.bin'","rompath='work/ki-startup/candidate.bin' if which=='after' else 'work/responsive-v3/candidate.bin'")
src=src.replace("if which=='after':","if True:")
sys.argv=['record',kind];exec(compile(src,'comparison-runtime','exec'),globals())
try:
 for cid,label in [(0,'Kamehameha'),(1,'Masenko')]:
  start(label,Path(f'work/ki-startup/routes/{cid}/charged.state').read_bytes(),True);ww(P2+0xa,364)
  for _ in range(15):tick()
  dirs=[['LEFT'],['DOWN','LEFT'],['DOWN'],['DOWN','RIGHT'],['RIGHT']]+([['LEFT']] if cid==1 else [])
  for k in [k for k in dirs for _ in range(4)]+[dirs[-1]+['A']]*4+[[]]*255:tick(k)
  finish()
 (root/'chapters.json').write_text(json.dumps(chapters,indent=2))
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()

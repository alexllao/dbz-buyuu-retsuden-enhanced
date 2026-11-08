from pathlib import Path
import sys,json
variant=sys.argv[1];src=Path('work/input-v2/record.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0].replace("root=baseDir/'work/input-v2/video'/which","root=baseDir/'work/jump-two/video'/which").replace("rompath='work/input-v2/candidate.bin' if which=='after' else 'work/responsive-cancels-v1/candidate.bin'",f"rompath='work/jump-two/{variant}.bin'").replace("if which=='after':","if True:").replace('keys=list(a)))','keys=list(a),flags=rw(P1+0x20)))')
sys.argv=['record',variant];exec(compile(src,'jump-record','exec'),globals())
try:
 for mode in ['vertical','diagonal','carrera','carrera-patada']:
  start(mode,Path('work/barrage-roster/seeds/0-0.state').read_bytes());wb(P1+0xbe,0);wb(P2+0xbe,0);ww(P1+0xa,100);ww(P1+0xc,0);ww(P2+0xa,280);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(20):tick()
  seq=[]
  if mode.startswith('carrera'):seq += [['RIGHT']]*4+[[]]*4+[['RIGHT']]*12
  seq += ([['UP']]*3 if mode=='vertical' else [['UP','RIGHT']]*3)
  if mode=='carrera-patada':seq += [[]]*6+[['B']]*3
  for k in seq+[[]]*110:tick(k)
  finish()
 (root/'chapters.json').write_text(json.dumps(chapters,indent=2))
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()

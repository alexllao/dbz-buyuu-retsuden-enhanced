from pathlib import Path
import sys,json
which=sys.argv[1];src=Path('work/input-v2/record.py').read_text(encoding='utf8').split('try:\n for j,entry in enumerate(steps[:-1]):')[0]
src=src.replace("root=baseDir/'work/input-v2/video'/which","root=baseDir/'work/barrage-roster/video'/which").replace("rompath='work/input-v2/candidate.bin' if which=='after' else 'work/responsive-cancels-v1/candidate.bin'","rompath='work/barrage-roster/candidate.bin' if which=='after' else 'work/knockdown-k4/candidate.bin'").replace("if which=='after':","if True:").replace('keys=list(a)))','keys=list(a),shot=rb(P1+0x3a),cost=rw(P1+0xe0)))')
sys.argv=['record',which];exec(compile(src,'roster-record','exec'),globals())
try:
 for cid,name in [(0,'Goku'),(3,'Vegeta'),(5,'Cell'),(6,'A18'),(7,'Krilin'),(9,'Recoome')]:
  start(name,Path(f'work/barrage-roster/seeds/{cid}-0.state').read_bytes());wb(P1+0xbe,0);wb(P2+0xbe,0)
  for b,x,facevalue in [(P1,300,0),(P2,420,1)]:ww(b+0xa,x);ww(b+0xc,0);wb(b+0x59,facevalue)
  for _ in range(15):tick()
  seq=([['DOWN']]*4+[['DOWN','RIGHT']]*4+[['RIGHT']]*4+[['RIGHT','A']]*3) if cid==0 else ([['DOWN']]*110+[['DOWN','LEFT']]*4+[['LEFT']]*4+[['LEFT','A']]*4)
  for k in seq+[[]]*400:tick(k)
  finish()
 (root/'chapters.json').write_text(json.dumps(chapters,indent=2))
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()

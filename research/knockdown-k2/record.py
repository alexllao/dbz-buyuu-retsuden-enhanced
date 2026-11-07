from pathlib import Path
import sys,json
which=sys.argv[1];src=Path('work/input-v2/record.py').read_text(encoding='utf8').split('try:\n for j,entry in enumerate(steps[:-1]):')[0]
src=src.replace("root=baseDir/'work/input-v2/video'/which","root=baseDir/'work/knockdown-k2/comparison'/which").replace("rompath='work/input-v2/candidate.bin' if which=='after' else 'work/responsive-cancels-v1/candidate.bin'","rompath='work/knockdown-k2/candidate.bin' if which=='after' else 'work/knockdown-k1/candidate.bin'").replace("if which=='after':","if True:").replace('for _ in range(8):tick()','for _ in range(0):tick()').replace('keys=list(a)))','keys=list(a),keys2=list(b)))')
sys.argv=['record',which];exec(compile(src,'knockdown-record','exec'),globals());sys.path.insert(0,str(Path('work/cpu-soak').resolve()));from menu_ai_setup import boot_versus
try:
 for cid,name in [(0,'Goku'),(4,'Trunks'),(2,'Piccolo'),(5,'Cell'),(9,'Recoome')]:
  seedPath=Path(f'work/knockdown-k2/seeds/{cid}.state')
  if which=='before':
   core.retro_reset();boot_versus(globals(),0,cid);wb(P1+0xbe,0);wb(P2+0xbe,0)
   for b,x,facing in [(P1,300,0),(P2,348,1)]:ww(b+0xa,x);ww(b+0xc,0);wb(b+0x59,facing)
   for _ in range(3):tick()
   for _ in range(20):tick(['DOWN'])
   seedPath.parent.mkdir(parents=True,exist_ok=True);seedPath.write_bytes(snap())
  start(name,seedPath.read_bytes())
  for f in range(230):tick(['DOWN','B'] if f<2 else [],['LEFT'] if f>=20 else [])
  finish()
 (root/'chapters.json').write_text(json.dumps(chapters,indent=2))
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()

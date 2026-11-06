from pathlib import Path
import sys,json
which=sys.argv[1]
src=Path('work/input-v2/record.py').read_text(encoding='utf8').split('try:\n for j,entry in enumerate(steps[:-1]):')[0]
src=src.replace("root=baseDir/'work/input-v2/video'/which","root=baseDir/'work/meteor-impact/comparison'/which").replace("rompath='work/input-v2/candidate.bin' if which=='after' else 'work/responsive-cancels-v1/candidate.bin'","rompath='work/meteor-impact/candidate.bin' if which=='after' else 'work/gohan-hits/candidate.bin'").replace("if which=='after':","if True:")
src=src.replace("rows.append(dict(p=st(P1),e=st(P2),keys=list(a)))", "rows.append(dict(p=st(P1),e=st(P2),keys=list(a),events=rw(0xf768),dx=rw(0xf766),force=rb(0xf763)))")
sys.argv=['record',which];exec(compile(src,'impact-record','exec'),globals())
names=['Goku','Gohan','Piccolo','Vegeta','Trunks','Cell','A18','Krilin','Freezer','Recoome'];lengths=[520,520,520,520,520,1050,520,520,520,520]
try:
 for cid,name in enumerate(names):
  folder='piccolo-hits' if cid in [0,1,2,3,5] else 'presentation-full';state='low-hp.state' if cid in [3,5] else 'charged.state';start(name,Path(f'work/{folder}/routes/{cid}/{state}').read_bytes(),True)
  for _ in range(12):tick()
  hcf=[['LEFT'],['DOWN','LEFT'],['DOWN'],['DOWN','RIGHT'],['RIGHT']];hcb=[['RIGHT'],['DOWN','RIGHT'],['DOWN'],['DOWN','LEFT'],['LEFT']]
  dirs=hcf*2 if cid==0 else [['DOWN'],['DOWN','RIGHT'],['RIGHT'],['LEFT']] if cid==5 else hcb+[['RIGHT']] if cid in [1,3,4,7,9] else hcf+[['LEFT']];btn=['A','B'] if cid==0 else ['B']
  seq=[k for k in dirs for _ in range(3)]+[dirs[-1]+btn]*4
  for k in seq+[[]]*(lengths[cid]-len(seq)-12):tick(k)
  finish()
 (root/'chapters.json').write_text(json.dumps(chapters,indent=2))
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()

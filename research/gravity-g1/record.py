from pathlib import Path
import sys,json
kind=sys.argv[1]
src=Path('work/input-v2/record.py').read_text(encoding='utf8').split('try:\n for j,entry in enumerate(steps[:-1]):')[0]
src=src.replace("root=baseDir/'work/input-v2/video'/which","root=baseDir/'work/gravity-probe/comparison'/which")
src=src.replace("rompath='work/input-v2/candidate.bin' if which=='after' else 'work/responsive-cancels-v1/candidate.bin'","rompath='work/gravity-probe/gravity-g1.bin' if which=='after' else 'work/gravity-probe/dash-fix.bin'")
src=src.replace("if which=='after':","if True:")
sys.argv=['record',kind];exec(compile(src,'gravity-record','exec'),globals())
names=['Goku','Gohan','Piccolo','Vegeta','Trunks','Cell','A18','Krilin','Freezer','Recoome','Ginyu']
try:
 for cid,name in enumerate(names):
  seed=Path(f'work/gravity-probe/seed-{cid}.state').read_bytes()
  for mode in ['normal','carrera']:
   start(name+' '+mode,seed)
   for _ in range(12):tick()
   if mode=='carrera':
    for k in [['RIGHT']]*4+[[]]*4+[['RIGHT']]*12:tick(k)
   for k in ([['UP','RIGHT']]*3 if mode=='carrera' else [['UP']]*3)+[[]]*87:tick(k)
   finish()
 start('Piccolo Meteor',Path('work/piccolo-hits/routes/2/charged.state').read_bytes(),True)
 for _ in range(15):tick()
 dirs=[['LEFT'],['DOWN','LEFT'],['DOWN'],['DOWN','RIGHT'],['RIGHT'],['LEFT']]
 for k in [k for k in dirs for _ in range(4)]+[dirs[-1]+['B']]*4+[[]]*420:tick(k)
 finish()
 (root/'chapters.json').write_text(json.dumps(chapters,indent=2))
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()

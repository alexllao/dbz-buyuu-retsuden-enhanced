from pathlib import Path
import sys,json
which=sys.argv[1];src=Path('work/input-v2/record.py').read_text(encoding='utf8').split('try:\n for j,entry in enumerate(steps[:-1]):')[0]
src=src.replace("root=baseDir/'work/input-v2/video'/which","root=baseDir/'work/barrage-five/video'/which").replace("rompath='work/input-v2/candidate.bin' if which=='after' else 'work/responsive-cancels-v1/candidate.bin'","rompath='work/barrage-five/candidate.bin' if which=='after' else 'work/knockdown-k4/candidate.bin'").replace("if which=='after':","if True:").replace('keys=list(a)))','keys=list(a),keys2=list(b),shot=rb(P1+0x3a)))')
sys.argv=['record',which];exec(compile(src,'barrage-record','exec'),globals())
def idle(n,guard=False):
 for _ in range(n):tick([],['RIGHT'] if guard else [])
def command(guard=False):
 for k in [['DOWN']]*4+[['DOWN','RIGHT']]*4+[['RIGHT']]*4+[['RIGHT','A']]*3:tick(k,['RIGHT'] if guard else [])
try:
 for label,guard in [('01 cinco impactos',False),('02 contra guardia',True)]:
  start(label,Path('work/responsive-v3/routes/0/charged.state').read_bytes());wb(P1+0xbe,0);wb(P2+0xbe,0)
  for b,x,facevalue in [(P1,300,0),(P2,420,1)]:ww(b+0xa,x);ww(b+0xc,0);wb(b+0x59,facevalue)
  idle(20,guard);command(guard);idle(285,guard);finish()
 start('03 lanzamiento y rafaga',Path('work/responsive-v3/routes/0/charged.state').read_bytes(),True);wb(P1+0xbe,0);wb(P2+0xbe,0);idle(15)
 for _ in range(3):tick(['RIGHT','A'])
 assert rb(P1+0x5b)==0x3a
 for _ in range(180):
  if rb(P1+0x5b)<=8:break
  tick()
 idle(48);command();idle(360);finish()
 (root/'chapters.json').write_text(json.dumps(chapters,indent=2))
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()

from pathlib import Path
import sys,json,hashlib
side=sys.argv[1];s=Path('work/gravity-probe/baseline.py').read_text().split('try:\n for j,entry')[0].replace("rompath='work/gohan-hits/candidate.bin' if which=='after' else 'work/gohan-hits/candidate.bin'", "rompath='work/meteor-impact/candidate.bin'" if side=='after' else "rompath='work/gohan-hits/candidate.bin'");sys.argv=['probe','after','2'];exec(compile(s,'hud-qa','exec'),globals());P=Path('work/meteor-impact');rr=[]
try:
 restore(Path('work/piccolo-hits/routes/2/charged.state').read_bytes());ww(P1+0xa,300);ww(P2+0xa,332);wb(P1+0x59,0);wb(P2+0x59,1)
 for _ in range(8):tick()
 dirs=[['LEFT'],['DOWN','LEFT'],['DOWN'],['DOWN','RIGHT'],['RIGHT'],['LEFT']]
 for i,k in enumerate([k for k in dirs for _ in range(3)]+[dirs[-1]+['B']]*4+[[]]*600):
  tick(k);w,h,pitch,data=latest

  if i in [38,39,40,41,42,43,44,45,46,67,68,69,70,71,72,73,74,75,76,216,217,218,219,220,221,222,223,224,225,226,227,228,229,91,200,212,215]:
   subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb565le','-video_size','320x224','-i','pipe:0','-frames:v','1',str(P/f'qa-{side}-{i}.png')],input=b''.join(data[y*pitch:y*pitch+w*2] for y in range(h)),check=True)
  keyState=[]
  for a in [P1,P2]:keyState += [rw(a+x) for x in [0,4,6,10,16,22,24,36,40]]+[rb(a+0xd20)]
  keyState += [rw(a) for a in [0xc034,0xc036,0xc038,0xc03a]]
  rr.append(dict(f=i,key=keyState,hud=hashlib.sha256(b''.join(data[y*pitch:y*pitch+w*2] for y in range(32))).hexdigest(),dx=rw(0xf77a),count=rw(0xf768)))
 (P/f'visual-qa-{side}.json').write_text(json.dumps(rr));print('VISUAL',side,len(rr),flush=True)
finally:core.retro_unload_game();core.retro_deinit()

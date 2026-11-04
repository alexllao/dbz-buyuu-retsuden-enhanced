from pathlib import Path
import sys,json,hashlib,subprocess
rompath=sys.argv[1];defcid=int(sys.argv[2]);out=Path(sys.argv[3]);out.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(Path('work').resolve()));sys.path.insert(0,str(Path('work/cpu-soak').resolve()))
sys.argv=['probe','--native','--rom',rompath,'--out',str(out)]
header=Path('work/gameplay_probe.py').read_text().split('try:\n for index,step in enumerate(steps[:-1]):')[0].replace('BASE=Path(__file__).resolve().parent.parent','BASE=Path.cwd()')
exec(compile(header,'manual-knockdown-native-menus','exec'),globals())
from menu_ai_setup import boot_versus
def actor(b):
 return dict(cid=rb(b+0x58),control=rb(b+0xbe),program=rw(b),pose=rb(b+4),cursor=rw(b+6),action=rb(b+0x5b),hp=rw(b+0x24),x=rw(b+0xa),y=rw(b+0x10),flags1E=rw(b+0x1e),flags20=rw(b+0x20),hitstop=rw(b+0x40))
encoder=None
try:
 boot_versus(globals(),0,defcid)
 # Helper sets BE1 at return but runs no core frame afterward. Disable both
 # immediately; every following combat frame is controlled manual input.
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for b,x,face in [(P1,300,0),(P2,348,1)]:
  ww(b+0xa,x);ww(b+0xc,0);wb(b+0x59,face)
 for _ in range(3):tick()
 for _ in range(20):tick(['DOWN'],[])
 w,h,pitch,data=latest
 encoder=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb565le','-video_size',f'{w}x{h}','-framerate',str(av.timing.fps),'-i','pipe:0','-vf','scale=640:448:flags=neighbor','-an','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(out/'Barrido.mp4')],stdin=subprocess.PIPE)
 rows=[];transitions=[];previous=None
 for f in range(245):
  tick(['DOWN','B'] if f<2 else [],[])
  row=dict(frame=f+1,tick=rw(0xe6a8),p1=actor(P1),p2=actor(P2));rows.append(row)
  w,h,pitch,data=latest;encoder.stdin.write(b''.join(data[y*pitch:y*pitch+w*2] for y in range(h)))
  statekey=(row['p2']['program'],row['p2']['pose'])
  if statekey!=previous:
   transitions.append(row)
   if row['p2']['program'] in [0xa1,0xa4,0xa5,0xc0,0xc1,0xc2] or previous and previous[0]!=0 and row['p2']['program']==0:
    save_image(out/f'F{f+1:03}-P{row["p2"]["program"]:04X}-pose{row["p2"]["pose"]:02X}.png')
  previous=statekey
 encoder.stdin.close();assert encoder.wait()==0;encoder=None
 result=dict(sha256=hashlib.sha256(rom).hexdigest(),fps=av.timing.fps,pair=[0,defcid],fixture='Native menu selects actual fighters. BothBE0 before any post-boot core frame. Only position/facing fixture writes; no HP/reaction/timer/AI/RNG forcing. P1holdsDOWN20frames,DOWN+B2frames, then empty pads both sides245frames. No CPU autoplay.',rows=rows,transitions=transitions)
 (out/'report.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'pair':result['pair'],'sha256':result['sha256'],'transitions':[(r['frame'],r['tick'],r['p2']['program'],r['p2']['pose']) for r in transitions if r['frame']<220]},indent=2))
finally:
 if encoder:encoder.stdin.close();encoder.wait()
 core.retro_unload_game();core.retro_deinit()

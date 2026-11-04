from pathlib import Path
import sys,json,hashlib,subprocess
ROOT=Path.cwd();cid=int(sys.argv[1]);romfile=sys.argv[2];out=ROOT/'work/side-switch/demo'/f'{cid:02}';out.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'work'));sys.argv=['probe','--native','--rom',romfile,'--out',str(out)]
header=(ROOT/'work/gameplay_probe.py').read_text().split('try:\n for index,step in enumerate(steps[:-1]):')[0].replace('BASE=Path(__file__).resolve().parent.parent','BASE=Path.cwd()')
exec(compile(header,'side-demo-setup','exec'),globals())
encoder=None
try:
 for index,step in enumerate(steps[:-1]):
  if index==9:
   for direction,count in [('DOWN',cid//3),('RIGHT',cid%3)]:
    for _ in range(count):
     for _ in range(4):tick([direction])
     for _ in range(16):tick()
  for _ in range(step.get('frames',1)):tick([] if index==11 else step.get('buttons',[]))
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(180):tick()
 assert rb(P1+0x58)==cid and rb(P2+0x58)==0
 ww(P1+0xa,200);ww(P1+0xc,0);wb(P1+0x59,0);ww(P2+0xa,264);ww(P2+0xc,0);wb(P2+0x59,1)
 for _ in range(3):tick()
 encoder=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb565le','-video_size','320x224','-framerate',str(av.timing.fps),'-i','pipe:0','-vf','scale=640:448:flags=neighbor','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(out/'Cambio-de-lado.mp4')],stdin=subprocess.PIPE)
 schedule=[[]]*20+[['RIGHT']]*4+[['LEFT']]*4+[['RIGHT','C']]*4+[['C']]*45+[[]]*43
 trace=[]
 for frame,keys in enumerate(schedule):
  tick(keys);w,h,pitch,data=latest;encoder.stdin.write(b''.join(data[y*pitch:y*pitch+w*2] for y in range(h)))
  trace.append({'frame':frame,'program':rw(P1),'x':rw(P1+0xa),'enemyX':rw(P2+0xa),'hp1':rw(P1+0x24),'hp2':rw(P2+0x24),'attack':bool(rb(P1+0x1e)&128)})
  if frame in [20,35,60]:save_image(out/f'F{frame:03}.png')
 encoder.stdin.close();assert encoder.wait()==0;encoder=None
 assert any(x['program']==0x843 for x in trace) and all(x['hp1']==200 and x['hp2']==200 and not x['attack'] for x in trace)
 (out/'report.json').write_text(json.dumps({'cid':cid,'romSha256':hashlib.sha256(rom).hexdigest(),'fps':av.timing.fps,'frames':len(trace),'trace':trace,'fixture':'Native menus and human pads; synthetic initial world position/facing only. FBF+C through actual inputs, C held after crossing; no action/HP/program forcing. Silent emulator capture.'},indent=2))
 print(cid,'recorded',flush=True)
finally:
 if encoder:encoder.stdin.close();encoder.wait()
 core.retro_unload_game();core.retro_deinit()

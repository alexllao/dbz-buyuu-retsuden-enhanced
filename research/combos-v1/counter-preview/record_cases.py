from pathlib import Path
import sys,json,subprocess,hashlib
ROOT=Path.cwd();cid=int(sys.argv[1]);romfile=sys.argv[2];tag=sys.argv[3];out=ROOT/'work/combo-counter/demo'/f'{cid:02}-{tag}';out.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'work'));sys.argv=['probe','--native','--rom',romfile,'--out',str(out)]
header=Path('work/gameplay_probe.py').read_text().split('try:\n for index,step in enumerate(steps[:-1]):')[0].replace('BASE=Path(__file__).resolve().parent.parent','BASE=Path.cwd()')
exec(compile(header,'combo-video-native','exec'),globals());encoder=None
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
 assert rb(P1+0x58)==cid
 ww(P1+0xa,300);ww(P2+0xa,460 if tag=='whiff' else 332);ww(P1+0xc,0);ww(P2+0xc,0);wb(P1+0x59,0);wb(P2+0x59,1)
 for _ in range(3):tick()
 encoder=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb565le','-video_size','320x224','-framerate',str(av.timing.fps),'-i','pipe:0','-vf','scale=640:448:flags=neighbor','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(out/'demo.mp4')],stdin=subprocess.PIPE)
 trace=[];hitFrames=[];previousHP=rw(P2+0x24)
 replay=json.loads((Path.cwd()/'work/combos/demo'/f'{cid:02}-combos'/'report.json').read_text())['trace'] if tag=='base' else None
 for frame in range(240):
  keys=[]
  if 25<=frame<27:keys=['A']
  if hitFrames and hitFrames[0]+3<=frame<hitFrames[0]+5:keys=['A']
  if len(hitFrames)>1:
   start=hitFrames[1]+3
   if start<=frame<start+4:keys=['LEFT']
   if start+4<=frame<start+6:keys=['RIGHT']
   if start+6<=frame<start+8:keys=['RIGHT','A']
  if replay is not None:keys=replay[frame]['keys']
  keys2=['RIGHT'] if tag=='guard' and frame>=25 else []
  tick(keys,keys2);w,h,pitch,data=latest;encoder.stdin.write(b''.join(data[y*pitch:y*pitch+w*2] for y in range(h)))
  trace.append({'f':frame,'keys':keys,'keys2':keys2,'program':rw(P1),'action':rb(P1+0x5b),'hp':rw(P1+0x24),'ki':rw(P1+0x28),'enemyHP':rw(P2+0x24),'enemyAction':rb(P2+0x5b),'comboState':rb(P1+0x106)})
  currentHP=rw(P2+0x24)
  if currentHP<previousHP:hitFrames.append(frame)
  previousHP=currentHP
  if frame in [55,85]:save_image(out/f'F{frame:03}.png')
 encoder.stdin.close();assert encoder.wait()==0;encoder=None
 hits=[t['f'] for i,t in enumerate(trace) if t['enemyHP']<(200 if not i else trace[i-1]['enemyHP'])]
 (out/'report.json').write_text(json.dumps({'romSha256':hashlib.sha256(rom).hexdigest(),'cid':cid,'tag':tag,'fps':av.timing.fps,'frames':len(trace),'hits':hits,'trace':trace,'fixture':'Native menus, actual human command inputs, fixed initial positions/facing only, no HP/ki/action/timer forcing; silent emulator capture'},indent=2));print(cid,tag,hits,flush=True)
finally:
 if encoder:encoder.stdin.close();encoder.wait()
 core.retro_unload_game();core.retro_deinit()

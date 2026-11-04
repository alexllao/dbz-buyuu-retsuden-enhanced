from pathlib import Path
import sys,json,hashlib,subprocess
ROOT=Path.cwd();cid=int(sys.argv[1]);mode=sys.argv[2] if len(sys.argv)>2 else 'downB';romfile='work/generic-combos/candidate.bin';port=1;turbo=False
out=ROOT/'work/generic-combos/demo'/f'{cid:02}-{mode}';out.mkdir(parents=True,exist_ok=True)
report=json.loads((ROOT/'work/generic-combos/finishers'/str(cid)/'report.json').read_text());assert report['romSha256']==hashlib.sha256(Path(romfile).read_bytes()).hexdigest()
case=next(r for r in report['results'] if r['summary']['mode']==mode and not r['summary']['charged']);recorded=case['trace'];last=case['summary']['hits'][-1];end=next((i+30 for i in range(last+60,len(recorded)-30) if recorded[i]['p']['action']==recorded[i]['enemy']['action']==0),len(recorded));end=max(240,end)
source=romfile;s=Path('work/side-switch/test_commands.py').read_text().split('results=[]')[0];s=s[s.index('sys.path.insert'):];exec(compile(s,'video-setup','exec'),globals());encoder=None
names=['Goku','Gohan','Piccolo','Vegeta','Trunks','Cell','A18','Krilin','Freezer','Recoome','Ginyu']
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
 ww(P1+0xa,300);ww(P2+0xa,332);ww(P1+0xc,0);ww(P2+0xc,0);wb(P1+0x59,0);wb(P2+0x59,1)
 for _ in range(3):tick()
 title=f'{names[cid]} - A, B, A + '+('Meteor nativo' if mode=='meteor19' else 'rafaga nativa' if mode=='flurry' else 'tecnica nativa')
 vf="scale=640:448:flags=neighbor,pad=640:504:0:56:color=0x10151c,drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='"+title+"':x=12:y=8:fontsize=19:fontcolor=white,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='COMBOS V3 - ROM REAL - SIN CONTADOR SUPERPUESTO':x=12:y=34:fontsize=13:fontcolor=0xbecbd8"
 encoder=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb565le','-video_size','320x224','-framerate',str(av.timing.fps),'-i','pipe:0','-vf',vf,'-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(out/'demo.mp4')],stdin=subprocess.PIPE)
 actual=[]
 for f in range(end):
  keys=recorded[f]['keys'];tick(keys);w,h,pitch,data=latest;encoder.stdin.write(b''.join(data[y*pitch:y*pitch+w*2] for y in range(h)))
  actual.append({'f':f,'keys':keys,'program':rw(P1),'action':rb(P1+0x5b),'enemyHP':rw(P2+0x24),'enemyAction':rb(P2+0x5b),'combo':rb(P1+0x106)})
  assert actual[-1]['enemyHP']==recorded[f]['enemy']['hp'],(cid,mode,f,actual[-1],recorded[f])
  if f==min(last+3,end-1):save_image(out/'capture.png')
 encoder.stdin.close();assert encoder.wait()==0;encoder=None
 assert actual[-1]['action']==actual[-1]['enemyAction']==0
 (out/'report.json').write_text(json.dumps({'romSha256':hashlib.sha256(rom).hexdigest(),'cid':cid,'mode':mode,'frames':end,'fps':av.timing.fps,'matchesTraceHP':True,'bothIdleAtEnd':True,'counterInRom':False,'counterOverlay':False,'fixture':report['fixture'],'summary':case['summary'],'trace':actual},indent=2),encoding='utf8');print(cid,mode,end,flush=True)
finally:
 if encoder:encoder.stdin.close();encoder.wait()
 core.retro_unload_game();core.retro_deinit()

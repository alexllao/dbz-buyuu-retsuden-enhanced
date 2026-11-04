from pathlib import Path
import json,subprocess,hashlib,shutil
# Reuse the pixel UI code, not the old video's fixed2-hit assertions.
s=Path('work/combo-counter/render_preview.py').read_text(encoding='utf-8').split('cases=[')[0]
s=s.replace("P=Path('work/combo-counter');O=Path('outputs/contador-combos-vista-previa')","P=Path('work/kick-combos');O=Path('outputs/combos-v2-patadas')")
exec(compile(s,'counter-preview-ui','exec'),globals())
def timeline(trace):
 active=False;chain=0;display=0;hold=-100;end=-100;changed=-100;previous=200;frames=[];events=[]
 for t in trace:
  f=t['f'];hp=t['enemyHP'];hurt=t['enemyAction'] in [11,12,19,0xa1,0xa4,0xa5] and hp>0
  damage=hp<previous
  # Count the finishing impact before testing recovery: it may change
  # the victim directly from standing hitstun into native knockdown.
  if damage and (active or hurt):
   if active:chain+=1
   else:active=True;chain=1;display=0
   events.append({'frame':f,'event':'real_damage','chainCount':chain,'hpLoss':previous-hp,'enemyAction':t['enemyAction']})
   if chain>=2:display=chain;changed=f
  if active and not hurt:
   active=False;chain=0;hold=f+36;end=hold+12;events.append({'frame':f,'event':'chain_ended','holdUntil':hold,'fadeEnds':end,'enemyAction':t['enemyAction']})
  previous=hp;alpha=1.0 if active else (1.0 if f<=hold else max(0,(end-f)/12))
  if display<2:alpha=0
  frames.append({'frame':f,'count':display if alpha>0 else 0,'alpha':alpha,'pop':display>=2 and 0<=f-changed<4})
 return frames,events
reports=[];clips=[]
for cid,name,expected,description in [(0,'Goku',5,'dos punos y tres patadas'),(3,'Vegeta',4,'dos punos y dos impactos de remate')]:
 folder=P/'demo'/f'{cid:02}-kicks';r=json.loads((folder/'report.json').read_text());trace=r['trace'];frames,events=timeline(trace);dest=O/f'{name}-A-A-B-contador-preview.mp4';clips.append(dest)
 assert max(f['count'] for f in frames)==expected and frames[-1]['count']==0
 assert len(r['hits'])==expected and all(t['enemyAction'] in [11,12] for t in trace[r['hits'][0]:r['hits'][-1]])
 font="fontfile='C\\:/Windows/Fonts/arial.ttf'";filters="pad=640:552:0:60:black,drawtext="+font+":text='COMBOS V2 - JUEGO REAL / CONTADOR SUPERPUESTO':fontsize=16:fontcolor=white:x=10:y=8,drawtext="+font+":text='"+name+' - '+description+"':fontsize=18:fontcolor=0xffd139:x=10:y=32,drawtext="+font+":text='A, A, B al conectar - el rival recupera el control al terminar':fontsize=16:fontcolor=white:x=10:y=525"
 decoder=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-i',str(folder/'demo.mp4'),'-f','rawvideo','-pix_fmt','rgb24','pipe:1'],stdout=subprocess.PIPE)
 encoder=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size','640x448','-framerate',str(r['fps']),'-i','pipe:0','-vf',filters,'-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)],stdin=subprocess.PIPE)
 try:
  for f in frames:
   b=decoder.stdout.read(640*448*3);assert len(b)==640*448*3;data=bytearray(b);draw_counter(data,f);encoder.stdin.write(data)
  assert not decoder.stdout.read(1)
 finally:decoder.stdout.close();encoder.stdin.close();assert decoder.wait()==0 and encoder.wait()==0
 shutil.copyfile(folder/'demo.mp4',O/f'{name}-combo-real-sin-contador.mp4')
 lastHP=200;damage=[]
 for f in r['hits']:damage.append(lastHP-trace[f]['enemyHP']);lastHP=trace[f]['enemyHP']
 reports.append({'cid':cid,'name':name,'romSha256':r['romSha256'],'frames':r['frames'],'fps':r['fps'],'hits':r['hits'],'damagePerHit':damage,'totalDamage':sum(damage),'maxCounter':expected,'uninterrupted':True,'bothActorsIdleAtEnd':trace[-1]['action']==trace[-1]['enemyAction']==0,'counterHiddenAtEnd':True,'counterEvents':events,'counterFrames':frames,'file':dest.name})
lst=P/'concat-video.txt';lst.write_text(''.join("file '"+str(f.resolve()).replace('\\','/')+"'\n" for f in clips),encoding='utf-8');final=O/'Combos-v2-punetazos-y-patadas.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(lst),'-c','copy','-movflags','+faststart',str(final)],check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','2.05','-i',str(final),'-frames:v','1',str(O/'Goku-5-HITS.png')],check=True)
(P/'video-validation.json').write_text(json.dumps({'counterIsInRom':False,'combatIsRealRomCapture':True,'previewSha256':hashlib.sha256(final.read_bytes()).hexdigest(),'cases':reports,'fixture':'Native menus, real command inputs, initial positions/facing fixed only; no forced HP, ki, program, action or timers'},indent=2)+'\n');print(json.dumps({'video':str(final),'results':[(r['name'],r['maxCounter'],r['totalDamage']) for r in reports]}))

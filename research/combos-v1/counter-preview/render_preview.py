"""Code-rendered HUD counter preview over unaltered emulator recordings.
Not a ROM patch: counters come from the synchronized native HP/action traces.
"""
from pathlib import Path
import json,subprocess,hashlib
P=Path('work/combo-counter');O=Path('outputs/contador-combos-vista-previa');O.mkdir(parents=True,exist_ok=True)
FONT={
'0':['01110','10001','10011','10101','11001','10001','01110'],
'1':['00100','01100','00100','00100','00100','00100','01110'],
'2':['01110','10001','00001','00010','00100','01000','11111'],
'3':['11110','00001','00001','01110','00001','00001','11110'],
'4':['00010','00110','01010','10010','11111','00010','00010'],
'5':['11111','10000','10000','11110','00001','00001','11110'],
'6':['01110','10000','10000','11110','10001','10001','01110'],
'7':['11111','00001','00010','00100','01000','01000','01000'],
'8':['01110','10001','10001','01110','10001','10001','01110'],
'9':['01110','10001','10001','01111','00001','00001','01110'],
'H':['10001','10001','10001','11111','10001','10001','10001'],
'I':['11111','00100','00100','00100','00100','00100','11111'],
'T':['11111','00100','00100','00100','00100','00100','00100'],
'S':['01111','10000','10000','01110','00001','00001','11110'],
' ':['00000']*7}

def timeline(trace):
 active=False;chain=0;display=0;hold=-100;end=-100;changed=-100;previous=200;frames=[];events=[]
 for t in trace:
  f=t['f'];hp=t['enemyHP'];hurt=t['enemyAction'] in [11,12] and hp>0
  if active and not hurt:
   active=False;chain=0;hold=f+36;end=hold+12;events.append({'frame':f,'event':'opponent_recovered','retainCounterUntil':hold,'fadeEnds':end})
  if hp<previous and hurt:
   if active:chain+=1
   else:
    active=True;chain=1;display=0
   events.append({'frame':f,'event':'unblocked_damage','chainCount':chain,'hpLoss':previous-hp})
   if chain>=2:display=chain;changed=f
  previous=hp
  alpha=1.0 if active else (1.0 if f<=hold else max(0,(end-f)/12))
  if display<2:alpha=0
  frames.append({'frame':f,'count':display if alpha>0 else 0,'alpha':alpha,'pop':display>=2 and 0<=f-changed<4})
 return frames,events

def draw_counter(data,frame):
 if frame['count']<2:return
 size=5 if frame['pop'] else 4;x0=24;y0=84;colored={}
 for c,char in enumerate(str(frame['count'])+' HITS'):
  color=(255,209,57) if char.isdigit() else (255,244,207)
  for yy,row in enumerate(FONT[char]):
   for xx,on in enumerate(row):
    if on=='1':
     for y in range(y0+yy*size,y0+(yy+1)*size):
      for x in range(x0+c*6*size+xx*size,x0+c*6*size+(xx+1)*size):colored[x,y]=color
 outline={}
 for x,y in colored:
  for dx,dy in [(0,0),(2,0),(-2,0),(0,2),(0,-2),(2,2),(-2,2),(2,-2),(-2,-2)]:outline[x+dx,y+dy]=(7,9,17)
 outline.update(colored);a=frame['alpha']
 for (x,y),color in outline.items():
  if not(0<=x<640 and 0<=y<448):continue
  at=(y*640+x)*3
  for k in range(3):data[at+k]=round(color[k]*a+data[at+k]*(1-a))

cases=[
 ('Goku',Path('work/combos/demo/00-combos'),'Dos impactos enlazados y retirada del contador','Al segundo impacto aparece el contador. Luego se apaga.'),
 ('Vegeta',Path('work/combos/demo/03-combos'),'El proyectil separado no suma al combo anterior','El rival se recupera antes del proyectil. No cuenta como 3.'),
 ('Bloqueo',P/'demo/00-guard','Golpe bloqueado','El bloqueo no cuenta y el contador permanece oculto.'),
 ('Fallo',P/'demo/00-whiff','Golpe al aire','Sin impacto no aparece el contador.')]
summaries=[];clips=[]
for name,folder,title,caption in cases:
 report=json.loads((folder/'report.json').read_text());trace=report['trace'];frames,events=timeline(trace);source=folder/'demo.mp4';dest=O/f'{name}-contador.mp4';clips.append(dest)
 fps=report['fps'];decoder=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-i',str(source),'-f','rawvideo','-pix_fmt','rgb24','pipe:1'],stdout=subprocess.PIPE)
 font="fontfile='C\\:/Windows/Fonts/arial.ttf'"
 filters="pad=640:552:0:60:black,drawtext="+font+":text='CONTADOR SUPERPUESTO - PREVISUALIZACION, NO INCLUIDO EN ROM':fontsize=15:fontcolor=white:x=10:y=8,drawtext="+font+":text='"+name+' - '+title+"':fontsize=17:fontcolor=0xffd139:x=10:y=32,drawtext="+font+":text='"+caption+"':fontsize=16:fontcolor=white:x=10:y=525"
 encoder=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size','640x448','-framerate',str(fps),'-i','pipe:0','-vf',filters,'-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)],stdin=subprocess.PIPE)
 try:
  for frame in frames:
   raw=decoder.stdout.read(640*448*3);assert len(raw)==640*448*3,(name,frame['frame'],len(raw));data=bytearray(raw);draw_counter(data,frame);encoder.stdin.write(data)
  assert not decoder.stdout.read(1)
 finally:
  decoder.stdout.close();encoder.stdin.close();assert decoder.wait()==0;assert encoder.wait()==0
 maxcount=max(f['count'] for f in frames)
 if name in ['Goku','Vegeta']:assert maxcount==2
 else:assert maxcount==0 and not report['hits']
 assert frames[-1]['count']==0
 summaries.append({'case':name,'sourceRomSha256':report['romSha256'],'sourceVideoSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'frames':len(trace),'fps':fps,'rawDamageFrames':report['hits'],'maxDisplayedCounter':maxcount,'counterHiddenAtEnd':True,'events':events,'counterFrames':frames,'file':dest.name,'previewSha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
lst=P/'concat.txt';lst.write_text(''.join("file '"+str(f.resolve()).replace('\\','/')+"'\n" for f in clips),encoding='utf-8');final=O/'Contador-combos-demostracion.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(lst),'-c','copy','-movflags','+faststart',str(final)],check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','1.1','-i',str(final),'-frames:v','1',str(O/'Contador-2-HITS.png')],check=True)
validation={'counterIsInRom':False,'method':'Postproduced pixel UI over real emulator recordings; counted from synchronized enemy HP and action11/12 in these standing-hit fixtures, not number of button presses','counterAppearsAt':2,'holdAfterRecoveryFrames':36,'fadeFrames':12,'allCasesCounterHiddenAtEnd':True,'videoSha256':hashlib.sha256(final.read_bytes()).hexdigest(),'cases':summaries,'limits':['Visual proposal, no Mega Drive counter code or native VRAM/SAT implementation yet','Decoder is specific to these recorded standing-hit fixtures, not a validated general combo detector for all moves and states','Third projectile damage in Vegeta occurs after recovery, so maximum is2 rather than3; Goku projectile causes no third damage in its recording','Silent captures, synthetic initial position/facing only; no forced HP, ki, action or timers']}
(P/'validation.json').write_text(json.dumps(validation,indent=2)+'\n');print(json.dumps({'video':str(final),'cases':[(c['case'],c['maxDisplayedCounter']) for c in summaries]}))

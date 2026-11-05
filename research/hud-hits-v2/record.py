from pathlib import Path
import sys,json,subprocess,struct,hashlib
requestedLabel=sys.argv[2]
raw=Path('work/hits-hud-v2/prepare.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0]
setup,functions=raw.split("exec(compile(header,'combo-side-setup','exec'),globals())",1)
exec(compile(setup,'load-route-setup','exec'),globals())
audioDef='def audio(l,r):\n if audio_file is not None:audio_file.write(struct.pack("<hh",l,r))'
batchDef='def batch(data,frames):\n if audio_file is not None:audio_file.write(C.string_at(data,frames*4))\n return frames'
replacement='src=src.replace('+repr('def audio(l,r):pass')+','+repr(audioDef)+')\nsrc=src.replace('+repr('def batch(data,frames):return frames')+','+repr(batchDef)+')\nexec(compile(src,"local-emulator-setup","exec"),globals())'
header=header.replace("exec(compile(src,'local-emulator-setup','exec'),globals())",replacement)
audio_file=None;exec(compile(header,'recording-setup','exec'),globals());exec(compile(functions,'route-functions','exec'),globals())
recordOut=BASE/'work/hits-hud-v2/video'/f'{cid}-{requestedLabel}';recordOut.mkdir(parents=True,exist_ok=True)
try:
 restore((out/('low-hp-charged.state' if cid in [3,5] else 'charged.state')).read_bytes())
 ww(P1+0xa,300);ww(P2+0xa,332);ww(P1+0xc,0);ww(P2+0xc,0);wb(P1+0x59,0);wb(P2+0x59,1)
 for _ in range(8):tick()
 names={0:'GOKU',2:'PICCOLO',3:'VEGETA',5:'CELL'}
 titles={'comboAAA-cambio-meteor':'BASICOS - CAMBIO DE LADO - METEOR','comboAAA-cambio-meteor-cerca':'BASICOS - CRUCE - ACERCAMIENTO - REMATE','comboAAA-cambio-especial':'BASICOS - CAMBIO DE LADO - ESPECIAL','cambio-rafaga':'CAMBIO DE LADO - RAFAGA NATIVA','cambio-meteor-guardia':'CAMBIO DE LADO - METEOR CONTRA GUARDIA','cambio-meteor':'CAMBIO DE LADO - METEOR','contra-P2':'P1 COMBO Y CRUCE - P2 CONTRA Y METEOR','meteor-solo':'METEOR SOLO - TRES CONTACTOS','combo-espera-meteor':'CADENA CADUCADA - METEOR EMPIEZA DE CERO','combo-mareo-meteor':'GOLPES - MAREO - GOLPE Y METEOR'}
 title=names[cid]+' | '+titles[requestedLabel]
 vf="scale=640:448:flags=neighbor,pad=640:500:0:52:color=0x10151c,drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='"+title+"':x=10:y=6:fontsize=15:fontcolor=white,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='HITS V2 - CADENA CONSERVADA - VELOCIDAD NORMAL':x=10:y=31:fontsize=11:fontcolor=0xbecbd8"
 encoder=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb565le','-video_size','320x224','-framerate',str(av.timing.fps),'-i','pipe:0','-vf',vf,'-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p',str(recordOut/'silent.mp4')],stdin=subprocess.PIPE)
 audio_file=(recordOut/'audio.pcm').open('wb');trace=[];phase='preparacion';idle(60)
 if requestedLabel.startswith('comboAAA') or requestedLabel in ['contra-P2','combo-espera-meteor']:basic_chain('AAA')
 if requestedLabel not in ['meteor-solo','combo-mareo-meteor','combo-espera-meteor']:cross()
 if requestedLabel=='combo-espera-meteor':
  phase='espera-agota-ventana';idle(180)
 if requestedLabel=='combo-mareo-meteor':
  phase='golpes-hasta-mareo';attempts=0
  while rw(P2+0x36)==0 and attempts<10:
   close_to(30);wait_actor()
   for f in range(80):run(['A'] if f<6 else [])
   attempts+=1
  assert rw(P2+0x36)>0, 'native dizzy not reached'
  phase='mareo-conserva-HITS';idle(120)
  assert rw(P2+0x36)>0
  close_to(30);phase='golpe-tras-mareo'
  for f in range(40):run(['A'] if f<6 else [])
 if requestedLabel=='contra-P2':
  phase='contra-P2';idle(4);f2='RIGHT' if rw(P2+0xa)<rw(P1+0xa) else 'LEFT';b2='LEFT' if f2=='RIGHT' else 'RIGHT'
  for k in [[f2]]*4+[[b2]]*4+[[f2,'C']]*4:run([],k)
  for _ in range(90):
   if rw(P2)!=0x843:break
   run()
  phase='meteor-P2';f2='RIGHT' if rw(P2+0xa)<rw(P1+0xa) else 'LEFT';b2='LEFT' if f2=='RIGHT' else 'RIGHT';dirs=[[f2],['DOWN',f2],['DOWN'],['DOWN',b2],[b2],[f2]]
  for k in [k for k in dirs for _ in range(4)]+[dirs[-1]+['B']]*4:run([],k)
 if requestedLabel.endswith('cerca'):close_to(30);idle(4)
 if 'meteor' in requestedLabel:
  if cid==5:
   phase='remate-Cell';f=forward();b=backward();dirs=[['DOWN'],['DOWN',f],[f],[b]]
   for k in [k for k in dirs for _ in range(4)]+[dirs[-1]+['B']]*4:run(k)
  else:move_command('meteor',requestedLabel.endswith('guardia'))
 elif requestedLabel.endswith('rafaga'):move_command('flurry')
 elif requestedLabel!='contra-P2':move_command('downB')
 phase='final-y-recuperacion';free=0
 for _ in range(1800):
  run([], [opponent_back()] if requestedLabel.endswith('guardia') else [])
  if rb(P1+0x5b)<=8 and (rb(P2+0x5b)<=8 or rb(P2+0x5b)==10) and not rb(0xe73c) and not rw(0xe9c4):free+=1
  else:free=0
  if free>=35 and len(trace)>280:break
 phase='control-devuelto';idle(65)
 audio_file.close();audio_file=None;encoder.stdin.close();assert encoder.wait()==0;encoder=None
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(recordOut/'silent.mp4'),'-f','s16le','-ar',str(round(av.timing.sample_rate)),'-ac','2','-i',str(recordOut/'audio.pcm'),'-c:v','copy','-c:a','aac','-b:a','160k','-movflags','+faststart',str(recordOut/'route.mp4')],check=True)
 hits=[dict(frame=y['f'],phase=y['phase'],delta=x['e']['hp']-y['e']['hp']) for x,y in zip(trace,trace[1:]) if y['e']['hp']<x['e']['hp']]
 programs=sorted(set(t['e' if requestedLabel=='contra-P2' else 'p']['program'] for t in trace));expected={0:0x83e,2:0x844,3:0x846,5:0x84a}[cid]
 report=dict(romSha256=hashlib.sha256(rom).hexdigest(),cid=cid,enemyCid=enemyCid,stage=stage,label=requestedLabel,frames=len(trace),fps=av.timing.fps,title=title,startHP=trace[0]['p']['hp'],startKi=trace[0]['p']['ki'],damage=trace[0]['e']['hp']-trace[-1]['e']['hp'],damageEvents=hits,programs=programs,expectedFinisher=hex(0x83e if requestedLabel=='contra-P2' else expected),expectedFinisherStarted=(0x83e in programs if requestedLabel=='contra-P2' else expected in programs if 'meteor' in requestedLabel else None),player1Damage=trace[0]['p']['hp']-trace[-1]['p']['hp'],controlReturned=free>=35,fixture='Existing advantage ROM unchanged; two human pads. Snapshot prepared with real charging and, for Vegeta/Cell, real received punches. Only initial spacing/facing set. No HP/ki/action/timer writes during capture. Native audio and animation speed; independent route takes.',trace=trace)
 (recordOut/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(cid,requestedLabel,'frames',len(trace),'damage',report['damage'],'finisher',report['expectedFinisherStarted'],'returned',report['controlReturned'],flush=True)
finally:
 if audio_file:audio_file.close()
 if encoder:encoder.stdin.close();encoder.wait()
 core.retro_unload_game();core.retro_deinit()

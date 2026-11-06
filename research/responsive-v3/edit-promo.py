from pathlib import Path
import json,subprocess,hashlib
p=Path('work/responsive-v3/video');o=Path('outputs/v1.0-build-20261106-100534');o.mkdir(parents=True,exist_ok=True)
chap=json.loads((p/'chapters.json').read_text());labels=[('ALEX LLAO','PRESENTA'),('GOKU','COMBO / CRUCE / METEOR'),('GOKU','TRES IMPACTOS'),('GOKU','SUPER KAMEHAMEHA'),('VEGETA','METEOR'),('PICCOLO','METEOR'),('GOHAN','LANZAMIENTO / MASENKO'),('VEGETA','LANZAMIENTO / FINAL FLASH'),('GOKU','LANZAMIENTO / KAMEHAMEHA'),('CELL','TRECE IMPACTOS'),('DOS JUGADORES','CRUCES Y RESPUESTAS'),('EN DESARROLLO','ALEX LLAO')]
edited=[];elapsed=0
for i,(c,(name,action)) in enumerate(zip(chap['chapters'],labels)):
 # Keep the complete game image and its native HUD; no time remapping.
 # Engineering captions are removed from the source, not the gameplay.
 vf="crop=640:448:0:52,scale=960:672:flags=neighbor,pad=1280:720:160:24:color=0x0b1018"
 def text(s,x,y,size,color='white'):
  return ",drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='"+s+f"':x={x}:y={y}:fontsize={size}:fontcolor={color}"
 vf+=text('DRAGON BALL Z  /  BUYUU RETSUDEN ENHANCED','(w-tw)/2',3,18)
 vf+=text(name+'  /  V1.0  /  BUILD 2026-11-06','(w-tw)/2',697,16,'0xf5c667')
 words=action.split(' / ')
 for j,w in enumerate(words):
  # Sidebar labels use short lines so they cannot cover the gameplay.
  parts=w.split(' ') if len(w)>13 else [w]
  for k,part in enumerate(parts):vf+=text(part,12,285+j*65+k*23,15,'0xf5c667')
 for j,w in enumerate(['JUEGO REAL','VELOCIDAD','NORMAL']):vf+=text(w,1130,290+j*26,14,'0xbac6d5')
 target=p/f'edit-{i:02}.mp4'
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',c['path'],'-vf',vf,'-af','afade=t=in:d=0.04,afade=t=out:st='+str(max(0,c['seconds']-.12))+':d=0.12','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k',str(target)],check=True)
 c['startSeconds']=elapsed;elapsed+=c['seconds'];edited.append(target.resolve())
(p/'concat.txt').write_text('\n'.join("file '"+str(t).replace('\\','/')+"'" for t in edited),encoding='utf8')
target=o/'DBZ-Enhanced-v1.0-build-20261106-100534-Anuncio.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(p/'concat.txt'),'-c','copy','-movflags','+faststart',str(target)],check=True)
chap.update(seconds=elapsed,gameplayTimeScaling=False,nativeAudio=True,nativeHitsHud=True,staging='Scripted human ports; native-charged seeds. Positions set before each take; critical HP earned via real damage before capture. No HP/timer/counter writes during takes.',video=dict(path='assets/media/release-v1-0/'+target.name,sha256=hashlib.sha256(target.read_bytes()).hexdigest()))
(p/'promo.json').write_text(json.dumps(chap,indent=2),encoding='utf8')
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','9','-i',str(target),'-frames:v','1',str(o/'captura.png')],check=True)
print('PROMO',elapsed,'seconds',target)

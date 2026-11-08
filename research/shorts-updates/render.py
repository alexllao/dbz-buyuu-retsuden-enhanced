from pathlib import Path
import sys,json,subprocess,hashlib
P=Path('work/shorts-updates');P.mkdir(exist_ok=True);O=Path('outputs/YouTube-Shorts-mejoras');O.mkdir(exist_ok=True,parents=True);fps=59.92274340431231;mode=sys.argv[1]
configs={
 'saltos':dict(title='DOS TIPOS DE SALTO',tag='GOKU',bottom='Normal corto / largo al correr',filename='Short-Goku-dos-saltos.mp4',build='20261108-143706',status='Prueba de Goku',scenes=[
  ('work/jump-two/video/candidate/carrera-patada.mp4',0,162,'SALTO + PATADA','Ataques aéreos con Goku'),
  ('work/jump-two/video/candidate/vertical.mp4',0,133,'SALTO NORMAL','Más bajo y vuelta rápida al suelo'),
  ('work/jump-two/video/candidate/diagonal.mp4',0,133,'NORMAL EN DIAGONAL','Recorrido más corto'),
  ('work/jump-two/video/candidate/carrera.mp4',0,153,'SALTO DESDE CARRERA','Más alcance, conservando la altura'),
  ('work/jump-two/video/candidate/carrera-patada.mp4',0,162,'REMATE EN EL AIRE','Correr + saltar + atacar')]),
 'enlaces':dict(title='LANZA Y REMATA',tag='LANZAMIENTO + ESPECIAL',bottom='El momento del especial importa',filename='Short-Lanzamiento-y-especiales.mp4',build='20261108-160337',status='Revisión de enlaces',scenes=[
  ('work/throw-links/video/after/link-Goku.mp4',0,350,'GOKU','Lanzamiento + Kamehameha'),
  ('work/throw-links/video/after/link-Vegeta.mp4',0,350,'VEGETA','Lanzamiento + Final Flash'),
  ('work/throw-links/video/after/link-Gohan.mp4',0,350,'GOHAN','Lanzamiento + Masenko'),
  ('work/throw-links/video/after/link-Piccolo.mp4',0,350,'PICCOLO','Lanzamiento + Special Beam Cannon'),
  ('work/throw-links/video/after/link-Cell.mp4',0,350,'CELL','Lanzamiento + Special Beam Cannon'),
  ('work/throw-links/video/after/link-Krilin.mp4',0,350,'KRILIN','Lanzamiento + Kamehameha')]),
 'rafagas':dict(title='¡CINCO DISPAROS!',tag='RÁFAGAS DE ENERGÍA',bottom='Daño repartido / mismo ki total',filename='Short-Rafagas-cinco-disparos.mp4',build='20261108-135651',status='Ráfagas aprobadas',scenes=[
  ('work/barrage-roster/video/after/Goku.mp4',0,320,'GOKU','Cinco proyectiles reales'),
  ('work/barrage-roster/video/after/Vegeta.mp4',100,420,'VEGETA','Su ráfaga, sus poses originales'),
  ('work/barrage-roster/video/after/Cell.mp4',100,420,'CELL','Cinco disparos con Cell'),
  ('work/barrage-roster/video/after/A18.mp4',100,420,'A18','También con A18'),
  ('work/barrage-roster/video/after/Krilin.mp4',100,420,'KRILIN','La ráfaga de Krilin'),
  ('work/barrage-roster/video/after/Recoome.mp4',100,420,'RECOOME','Seis personajes mejorados')])}
c=configs[mode];D=P/mode;D.mkdir(exist_ok=True);clips=[];records=[]
def escaped(path):return str(path.resolve()).replace('\\','/').replace(':','\\:')
def textfile(name,text):
 p=D/(name+'.txt');p.write_text(text,encoding='utf8');return escaped(p)
def textdraw(vf,name,text,y,size,color='white',bold=False):
 font='arialbd.ttf' if bold else 'arial.ttf';return vf+f",drawtext=fontfile='C\\:/Windows/Fonts/{font}':textfile='{textfile(name,text)}':x=82:y={y}:fontsize={size}:fontcolor={color}"
for i,(source,start,end,label,sub) in enumerate(c['scenes']):
 path=Path(source);assert '/before/' not in path.as_posix() and '/control/' not in path.as_posix();n=end-start;duration=n/fps
 vf=f'[0:v]trim=start_frame={start}:end_frame={end},setpts=PTS-STARTPTS,crop=640:448:0:52,split=2[bg][game];[bg]scale=270:480:force_original_aspect_ratio=increase,crop=270:480,boxblur=12:2,eq=brightness=-0.19:saturation=0.55,scale=1080:1920[back];[game]scale=960:672:flags=neighbor[fg];[back][fg]overlay=60:640,drawbox=x=56:y=636:w=968:h=680:color=0x8492a3@0.7:t=3'
 vf=textdraw(vf,f'{i}-platform','MEGA DRIVE / GENESIS',112,31,'0xb9c6d6')
 vf=textdraw(vf,f'{i}-brand','DBZ BUYUU RETSUDEN',188,48,'white',True)
 vf=textdraw(vf,f'{i}-enhanced','E N H A N C E D',250,29,'0xb9c6d6')
 vf=textdraw(vf,f'{i}-title',c['title'],352,62,'0xffd35a',True)
 vf=textdraw(vf,f'{i}-tag',c['tag'],450,33,'white')
 vf=textdraw(vf,f'{i}-scene',label,1390,49,'0xffd35a',True)
 vf=textdraw(vf,f'{i}-sub',sub,1462,34,'white')
 vf=textdraw(vf,f'{i}-bottom',c['bottom'],1550,31,'0xd2dbe7')
 vf=textdraw(vf,f'{i}-credit','ALEX LLAO / MOD EN DESARROLLO',1655,28,'0xb9c6d6')
 vf=textdraw(vf,f'{i}-speed','Juego real / velocidad normal / sonido original',1700,25,'0xb9c6d6')
 vf+=f",drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='{i+1:02d} / {len(c['scenes']):02d}':x=82:y=546:fontsize=31:fontcolor=0xffd35a[v];[0:a]atrim=start={start/fps}:end={end/fps},asetpts=PTS-STARTPTS,afade=t=in:d=0.018,afade=t=out:st={max(0,duration-.025)}:d=0.025[a]"
 out=D/f'{i:02d}.mp4';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-filter_complex_threads','1','-i',str(path),'-filter_complex',vf,'-map','[v]','-map','[a]','-c:v','libx264','-preset','veryfast','-crf','20','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-ar','44100','-r',str(fps),'-fps_mode','cfr','-t',str(duration),str(out)],check=True);clips.append(out);records.append(dict(source=path.as_posix(),sourceSha256=hashlib.sha256(path.read_bytes()).hexdigest(),startFrame=start,endFrame=end,label=label,seconds=duration));print(mode,'clip',i+1,flush=True)
concat=D/'concat.txt';concat.write_text('\n'.join("file '"+str(p.resolve()).replace('\\','/')+"'" for p in clips));movie=O/c['filename']
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c:v','libx264','-preset','veryfast','-crf','20','-threads','2','-pix_fmt','yuv420p','-r',str(fps),'-fps_mode','cfr','-c:a','aac','-b:a','128k','-movflags','+faststart',str(movie)],check=True)
thumb=movie.with_suffix('.png');subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','1.2','-i',str(movie),'-frames:v','1',str(thumb)],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(movie)]));v=next(x for x in probe['streams'] if x['codec_type']=='video');assert (v['width'],v['height'])==(1080,1920);assert float(probe['format']['duration'])<60
manifest=dict(mode=mode,title=c['title'],file=movie.name,sha256=hashlib.sha256(movie.read_bytes()).hexdigest(),buildId=c['build'],status=c['status'],width=1080,height=1920,seconds=float(probe['format']['duration']),nativeAudio=True,nativeHud=True,gameplaySpeedScaling=False,fullGameImagePreserved=True,onlyImprovedFootage=True,background='Blurred darkened copy of the same footage',clips=records);(O/f'{mode}-montaje.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('READY',movie,manifest['seconds'],flush=True)

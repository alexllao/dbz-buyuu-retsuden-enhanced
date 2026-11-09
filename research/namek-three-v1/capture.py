from pathlib import Path
import sys,json,hashlib,subprocess
setup=Path('work/namek-simulation/record.py').read_text().split('\ntry:\n if capture_from')[0]
sys.argv=['three'];exec(compile(setup,'native-gameplay-capture-setup','exec'),globals())
sys.path.insert(0,str(Path('work/namek-three').resolve()))
from composite_three import Composite as ThreeComposite
from PIL import Image
import numpy as np
T=Path('work/namek-three');A=Path('repository/assets/concepts/namek-three-v1');V=T/'video';V.mkdir(exist_ok=True)
variantDefs=[('normal','NAMEK NORMAL'),('aldea','ALDEA DEVASTADA'),('porunga','INVOCACION DE PORUNGA')]
renderer=ThreeComposite(A/'normal.png');arts=[np.asarray(Image.open(A/(slug+'.png')).convert('RGB').resize((512,512),Image.Resampling.NEAREST)) for slug,_ in variantDefs]
fontBold='work/namek-three/arialbd.ttf';fontPlain='work/namek-three/arial.ttf'
sceneDefs=[('01-vuelo',0,280,'VUELO - DESPLAZAMIENTO - ATERRIZAJE'),('02-goku',0,32,'GOKU / BASICOS + KAMEHAMEHA'),('03-gohan',1,32,'GOHAN / BASICOS + MASENKO'),('04-vegeta',3,32,'VEGETA / BASICOS + METEOR'),('05-cell',5,32,'CELL / CRUCE + METEOR'),('06-pantalla-partida',0,400,'KAMEHAMEHA / PANTALLA PARTIDA')]
encoders=[];audit=[]

def encoder(target,width,height,vf):
 return subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{width}x{height}','-framerate',str(fps),'-i','pipe:0','-vf',vf,'-an','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',str(target)],stdin=subprocess.PIPE)

def textFilter(text,x,y,size,color='white',bold=False):
 return "drawtext=fontfile='"+(fontBold if bold else fontPlain)+"':text='"+text+"':x="+str(x)+":y="+str(y)+":fontsize="+str(size)+":fontcolor="+color

try:
 for label,cid,distance,title in sceneDefs:
  restore((N/(f'critical-{cid}.state' if cid in [3,5] else f'seed-{cid}.state')).read_bytes());wb(P1+0xbe,0);wb(P2+0xbe,0);ww(P1+0xa,300);ww(P2+0xa,300+distance);ww(P1+0xc,0);ww(P2+0xc,0);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(8):rawtick()
  oldrows=json.loads((root/(label+'.json')).read_text());encoders=[];targets=[]
  for slug,name in variantDefs:
   dest=V/slug;dest.mkdir(exist_ok=True);target=dest/(label+'-silent.mp4');targets.append(target)
   vf='scale=960:672:flags=neighbor,pad=960:764:0:92:color=0x10151c,'+','.join([textFilter(name,16,7,25,'0xffd35a',True),textFilter(title,16,40,19),textFilter('SIMULACION / FONDO NO INTEGRADO / MOVIMIENTO REAL',16,66,15,'0xcbd6e4')])
   encoders.append(encoder(target,320,224,vf))
  dest=V/'tres';dest.mkdir(exist_ok=True);target=dest/(label+'-silent.mp4');targets.append(target)
  vf='scale=1920:448:flags=neighbor,pad=1920:538:0:90:color=0x10151c,'+','.join([textFilter(name,i*640+14,6,23,'0xffd35a',True) for i,(_,name) in enumerate(variantDefs)]+[textFilter(title,14,40,20),textFilter('SIMULACION - FONDOS NO INTEGRADOS - JUEGO A VELOCIDAD NORMAL',654,43,16,'0xcbd6e4')])
  encoders.append(encoder(target,960,224,vf));audio_file=(V/(label+'.pcm')).open('wb');rasterFrames=0
  for f,ref in enumerate(oldrows):
   rawtick(ref['keys1'],ref['keys2']);assert st(P1)==ref['p'] and st(P2)==ref['e'],(label,f,'native replay differs')
   original,_,meta=renderer.frame(snap(),latest,raster=(label=='06-pantalla-partida'));sx,sy,foreground=renderer.coordinates
   frames=[original.copy() if renderer.blank else np.where(foreground[:,:,None],original,art[sy,sx]) for art in arts]
   rasterFrames+=bool(meta['rasterRowsCorrected'])
   for proc,pixels in zip(encoders,frames):proc.stdin.write(pixels.tobytes())
   triptych=np.concatenate(frames,axis=1);encoders[-1].stdin.write(triptych.tobytes())
   if f in [1,90,180,360,450,630]:Image.fromarray(triptych).resize((1920,448),Image.Resampling.NEAREST).save(V/f'{label}-qa-{f:04}.png')
  audio_file.close();audio_file=None
  for proc in encoders:proc.stdin.close();assert proc.wait()==0
  encoders=[]
  for target in targets:
   out=target.with_name(label+'.mp4')
   subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(target),'-f','s16le','-ar',str(int(av.timing.sample_rate)),'-ac','2','-i',str(V/(label+'.pcm')),'-c:v','copy','-c:a','aac','-b:a','128k','-shortest','-movflags','+faststart',str(out)],check=True)
  audit.append(dict(label=label,frames=len(oldrows),seconds=len(oldrows)/fps,allNativeActorStatesMatch=True,rasterFrames=rasterFrames));(T/'replay-audit.json').write_text(json.dumps(audit,indent=2));print('CAPTURED THREE',audit[-1],flush=True)
finally:
 for proc in encoders:
  try:proc.stdin.close();proc.wait()
  except Exception:pass
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()

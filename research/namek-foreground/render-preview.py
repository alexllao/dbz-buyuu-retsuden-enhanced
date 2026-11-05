from pathlib import Path
import json,subprocess,hashlib,shutil
D=Path('work/namek-foreground-video');O=Path('outputs/namek-primer-plano');r=json.loads((D/'report.json').read_text());motion=json.loads((D/'background-motion.json').read_text());factor=1.15;xexpr='-72'
for a,b in zip(motion,motion[1:]):
 delta=b['dx']-a['dx']
 if delta:xexpr+=f'+({2*factor*delta:.5f})*clip((n-{a["frame"]})/{b["frame"]-a["frame"]},0,1)'
files=[]
for variant in ['actual','propuesta']:
 if variant=='actual':prefix='[0:v]';inputs=[];title='ACTUAL | NAMEK - PELEA Y DESPLAZAMIENTO';note='GRABACION REAL - VELOCIDAD NORMAL'
 else:
  inputs=['-loop','1','-framerate',str(r['fps']),'-i',str(D/'tree.png')];prefix="[1:v]scale=184:368:flags=neighbor,format=rgba[tree];[0:v][tree]overlay=x='"+xexpr+"':y=116:shortest=1[scene];[scene]";title='PROPUESTA | ARBOL NAMEKIANO EN PRIMER PLANO';note='MAQUETA VISUAL - AUN NO INTEGRADO EN LA ROM'
 vf=prefix+"drawbox=x=0:y=0:w=640:h=52:color=0x10151c:t=fill,drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='"+title+"':x=10:y=6:fontsize=15:fontcolor=white,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+note+"':x=10:y=31:fontsize=12:fontcolor=0xbecbd8[v]"
 dest=D/(variant+'.mp4');subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(D/'source.mp4'),*inputs,'-filter_complex',vf,'-map','[v]','-map','0:a:0','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(dest)],check=True)
 frames=int(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames','-of','csv=p=0',str(dest)],text=True).strip());assert frames==r['frames'],(variant,frames,r['frames']);files.append("file '"+dest.resolve().as_posix()+"'")
(D/'concat.txt').write_text('\n'.join(files)+'\n');dest=O/'Namek-arbol-prueba-en-movimiento-v1.mp4';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(D/'concat.txt'),'-c','copy','-movflags','+faststart',str(dest)],check=True)
for frame in [0,100,300,500]:subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(D/'propuesta.mp4'),'-vf',f'select=eq(n\\,{frame})','-frames:v','1',str(D/f'qa-{frame}.png')],check=True)
shutil.copyfile(D/'tree.png',O/'Arbol-namekiano-transparente-v1.png')
m=dict(status='Video mockup pending user validation; no native integration',romSha256=r['romSha256'],sourceFrames=r['frames'],fps=r['fps'],frames=r['frames']*2,seconds=r['frames']*2/r['fps'],romModifiedForTree=False,postproductionTree=True,assetMethod='Built-in image_gen generated transparent tree; FFmpeg composited the video',treeNativeCompatibilityVerified=False,backgroundMotionMethod='Grayscale background template matching every4 source frames, continuous shift unwrapping',backgroundDisplacementRange=[min(x['dx'] for x in motion),max(x['dx'] for x in motion)],parallaxFactor=factor,hudUntouched=True,treeSwayImplemented=False,sourceNativeAudio=True,gameplayTimeScaling=False,video=dict(file=dest.name,sha256=hashlib.sha256(dest.read_bytes()).hexdigest()),tree=dict(file='Arbol-namekiano-transparente-v1.png',sha256=hashlib.sha256((D/'tree.png').read_bytes()).hexdigest()))
(D/'manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8');print('PASS',m['seconds'],'seconds',m['frames'],'frames')

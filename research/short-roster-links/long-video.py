from pathlib import Path
import subprocess
O=Path('outputs/Short-once-personajes-y-Cell');O.mkdir(exist_ok=True,parents=True)
vf="drawbox=x=0:y=0:w=640:h=52:color=0x10151c:t=fill,drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='CELL - BASICOS + CRUCE + METEOR':x=10:y=6:fontsize=17:fontcolor=white,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='16 impactos en esta toma - existe salida saltando antes del Meteor':x=10:y=31:fontsize=12:fontcolor=0xffd35a"
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i','work/long-chain/video/after/Cell-16-impactos.mp4','-vf',vf,'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(O/'Cell-16-impactos-toma-completa.mp4')],check=True)

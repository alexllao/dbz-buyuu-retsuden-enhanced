from pathlib import Path
import subprocess,json
P=Path('work/gravity-g2');O=Path('outputs/saltos-gravedad-G2');O.mkdir(exist_ok=True,parents=True);clips=[]
for name,explain in [('normal','SALTO NORMAL - 87 a 61 px - tiempo en el aire 0.58 s a 0.40 s'),('diagonal','SALTO DIAGONAL - aterriza antes - recorrido mas corto con la misma velocidad'),('carrera','SALTO DESDE CARRERA - 87 a 138 px - conserva duracion y recorrido')]:
 a=P/'comparison/before'/(name+'.mp4');b=P/'comparison/after'/(name+'.mp4');target=P/'comparison'/('edit-'+name+'.mp4')
 vf="[0:v]crop=640:448:0:52[l];[1:v]crop=640:448:0:52[r];[l][r]hstack=inputs=2,pad=1280:520:0:72:color=0x10151c,drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='ANTES - BASE V1.0':x=15:y=8:fontsize=24:fontcolor=white,drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='PRUEBA G2 - SOLO GOKU':x=655:y=8:fontsize=24:fontcolor=0xf5c667,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+explain+"':x=15:y=43:fontsize=18:fontcolor=white[v]"
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(a),'-i',str(b),'-filter_complex',vf,'-map','[v]','-map','1:a','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(target)],check=True)
 clips += [target.resolve()]*3
(P/'comparison/concat.txt').write_text('\n'.join("file '"+str(t).replace('\\','/')+"'" for t in clips))
out=O/'Goku-G2-saltos-antes-despues.mp4';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(P/'comparison/concat.txt'),'-c','copy','-movflags','+faststart',str(out)],check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','0.7','-i',str(out),'-frames:v','1',str(O/'comparacion.png')],check=True)
print(out)

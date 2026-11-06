from pathlib import Path
import subprocess,json,hashlib
P=Path('work/gravity-probe');O=Path('outputs/saltos-gravedad-G1');O.mkdir(parents=True,exist_ok=True);clips=[]
chapters=json.loads((P/'comparison/after/chapters.json').read_text())
for ch in chapters:
 name=ch['label'];a=P/'comparison/before'/(name+'.mp4');b=P/'comparison/after'/(name+'.mp4');target=P/'comparison'/('edit-'+name+'.mp4')
 text=name+' - '+('misma altura - nueva subida y caida' if name=='Piccolo Meteor' else ('salto mas alto y largo desde carrera' if name.endswith('carrera') else 'salto normal mas bajo'))
 vf="[0:v]crop=640:448:0:52[l];[1:v]crop=640:448:0:52[r];[l][r]hstack=inputs=2,pad=1280:520:0:72:color=0x10151c,drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='ANTES - BASE V1.0':x=15:y=8:fontsize=24:fontcolor=white,drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='PRUEBA G1 - DOS SALTOS':x=655:y=8:fontsize=24:fontcolor=0xf5c667,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+text+"':x=15:y=43:fontsize=18:fontcolor=white[v]"
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(a),'-i',str(b),'-filter_complex',vf,'-map','[v]','-map','1:a','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(target)],check=True);clips.append(target.resolve())
(P/'comparison/concat.txt').write_text('\n'.join("file '"+str(t).replace('\\','/')+"'" for t in clips))
output=O/'Saltos-y-Meteor-antes-despues-G1.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(P/'comparison/concat.txt'),'-c','copy','-movflags','+faststart',str(output)],check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','2.65','-i',str(output),'-frames:v','1',str(O/'Comparacion-salto-carrera.png')],check=True)
print(output,output.stat().st_size,flush=True)

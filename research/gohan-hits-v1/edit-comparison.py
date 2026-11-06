from pathlib import Path
import subprocess,json,hashlib,shutil
P=Path('work/gohan-hits');O=Path('outputs/v1.0-build-20261106-124607');clips=[]
for name in ['Gohan Meteor']:
 before=P/'comparison/before'/(name+'.mp4');after=P/'comparison/after'/(name+'.mp4');target=P/'comparison'/('edit-'+name+'.mp4')
 vf="[0:v]crop=640:448:0:52[l];[1:v]crop=640:448:0:52[r];[l][r]hstack=inputs=2,pad=1280:520:0:72:color=0x10151c,drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='ANTES - BUILD 10.54':x=15:y=10:fontsize=24:fontcolor=white,drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='DESPUES - BUILD 12.46':x=655:y=10:fontsize=24:fontcolor=0xf5c667,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+name+" - misma secuencia de mando y velocidad normal - sonido de la derecha':x=15:y=45:fontsize=18:fontcolor=white[v]"
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(before),'-i',str(after),'-filter_complex',vf,'-map','[v]','-map','1:a','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(target)],check=True);clips.append(target.resolve())
(P/'comparison/concat.txt').write_text('\n'.join("file '"+str(t).replace('\\','/')+"'" for t in clips))
output=O/'Gohan-Meteor-HITS-antes-despues-v1.0-build-20261106-124607.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(P/'comparison/concat.txt'),'-c','copy','-movflags','+faststart',str(output)],check=True)

print('GOHAN COMPARISON',output)

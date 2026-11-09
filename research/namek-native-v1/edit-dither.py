from pathlib import Path
import json,subprocess
P=Path('work/namek-native/dither-video');O=Path('outputs/Namek-nativo-dithering');O.mkdir(exist_ok=True,parents=True)
for side in ['before','after']:
 p=P/side/'concat.txt';p.write_text('\n'.join("file '"+(P/side/(label+'.mp4')).resolve().as_posix()+"'" for label in ['01-vuelo','02-goku']))
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(p),'-c','copy',str(P/(side+'.mp4'))],check=True)
font='work/namek-three/arialbd.ttf';plain='work/namek-three/arial.ttf'
vf="[0:v][1:v]hstack=inputs=2,scale=1280:448:flags=neighbor,pad=1280:526:0:78:color=0x10151c,drawtext=fontfile='"+font+"':text='SIN TRAMADO':x=14:y=8:fontsize=24:fontcolor=white,drawtext=fontfile='"+font+"':text='TRAMADO SELECTIVO':x=654:y=8:fontsize=24:fontcolor=0xffd35a,drawtext=fontfile='"+plain+"':text='DOS CAPTURAS REALES DEL EMULADOR / FONDO INTEGRADO EN ROM':x=14:y=47:fontsize=18:fontcolor=0xcbd6e4[v]"
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(P/'before.mp4'),'-i',str(P/'after.mp4'),'-filter_complex',vf,'-map','[v]','-map','1:a','-c:v','libx264','-crf','18','-preset','veryfast','-c:a','aac','-b:a','128k','-movflags','+faststart',str(O/'Porunga-nativo-sin-y-con-dithering.mp4')],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(O/'Porunga-nativo-sin-y-con-dithering.mp4'),'-f','null','-'],check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','9','-i',str(O/'Porunga-nativo-sin-y-con-dithering.mp4'),'-frames:v','1',str(O/'Comparacion.png')],check=True)
comparisons=[]
for label in ['01-vuelo','02-goku']:
 a=json.loads((P/'before'/(label+'.json')).read_text());b=json.loads((P/'after'/(label+'.json')).read_text());comparisons.append(dict(take=label,framesBefore=len(a),framesAfter=len(b),actorStatesIdentical=a==b))
(P/'comparison-proof.json').write_text(json.dumps(comparisons,indent=2));print(comparisons)

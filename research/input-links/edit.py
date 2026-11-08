from pathlib import Path
import subprocess,json
P=Path('work/input-links');O=Path('outputs/Buffer-enlaces-v1');O.mkdir(exist_ok=True,parents=True);fps=59.92274340431231
paths=[P/f'video/{v}/AAB-Kamehameha.mp4' for v in ['before','after']]
vf='[0:v]crop=640:448:0:52[a];[1:v]crop=640:448:0:52[b];[a][b]hstack=inputs=2,pad=1280:560:0:112:color=0x10151c'
for x,title in [(15,'ANTES - SE PIERDE EL ESPECIAL'),(655,'DESPUES - SE CONSERVA LA ORDEN')]:
 vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='"+title+f"':x={x}:y=14:fontsize=22:fontcolor=white"
vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='Mismo mando y ritmo - juego real a velocidad normal':x=15:y=54:fontsize=24:fontcolor=0xf5c667,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='A - A - B - medio circulo + A. No se amplia el aturdimiento del rival.':x=15:y=87:fontsize=20:fontcolor=white[v]"
raw=P/'video/comparison.mp4';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(paths[0]),'-i',str(paths[1]),'-filter_complex',vf,'-map','[v]','-map','1:a','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-movflags','+faststart',str(raw)],check=True)
lst=P/'video/concat.txt';lst.write_text('\n'.join("file '"+str(raw.resolve()).replace('\\','/')+"'" for _ in range(2)))
out=O/'Buffer-Kamehameha-antes-despues.mp4';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(lst),'-c','copy','-movflags','+faststart',str(out)],check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(126/fps),'-i',str(out),'-frames:v','1',str(O/'comparacion.png')],check=True)
metrics=[]
for p in paths:
 r=json.loads(p.with_suffix('.json').read_text());metrics.append(dict(side=p.parent.name,programs=sorted(set(t['p']['program'] for t in r)),damage=r[0]['e']['hp']-r[-1]['e']['hp'],hits=max(t['p']['hits'] for t in r)))
(P/'video/metrics.json').write_text(json.dumps(metrics,indent=2));print(metrics)

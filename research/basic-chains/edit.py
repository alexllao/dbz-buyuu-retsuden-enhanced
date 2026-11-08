from pathlib import Path
import json,subprocess
P=Path('work/basic-chains');O=Path('outputs/Combos-Goku-y-Short');O.mkdir(parents=True,exist_ok=True);fps=59.92274340431231;clips=[];cases=[]
for label,title in [('AAB','GOKU / A - A - B'),('AAA','GOKU / A - A - A'),('ABB-far','GOKU / A - B - B / MAS DISTANCIA')]:
 paths=[P/f'video/{side}/{label}.mp4' for side in ['before','after']];metrics=[]
 for p in paths:
  r=json.loads(p.with_suffix('.json').read_text());metrics.append(dict(damage=r[0]['e']['hp']-r[-1]['e']['hp'],hits=max(t['p']['hits'] for t in r)))
 vf=';'.join(f'[{i}:v]trim=end_frame=180,setpts=PTS-STARTPTS,crop=640:448:0:52[v{i}]' for i in range(2))+';[v0][v1]hstack=inputs=2,pad=1280:578:0:130:color=0x10151c'
 for x,heading,color,m in zip([15,655],['BASE ANTERIOR','VARIANTES DE GOKU'],['white','0xf5c667'],metrics):
  vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='"+heading+f"':x={x}:y=10:fontsize=25:fontcolor={color},drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+f"{m['hits']} HITS / {m['damage']} dano':x={x}:y=49:fontsize=23:fontcolor=white"
 vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+title+" - mismos mandos - velocidad normal':x=15:y=87:fontsize=21:fontcolor=white,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='Poses y tiempos de los golpes nativos; recuperacion cancelable tras acierto':x=15:y=112:fontsize=17:fontcolor=0xbecbd8[v]"
 out=P/f'video/comparison-{label}.mp4';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(paths[0]),'-i',str(paths[1]),'-filter_complex',vf,'-map','[v]','-map','1:a','-t',str(180/fps),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac',str(out)],check=True);clips.extend([out.resolve()]*2);cases.append(dict(label=label,metrics=metrics))
concat=P/'video/comparison-concat.txt';concat.write_text('\n'.join("file '"+str(p).replace('\\','/')+"'" for p in clips));movie=O/'Goku-cadenas-variadas-antes-despues.mp4';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-r',str(fps),'-fps_mode','cfr','-c:a','aac','-movflags','+faststart',str(movie)],check=True);(P/'comparison-cases.json').write_text(json.dumps(cases,indent=2));subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(50/fps),'-i',str(movie),'-frames:v','1',str(O/'comparacion.png')],check=True);print(cases)

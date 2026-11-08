from pathlib import Path
import json,subprocess
P=Path('work/barrage-five');O=Path('outputs/rafaga-cinco-Goku');O.mkdir(parents=True,exist_ok=True);fps=59.92274340431231;clips=[];cases=[]
for label,title in [('01 cinco impactos','GOKU - IMPACTOS REALES'),('02 contra guardia','GOKU - CONTRA GUARDIA'),('03 distancia larga','GOKU - MAS DISTANCIA')]:
 paths=[P/f'video/{side}/{label}.mp4' for side in ['before','after']];metrics=[]
 for path in paths:
  r=json.loads(path.with_suffix('.json').read_text());events=[dict(frame=i,damage=a['e']['hp']-t['e']['hp']) for i,(a,t) in enumerate(zip(r,r[1:]),1) if t['e']['hp']<a['e']['hp']];metrics.append(dict(hits=max(t['p']['hits'] for t in r),damage=sum(x['damage'] for x in events),events=events))
 vf="[0:v]crop=640:448:0:52[l];[1:v]crop=640:448:0:52[r];[l][r]hstack=inputs=2,pad=1280:570:0:122:color=0x10151c"
 for x,heading,color in [(15,'ACTUAL K4 - 3 DISPAROS','white'),(655,'PRUEBA GOKU - 5 DISPAROS','0xf5c667')]:vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='"+heading+f"':x={x}:y=10:fontsize=25:fontcolor={color}"
 for x,m in zip([15,655],metrics):vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+f"{m['hits']} HITS - {m['damage']} dano':x={x}:y=48:fontsize=24:fontcolor=white"
 vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+title+" - mismo mando - velocidad normal':x=15:y=88:fontsize=22:fontcolor=0xbecbd8[v]"
 out=P/f'video/{label}-comparison.mp4';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(paths[0]),'-i',str(paths[1]),'-filter_complex',vf,'-map','[v]','-map','1:a','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(out)],check=True);clips.append(out.resolve());cases.append(dict(label=label,metrics=metrics))
# Repetir el primer caso completo al final, sin ralentizacion.
clips.append(clips[0]);concat=P/'video/concat.txt';concat.write_text('\n'.join("file '"+str(p).replace('\\','/')+"'" for p in clips));movie=O/'Goku-rafaga-3-vs-5-comparacion.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-r',str(fps),'-fps_mode','cfr','-c:a','aac','-movflags','+faststart',str(movie)],check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','3.4','-i',str(movie),'-frames:v','1',str(O/'comparacion.png')],check=True);(P/'video-cases.json').write_text(json.dumps(cases,indent=2));print(cases)

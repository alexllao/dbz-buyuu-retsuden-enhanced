from pathlib import Path
import json,subprocess
P=Path('work/barrage-roster');O=Path('outputs/rafagas-cinco-plantel');O.mkdir(parents=True,exist_ok=True);fps=59.92274340431231;clips=[];cases=[]
for cid,name in [(0,'Goku'),(3,'Vegeta'),(5,'Cell'),(6,'A18'),(7,'Krilin'),(9,'Recoome')]:
 paths=[P/f'video/{s}/{name}.mp4' for s in ['before','after']];metrics=[]
 for path in paths:
  rows=json.loads(path.with_suffix('.json').read_text());shots=max(t['shot'] for t in rows);events=[dict(frame=i,damage=a['e']['hp']-t['e']['hp']) for i,(a,t) in enumerate(zip(rows,rows[1:]),1) if t['e']['hp']<a['e']['hp']];cost=next(t['cost'] for t in rows if t['shot']>0)
  metrics.append(dict(shots=shots,hits=max(t['p']['hits'] for t in rows),damage=sum(t['damage'] for t in events),events=events,nativeCostPerShot=cost))
 assert metrics[0]['shots']==3 and metrics[1]['shots']==metrics[1]['hits']==5
 start=0 if cid==0 else 100;n=360
 vf=';'.join(f'[{i}:v]trim=start_frame={start}:end_frame={start+n},setpts=PTS-STARTPTS,crop=640:448:0:52[v{i}]' for i in range(2))+';[v0][v1]hstack=inputs=2,pad=1280:570:0:122:color=0x10151c'
 for x,title,color,m in zip([15,655],['K4 - 3 DISPAROS','PRUEBA - 5 DISPAROS'],['white','0xf5c667'],metrics):
  vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='"+name.upper()+' / '+title+f"':x={x}:y=10:fontsize=25:fontcolor={color}"
  vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+f"{m['hits']} HITS - {m['damage']} dano':x={x}:y=49:fontsize=24:fontcolor=white"
 vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='Poses y comando propios - mismo mando - velocidad normal - sonido del juego':x=15:y=88:fontsize=21:fontcolor=0xbecbd8[v]"
 vf+=f';[1:a]atrim=start={start/fps}:end={(start+n)/fps},asetpts=PTS-STARTPTS[a]';out=P/f'video/{name}-comparison.mp4';args=['ffmpeg','-hide_banner','-loglevel','error','-y']
 for path in paths:args+=['-i',str(path)]
 args+=['-filter_complex',vf,'-map','[v]','-map','[a]','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(out)];subprocess.run(args,check=True);clips.append(out.resolve());cases.append(dict(cid=cid,name=name,metrics=metrics,trimStartFrame=start,frames=n))
concat=P/'video/concat.txt';concat.write_text('\n'.join("file '"+str(p).replace('\\','/')+"'" for p in clips));movie=O/'Rafagas-3-vs-5-seis-personajes.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-r',str(fps),'-fps_mode','cfr','-c:a','aac','-movflags','+faststart',str(movie)],check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','15.7','-i',str(movie),'-frames:v','1',str(O/'comparacion.png')],check=True);(P/'video-cases.json').write_text(json.dumps(cases,indent=2));print(cases)

from pathlib import Path
import json,subprocess
P=Path('work/jump-two');O=Path('outputs/Goku-dos-saltos');O.mkdir(parents=True,exist_ok=True);fps=59.92274340431231;clips=[];cases=[]
for mode,title in [('vertical','SALTO NORMAL VERTICAL'),('diagonal','SALTO NORMAL EN DIAGONAL'),('carrera','SALTO LARGO DESDE CARRERA'),('carrera-patada','CARRERA Y PATADA AEREA')]:
 paths=[P/f'video/{v}/{mode}.mp4' for v in ['control','candidate']];metrics=[]
 for path in paths:
  r=json.loads(path.with_suffix('.json').read_text());first=next(i for i,t in enumerate(r) if t['p']['y']<448);land=next(i for i in range(first+1,len(r)) if r[i]['p']['y']==448);metrics.append(dict(height=448-min(t['p']['y'] for t in r),takeoff=first,landing=land,airFrames=land-first,airSeconds=(land-first)/fps,range=abs(r[land]['p']['x']-r[first-1]['p']['x']),run=any(t['p']['action'] in [7,8] for t in r),damage=r[0]['e']['hp']-r[-1]['e']['hp']))
 vf="[0:v]crop=640:448:0:52[l];[1:v]crop=640:448:0:52[r];[l][r]hstack=inputs=2,pad=1280:578:0:130:color=0x10151c"
 for x,label,color,m in zip([15,655],['ANTES','PROPUESTA GOKU'],['white','0xf5c667'],metrics):
  vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='"+label+' / '+title+f"':x={x}:y=10:fontsize=21:fontcolor={color}"
  vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+f"Altura {m['height']} px - aire {m['airSeconds']:.2f} s - alcance {m['range']} px':x={x}:y=46:fontsize=21:fontcolor=white"
 vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='Carrera reparada en ambos lados - solo la derecha cambia el salto - velocidad normal':x=15:y=83:fontsize=20:fontcolor=0xbecbd8,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='Cada ejemplo se repite dos veces - K4 y seis rafagas conservadas':x=15:y=107:fontsize=17:fontcolor=0xbecbd8[v]"
 out=P/f'video/{mode}-comparison.mp4';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(paths[0]),'-i',str(paths[1]),'-filter_complex',vf,'-map','[v]','-map','1:a','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(out)],check=True);clips.extend([out.resolve()]*2);cases.append(dict(mode=mode,metrics=metrics))
concat=P/'video/concat.txt';concat.write_text('\n'.join("file '"+str(p).replace('\\','/')+"'" for p in clips));movie=O/'Goku-salto-normal-y-largo-antes-despues.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-r',str(fps),'-fps_mode','cfr','-c:a','aac','-movflags','+faststart',str(movie)],check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','0.9','-i',str(movie),'-frames:v','1',str(O/'comparacion.png')],check=True);(P/'video-cases.json').write_text(json.dumps(cases,indent=2));print(cases)

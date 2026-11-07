from pathlib import Path
import json,subprocess
P=Path('work/knockdown-k4');O=Path('outputs/derribos-K4');O.mkdir(exist_ok=True,parents=True);fps=59.92274340431231;cases=[];clips=[]
for name in ['Goku','Cell']:
 paths=[Path(f'work/knockdown-k3/comparison/after/{name}.mp4'),P/f'comparison/after/{name}.mp4'];rows=[json.loads(p.with_suffix('.json').read_text()) for p in paths];metrics=[]
 for label,r in zip(['K3','K4'],rows):
  hit=next(i for i,t in enumerate(r) if t['e']['hp']<r[0]['e']['hp']);wake=next(i for i,t in enumerate(r[hit:],hit) if t['e']['action']==21);settled=wake-1
  while settled>hit and r[settled-1]['e']['y']==448:settled-=1
  idle=next(i for i,t in enumerate(r[wake:],wake) if t['e']['program']==0)
  metrics.append(dict(variant=label,hit=hit,settled=settled,wake=wake,idle=idle,lyingSeconds=(wake-settled)/fps))
 end=metrics[0]['wake'];keys=['program','cursor','x','y','hp'];same=all(all(a['e'][k]==b['e'][k] for k in keys) for a,b in zip(rows[0][:end],rows[1][:end]));assert same
 assert metrics[1]['settled']==metrics[0]['settled'] and metrics[1]['lyingSeconds']>metrics[0]['lyingSeconds']+.20
 cases.append(dict(name=name,sameThroughOldWake=same,metrics=metrics))
 out=P/f'comparison/{name}-side-by-side.mp4'
 vf="[0:v]crop=640:448:0:52[l];[1:v]crop=640:448:0:52[r];[l][r]hstack=inputs=2,pad=1280:560:0:112:color=0x10151c"
 for x,title,color in [(15,'ANTES - K3','white'),(655,'PROPUESTA - K4','0xf5c667')]:vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='"+title+"':x="+str(x)+":y=12:fontsize=27:fontcolor="+color
 for x,m in zip([15,655],metrics):vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+name+f" - espera tumbado {m['lyingSeconds']:.2f} s':x={x}:y=51:fontsize=24:fontcolor=white"
 vf+=",drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='Mismo golpe y mandos - velocidad normal - solo se alarga la espera':x=15:y=85:fontsize=20:fontcolor=0xbecbd8[v]"
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(paths[0]),'-i',str(paths[1]),'-filter_complex',vf,'-map','[v]','-map','1:a','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(out)],check=True);clips.extend([out.resolve()]*2)
(P/'video-cases.json').write_text(json.dumps(cases,indent=2));concat=P/'comparison/concat.txt';concat.write_text('\n'.join("file '"+str(p).replace('\\','/')+"'" for p in clips));movie=O/'Derribos-K3-vs-K4-espera-tumbado.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-r',str(fps),'-fps_mode','cfr','-c:a','aac','-movflags','+faststart',str(movie)],check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(103/fps),'-i',str(movie),'-frames:v','1',str(O/'comparacion.png')],check=True);print(cases)

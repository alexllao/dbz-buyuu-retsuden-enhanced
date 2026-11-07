from pathlib import Path
import json,subprocess
P=Path('work/knockdown-k1');O=Path('outputs/derribos-K1');O.mkdir(exist_ok=True,parents=True);fps=59.92274340431231;clips=[];cases=[]
for name in ['Goku','Trunks','Piccolo','Cell','Recoome']:
 report=[]
 for side in ['before','after']:
  r=json.loads((P/f'comparison/{side}/{name}.json').read_text());hit=next(i for i,t in enumerate(r) if t['e']['hp']<r[0]['e']['hp']);moved=next(i for i,t in enumerate(r[hit+1:],hit+1) if t['e']['action'] in [1,2,7,8] and t['e']['x']!=r[i-1]['e']['x']);report.append(dict(side=side,hit=hit,movement=moved,seconds=(moved-hit)/fps,damage=r[0]['e']['hp']-r[-1]['e']['hp']));assert moved<230
 assert report[0]['damage']==report[1]['damage'];cases.append(dict(name=name,comparison=report))
 text=name+' - del golpe a caminar '+f"{report[0]['seconds']:.2f} s -> {report[1]['seconds']:.2f} s"+' - mismos mandos - velocidad normal'
 vf="[0:v]crop=640:448:0:52[l];[1:v]crop=640:448:0:52[r];[l][r]hstack=inputs=2,pad=1280:520:0:72:color=0x10151c,drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='ANTES - ROM ACTUAL':x=15:y=8:fontsize=24:fontcolor=white,drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='PRUEBA K1 - RECUPERACION BREVE':x=655:y=8:fontsize=22:fontcolor=0xf5c667,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+text+"':x=15:y=43:fontsize=18:fontcolor=white[v]"
 target=P/'comparison'/('edit-'+name+'.mp4');subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(P/f'comparison/before/{name}.mp4'),'-i',str(P/f'comparison/after/{name}.mp4'),'-filter_complex',vf,'-map','[v]','-map','1:a','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(target)],check=True);clips.append(target.resolve())
(P/'comparison/concat.txt').write_text('\n'.join("file '"+str(t).replace('\\','/')+"'" for t in clips));out=O/'Derribos-recuperacion-antes-despues-K1.mp4';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(P/'comparison/concat.txt'),'-c','copy','-movflags','+faststart',str(out)],check=True);(P/'video-cases.json').write_text(json.dumps(cases,indent=2));print(out,cases,flush=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','2.1','-i',str(out),'-frames:v','1',str(O/'comparacion.png')],check=True)

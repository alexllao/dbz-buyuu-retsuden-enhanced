from pathlib import Path
import subprocess,json
P=Path('work/meteor-impact');O=Path('outputs/meteor-impact-v1');O.mkdir(exist_ok=True,parents=True);clips=[];chapters=[];time=0;fps=59.92274340431231
for name in ['Piccolo','Goku','Gohan','Vegeta','Trunks','Cell','A18','Krilin','Freezer','Recoome']:
 rows=[json.loads((P/f'comparison/{side}/{name}.json').read_text()) for side in ['before','after']];ends=[]
 for r in rows:
  last=max(i for i,t in enumerate(r) if 0x83c<=t['p']['program']<0x860)
  end=next((i for i in range(last+1,len(r)) if r[i]['p']['program']==0 and r[i]['e']['program']==0),len(r)-1);ends.append(min(len(r),end+30))
 n=max(ends);a=P/f'comparison/before/{name}.mp4';b=P/f'comparison/after/{name}.mp4';target=P/'comparison'/('edit-'+name+'.mp4')
 vf="[0:v]crop=640:448:0:52,scale=960:672:flags=neighbor[l];[1:v]crop=640:448:0:52,scale=960:672:flags=neighbor[r];[l][r]hstack=inputs=2,pad=1920:744:0:72:color=0x10151c,drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='ANTES - V1.0':x=18:y=9:fontsize=26:fontcolor=white,drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='PRUEBA - IMPACTOS EN LA ROM':x=978:y=9:fontsize=26:fontcolor=0xf5c667,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+name+" - sacudidas en contactos y remates - sonido de la derecha - velocidad normal':x=18:y=43:fontsize=19:fontcolor=white[v]"
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(a),'-i',str(b),'-filter_complex',vf,'-map','[v]','-map','1:a','-frames:v',str(n),'-t',str(n/fps),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k',str(target)],check=True);clips.append(target.resolve());chapters.append(dict(name=name,start=time,seconds=n/fps,frames=n));time+=n/fps
(P/'comparison/concat.txt').write_text('\n'.join("file '"+str(t).replace('\\','/')+"'" for t in clips))
out=O/'Meteor-impactos-reales-antes-despues.mp4';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(P/'comparison/concat.txt'),'-c','copy','-movflags','+faststart',str(out)],check=True)
(P/'chapters.json').write_text(json.dumps(chapters,indent=2));print(out,time,out.stat().st_size,flush=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','1.3','-i',str(out),'-frames:v','1',str(O/'comparacion.png')],check=True)

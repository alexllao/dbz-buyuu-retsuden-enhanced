from pathlib import Path
import subprocess,json,hashlib
p=Path('work/combos/demo');out=Path('outputs/combos-v1');out.mkdir(parents=True,exist_ok=True)
clips=[];reports=[]
for cid,name in [(0,'Goku'),(3,'Vegeta')]:
 a=p/f'{cid:02}-base/demo.mp4';b=p/f'{cid:02}-combos/demo.mp4';dest=out/f'{name}-antes-despues.mp4'
 def banner(label):return "pad=iw:ih+32:0:32:black,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+label+"':fontsize=19:fontcolor=white:x=12:y=6"
 filters='[0:v]'+banner(name+' - v6.6 actual')+'[a];[1:v]'+banner(name+' - prueba combos')+'[b];[a][b]hstack=inputs=2[v]'
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(a),'-i',str(b),'-filter_complex',filters,'-map','[v]','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)],check=True);clips.append(dest)
 for tag in ['base','combos']:
  d=json.loads((p/f'{cid:02}-{tag}/report.json').read_text());reports.append({k:d[k] for k in ['romSha256','cid','tag','fps','frames','hits','fixture']})
 akeys=json.loads((p/f'{cid:02}-base/report.json').read_text())['trace'];bkeys=json.loads((p/f'{cid:02}-combos/report.json').read_text())['trace'];assert [x['keys'] for x in akeys]==[x['keys'] for x in bkeys]
lst=p/'concat.txt';lst.write_text(''.join("file '"+str(f.resolve()).replace('\\','/')+"'\n" for f in clips),encoding='utf-8')
final=out/'Comparacion-combos-Goku-Vegeta.mp4';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(lst),'-c','copy','-movflags','+faststart',str(final)],check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','1.3','-i',str(final),'-frames:v','1',str(out/'Comparacion-combos-captura.png')],check=True)
Path('work/combos/video-validation.json').write_text(json.dumps({'recordings':reports,'sameInputsPerPair':True,'comparisonSha256':hashlib.sha256(final.read_bytes()).hexdigest(),'comparisonBytes':final.stat().st_size,'comparisonPath':str(final),'left':'v6.6 actual','right':'Prototype normal-speed combos','silent':True},indent=2));print('Comparison video ready',final)

from pathlib import Path
import subprocess,json,hashlib
P=Path('work/combo-charge-all');O=Path('outputs/Cargas-minimas-en-combo');O.mkdir(parents=True,exist_ok=True)
labels=['01-super-kame','02-masenko','03-final-flash','04-trunks','05-cell-cruce-meteor']
parts=[]
for label in labels:
 a=P/'captures/before'/(label+'.mp4');b=P/'captures/after'/(label+'.mp4');out=P/(label+'-comparison.mp4')
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(a),'-i',str(b),'-filter_complex','[0:v][1:v]hstack=inputs=2[v]','-map','[v]','-map','1:a','-c:v','libx264','-preset','veryfast','-crf','17','-c:a','aac','-b:a','160k','-pix_fmt','yuv420p','-shortest',str(out)],check=True)
 parts.append(out.resolve().as_posix())
lst=P/'concat.txt';lst.write_text(''.join("file '"+p+"'\n" for p in parts))
video=O/'Cargas-en-combo-antes-despues-v1.0.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(lst),'-c','copy','-movflags','+faststart',str(video)],check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','2.75','-i',str(P/'05-cell-cruce-meteor-comparison.mp4'),'-frames:v','1',str(O/'comparacion-cell.png')],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(video)],text=True))
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(video),'-f','null','-'],check=True)
(P/'video.json').write_text(json.dumps(dict(file=video.as_posix(),sha256=hashlib.sha256(video.read_bytes()).hexdigest(),duration=float(probe['format']['duration']),width=probe['streams'][0]['width'],height=probe['streams'][0]['height'],sources=[json.loads((P/'captures'/v/'manifest.json').read_text()) for v in ['before','after']],audio='Native sound from the new ROM; no tempo adjustment',editing='Simultaneous comparison from first basic, same inputs, integer 2x per panel; no time warping'),indent=2))
print(video,probe['format']['duration'])

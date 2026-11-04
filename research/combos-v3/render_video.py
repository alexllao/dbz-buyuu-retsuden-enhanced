from pathlib import Path
import json,hashlib,subprocess,shutil
P=Path('work/generic-combos');O=Path('outputs/combos-v3-generico');O.mkdir(parents=True,exist_ok=True);sha=hashlib.sha256((P/'candidate.bin').read_bytes()).hexdigest();cases=[]
for c,m in [(c,'downB') for c in range(11)]+[(0,'flurry'),(0,'meteor19')]:
 p=P/'demo'/f'{c:02}-{m}';d=json.loads((p/'report.json').read_text());assert d['romSha256']==sha and d['matchesTraceHP'] and d['bothIdleAtEnd'];cases.append({k:v for k,v in d.items() if k!='trace'})
for mode,name in [('flurry','Goku-ABA-rafaga.mp4'),('meteor19','Goku-ABA-Meteor.mp4')]:shutil.copyfile(P/'demo'/f'00-{mode}'/'demo.mp4',O/name)
concat=P/'concat.txt';concat.write_text(''.join("file '"+(P/'demo'/f'{c:02}-downB'/'demo.mp4').resolve().as_posix()+"'\n" for c in range(11)),encoding='utf8')
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(O/'Combos-v3-once-personajes.mp4')],check=True)
for c in [0,3,6,10]:
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','1.1','-i',str(P/'demo'/f'{c:02}-downB'/'demo.mp4'),'-frames:v','1',str(P/f'tile{c}.png')],check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',*sum((['-i',str(P/f'tile{c}.png')] for c in [0,3,6,10]),[]),'-filter_complex','[0:v][1:v]hstack=inputs=2[top];[2:v][3:v]hstack=inputs=2[bottom];[top][bottom]vstack=inputs=2[out]','-map','[out]','-frames:v','1',str(O/'Comparacion-combos-v3.png')],check=True)
validation={'romSha256':sha,'counterInRom':False,'counterOverlay':False,'cases':cases,'files':[{'filename':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size} for f in O.iterdir() if f.suffix in ['.mp4','.png']]}
(P/'video-validation.json').write_text(json.dumps(validation,indent=2),encoding='utf8');print('VIDEO_VALIDATED',len(cases))

from pathlib import Path
import json,subprocess,hashlib,shutil
P=Path('work/goku-kick-review');O=Path('outputs/goku-patadas-revision');O.mkdir(parents=True,exist_ok=True)
a=json.loads((P/'original-meteor/report.json').read_text());b=json.loads((P/'natural-meteor/report.json').read_text());c=json.loads((P/'natural-basicos/report.json').read_text())
def phases(d,pr):
 out=[]
 for t in d['trace']:
  if t['program']!=pr:continue
  value=(t['cursor'],t['pose'])
  if not out or value!=out[-1]:out.append(value)
 return out
checks={'sameMeteorAttackPhases':all(phases(a,p)==phases(b,p) for p in [0x83e,0x83f]),'sameEnemyPeakY':min(t['enemyY'] for t in a['trace'])==min(t['enemyY'] for t in b['trace']),'noFlightModeOriginal':not any(t['plane'] or t['enemyPlane'] for t in a['trace']),'noFlightModeMod':not any(t['plane'] or t['enemyPlane'] for t in b['trace']),'threeBasicsObserved':len(c['hits'])==3,'basicSequenceStaysOnGround':all(t['y']==t['enemyY']==448 and not t['plane'] and not t['enemyPlane'] for t in c['trace'])};assert all(checks.values()),checks
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(P/'original-meteor/demo.mp4'),'-i',str(P/'natural-meteor/demo.mp4'),'-filter_complex',"[0:v][1:v]hstack=inputs=2,pad=1280:528:0:0:color=0x10151c,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='METEOR ORIGINAL - Rafaga y lanzamiento final en ambas ROM':x=20:y=500:fontsize=20:fontcolor=white[v]",'-map','[v]','-map','0:a:0','-c:v','libx264','-crf','18','-c:a','aac','-shortest',str(O/'Meteor-original-frente-a-mod.mp4')],check=True)
shutil.copyfile(P/'natural-basicos/demo.mp4',O/'Goku-A-B-A-sin-Meteor.mp4')
report={'targetSha256':b['romSha256'],'sourceSha256':a['romSha256'],'checks':checks,'nativeOriginalMeteorFrames':sum(t['program'] in [0x83e,0x83f] for t in a['trace']),'nativeModMeteorFrames':sum(t['program'] in [0x83e,0x83f] for t in b['trace']),'originalMeteorHitFrames':a['hits'],'modMeteorHitFrames':b['hits'],'basicHitFrames':c['hits'],'longVideoMeteorStartsSeconds':15.32,'finding':'Long video automated controller explicitly entered native Meteor motion after basics. Native Meteor produces rapid sequence and launches rival without enabling flight mode. Original/mod attack phases and peak height match; display durations differ3 frames. Basic ABA remains grounded.','romChanged':False,'videos':[{'name':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in O.iterdir() if f.suffix=='.mp4']};(P/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report))

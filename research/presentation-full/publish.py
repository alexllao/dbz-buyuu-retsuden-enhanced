from pathlib import Path
import json,hashlib,shutil,gzip,subprocess
P=Path('work/presentation-full');R=Path('repository');O=Path('outputs/presentacion-completa-v1.0');sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf8',newline='\n')
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
d=json.loads((P/'presentation.json').read_text());assert d['romSha256']==sha(Path('work/piccolo-hits/candidate.bin').read_bytes());assert not d['romChanged'] and not d['gameplayTimeScaling'] and d['nativeAudio'] and d['nativeHitsHud'];assert len(d['chapters'])==26
clips={c['label']:c for c in d['chapters']}
for name,hits in [('combo-3-ABA-meteor',11),('combo-5-ABA-meteor',16),('06 piccolo meteor',9),('combo-0-AAB-flurry',6),('combo-1-ABA-masenko',4)]:assert clips[name]['maxHitsP1']==hits
assert clips['p2-crosses-meteor']['maxHitsP2']==3 and clips['p2-crosses-meteor']['damageP1']>0
roster=[]
for cid in range(11):
 folder='piccolo-hits' if cid in [0,1,2,3,5] else 'presentation-full';info=json.loads(Path(f'work/{folder}/routes/{cid}/report.json').read_text());assert info['romSha256']==d['romSha256'] and info['cid']==cid;roster.append(dict(cid=cid,stage=info['stage']))
assert len(set(r['stage'] for r in roster))==9
media=[]
for key in ['video','compactVideo']:
 rec=d[key];source=O/Path(rec['path']).name;assert sha(source.read_bytes())==rec['sha256'];cp(source,R/rec['path']);media.append(dict(path=rec['path'],sha256=rec['sha256'],bytes=source.stat().st_size))
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,width,height','-of','json',str(source)],text=True));assert abs(float(probe['format']['duration'])-d['seconds'])<.1
 # Check actual muxed packet times, including the small encode-timebase differences at cuts.
 packets=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_packets','-show_entries','packet=stream_index,dts_time','-of','json',str(source)],text=True));last={}
 for packet in packets['packets']:
  if 'dts_time' not in packet:continue
  stream=packet['stream_index'];time=float(packet['dts_time']);assert stream not in last or time>last[stream],(key,stream,time,last.get(stream));last[stream]=time
assert d['compactVideo']['bytes']<20*1024*1024
cp(O/'captura.png',R/'assets/media/presentation-full/captura.png')
for c in d['chapters']:
 source=Path(c['source']).with_suffix('.json');assert sha(source.read_bytes())==c['traceSha256'];dest=R/'evidence/presentation-full/traces'/f'{c["index"]:02}-{c["label"]}.json.gz';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(gzip.compress(source.read_bytes(),mtime=0))
summary=dict(passed=True,romSha256=d['romSha256'],buildId=d['buildId'],romChanged=False,gameplayTimeScaling=False,nativeAudio=True,nativeHitsHud=True,seconds=d['seconds'],takes=len(d['chapters']),roster=roster,stages=9,comboTakes=8,meteorAndFinisherTakes=9,media=media,chapters=d['chapters'],staging=d['staging'],limitations=['Coordinated human-port inputs and staged native states for a presentation; not an unedited competitive match.','Counter windows do not imply every showcased link is inescapable.','Only footage from the current ROM; portrait HUD, new shake, foreground objects and stage10 proposals not integrated.'])
write(R/'evidence/presentation-full/validation.json',json.dumps(summary,ensure_ascii=False,indent=2)+'\n');write(R/'evidence/presentation-full/presentation.json',json.dumps(d,ensure_ascii=False,indent=2)+'\n');write(O/'version-y-contenido.json',json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
for name in ['record.py','probe.py','probe-specials.py','prepare.py','edit.py','compact.py','publish.py']:cp(P/name,R/'research/presentation-full'/name)
cp(R/'docs/mejoras-frente-original.md',O/'Mejoras-frente-original.md')
mail=(R/'docs/correo-presentacion.md').read_text(encoding='utf8').replace('# Borrador de correo\n\n','').replace('**Asunto:','Asunto:').replace('Mega Drive**','Mega Drive');write(O/'Correo-para-canal-retro.txt',mail)
print('PUBLISHED',round(d['seconds'],2),'seconds',len(d['chapters']),'takes',round(d['compactVideo']['bytes']/1024/1024,2),'MiB compact')

from pathlib import Path
import json,subprocess,hashlib
P=Path('work/shake-varied-preview');O=Path('outputs/shake-varied-preview');O.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
routes=[('0-guardia-demo','BLOQUEOS','BLOQUEOS SUAVES'),('0-cambio-rafaga','ATAQUE MULTIGOLPE','CONTACTOS SUAVES - REMATE B'),('0-meteor-solo','METEOR DE GOKU','DOS CONTACTOS SUAVES - FINAL B'),('0-comboAAA-cambio-meteor','GOLPES - CRUCE - METEOR','BASICOS SUAVES - METEOR CON FINAL B')]
files=[];chapters=[];clips=[];total=0;fps=None
for index,(route,label,proposedLabel) in enumerate(routes):
 d=Path('work/hits-hud-v3/video')/route;src=d/'route.mp4';r=json.loads((d/'report.json').read_text());t=r['trace'];fps=r['fps'];assert r['controlReturned']
 if route=='0-guardia-demo':
  events=[dict(frame=x['f'],kind='guard',nativePixels=1) for prev,x in zip(t,t[1:]) if x['e']['action']==10 and prev['e']['action']!=10]
 elif route=='0-cambio-rafaga':
  events=[dict(frame=x['frame'],kind='multihit',nativePixels=1) for x in r['damageEvents']];events[-1].update(kind='finisher-B',nativePixels=2)
 else:
  events=[dict(frame=x['f'],kind='basic',nativePixels=1) for prev,x in zip(t,t[1:]) if x['p']['hits']>prev['p']['hits'] and x['p']['hitTTL']>0]
  assert len(events)==(3 if route=='0-meteor-solo' else 6)
  events[-1].update(kind='meteor-finisher-B',nativePixels=2)
 assert len(events)==(6 if index==3 else 3)
 assert all(t[e['frame']]['e']['action']!=0 for e in events)
 for variant in ['actual','propuesta']:
  ex='0';ey='0'
  if variant=='propuesta':
   for e in events:
    amplitude=e['nativePixels']*2
    for j,v in enumerate([1,-1,.5,-.5]):ex+=f'+({v*amplitude})*eq(n,{e["frame"]+j})'
    for j,v in enumerate([0,.5,0,-.5]):
     if v:ey+=f'+({v*amplitude/3})*eq(n,{e["frame"]+j})'
  title=('ACTUAL | '+label if variant=='actual' else 'PROPUESTA | '+proposedLabel)
  note=('MISMA GRABACION - VELOCIDAD NATURAL' if variant=='actual' else 'PRUEBA VISUAL - AUN NO INTEGRADA EN LA ROM')
  vf=f"[0:v]split=2[base][world];[world]crop=628:360:x='6+{ex}':y='120+{ey}',scale=640:368:flags=neighbor[moved];[base][moved]overlay=0:116,drawbox=x=0:y=0:w=640:h=52:color=0x10151c:t=fill,drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='{title}':x=10:y=6:fontsize=15:fontcolor=white,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='{note}':x=10:y=31:fontsize=12:fontcolor=0xbecbd8[v]"
  dest=P/f'{index:02}-{variant}.mp4';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),'-filter_complex',vf,'-map','[v]','-map','0:a:0','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k',str(dest)],check=True)
  frames=int(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames','-of','csv=p=0',str(dest)],text=True).strip());assert frames==r['frames']
  chapters.append(dict(route=route,variant=variant,start=total/fps,frames=frames,label=title));total+=frames;files.append("file '"+dest.resolve().as_posix()+"'")
 clips.append(dict(route=route,sourceRom=r['romSha256'],sourceFrames=r['frames'],sourceVideoSha256=sha(src.read_bytes()),sourceReportSha256=sha((d/'report.json').read_bytes()),events=events,controlReturned=r['controlReturned']))
(P/'concat.txt').write_text('\n'.join(files)+'\n',encoding='utf-8');dest=O/'Impactos-variados-actual-y-propuesta.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(P/'concat.txt'),'-c','copy','-movflags','+faststart',str(dest)],check=True)
frames=int(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames','-of','csv=p=0',str(dest)],text=True).strip());assert frames==total
manifest=dict(passed=True,romModifiedForShake=False,postproductionShake=True,previewOnly=True,sourceNativeAudio=True,nativeTiming=True,hudKeptSteady=True,frameCountPreserved=True,frames=total,fps=fps,seconds=total/fps,policy=dict(normalNativePixels=1,guardNativePixels=1,intermediateMultihitNativePixels=1,finisherNativePixels=2,finisherMatchesEarlierVariant='B',shakeOnWhiffOrSideSwitch=False),clips=clips,chapters=chapters,video=dict(filename=dest.name,sha256=sha(dest.read_bytes())),status='Pending visual validation; no new shake in ROM')
(P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8');print('PASS',total,'frames',total/fps,'seconds',sum(len(x['events']) for x in clips),'contact events per pass')

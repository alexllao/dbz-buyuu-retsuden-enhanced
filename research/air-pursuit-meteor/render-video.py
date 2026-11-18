from pathlib import Path
import json,subprocess,hashlib,concurrent.futures
P=Path('work/air-pursuit-fall');D=P/'render';O=Path('outputs/Persecucion-Aerea-Meteor')
for p in [D,O]:p.mkdir(parents=True,exist_ok=True)
capture=json.loads((P/'captures/manifest.json').read_text());build=json.loads((P/'build.json').read_text());fps=capture['fps'];assert capture['romSha256']==build['targetSha256']
jobs=[];scenes=[]
def draw(vf,name,value,y,size,color='white',bold=False):
 f=D/(name+'.txt');f.write_text(value,encoding='utf-8');escape=f.resolve().as_posix().replace(':','\\:');font='arialbd.ttf' if bold else 'arial.ttf'
 return vf+f",drawtext=fontfile='work/namek-three/{font}':textfile='{escape}':x=18:y={y}:fontsize={size}:fontcolor={color}"
for i,take in enumerate(capture['takes']):
 source=P/'captures'/(take['label']+'.mp4');rows=json.loads(source.with_suffix('.json').read_text());n=450 if take['cid']==0 else 520
 expected=0x83e if take['cid']==0 else 0x846;assert take['lastDamageFrame']<n and expected in take['programs']
 assert rows[n-1]['p']['program']<0x400 and rows[n-1]['p']['y']==448
 vf=f'[0:v]trim=start_frame=0:end_frame={n},setpts=PTS-STARTPTS,scale=960:672:flags=neighbor,pad=960:850:0:88:color=0x0b1520'
 character='GOKU' if take['cid']==0 else 'VEGETA'
 vf=draw(vf,f'{i}-head',character+' / PERSECUCION + DOS GOLPES + METEOR',12,28,'0xffd46b',True)
 vf=draw(vf,f'{i}-meta','ROM REAL / VELOCIDAD NORMAL / v1.0 / '+build['buildId'],51,20,'0xc8d9dd')
 vf=draw(vf,f'{i}-cmd','TRAS LANZAR: ↑ + C / A, B / COMANDO DEL METEOR DURANTE LA CAIDA',776,23,'0xffd46b')
 vf=draw(vf,f'{i}-credit','ALEX LLAO / PROTOTIPO / EL METEOR SE INICIA AL ATERRIZAR',813,19,'0xc8d9dd')
 duration=n/fps;vf+=f'[v];[0:a]atrim=start=0:end={duration},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={duration-.018}:d=0.018[a]'
 target=D/f'{i:02}.mp4';jobs.append((source,target,vf));scenes.append(dict(label=take['label'],frames=n,seconds=duration,sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),lastDamageFrame=take['lastDamageFrame']))
def render(job):
 source,target,vf=job
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-filter_complex_threads','1','-i',str(source),'-filter_complex',vf,'-map','[v]','-map','[a]','-r',str(fps),'-c:v','libx264','-preset','veryfast','-threads','2','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k',str(target)],check=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(render,jobs))
listing=D/'concat.txt';listing.write_text('\n'.join("file '"+j[1].resolve().as_posix()+"'" for j in jobs),encoding='utf-8')
target=O/'DBZ-Persecucion-Aerea-Combos-Meteor.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(listing),'-c:v','copy','-c:a','aac','-b:a','160k','-af','aresample=async=1:first_pts=0','-movflags','+faststart',str(target)],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,codec_name,width,height,r_frame_rate','-of','json',str(target)],text=True))
assert 32<float(probe['format']['duration'])<34
for i,sec in enumerate([1.7,5.5,10,14,18,23,27,31]):subprocess.run(['ffmpeg','-v','error','-y','-ss',str(sec),'-i',str(target),'-frames:v','1',str(O/f'Vista-{i+1}.png')],check=True)
manifest=dict(date='2026-11-18',romBuild=build['buildId'],romSha256=capture['romSha256'],realROMGameplay=True,normalSpeed=True,fullGameAndHUD=True,integerScale=3,gameRect=[0,88,960,672],seconds=float(probe['format']['duration']),scenes=scenes,file=str(target.resolve()),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),editing='Four continuous real sequences including complete Meteor and recovery, native audio, captions outside game; no speed changes.',probe=probe)
(O/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');(P/'video-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');print('VIDEO READY',manifest['seconds'],target,flush=True)


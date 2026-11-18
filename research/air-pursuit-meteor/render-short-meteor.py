"""Short vertical a velocidad nativa; conserva toda la pantalla y sonido de ROM."""
from pathlib import Path
import json,subprocess,hashlib,concurrent.futures
P=Path('work/air-pursuit-fall');D=P/'render-short-meteor';O=Path('outputs/YouTube-Short-Meteor-Aereo')
for p in [D,O]:p.mkdir(parents=True,exist_ok=True)
capture=json.loads((P/'captures/manifest.json').read_text());build=json.loads((P/'build.json').read_text());fps=capture['fps']
assert capture['romSha256']==build['targetSha256']

def draw(vf,key,value,y,size,color='white',bold=False):
 p=D/(key+'.txt');p.write_text(value,encoding='utf-8');escaped=p.resolve().as_posix().replace(':','\\:')
 font='arialbd.ttf' if bold else 'arial.ttf'
 return vf+f",drawtext=fontfile='work/namek-three/{font}':textfile='{escaped}':x=(w-text_w)/2:y={y}:fontsize={size}:fontcolor={color}"

jobs=[];clips=[]
for i,take in enumerate(capture['takes']):
 caption='METEOR DE GOKU' if take['cid']==0 else 'METEOR DE VEGETA'
 source=P/'captures'/(take['label']+'.mp4');rows=json.loads(source.with_suffix('.json').read_text());n=450 if take['cid']==0 else 520;duration=n/fps
 expected=0x83e if take['cid']==0 else 0x846
 assert take['second'] and expected in take['programs'] and take['lastDamageFrame']<n
 assert rows[n-1]['p']['program']<0x400 and rows[n-1]['p']['y']==448
 assert all(t['stage']==6 and t['variant']==['normal','aldea','porunga'].index(take['scenario'])+1 for t in rows[:n])
 vf=f'[0:v]trim=start_frame=0:end_frame={n},setpts=PTS-STARTPTS,scale=960:672:flags=neighbor,pad=1080:1920:60:560:color=0x0b1520'
 vf+=",drawbox=x=60:y=540:w=960:h=3:color=0xe7c269:t=fill,drawbox=x=60:y=1249:w=960:h=3:color=0xe7c269:t=fill"
 for key,value,y,size,color,bold in [('dbz','DRAGON BALL Z',145,45,'0xd5dce6',False),('headline','¡REMATE METEOR!',245,76,'0xffd46b',True),('game','BUYUU RETSUDEN ENHANCED',365,39,'white',True),('tag','NUEVOS COMBOS / PROTOTIPO',465,30,'0xc8d9dd',False),('action',caption,1325,49,'0xffd46b',True),('speed','ROM REAL / SIN ACELERAR',1515,29,'0xc8d9dd',False),('credit','ALEX LLAO',1640,38,'white',True),('build','v1.0 / '+build['buildId'],1710,24,'0x90a4b5',False)]:vf=draw(vf,f'{i}-{key}',value,y,size,color,bold)
 for j,(words,begin,end) in enumerate([('LANZA AL RIVAL',0,1.15),('PERSIGUE Y ENLAZA DOS GOLPES',1.15,2.7),('¡REMATA CON EL METEOR!',2.7,duration)]):
  vf=draw(vf,f'{i}-step-{j}',words,1420,32,'white',True)+f":enable='gte(t,{begin})*lt(t,{end})'"
 vf+=f'[v];[0:a]atrim=start=0:end={duration},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={duration-.018}:d=0.018[a]'
 target=D/f'{i:02}.mp4';jobs.append((source,target,vf));clips.append(dict(label=take['label'],frames=n,seconds=duration,sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),lastDamageFrame=take['lastDamageFrame'],caption=caption))

def render(job):
 source,target,vf=job
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-filter_complex_threads','1','-i',str(source),'-filter_complex',vf,'-map','[v]','-map','[a]','-r',str(fps),'-fps_mode','cfr','-c:v','libx264','-preset','veryfast','-threads','2','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k',str(target)],check=True)
 print('Rendered',target.name,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(render,jobs))
listing=D/'concat.txt';listing.write_text('\n'.join("file '"+j[1].resolve().as_posix()+"'" for j in jobs),encoding='utf-8')
target=O/'DBZ-Combos-Aereos-Meteor-Short.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(listing),'-c:v','copy','-c:a','aac','-b:a','160k','-af','aresample=async=1:first_pts=0','-movflags','+faststart',str(target)],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,codec_name,width,height,r_frame_rate','-of','json',str(target)],text=True))
stream=next(s for s in probe['streams'] if s['codec_type']=='video');assert (stream['width'],stream['height'])==(1080,1920) and 32<float(probe['format']['duration'])<34
for index,sec in enumerate([.6,1.7,5.5,10,14,18,23,27,31]):subprocess.run(['ffmpeg','-v','error','-y','-ss',str(sec),'-i',str(target),'-frames:v','1',str(O/f'Vista-{index+1}.png')],check=True)
manifest=dict(date='2026-11-18',status='Gameplay prototype; user/gamepad validation pending.',romBuild=build['buildId'],romSha256=capture['romSha256'],realROMGameplay=True,normalSpeed=True,fullGameAndHUD=True,nativeSize=[320,224],integerScale=3,gameRect=[60,560,960,672],clips=clips,seconds=float(probe['format']['duration']),file=str(target.resolve()),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),editing='Four continuous sequences including complete Meteor and recovery, cuts between takes, no acceleration or interpolated motion; native audio and timed captions outside game.',probe=probe)
(O/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');(P/'short-meteor-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(O/'Texto-YouTube.txt').write_text('TITULO\n¡Combos aéreos + Meteor en Dragon Ball Z de Mega Drive! 🔥\n\nDESCRIPCION\nLanzamiento, persecución aérea y remate Meteor con Goku y Vegeta 🔥 Nueva prueba de mi mod de Buyuu Retsuden, desarrollado a ratos libres con ayuda de IA. Gameplay real, sin acelerar. ¿Qué os parece?\n#DragonBallZ #MegaDrive #RomHack #Shorts\n',encoding='utf-8')
print('SHORT READY',manifest['seconds'],target,flush=True)


from pathlib import Path
import json,subprocess,hashlib,concurrent.futures
P=Path('work/namek-r10-short');D=P/'render';O=Path('outputs/YouTube-Short-Namek-R10')
for p in [D,O]:p.mkdir(parents=True,exist_ok=True)
fps=59.92274340431231;rom=Path('work/namek-native-r10/integrated.bin');expected='85d7090885e83cba884ecaf161c1913feb80a118d0aa3c86f58f7945de2483cf'
assert hashlib.sha256(rom.read_bytes()).hexdigest()==expected
scenes=[('normal','02-crosses-meteor',0,322,'NAMEK','3 CRUCES + METEOR'),('aldea','01-vegeta-finalflash',0,190,'NAMEK DEVASTADO','COMBO + FINAL FLASH'),('aldea','02-vegeta-meteor',0,322,'NAMEK DEVASTADO','METEOR DE VEGETA'),('porunga','01-cell-chain',0,678,'PORUNGA','COMBO + CRUCE + METEOR'),('normal','01-goku-super',0,286,'NAMEK','SUPER KAMEHAMEHA')]

def textfile(name,value):
 p=D/(name+'.txt');p.write_text(value,encoding='utf-8');return p.resolve().as_posix().replace(':','\\:')

def draw(vf,key,value,y,size,color='white',bold=False):
 font='arialbd.ttf' if bold else 'arial.ttf'
 return vf+f",drawtext=fontfile='work/namek-three/{font}':textfile='{textfile(key,value)}':x=(w-text_w)/2:y={y}:fontsize={size}:fontcolor={color}"

jobs=[];records=[];checks=[]
for i,(slug,label,first,last,stage,caption) in enumerate(scenes):
 source=P/'captures'/slug/(label+'.mp4');report=json.loads(source.with_name(label+'-report.json').read_text());rows=json.loads(source.with_suffix('.json').read_text())
 assert report['romSha256']==expected and 0<=first<last<=len(rows)
 assert all(t['physicalStage']==6 and t['nativeVariant']==['normal','aldea','porunga'].index(slug)+1 for t in rows[first:last])
 n=last-first;duration=n/fps
 vf=f'[0:v]trim=start_frame={first}:end_frame={last},setpts=PTS-STARTPTS,crop=640:448:0:64,scale=320:224:flags=neighbor,scale=960:672:flags=neighbor,pad=1080:1920:60:560:color=0x0b1520'
 vf+=",drawbox=x=60:y=540:w=960:h=3:color=0xe7c269:t=fill,drawbox=x=60:y=1249:w=960:h=3:color=0xe7c269:t=fill"
 vf=draw(vf,f'{i}-dbz','DRAGON BALL Z',150,44,'0xd5dce6')
 vf=draw(vf,f'{i}-namek','NAMEK RENACE',245,82,'0xffd46b',True)
 vf=draw(vf,f'{i}-game','BUYUU RETSUDEN ENHANCED',365,39,'white',True)
 vf=draw(vf,f'{i}-stage',stage,465,34,'0xc8d9dd')
 vf=draw(vf,f'{i}-action',caption,1330,45,'0xffd46b',True)
 vf=draw(vf,f'{i}-native','GAMEPLAY REAL / VELOCIDAD NORMAL',1435,28,'0xc8d9dd')
 vf=draw(vf,f'{i}-platform','MEGA DRIVE / GENESIS',1505,33,'white')
 vf=draw(vf,f'{i}-credit','ALEX LLAO',1640,37,'white',True)
 vf=draw(vf,f'{i}-version','v1.0 / 20261110-094744',1705,24,'0x90a4b5')
 vf+=f'[v];[0:a]atrim=start={first/fps}:end={last/fps},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={max(0,duration-.018)}:d=0.018[a]'
 target=D/f'{i:02}.mp4';jobs.append((source,target,vf))
 records.append(dict(source=source.as_posix(),sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),stage=slug,label=label,firstFrame=first,lastFrame=last,frames=n,seconds=duration,caption=caption,maxHitsInExcerpt=max(t['p']['hits'] for t in rows[first:last]),programs=sorted({t['p']['program'] for t in rows[first:last]})))

def render(job):
 source,target,vf=job
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-filter_complex_threads','1','-i',str(source),'-filter_complex',vf,'-map','[v]','-map','[a]','-r',str(fps),'-fps_mode','cfr','-c:v','libx264','-preset','veryfast','-threads','2','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k',str(target)],check=True)
 print('Rendered',target.name,flush=True)

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(render,jobs))
listing=D/'concat.txt';listing.write_text('\n'.join("file '"+job[1].resolve().as_posix()+"'" for job in jobs),encoding='utf-8')
target=O/'DBZ-Namek-R10-Short-30s.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(listing),'-c:v','copy','-c:a','aac','-b:a','160k','-af','aresample=async=1:first_pts=0','-movflags','+faststart',str(target)],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,codec_name,width,height,r_frame_rate','-of','json',str(target)],text=True))
video=next(t for t in probe['streams'] if t['codec_type']=='video');assert (video['width'],video['height'])==(1080,1920) and 29<float(probe['format']['duration'])<32
subprocess.run(['ffmpeg','-v','error','-y','-ss','1.8','-i',str(target),'-frames:v','1',str(O/'Portada-Short-Namek-R10.png')],check=True)
for t,name in [(1,'Cruces'),(7,'Final-Flash'),(12,'Meteor-Vegeta'),(22,'Meteor-Cell'),(28,'Super-Kamehameha')]:
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(target),'-frames:v','1',str(O/(name+'.png'))],check=True)
manifests=[json.loads((P/'captures'/slug/'capture-manifest.json').read_text()) for slug in ['normal','aldea','porunga']]
assert len(manifests[0]['sideSwitches'])==3 and len(manifests[2]['sideSwitches'])==1
assert hashlib.sha256(rom.read_bytes()).hexdigest()==expected
manifest=dict(date='2026-11-10',romBuild='20261110-094744',romSha256=expected,romUnchanged=True,realROMGameplay=True,gameRect=[60,560,960,672],nativeGameSize=[320,224],integerGameScale=3,fullGameAndHUDVisible=True,width=1080,height=1920,seconds=float(probe['format']['duration']),fps=fps,gameSpeedChanged=False,postproductionBackgroundReplacement=False,editing='Five continuous native excerpts, hard cuts between takes, no speed ramps. Native audio with12/18ms edge fades; no added music.',scenes=records,captures=manifests,publication='Local deliverable for user to upload; not published to YouTube/GitHub.',file=dict(path=target.resolve().as_posix(),bytes=target.stat().st_size,sha256=hashlib.sha256(target.read_bytes()).hexdigest()),probe=probe)
(O/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8');(P/'short-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(O/'Texto-YouTube.txt').write_text('TITULO\nNamek renace en Mega Drive | DBZ Buyuu Retsuden Enhanced\n\nDESCRIPCION\nCombos, cambios de lado, Meteor y Super Kamehameha en los nuevos Namek. Gameplay real de mi mod, desarrollado a ratos libres con ayuda de IA.\n#DragonBallZ #MegaDrive #Shorts\n',encoding='utf-8')
print('SHORT READY',manifest['seconds'],target,flush=True)

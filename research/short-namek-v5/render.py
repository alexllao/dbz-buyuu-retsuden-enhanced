from pathlib import Path
import json,subprocess,hashlib,concurrent.futures,shutil
P=Path('work/namek-v5-short');D=P/'render';O=Path('outputs/YouTube-Short-Namek-V5')
for p in [D,O]:p.mkdir(parents=True,exist_ok=True)
fps=59.92274340431231;expected='ed28bb56d207f0d0fd12f1cd1e6eff5597c0f8344e6a7bcf39c8b4017c89f2a8'
assert hashlib.sha256(Path('work/namek-native-v5/integrated.bin').read_bytes()).hexdigest()==expected
scenes=[
 ('work/namek-v5-short/captures/normal/01-carrera.mp4',332,1000,'NAMEK','FINAL FLASH + CARRERA','normal','Vegeta controlled by native CPU'),
 ('work/namek-native-v5/promo/aldea/01-vuelo.mp4',20,230,'NAMEK DEVASTADO','COMBATE EN EL AIRE','aldea','Human input flight route'),
 ('work/namek-v5-short/captures/aldea/02-onda-partida.mp4',160,771,'NAMEK DEVASTADO','KAMEHAMEHA','aldea','Human Goku half-circle + A'),
 ('work/namek-native-v5/promo/porunga/02-goku.mp4',0,210,'PORUNGA','GOLPES + ONDA DE KI','porunga','Human Goku basics and Kamehameha'),
 ('work/namek-native-v5/promo/porunga/01-vuelo.mp4',80,220,'PORUNGA','VUELO Y DESPLAZAMIENTO','porunga','Human input flight route'),
 ('work/namek-v5-short/captures/porunga/02-onda-partida.mp4',160,776,'PORUNGA','KAMEHAMEHA A DISTANCIA','porunga','Human Goku half-circle + A')]
def escaped(p):return p.resolve().as_posix().replace(':','\\:')
def textfile(name,text):
 p=D/(name+'.txt');p.write_text(text,encoding='utf-8');return escaped(p)
def draw(vf,name,text,y,size,color='white',bold=False):
 font='arialbd.ttf' if bold else 'arial.ttf'
 return vf+f",drawtext=fontfile='work/namek-three/{font}':textfile='{textfile(name,text)}':x=(w-text_w)/2:y={y}:fontsize={size}:fontcolor={color}"
jobs=[];records=[]
for i,(source,first,last,stage,label,slug,control) in enumerate(scenes):
 path=Path(source);assert '/namek-native-v5/' in path.as_posix() or '/namek-v5-short/captures/' in path.as_posix()
 assert 'comparacion' not in path.name and 'before' not in path.as_posix()
 report=json.loads(path.with_name(path.stem+'-report.json').read_text());assert report['romSha256']==expected
 rows=json.loads(path.with_suffix('.json').read_text());assert 0<=first<last<=len(rows)
 v={'normal':1,'aldea':2,'porunga':3}[slug];assert all(t['physicalStage']==6 and t['nativeVariant']==v for t in rows[first:last])
 n=last-first;duration=n/fps
 vf=f'[0:v]trim=start_frame={first}:end_frame={last},setpts=PTS-STARTPTS,crop=960:672:0:82,scale=1080:756:flags=neighbor,pad=1080:1920:0:500:color=0x10151c'
 vf=draw(vf,f'{i}-brand','DRAGON BALL Z',125,46,'0xcbd6e4')
 vf=draw(vf,f'{i}-game','BUYUU RETSUDEN',200,64,'white',True)
 vf=draw(vf,f'{i}-mod','E N H A N C E D',285,38,'0xffd35a',True)
 vf=draw(vf,f'{i}-stage',stage+' / V5',395,40,'white',True)
 vf=draw(vf,f'{i}-action',label,1350,48,'0xffd35a',True)
 vf=draw(vf,f'{i}-platform','MEGA DRIVE / GENESIS',1450,34,'0xcbd6e4')
 vf=draw(vf,f'{i}-credit','ALEX LLAO',1580,34,'white',True)
 vf=draw(vf,f'{i}-speed','GAMEPLAY REAL / VELOCIDAD NORMAL',1650,27,'0xcbd6e4')
 vf+=f'[v];[0:a]atrim=start={first/fps}:end={last/fps},asetpts=PTS-STARTPTS,afade=t=in:d=0.018,afade=t=out:st={max(0,duration-.025)}:d=0.025[a]'
 out=D/f'{i:02d}.mp4';jobs.append((path,vf,out,duration))
 records.append(dict(source=path.as_posix(),sourceSha256=hashlib.sha256(path.read_bytes()).hexdigest(),romSha256=report['romSha256'],startFrame=first,endFrame=last,seconds=duration,stage=stage,label=label,control=control,nativeSplitScreen=any(t['scene'] or t['cinema'] for t in rows[first:last])))
def render(job):
 path,vf,out,duration=job
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-filter_complex_threads','1','-i',str(path),'-filter_complex',vf,'-map','[v]','-map','[a]','-t',str(duration),'-r',str(fps),'-fps_mode','cfr','-c:v','libx264','-preset','veryfast','-crf','18','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k',str(out)],check=True)
 print('RENDERED',out.name,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(render,jobs))
listing=D/'concat.txt';listing.write_text('\n'.join("file '"+job[2].resolve().as_posix()+"'" for job in jobs),encoding='utf-8')
target=O/'DBZ-Namek-V5-YouTube-Short.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(listing),'-r',str(fps),'-fps_mode','cfr','-c:v','libx264','-preset','veryfast','-crf','18','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-af','aresample=async=1:first_pts=0','-movflags','+faststart',str(target)],check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(target),'-f','null','-'],check=True)
cover=target.with_suffix('.png');subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','2','-i',str(target),'-frames:v','1',str(cover)],check=True)
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(target)],text=True));video=next(s for s in info['streams'] if s['codec_type']=='video');assert (video['width'],video['height'])==(1080,1920);assert 35<float(info['format']['duration'])<60
motion=json.loads(Path(scenes[0][0]).with_suffix('.json').read_text());run=[t for t in motion[891:970] if t['p']['action'] in [7,8]]
assert len(run)==79 and all(t['p']['y']==448 for t in run)
manifest=dict(romBuild='20261109-093419',romSha256=expected,romChanged=False,onlyV5=True,noBeforeAfterComparisons=True,fullGameAndHUDPreserved=True,gameRect=[0,500,1080,756],width=1080,height=1920,seconds=float(info['format']['duration']),fps=fps,gameplaySpeedScaling=False,gameNativeSplitScreenPreserved=True,audio='Native game sound;18/25ms fades at cuts; no added music',publishedToYouTube=False,scenes=records,groundRun=dict(character='Vegeta',controller='Native CPU',frames=79,y=448,xRange=[min(t['p']['x'] for t in run),max(t['p']['x'] for t in run)]),file=dict(name=target.name,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),bytes=target.stat().st_size))
(O/'manifest.json').write_text(json.dumps(manifest,indent=2));(P/'short-manifest.json').write_text(json.dumps(manifest,indent=2))
(O/'texto-youtube.txt').write_text('TITULO\nNamek se renueva en Mega Drive | DBZ Buyuu Retsuden Enhanced\n\nDESCRIPCION\nTres versiones de Namek, vuelo, carrera y ataques con pantalla partida. Gameplay real de V5, a velocidad normal. Mod en desarrollo por Alex Llao con ayuda de IA.\n#DragonBallZ #MegaDrive #Shorts\n',encoding='utf-8')
print('SHORT READY',manifest['seconds'],target,flush=True)

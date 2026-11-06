from pathlib import Path
import json,subprocess,hashlib
P=Path('work/youtube-short');P.mkdir(exist_ok=True);O=Path('outputs/youtube-short-v1.0');O.mkdir(parents=True,exist_ok=True)
fps=59.92274340431231;sha=lambda b:hashlib.sha256(b).hexdigest()
plan=[
 ('piccolo-hits','11 cruces y meteor',.20,4.80,'CRUCES RÁPIDOS','Y METEOR DE REMATE'),
 ('presentation-full','combo-0-AAB-flurry',.10,3.65,'COMBOS ENCADENADOS','PUÑOS + PATADAS + REMATE'),
 ('presentation-full','combo-3-ABA-meteor',1.90,6.10,'VEGETA','METEOR'),
 ('piccolo-hits','06 piccolo meteor',.90,4.25,'PICCOLO','CADA IMPACTO CUENTA'),
 ('presentation-full','combo-0-ABB-super',3.10,4.90,'SUPER KAMEHAMEHA','TODO DENTRO DEL JUEGO'),
 ('piccolo-hits','08 lanzamiento final flash',2.65,4.95,'FINAL FLASH','MEGA DRIVE / GENESIS'),
 ('presentation-full','combo-5-ABA-meteor',6.55,12.15,'CELL','RÁFAGA FINAL'),
 ('piccolo-hits','01 titulo',1.0,3.4,'V1.0 EN DESARROLLO','DRAGON BALL Z: BUYUU RETSUDEN')]
def draw(s,y,size,color='white'):
 return ",drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='"+s.replace(':','\\:')+f"':x=(w-tw)/2:y={y}:fontsize={size}:fontcolor={color}:borderw=2:bordercolor=black@0.65"
clips=[];chapters=[];elapsed=0
for i,(folder,label,begin,end,headline,subline) in enumerate(plan):
 source=Path(f'work/{folder}/video/{label}.mp4');first=round(begin*fps);last=round(end*fps);seconds=(last-first)/fps
 vf=f"[0:v]trim=start_frame={first}:end_frame={last},setpts=PTS-STARTPTS,crop=640:448:0:52,split=2[g][b];[b]scale=180:320:force_original_aspect_ratio=increase,crop=180:320,boxblur=8:2,eq=brightness=-0.38:saturation=0.7,scale=1080:1920[bg];[g]scale=1080:756:flags=neighbor[game];[bg][game]overlay=0:550"
 vf+=draw('DRAGON BALL Z',175,76)+draw('ENHANCED',275,78,'0xf5c667')+draw('BUYUU RETSUDEN',385,43)
 vf+=draw(headline,1390,54,'0xf5c667')+draw(subline,1470,32)+draw('JUEGO REAL  /  VELOCIDAD NORMAL',1565,29,'0xd1d9e2')+draw('MOD DE ALEX LLAO  /  V1.0',1640,32,'0xf5c667')+'[v]'
 af=f'atrim=start={first/fps}:end={last/fps},asetpts=PTS-STARTPTS,afade=t=in:d=0.025,afade=t=out:st={max(0,seconds-.08)}:d=0.08'
 target=P/f'{i:02}.mp4'
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-filter_complex',vf,'-map','[v]','-map','0:a','-af',af,'-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k',str(target)],check=True)
 chapters.append(dict(source=str(source),sourceSha256=sha(source.read_bytes()),sourceFrameStart=first,sourceFrameEnd=last,startSeconds=elapsed,seconds=seconds,headline=headline));elapsed+=seconds;clips.append(target.resolve());print('SHOT',i,headline,flush=True)
(P/'concat.txt').write_text('\n'.join("file '"+str(f).replace('\\','/')+"'" for f in clips),encoding='utf8')
target=O/'DBZ-Buyuu-Retsuden-Enhanced-YouTube-Short-v1.0.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(P/'concat.txt'),'-c','copy','-movflags','+faststart',str(target)],check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','1','-i',str(target),'-frames:v','1',str(O/'Portada-Short-v1.0.png')],check=True)
report=dict(version='1.0',buildId='20261106-105411',romSha256=sha(Path('work/piccolo-hits/candidate.bin').read_bytes()),romChanged=False,seconds=elapsed,width=1080,height=1920,aspect='9:16',nativeAudio=True,nativeHitsHud=True,gameplayTimeScaling=False,fullGameImagePreserved=True,background='Enlarged, blurred and darkened copy behind the untouched full game frame',chapters=chapters,video=dict(path='assets/media/youtube-short/'+target.name,sha256=sha(target.read_bytes()),bytes=target.stat().st_size))
(P/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('SHORT',elapsed,'seconds',target,flush=True)

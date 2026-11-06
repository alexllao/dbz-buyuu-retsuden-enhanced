from pathlib import Path
import subprocess,json,hashlib
P=Path('work/presentation-full');O=Path('outputs/presentacion-completa-v1.0');report=json.loads((P/'presentation.json').read_text());source=O/'DBZ-Buyuu-Retsuden-Enhanced-Presentacion-completa-v1.0.mp4'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(source)],text=True));seconds=float(probe['format']['duration']);bitrate=int((17*1024*1024*8/seconds-96000)*.97)
common=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-vf','scale=854:480:flags=neighbor','-c:v','libx264','-b:v',str(bitrate),'-pix_fmt','yuv420p','-fps_mode','passthrough','-passlogfile',str(P/'compact-pass')]
subprocess.run(common+['-pass','1','-an','-f','null','NUL'],check=True)
target=O/'DBZ-Enhanced-v1.0-Presentacion-para-correo.mp4'
subprocess.run(common+['-pass','2','-c:a','aac','-b:a','96k','-movflags','+faststart',str(target)],check=True)
assert target.stat().st_size<20*1024*1024
report['compactVideo']=dict(path='assets/media/presentation-full/'+target.name,bytes=target.stat().st_size,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),width=854,height=480,gameplayTimeScaling=False)
report['video']['bytes']=source.stat().st_size
(P/'presentation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print('COMPACT',seconds,'seconds',round(target.stat().st_size/1024/1024,2),'MiB',flush=True)

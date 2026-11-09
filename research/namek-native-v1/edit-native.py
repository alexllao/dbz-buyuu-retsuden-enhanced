from pathlib import Path
import subprocess,json,shutil
P=Path('work/namek-native/cpu-video');O=Path('outputs/Namek-escenarios-extra-nativos');O.mkdir(exist_ok=True,parents=True);listing=P/'montage.txt';clips=[P/slug/(label+'.mp4') for slug in ['normal','aldea','porunga'] for label in ['selector','cpu-vs-cpu']];listing.write_text('\n'.join("file '"+p.resolve().as_posix()+"'" for p in clips),encoding='utf-8')
video=O/'Namek-tres-escenarios-nativos-CPU-vs-CPU.mp4';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(video)],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],check=True);probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,width,height,r_frame_rate','-of','json',str(video)],text=True));print(probe)
for name,at in [('Porunga-nativo.png','36'),('Namek-normal-nativo.png','4'),('Namek-aldea-nativa.png','20')]:subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',at,'-i',str(video),'-frames:v','1',str(O/name)],check=True)
M=Path('repository/assets/media/namek-native-v1');M.mkdir(exist_ok=True,parents=True);shutil.copy2(video,M/'escenarios-cpu.mp4')
for name in ['Porunga-nativo.png','Namek-normal-nativo.png','Namek-aldea-nativa.png']:shutil.copy2(O/name,M/name)
shutil.copy2('outputs/Namek-nativo-dithering/Porunga-nativo-sin-y-con-dithering.mp4',M/'dithering.mp4');shutil.copy2('outputs/Namek-nativo-dithering/Comparacion.png',M/'dithering.png')

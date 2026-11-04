from pathlib import Path
import sys,json,subprocess

record_args=list(sys.argv)
target=Path(record_args[1]);output=Path(record_args[2]);output.mkdir(parents=True,exist_ok=True)
sys.argv=['probe','--native','--rom',str(target),'--out',str(output)]
header=Path('work/gameplay_probe.py').read_text().split('try:\n for index,step in enumerate(steps[:-1]):')[0]
exec(compile(header,'record-controls-setup','exec'),globals())

try:
 for step in steps[:-1]:
  for _ in range(step.get('frames',1)):tick(step.get('buttons',[]))
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(180):tick()
 baseline=snap()
 scenes=[
  ('Soltar tras un toque corto',[['RIGHT']]*5+[[]]*115),
  ('Cambiar de direccion',[['RIGHT']]*20+[['LEFT']]*20+[[]]*80),
  ('Pulsar de nuevo al final del puno',[['A']]*2+[[]]*15+[['A']]*3+[[]]*100),
  ('Recuperacion de la patada',[['B']]*2+[[]]*118),
  ('Transicion de caminar a guardia',[['RIGHT']]*12+[[]]*108),
  ('Avanzar despues de un puno',[['A']]*2+[['RIGHT']]*118),
 ]
 encoder=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb565le','-video_size','320x224','-framerate',str(av.timing.fps),'-i','pipe:0','-c:v','libx264','-preset','slow','-crf','14','-pix_fmt','yuv420p',str(output/'gameplay.mp4')],stdin=subprocess.PIPE)
 recordings=[]
 for name,schedule in scenes:
  restore(baseline);trace=[]
  for keys in schedule:
   tick(keys);trace.append(state())
   w,h,pitch,data=latest
   encoder.stdin.write(b''.join(data[y*pitch:y*pitch+w*2] for y in range(h)))
  recordings.append({'name':name,'schedule':schedule,'frames':trace})
 encoder.stdin.close();assert encoder.wait()==0
 (output/'sequence.json').write_text(json.dumps({'fps':av.timing.fps,'rom_sha256':hashlib.sha256(rom).hexdigest(),'scenes':recordings},indent=2),encoding='utf-8')
 print('Recorded',len(scenes),'scenes',str(target))
finally:
 core.retro_unload_game();core.retro_deinit()

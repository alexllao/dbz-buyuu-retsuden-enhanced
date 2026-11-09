from pathlib import Path
import sys,json,hashlib
setup=Path('work/namek-native-r6/record-promo.py').read_text().split('\ntry:\n if capture_from==1:')[0].replace('work/namek-native-r6/','work/namek-native-r8/').replace('states-q3','states-final-r8')
exec(compile(setup,'r8-native-record-runtime','exec'),globals())
sys.path.insert(0,str(Path('work/namek-native-r8').resolve()))
from resource_check import inspect
checks=[];T=Path('work/namek-native-r8')
def start(label,state,title):
 global captureEncoder,audio_file,rows,chapter
 restore(state);chapter=label;rows=[];checks.append(inspect(snap(),T,promoSlug,label+'-start'))
 name={'normal':'NAMEK NORMAL','aldea':'NAMEK DEVASTADO / LAVA','porunga':'NAMEK / PORUNGA'}[promoSlug]
 font='work/namek-three/arialbd.ttf';plain='work/namek-three/arial.ttf'
 vf="scale=640:448:flags=neighbor,pad=640:512:0:64:color=0x10151c,drawtext=fontfile='"+font+"':text='"+name+"':x=10:y=5:fontsize=18:fontcolor=0xffd35a,drawtext=fontfile='"+plain+"':text='"+title+"':x=10:y=28:fontsize=13:fontcolor=white,drawtext=fontfile='"+plain+"':text='R8 / ROM REAL / ESCALA 2X / VELOCIDAD NORMAL':x=10:y=46:fontsize=10:fontcolor=0xcbd6e4"
 captureEncoder=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb565le','-video_size','320x224','-framerate',str(fps),'-i','pipe:0','-vf',vf,'-an','-c:v','libx264','-preset','veryfast','-crf','16','-pix_fmt','yuv420p',str(root/(label+'-silent.mp4'))],stdin=subprocess.PIPE)
 audio_file=(root/(label+'.pcm')).open('wb')
try:
 begin(0,'01-vuelo','SUELO - VUELO - ATERRIZAJE',280);sim_phase='vuelo'
 for a,b,n in [([],[],30),(['C'],[],3),([],[],90),([],['C'],3),([],[],90),(['RIGHT'],['RIGHT'],35),(['C'],[],3),([],[],90),([],['C'],3),([],[],90)]:
  for _ in range(n):tick(a,b)
 assert any(t['p']['plane'] for t in rows) and any(t['e']['plane'] for t in rows)
 summarize();checks.append(inspect(snap(),T,promoSlug,'flight-end'))
 begin(0,'02-goku','COMBATE / KAMEHAMEHA');sim_phase='basicos';hits=basics();assert len(hits)==3
 for _ in range(3):tick()
 sim_phase='kamehameha';f,b=face();command([[b],['DOWN',b],['DOWN'],['DOWN',f],[f]],['A'],4)
 for _ in range(270):tick()
 summarize(0xc04);checks.append(inspect(snap(),T,promoSlug,'ground-special-end'))
 begin(0,'06-pantalla-partida','KAMEHAMEHA / PANTALLA PARTIDA',400);sim_phase='especial-pantalla-partida';f,b=face();command([[b],['DOWN',b],['DOWN'],['DOWN',f],[f]],['A'],4)
 for i in range(900):
  tick()
  if i>360 and rw(P1)<0x400 and not rb(0xe73c) and not rw(0xe9c4):break
 assert any(t['scene'] or t['cinema'] for t in rows)
 summarize(0xc04);checks.append(inspect(snap(),T,promoSlug,'split-screen-special-end'))
 (N/'capture-manifest.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),backgroundIntegrated=True,method='Direct native ROM framebuffer/audio; integer2x presentation; no background replacement',checks=checks,takes=[json.loads(p.read_text()) for p in sorted(root.glob('*-report.json'))]),indent=2))
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()

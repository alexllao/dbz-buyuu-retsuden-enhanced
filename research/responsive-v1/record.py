from pathlib import Path
import sys,json,subprocess,struct
which=sys.argv[1];baseDir=Path.cwd();root=baseDir/'work/responsive-cancels-v1/video'/which;root.mkdir(parents=True,exist_ok=True)
rompath='work/responsive-cancels-v1/candidate.bin' if which=='after' else 'work/hits-hud-v3/candidate.bin'
sys.argv=['record','0']
raw=Path('work/hits-hud-v3/prepare.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0].replace("romfile=BASE/'work/hits-hud-v3/candidate.bin'",f"romfile=BASE/'{rompath}'")
setup,functions=raw.split("exec(compile(header,'combo-side-setup','exec'),globals())",1)
exec(compile(setup,'record-setup','exec'),globals())
audioDef='def audio(l,r):\n if audio_file is not None:audio_file.write(struct.pack("<hh",l,r))'
batchDef='def batch(data,frames):\n if audio_file is not None:audio_file.write(C.string_at(data,frames*4))\n return frames'
replacement='src=src.replace('+repr('def audio(l,r):pass')+','+repr(audioDef)+')\nsrc=src.replace('+repr('def batch(data,frames):return frames')+','+repr(batchDef)+')\nexec(compile(src,"local-emulator-setup","exec"),globals())'
header=header.replace("exec(compile(src,'local-emulator-setup','exec'),globals())",replacement)
audio_file=None;exec(compile(header,'record-runtime','exec'),globals());exec(compile(functions,'record-functions','exec'),globals())
rawtick=tick;captureEncoder=None;rows=[];chapter='';chapters=[]
def tick(a=(),b=()):
 rawtick(a,b)
 if captureEncoder:
  w,h,pitch,data=latest;captureEncoder.stdin.write(b''.join(data[y*pitch:y*pitch+w*2] for y in range(h)))
  rows.append(dict(p=st(P1),e=st(P2),keys=list(a)))
def start(label,state,close=False):
 global captureEncoder,audio_file,rows,chapter
 restore(state)
 if close:ww(P1+0xa,300);ww(P2+0xa,332);wb(P1+0x59,0);wb(P2+0x59,1)
 for _ in range(8):tick()
 chapter=label;rows=[]
 title=('NUEVA ROM' if which=='after' else 'ROM ANTERIOR')+' - '+label.upper()
 vf="scale=640:448:flags=neighbor,pad=640:500:0:52:color=0x10151c,drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='"+title+"':x=10:y=7:fontsize=15:fontcolor=white,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='Juego real - velocidad normal - sin acelerar animaciones':x=10:y=31:fontsize=12:fontcolor=0xbecbd8"
 captureEncoder=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb565le','-video_size','320x224','-framerate',str(av.timing.fps),'-i','pipe:0','-vf',vf,'-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p',str(root/(label+'-silent.mp4'))],stdin=subprocess.PIPE)
 audio_file=(root/(label+'.pcm')).open('wb')
def finish():
 global captureEncoder,audio_file
 captureEncoder.stdin.close();assert captureEncoder.wait()==0;captureEncoder=None;audio_file.close();audio_file=None
 target=root/(chapter+'.mp4')
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(root/(chapter+'-silent.mp4')),'-f','s16le','-ar',str(int(av.timing.sample_rate)),'-ac','2','-i',str(root/(chapter+'.pcm')),'-c:v','copy','-c:a','aac','-b:a','128k','-shortest','-movflags','+faststart',str(target)],check=True)
 chapters.append(dict(label=chapter,path=str(target),frames=len(rows),seconds=len(rows)/av.timing.fps))
 (root/(chapter+'.json')).write_text(json.dumps(rows));print('CLIP',which,chapter,len(rows),flush=True)
def schedule(seq):
 for keys in seq:tick(keys)
try:
 for j,entry in enumerate(steps[:-1]):
  if j==11:
   for _ in range(4):tick(['DOWN'])
   for _ in range(16):tick()
  for _ in range(entry.get('frames',1)):tick([] if j==11 else entry.get('buttons',[]))
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(300):tick()
 baseline=snap()
 start('carga y movimiento',baseline);schedule([[]]*30+[['A','B']]*90+[['RIGHT']]*90);finish()
 start('lanzamiento y control',baseline,True);ww(P2+0xa,320);schedule([['RIGHT','A']]*3+[['LEFT']]*237);finish()
 restore(baseline)
 for _ in range(2400):
  tick(['A','B'])
  if rw(P1+0x28)>=240:break
 nearfull=snap()
 if which=='after':
  start('barra llena y salida',nearfull);schedule([['A','B']]*170+[['LEFT']]*70);finish()
 schedule([[]]*70);charged=snap()
 start('cancel de basicos A B A',charged,True);hits=[];prev=rw(P2+0x24)
 for f in range(180):
  keys=['A'] if f<3 else []
  for idx,t in enumerate(hits[:2]):
   if t+3<=f<t+6:keys=[['B','A'][idx]]
  tick(keys);hp=rw(P2+0x24)
  if hp<prev:hits.append(f)
  prev=hp
 finish()
 if which=='after':
  start('buffer durante carga',baseline);schedule([['A','B']]*60+[['A','B','DOWN']]*4+[['A','B','DOWN','RIGHT']]*4+[['A','B','RIGHT']]*4+[[]]*3+[['A']]*3+[[]]*162);finish()
  start('cancel de puno a Kamehameha',charged,True)
  prevHP=rw(P2+0x24)
  for f in range(40):
   tick(['A'] if f<3 else [])
   if rw(P2+0x24)<prevHP:break
  schedule([['DOWN']]*3+[['DOWN','RIGHT']]*3+[['RIGHT']]*3+[['RIGHT','A']]*3+[[]]*210);finish()
  start('patada descendente en aire',charged,True)
  schedule([['UP']]*20+[['DOWN']]*4+[['DOWN','RIGHT']]*4+[['RIGHT']]*4+[['RIGHT','B']]*3+[[]]*220);finish()
  commands={'Kamehameha' :(['DOWN','DR','RIGHT'],'A'),'Super Kamehameha':(['DOWN','DR','RIGHT','DOWN','DR','RIGHT'],'A'),'Proyectil':(['LEFT','RIGHT'],'A'),'Rafaga':(['LEFT','DL','DOWN','DR','RIGHT'],'A'),'Kiai Cannon':(['RIGHT','DOWN','DR'],'A'),'Codazo':(['DOWN','DL','LEFT'],'A'),'Solar Flare':(['DOWN','NEUTRAL','DOWN'],'A'),'Patadas multiples':(['DOWN','DL','LEFT'],'B'),'Rodillazo':(['RIGHT','DOWN','DR'],'B'),'Deslizante':(['DOWN','DR','RIGHT'],'B'),'Meteor':(['DOWN','DR','RIGHT','DOWN','DR','RIGHT'],'B'),'Desplazamiento original':(['RIGHT','LEFT','RIGHT'],'B')}
  for name,(dirs,button) in commands.items():
   start(name,charged,True)
   for d in dirs:schedule([{'DR':['DOWN','RIGHT'],'DL':['DOWN','LEFT'],'NEUTRAL':[]}.get(d,[d])]*4)
   schedule([rows[-1]['keys']+[button]]*3+[[]]*237);finish()
 (root/'chapters.json').write_text(json.dumps(chapters,indent=2))
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()

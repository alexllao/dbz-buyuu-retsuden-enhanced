from pathlib import Path
import sys,json,subprocess,struct
which=sys.argv[1];baseDir=Path.cwd();root=baseDir/'work/input-v2/video'/which;root.mkdir(parents=True,exist_ok=True)
rompath='work/input-v2/candidate.bin' if which=='after' else 'work/responsive-cancels-v1/candidate.bin'
sys.argv=['record','0']
raw=Path('work/hits-hud-v3/prepare.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0].replace("romfile=BASE/'work/hits-hud-v3/candidate.bin'",f"romfile=BASE/'{rompath}'")
if which=='after':
 for old in [0x104,0x106,0x117,0x120,0x121,0x122,0x124]:raw=raw.replace('b+'+hex(old)+')','b+'+hex(old+0xc00)+')')
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
 title=('RESPUESTA V2' if which=='after' else 'RESPUESTA V1')+' - '+label.upper()
 vf="scale=640:448:flags=neighbor,pad=640:500:0:52:color=0x10151c,drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='"+title+"':x=10:y=7:fontsize=15:fontcolor=white,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='Juego real - velocidad normal - comparacion de controles y saltos':x=10:y=31:fontsize=12:fontcolor=0xbecbd8"
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
 start('toque corto y frenada',baseline);schedule([[]]*20+[['RIGHT']]*2+[[]]*118);finish()
 start('salto normal',baseline);schedule([[]]*20+[['UP']]*3+[[]]*117);finish()
 restore(baseline)
 for _ in range(2400):
  tick(['A','B'])
  if rw(P1+0x28)>=240:break
 schedule([[]]*70);charged=snap()
 start('rafaga de tres bolas',charged,True);ww(P2+0xa,364)
 dirs=[['DOWN'],['DOWN','RIGHT'],['RIGHT']] if which=='after' else [['LEFT'],['DOWN','LEFT'],['DOWN'],['DOWN','RIGHT'],['RIGHT']]
 for k in dirs:schedule([k]*4)
 schedule([['RIGHT','A']]*3+[[]]*257);finish()
 if which=='after':
  hcf=[['LEFT'],['DOWN','LEFT'],['DOWN'],['DOWN','RIGHT'],['RIGHT']]
  for name,dirs,button in [('Kamehameha medio circulo',hcf,['A']),('Super doble medio circulo',hcf*2,['A']),('Meteor doble circulo A y B',hcf*2,['A','B'])]:
   start(name,charged,True)
   for k in dirs:schedule([k]*3)
   schedule([dirs[-1]+button]*3+[[]]*300);finish()
  start('buffer cargando y Kamehameha',baseline)
  schedule([['A','B']]*60)
  for k in hcf:schedule([k+['A','B']]*3)
  schedule([[]]*4+[['A']]*3+[[]]*218);finish()
  start('puno cancelado a Kamehameha',charged,True);hp=rw(P2+0x24)
  for f in range(35):
   tick(['A'] if f<3 else [])
   if rw(P2+0x24)<hp:break
  for k in hcf:schedule([k]*3)
  schedule([['RIGHT','A']]*3+[[]]*220);finish()
  start('Kamehameha mirando izquierda',charged,True);ww(P1+0xa,400);ww(P2+0xa,300);wb(P1+0x59,1);wb(P2+0x59,0)
  for k in hcf:schedule([[{'RIGHT':'LEFT','LEFT':'RIGHT'}.get(d,d) for d in k]]*3)
  schedule([['LEFT','A']]*3+[[]]*220);finish()
  start('movilidad y ataques variados',charged)
  pattern=[['RIGHT']]*22+[[]]*9+[['UP','RIGHT']]*3+[[]]*55+[['LEFT']]*12+[[]]*7+[['A']]*3+[[]]*8+[['B']]*3+[[]]*35+[['A','B']]*40+[[]]*5+[['LEFT']]*3+[['DOWN','LEFT']]*3+[['DOWN']]*3+[['DOWN','RIGHT']]*3+[['RIGHT']]*3+[['RIGHT','A']]*3+[[]]*95
  for f in range(1800):
   keysA=pattern[f%len(pattern)];keysB=[{'LEFT':'RIGHT','RIGHT':'LEFT'}.get(k,k) for k in pattern[(f+91)%len(pattern)]]
   if rw(P1+0x24)==0 or rw(P2+0x24)==0:restore(charged)
   tick(keysA,keysB)
  finish()
 (root/'chapters.json').write_text(json.dumps(chapters,indent=2))
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()

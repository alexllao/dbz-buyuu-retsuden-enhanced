from pathlib import Path
import sys,json,subprocess,struct
which=sys.argv[1];baseDir=Path.cwd();root=baseDir/'work/throw-kamehameha/video'/which;root.mkdir(parents=True,exist_ok=True)
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
 for _ in range(0):tick()
 chapter=label;rows=[]
 title=('RESPUESTA V2' if which=='after' else 'RESPUESTA V1')+' - '+label.upper()
 vf="scale=640:448:flags=neighbor,pad=640:500:0:52:color=0x10151c,drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='"+title+"':x=10:y=7:fontsize=15:fontcolor=white,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='ROM sin modificar - velocidad normal - secuencias reales':x=10:y=31:fontsize=12:fontcolor=0xbecbd8"
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
 while rw(P1+0x28)<235:tick(['A','B'])
 for _ in range(70):tick()
 seed=snap();results=[]
 for label,delay,guard in [('1 - Preparacion temprana',8,False),('2 - Esperar el descenso',48,False),('3 - Rival intentando cubrirse',48,True)]:
  restore(seed);ww(P1+0xa,300);ww(P2+0xa,320);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(8):tick()
  fixture=snap();start(label,fixture)
  for _ in range(3):tick(['RIGHT','A'])
  assert rw(P1)==0x40a
  for _ in range(140):
   if rb(P1+0x5b)<=8:break
   tick()
  free=len(rows)
  for _ in range(delay):tick()
  fwd='LEFT' if rb(P1+0x59) else 'RIGHT';back='RIGHT' if fwd=='LEFT' else 'LEFT'
  # Guard away from Goku, only after launch: the throw itself is unaltered.
  guardKeys=['LEFT'] if guard else []
  for k in [[back],['DOWN',back],['DOWN'],['DOWN',fwd],[fwd]]:
   for _ in range(3):tick(k,guardKeys)
  for _ in range(3):tick([fwd,'A'],guardKeys)
  for _ in range(390):tick([],guardKeys)
  kame=next((t for t in enumerate(rows) if t[1]['p']['program']==0xc04),None)
  hits=[dict(frame=i,damage=rows[i-1]['e']['hp']-t['e']['hp'],y=t['e']['y'],action=t['e']['action']) for i,t in enumerate(rows) if i and rows[i-1]['e']['hp']>t['e']['hp']]
  firstAir=next((i for i,t in enumerate(rows) if t['e']['y']<448),None);land=next((i for i,t in enumerate(rows) if firstAir is not None and i>firstAir and t['e']['y']==448),None)
  summary=dict(label=label,delay=delay,guard=guard,controlFree=free,kameFrame=kame[0] if kame else None,enemyYAtKame=kame[1]['e']['y'] if kame else None,firstLanding=land,hits=hits,kameDamage=sum(t['damage'] for t in hits if t['damage']!=12),finalActions=[rows[-1]['p']['action'],rows[-1]['e']['action']])
  results.append(summary);print('RESULT',summary,flush=True);finish()
 (root/'report.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),fps=av.timing.fps,results=results,fixture='Native menus; ki charged using A+B. Only initial spacing/facing set before each take. Two human ports; opponent idle in first two, holds back after launch in third. No ROM,HP,damage,timer or animation edits.'),indent=2),encoding='utf8')
 (root/'chapters.json').write_text(json.dumps(chapters,indent=2),encoding='utf8')
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()

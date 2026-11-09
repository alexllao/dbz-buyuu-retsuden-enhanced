from pathlib import Path
import sys,json,hashlib,subprocess,struct
s=Path('work/input-v2/record.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0].replace("rompath='work/input-v2/candidate.bin' if which=='after' else 'work/responsive-cancels-v1/candidate.bin'","rompath='work/namek-native/integrated.bin'").replace("if which=='after':",'if True:')
sys.argv=['record','after'];exec(compile(s,'native-extra-record-runtime','exec'),globals());T=Path('work/namek-native/cpu-video');T.mkdir(exist_ok=True);nativeProc=None;nativeRows=[];currentVariant=0

def tick(a=(),b=()):
 rawtick(a,b)
 if nativeProc:
  w,h,pitch,data=latest;nativeProc.stdin.write(b''.join(data[y*pitch:y*pitch+w*2] for y in range(h)));nativeRows.append(dict(p=st(P1),e=st(P2),physical=rb(0xe741),variant=rb(0xf7c0),state=rw(0xe6a4),phase=rw(0xe750),keys1=list(a),keys2=list(b)))

def press(k,n=3,k2=()):
 for _ in range(n):tick(k,k2)
 for _ in range(20):tick()

def record_take(slug,label,seq):
 global nativeProc,audio_file,nativeRows
 dest=T/slug;dest.mkdir(exist_ok=True);nativeRows=[];font='work/namek-three/arialbd.ttf';plain='work/namek-three/arial.ttf';names={'normal':'NAMEK NUEVO','aldea':'ALDEA DEVASTADA','porunga':'INVOCACION DE PORUNGA'}
 vf="scale=960:672:flags=neighbor,pad=960:750:0:78:color=0x10151c,drawtext=fontfile='"+font+"':text='"+names[slug]+" / "+label.upper()+"':x=14:y=8:fontsize=24:fontcolor=0xffd35a,drawtext=fontfile='"+plain+"':text='CAPTURA NATIVA DEL EMULADOR / TRES ESCENARIOS EXTRA EN LA ROM':x=14:y=47:fontsize=17:fontcolor=0xcbd6e4"
 nativeProc=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb565le','-video_size','320x224','-framerate',str(av.timing.fps),'-i','pipe:0','-vf',vf,'-an','-c:v','libx264','-crf','17','-preset','veryfast','-pix_fmt','yuv420p',str(dest/(label+'-silent.mp4'))],stdin=subprocess.PIPE);audio_file=(dest/(label+'.pcm')).open('wb')
 for a,b in seq:tick(a,b)
 nativeProc.stdin.close();assert nativeProc.wait()==0;nativeProc=None;audio_file.close();audio_file=None
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(dest/(label+'-silent.mp4')),'-f','s16le','-ar','44100','-ac','2','-i',str(dest/(label+'.pcm')),'-c:v','copy','-c:a','aac','-b:a','128k','-shortest','-movflags','+faststart',str(dest/(label+'.mp4'))],check=True)
 (dest/(label+'.json')).write_text(json.dumps(nativeRows));print('NATIVE TAKE',slug,label,len(nativeRows),flush=True)

def check_assets(slug):
 data=snap();vo=0x12425;rawv=data[vo:vo+65536];v=bytearray(65536);v[0::2]=rawv[1::2];v[1::2]=rawv[0::2];expected=(Path('work/namek-native')/slug/'tiles.bin').read_bytes();assert v[:0x5c00]==expected[:0x5c00]
 p=(Path('work/namek-native')/slug/'palette.bin').read_bytes();words=[int.from_bytes(p[i:i+2],'big') for i in range(0,44,2)];cram=[int.from_bytes(data[vo+65536+i*2:vo+65536+i*2+2],'little') for i in range(32,54)];expect=[((v>>1)&7)|(((v>>5)&7)<<3)|(((v>>9)&7)<<6) for v in words];assert cram==expect
 return dict(backgroundVramExact=True,palette22WordsExact=True)
try:
 # Native main menu -> CPU watch -> normal character confirmation -> battle settings.
 core.retro_reset()
 for entry in steps[:7]:
  for _ in range(entry.get('frames',1)):tick(entry.get('buttons',[]))
 press(['RIGHT']);press(['RIGHT']);press(['C'])
 for f in range(2400):
  if rw(0xe6a4)==0x20 and rw(0xe750)==3:break
  tick(['C'] if f%120<3 else [])
 assert rw(0xe6a4)==0x20 and rw(0xe750)==3
 baseMenu=snap();proof=[]
 for variant,slug in [(1,'normal'),(2,'aldea'),(3,'porunga')]:
  restore(baseMenu);press(['DOWN']);assert rw(0xe9f6)==1
  for _ in range(4-variant):press(['B']);[tick() for _ in range(100)]
  assert rb(0xe741)==6 and rb(0xf7c0)==variant
  save_image(T/(slug+'-selector.png'));record_take(slug,'selector',[([],[])]*70);(T/(slug+'-selector.state')).write_bytes(snap());press(['START'])
  for f in range(1200):tick(['C'] if f%120<3 else [])
  assert rw(0xe6a4)==0xc and [rb(P1+0xbe),rb(P2+0xbe)]==[255,255]
  assets=check_assets(slug);save_image(T/(slug+'-game.png'));hp0=[rw(P1+0x24),rw(P2+0x24)];(T/(slug+'-playing.state')).write_bytes(snap())
  record_take(slug,'cpu-vs-cpu',[([],[])]*900);hp1=[rw(P1+0x24),rw(P2+0x24)];assetsEnd=check_assets(slug);proof.append(dict(variant=variant,slug=slug,controls=[rb(P1+0xbe),rb(P2+0xbe)],hpBefore=hp0,hpAfter=hp1,assetChecksBefore=assets,assetChecksAfter=assetsEnd,stageSelectionViaController=True,fixtureWrites=[]))
 (T/'validation.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),mode='Native COM watching selected from main menu with RIGHT twice',cases=proof),indent=2));print(proof)
finally:
 if nativeProc:nativeProc.stdin.close();nativeProc.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()

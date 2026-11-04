from pathlib import Path
import sys,json,subprocess,struct,hashlib
BASE=Path.cwd();tag=sys.argv[1];mode=sys.argv[2];romfile=BASE/('work/rom/original.bin' if tag=='original' else 'work/natural-combos/candidate.bin');out=BASE/'work/goku-kick-review'/f'{tag}-{mode}';out.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(BASE/'work'));sys.argv=['probe','--native','--rom',str(romfile),'--out',str(out)]
header=(BASE/'work/gameplay_probe.py').read_text().split('try:\n for index,step in enumerate(steps[:-1]):')[0].replace('BASE=Path(__file__).resolve().parent.parent','BASE=Path.cwd()')
header=header.replace("exec(compile(src,'local-emulator-setup','exec'),globals())",'''src=src.replace('def audio(l,r):pass', 'def audio(l,r):\\n if audio_file is not None:audio_file.write(struct.pack("<hh",l,r))')
src=src.replace('def batch(data,frames):return frames', 'def batch(data,frames):\\n if audio_file is not None:audio_file.write(C.string_at(data,frames*4))\\n return frames')
exec(compile(src,'local-emulator-setup','exec'),globals())''');audio_file=None;exec(compile(header,'kick-review','exec'),globals());encoder=None
try:
 for i,step in enumerate(steps[:-1]):
  for _ in range(step.get('frames',1)):tick([] if i==11 else step.get('buttons',[]))
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(180):tick()
 ww(P1+0xa,300);ww(P2+0xa,332);ww(P1+0xc,0);ww(P2+0xc,0);wb(P1+0x59,0);wb(P2+0x59,1)
 for _ in range(8):tick()
 dirs=[['RIGHT'],['DOWN','RIGHT'],['DOWN'],['DOWN','LEFT'],['LEFT'],['RIGHT']] if mode=='meteor' else [['LEFT'],['DOWN','LEFT'],['DOWN'],['DOWN','RIGHT'],['RIGHT']]
 seq=[k for k in dirs for _ in range(4)]+[dirs[-1]+['B']]*4
 title=('ROM ORIGINAL' if tag=='original' else 'MOD V4 NATURAL')+' - '+('METEOR' if mode=='meteor' else 'BASICOS A-B-A' if mode=='basicos' else 'RAFAGA NATIVA')
 vf="scale=640:448:flags=neighbor,pad=640:488:0:40:color=0x10151c,drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='"+title+"':x=10:y=10:fontsize=19:fontcolor=white"
 encoder=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb565le','-video_size','320x224','-framerate',str(av.timing.fps),'-i','pipe:0','-vf',vf,'-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p',str(out/'silent.mp4')],stdin=subprocess.PIPE);audio_file=(out/'audio.pcm').open('wb');trace=[];hits=[];hp=rw(P2+0x24)
 for f in range(420 if mode=='meteor' else 300):
  k=[]
  if mode=='basicos':
   if 20<=f<26:k=['A']
   if hits and hits[0]+9<=f<hits[0]+13:k=['B']
   if len(hits)>1 and hits[1]+9<=f<hits[1]+13:k=['A']
  elif 20<=f<20+len(seq):k=seq[f-20]
  tick(k);w,h,pitch,data=latest;encoder.stdin.write(b''.join(data[y*pitch:y*pitch+w*2] for y in range(h)));curHP=rw(P2+0x24)
  if curHP<hp:hits.append(f)
  hp=curHP;trace.append({'f':f,'keys':k,'program':rw(P1),'action':rb(P1+0x5b),'pose':rb(P1+4),'cursor':rw(P1+6),'plane':bool(rb(P1+0x1e)&16),'y':rw(P1+0x10),'enemyHP':hp,'enemyAction':rb(P2+0x5b),'enemyY':rw(P2+0x10),'enemyPlane':bool(rb(P2+0x1e)&16)})
 audio_file.close();audio_file=None;encoder.stdin.close();assert encoder.wait()==0;encoder=None
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(out/'silent.mp4'),'-f','s16le','-ar',str(round(av.timing.sample_rate)),'-ac','2','-i',str(out/'audio.pcm'),'-c:v','copy','-c:a','aac','-shortest',str(out/'demo.mp4')],check=True)
 (out/'report.json').write_text(json.dumps({'romSha256':hashlib.sha256(rom).hexdigest(),'tag':tag,'mode':mode,'fps':av.timing.fps,'hits':hits,'trace':trace},indent=2),encoding='utf8');print(tag,mode,hits,sorted(set(t['program'] for t in trace)))
finally:
 if audio_file:audio_file.close()
 if encoder:encoder.stdin.close();encoder.wait()
 core.retro_unload_game();core.retro_deinit()

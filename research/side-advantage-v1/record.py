from pathlib import Path
import sys,json,subprocess,struct,hashlib
BASE=Path.cwd();index=int(sys.argv[1]);pairs=[(0,3,6),(3,0,0),(2,8,2)];cid1,cid2,stage=pairs[index]
out=BASE/'work/teleport-advantage/demo'/f'{index:02}';out.mkdir(parents=True,exist_ok=True);romfile=BASE/'work/teleport-advantage/candidate.bin'
sys.path.insert(0,str(BASE/'work'));sys.argv=['probe','--native','--rom',str(romfile),'--out',str(out)]
header=(BASE/'work/gameplay_probe.py').read_text().split('try:\n for index,step in enumerate(steps[:-1]):')[0].replace('BASE=Path(__file__).resolve().parent.parent','BASE=Path.cwd()')
header=header.replace("exec(compile(src,'local-emulator-setup','exec'),globals())","""src=src.replace('def audio(l,r):pass', 'def audio(l,r):\\n if audio_file is not None:audio_file.write(struct.pack("<hh",l,r))')
src=src.replace('def batch(data,frames):return frames', 'def batch(data,frames):\\n if audio_file is not None:audio_file.write(C.string_at(data,frames*4))\\n return frames')
exec(compile(src,'local-emulator-setup','exec'),globals())""")
audio_file=None;exec(compile(header,'teleport-exchange-setup','exec'),globals());encoder=None;trace=[];events=[];frame=0;phase='inicio'

def state(b):return dict(program=rw(b),action=rb(b+0x5b),x=rw(b+0xa),y=rw(b+0x10),hp=rw(b+0x24),ki=rw(b+0x28),facing=rb(b+0x59),attack=bool(rb(b+0x1e)&128),plane=bool(rb(b+0x1e)&16),window=rb(b+0x117)&7)
def run(a=(),b=()):
 global frame
 tick(a,b);w,h,pitch,data=latest;encoder.stdin.write(b''.join(data[y*pitch:y*pitch+w*2] for y in range(h)))
 fixed=bytes(byte for yy in range(26) for xx in range(320) if not (((18<=xx<=141) or (178<=xx<=301)) and ((10<=yy<=13) or (18<=yy<=21))) for byte in data[yy*pitch+xx*2:yy*pitch+xx*2+2])
 trace.append(dict(f=frame,phase=phase,keys1=list(a),keys2=list(b),p1=state(P1),p2=state(P2),fixedHudSha256=hashlib.sha256(fixed).hexdigest(),auraDirty=rb(0xe874)));frame+=1

def neutral(n=1):
 for _ in range(n):run()

def wait_free():
 for _ in range(160):
  if rb(P1+0x5b)<=8 and rb(P2+0x5b)<=8:return
  run()
 raise AssertionError('not free')

def cross(port,attack=False):
 actor=P1 if port==1 else P2;other=P2 if port==1 else P1;wait_free();start=frame;before=[state(P1),state(P2)];f='RIGHT' if rw(actor+0xa)<rw(other+0xa) else 'LEFT';back='LEFT' if f=='RIGHT' else 'RIGHT'
 seq=[[f]]*4+[[back]]*4+[[f,'C']]*4+[[]]*3
 for i,k in enumerate(seq):
  rival=['A'] if attack and i in [10,11] else []
  run(k,rival) if port==1 else run(rival,k)
 for _ in range(60):
  if rw(actor)!=0x843:break
  run()
 after=[state(P1),state(P2)];rows=trace[start:];activated=any((r['p1'] if port==1 else r['p2'])['program']==0x843 for r in rows);crossed=(before[0]['x']-before[1]['x'])*(after[0]['x']-after[1]['x'])<0

 if not activated or not crossed:
  (out/'failed.json').write_text(json.dumps(dict(port=port,start=start,before=before,after=after,trace=trace),indent=2))
 assert activated and crossed,(port,start,before,after)
 events.append(dict(start=start,end=frame,port=port,attackAttempt=attack,activated=activated,crossed=crossed,hpBefore=[v['hp'] for v in before],hpAfter=[v['hp'] for v in after],incomingWindow=before[port-1]['window'],liveCounter=any((r['p1'] if port==1 else r['p2'])['program']==0x843 and ((rows[j-1]['p1'] if port==1 else rows[j-1]['p2'])['window'] if j else before[port-1]['window'])>0 for j,r in enumerate(rows))))

try:
 for j,step in enumerate(steps[:-1]):
  if j in [9,11]:
   selected=cid1 if j==9 else cid2
   for direction,count in [('DOWN',selected//3),('RIGHT',selected%3)]:
    for _ in range(count):
     for _ in range(4):tick([direction])
     for _ in range(16):tick()
  if j==13:wb(0xe741,stage)
  for _ in range(step.get('frames',1)):tick([] if j==11 else step.get('buttons',[]))
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(300):tick()
 assert [rb(P1+0x58),rb(P2+0x58)]==[cid1,cid2]
 ww(P1+0xa,300);ww(P1+0xc,0);wb(P1+0x59,0);ww(P2+0xa,364);ww(P2+0xc,0);wb(P2+0x59,1)
 for _ in range(8):tick()
 names=['Goku','Gohan','Piccolo','Vegeta','Trunks','Cell','A18','Krilin','Freezer','Recoome','Ginyu']
 title=f'{names[cid1]} / {names[cid2]} - VENTAJA EXTRA P1 / P2'
 vf="scale=640:448:flags=neighbor,pad=640:496:0:48:color=0x10151c,drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='"+title+"':x=12:y=6:fontsize=16:fontcolor=white,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='ROM DE PRUEBA - VENTANA EXTRA - VELOCIDAD NORMAL':x=12:y=30:fontsize=12:fontcolor=0xbecbd8"
 encoder=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb565le','-video_size','320x224','-framerate',str(av.timing.fps),'-i','pipe:0','-vf',vf,'-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p',str(out/'silent.mp4')],stdin=subprocess.PIPE)
 audio_file=(out/'audio.pcm').open('wb');neutral(60)
 phase='cadena-alternada'
 for port in [1,2,1,2,1,2]:cross(port);neutral(0)
 phase='ventaja-frente-a-respuesta-ofensiva'
 for f in range(45):run(['A'] if f<6 else [],['B'] if f<6 else [])
 neutral(15);phase='cambio-con-intento-de-golpe'
 for port in [1,2,1,2]:cross(port,True);neutral(8)
 phase='ataques-tras-el-intercambio';wait_free();neutral(30)
 # Approach by actual walking; no position/HP/pose writes during capture.
 for _ in range(120):
  if abs(rw(P1+0xa)-rw(P2+0xa))<=30:break
  run(['RIGHT'] if rw(P1+0xa)<rw(P2+0xa) else ['LEFT'])
 for f in range(120):run(['A'] if f<6 else [])
 wait_free()
 for f in range(120):run([],['B'] if f<6 else [])
 phase='final';neutral(60)
 audio_file.close();audio_file=None;encoder.stdin.close();assert encoder.wait()==0;encoder=None
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(out/'silent.mp4'),'-f','s16le','-ar',str(round(av.timing.sample_rate)),'-ac','2','-i',str(out/'audio.pcm'),'-c:v','copy','-c:a','aac','-b:a','160k','-movflags','+faststart',str(out/'exchange.mp4')],check=True)
 report=dict(romSha256=hashlib.sha256(rom).hexdigest(),pair=[cid1,cid2],stage=stage,frames=frame,fps=av.timing.fps,seconds=frame/av.timing.fps,events=events,trace=trace,fixture='New advantage prototype based on Stun v2; two scripted human pads. Initial spacing/facing only; no position, action, HP, ki or timer writes during recording. Coordinated responses, not reactive CPU. New window delays opponent A/B only; no extra invulnerability.',additionalReactionAdvantageImplemented=True,windowInputUpdates=6)
 (out/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(index,frame,len(events),[(e['port'],e['hpBefore'],e['hpAfter']) for e in events],flush=True)
finally:
 if audio_file:audio_file.close()
 if encoder:encoder.stdin.close();encoder.wait()
 core.retro_unload_game();core.retro_deinit()

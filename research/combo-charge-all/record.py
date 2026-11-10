from pathlib import Path
import sys,json,subprocess,hashlib
audit_variant=sys.argv[1]
exec(compile(Path('work/combo-charge-all/runtime.py').read_text(),'charge-video-runtime','exec'),globals())
root=Path('work/combo-charge-all/captures')/audit_variant;root.mkdir(parents=True,exist_ok=True)
reports=[]
def tick(a=(),b=()):
 rawtick(a,b)
 w,h,pitch,data=latest
 captureEncoder.stdin.write(b''.join(data[y*pitch:y*pitch+w*2] for y in range(h)))
 rows.append(dict(f=len(rows),p=st(P1),e=st(P2),fast=rb(0xf7b2),pose=rb(P1+4),types=[rb(P1+0xe2+i*30) for i in range(3)]))
try:
 for cid,label,kind,clip_frames in [(0,'01-super-kame','super',330),(1,'02-masenko','gohan',290),(3,'03-final-flash','flash',320),(4,'04-trunks','trunks',330),(5,'05-cell-cruce-meteor','cell',880)]:
  if cid in [0,3,5]:staged({0:'normal',3:'aldea',5:'porunga'}[cid],cid,cid==5)
  else:
   restore((S/'states/normal'/f'seed-{cid}.state').read_bytes());ww(P1+10,300);ww(P2+10,332);wb(P1+0x59,0);wb(P2+0x59,1)
   for _ in range(8):rawtick()
   rows=[]
  chapter=label
  heading=('ANTES - R10' if audit_variant=='before' else 'NUEVA - CARGA MINIMA EN COMBO')
  names={0:'GOKU / SUPER KAMEHAMEHA',1:'GOHAN / MASENKO',3:'VEGETA / FINAL FLASH',4:'TRUNKS / BURNING ATTACK',5:'CELL / COMBO - CRUCE - METEOR'}
  vf="scale=640:448:flags=neighbor,pad=640:512:0:64:color=0x10151c,drawtext=fontfile='work/namek-three/arialbd.ttf':text='"+heading+"':x=12:y=8:fontsize=21:fontcolor=0xffd35a,drawtext=fontfile='work/namek-three/arial.ttf':text='"+names[cid]+"':x=12:y=36:fontsize=17:fontcolor=white"
  captureEncoder=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb565le','-video_size','320x224','-framerate',str(fps),'-i','pipe:0','-vf',vf,'-an','-c:v','libx264','-preset','veryfast','-crf','16','-pix_fmt','yuv420p',str(root/(chapter+'-silent.mp4'))],stdin=subprocess.PIPE)
  audio_file=(root/(chapter+'.pcm')).open('wb')
  chain()
  if cid==5:cross()
  idle(3);f,b=face();hcf=[[b],['DOWN',b],['DOWN'],['DOWN',f],[f]]
  dirs=hcf*2 if cid==0 else hcf+[[b]] if cid==1 else [['DOWN'],['DOWN',f],[f],[b]] if cid==5 else [['DOWN'],['DOWN',b],[b],[f]]
  command(dirs,['B'] if cid==5 else ['A'],3 if cid!=1 else 4)
  while len(rows)<clip_frames:tick()
  expected={0:0xc05,1:0xc0f,3:0xc27,4:0xc31,5:0x84a}[cid]
  assert any(t['p']['program']==expected for t in rows)
  save_image(root/(chapter+'.png'))
  result=dict(label=chapter,frames=len(rows),damage=rows[0]['e']['hp']-rows[-1]['e']['hp'],maxHits=max(t['p']['hits'] for t in rows),fast=any(t['fast']&2 for t in rows),program=expected)
  reports.append(result);finish();print(result,flush=True)
 (root/'manifest.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),fps=fps,takes=reports,method='Native ROM framebuffer and audio; same scheduled inputs; normal speed. Initial spacing and facing staged before capture, no live HP/KI/timer edits. Coordinated human ports, not CPU play.'),indent=2))
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()

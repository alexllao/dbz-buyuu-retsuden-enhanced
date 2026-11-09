from pathlib import Path
import sys,json,hashlib
promoSlug=sys.argv[1];capture_from=int(sys.argv[2]) if len(sys.argv)>2 else 1
sys.path.insert(0,str(Path('work/namek-simulation').resolve()))
s=Path('work/input-v2/record.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0].replace("root=baseDir/'work/input-v2/video'/which","root=baseDir/'work/namek-native/promo'/promoSlug").replace("rompath='work/input-v2/candidate.bin' if which=='after' else 'work/responsive-cancels-v1/candidate.bin'","rompath='work/namek-native/integrated.bin'").replace("if which=='after':",'if True:')
sys.argv=['record','native'];exec(compile(s,'namek-video-runtime','exec'),globals())
from composite import Composite,np,Image
N=Path('work/namek-native/states')/promoSlug;reports=[];sim_phase='';fps=av.timing.fps

def tick(a=(),b=()):
 rawtick(a,b)
 if captureEncoder:
  w,h,pitch,data=latest;captureEncoder.stdin.write(b''.join(data[y*pitch:y*pitch+w*2] for y in range(h)))
  rows.append(dict(f=len(rows),phase=sim_phase,keys1=list(a),keys2=list(b),p=st(P1),e=st(P2),scene=rb(0xe73c),cinema=rw(0xe9c4),physicalStage=rb(0xe741),nativeVariant=rb(0xf7c0)))
  if len(rows)%90==1:save_image(root/f'{chapter}-qa-{len(rows):04}.png')

def start(label,state,title):
 global captureEncoder,audio_file,rows,chapter
 restore(state);chapter=label;rows=[]
 name={'original':'NAMEK ORIGINAL','normal':'NAMEK / GRAN PATRIARCA','aldea':'NAMEK / ALDEA DEVASTADA','porunga':'NAMEK / INVOCACION DE PORUNGA'}[promoSlug]
 vf="scale=960:672:flags=neighbor,pad=960:754:0:82:color=0x10151c,drawtext=fontfile='work/namek-three/arialbd.ttf':text='"+name+"':x=14:y=7:fontsize=25:fontcolor=0xffd35a,drawtext=fontfile='work/namek-three/arial.ttf':text='"+title+"':x=14:y=39:fontsize=19:fontcolor=white,drawtext=fontfile='work/namek-three/arial.ttf':text='CAPTURA REAL DEL EMULADOR / VELOCIDAD NORMAL':x=14:y=63:fontsize=13:fontcolor=0xcbd6e4"
 captureEncoder=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb565le','-video_size','320x224','-framerate',str(fps),'-i','pipe:0','-vf',vf,'-an','-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p',str(root/(label+'-silent.mp4'))],stdin=subprocess.PIPE)
 audio_file=(root/(label+'.pcm')).open('wb')

def begin(cid,label,title,distance=32,critical=False):
 restore((N/(f'critical-{cid}.state' if critical else f'seed-{cid}.state')).read_bytes());wb(P1+0xbe,0);wb(P2+0xbe,0);ww(P1+0xa,300);ww(P2+0xa,300+distance);ww(P1+0xc,0);ww(P2+0xc,0);wb(P1+0x59,0);wb(P2+0x59,1)
 for _ in range(8):tick()
 start(label,snap(),title)

def command(dirs,btn,speed=3):
 for k in [k for k in dirs for _ in range(speed)]+[dirs[-1]+btn]*3:tick(k)

def face():
 f='LEFT' if rb(P1+0x59) else 'RIGHT';return f,'RIGHT' if f=='LEFT' else 'LEFT'

def basics():
 contacts=[];hp=rw(P2+0x24)
 for f in range(120):
  k=['A'] if f<3 else []
  for i,t in enumerate(contacts[:2]):
   if t+3<=f<t+6:k=[['A','B'][i]]
  tick(k);now=rw(P2+0x24)
  if now<hp:contacts.append(f)
  hp=now
  if len(contacts)>=3:break
 return contacts

def summarize(expected=None):
 result=dict(label=chapter,romSha256=hashlib.sha256(rom).hexdigest(),stage=rb(0xe741),frames=len(rows),seconds=len(rows)/fps,damage=rows[0]['e']['hp']-rows[-1]['e']['hp'],maxHits=max(t['p']['hits'] for t in rows),nativeScenes=sorted(set(t['scene'] for t in rows)),nativeCinematics=sorted(set(t['cinema'] for t in rows)),programs=sorted(set(t['p']['program'] for t in rows)),expected=expected,firstHP=rows[0]['p']['hp'])
 if expected is not None:assert expected in result['programs'],result
 reports.append(result);finish();(root/(chapter+'-report.json')).write_text(json.dumps(result,indent=2));print(result,flush=True)

try:
 if capture_from==1:
  begin(0,'01-vuelo','SUELO - VUELO - DESPLAZAMIENTO - ATERRIZAJE',280);sim_phase='vuelo'
  for a,b,n in [([],[],30),(['C'],[],3),([],[],90),([],['C'],3),([],[],90),(['RIGHT'],['RIGHT'],35),(['C'],[],3),([],[],90),([],['C'],3),([],[],90)]:
   for _ in range(n):tick(a,b)
  assert any(t['p']['plane'] for t in rows) and any(t['e']['plane'] for t in rows)
  summarize()
 else:
  for label in ['01-vuelo','02-goku','03-gohan']:
   saved=json.loads((root/(label+'.json')).read_text());result=dict(label=label,romSha256=hashlib.sha256(rom).hexdigest(),stage=6,frames=len(saved),seconds=len(saved)/fps,damage=saved[0]['e']['hp']-saved[-1]['e']['hp'],maxHits=max(t['p']['hits'] for t in saved),nativeScenes=sorted(set(t['scene'] for t in saved)),nativeCinematics=sorted(set(t['cinema'] for t in saved)),programs=sorted(set(t['p']['program'] for t in saved)),firstHP=saved[0]['p']['hp']);reports.append(result);(root/(label+'-report.json')).write_text(json.dumps(result,indent=2))
 for cid,label,title,kind,expected in [(0,'02-goku','GOKU / BASICOS + KAMEHAMEHA','kame',0xc04),(1,'03-gohan','GOHAN / BASICOS + MASENKO','masenko',0xc0f),(3,'04-vegeta','VEGETA / BASICOS + METEOR','meteor',0x846),(5,'05-cell','CELL / BASICOS + CRUCE + METEOR','meteor',0x84a)]:
  if int(label[:2])<capture_from:continue
  begin(cid,label,title,critical=cid in [3,5]);sim_phase='basicos';hits=basics();assert len(hits)==3,(cid,hits)
  if cid==5:
   sim_phase='cambio-de-lado'
   for _ in range(120):
    if rb(P1+0x5b)<=8:break
    tick()
   f,b=face();command([[f],[b],[f]],['C'],4)
   for _ in range(100):
    if rw(P1)!=0x843 and rb(P1+0x5b)<=8:break
    tick()
  else:
   for _ in range(3):tick()
  sim_phase=kind;f,b=face();hcf=[[b],['DOWN',b],['DOWN'],['DOWN',f],[f]]
  if kind=='kame':command(hcf,['A'],4)
  elif kind=='masenko':command(hcf+[[b]],['A'],4)
  elif cid==3:command([[f],['DOWN',f],['DOWN'],['DOWN',b],[b],[f]],['B'],3)
  else:command([['DOWN'],['DOWN',f],[f],[b]],['B'],3)
  for i in range(900 if kind=='meteor' else 270):
   tick()
   if i>180 and rb(P1+0x5b)<=8 and rb(P2+0x5b)<=10 and not rb(0xe73c) and not rw(0xe9c4):
    for _ in range(40):tick()
    break
  summarize(expected)
 begin(0,'06-pantalla-partida','KAMEHAMEHA / ATAQUE GRANDE A DISTANCIA',400);sim_phase='especial-pantalla-partida';f,b=face();command([[b],['DOWN',b],['DOWN'],['DOWN',f],[f]],['A'],4)
 for i in range(900):
  tick()
  if i>360 and rw(P1)<0x400 and not rb(0xe73c) and not rw(0xe9c4):break
 assert any(t['scene'] or t['cinema'] for t in rows),'large technique cinematic did not start'
 summarize(0xc04)
 (N/'capture-manifest.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),backgroundIntegrated=True,method='Direct native RGB565 framebuffer/audio from integrated ROM. No background compositing. Stage selected by real menu inputs before fixture preparation.',takes=[json.loads(p.read_text()) for p in sorted(root.glob('*-report.json'))]),indent=2))
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()

from pathlib import Path
import sys,json,subprocess,struct,hashlib
BASE=Path.cwd();index=int(sys.argv[1]);pairs=[(0,3),(1,5),(2,8),(4,6),(7,9),(10,0),(3,4),(5,2),(6,1),(8,7),(9,10)];cid1,cid2=pairs[index];stage=index%9
out=BASE/'work/long-combos'/f'{index:02}';out.mkdir(parents=True,exist_ok=True);romfile=BASE/'outputs/combos-v3-generico/Buyuu_Retsuden_Enhanced_Combos_v3.bin'
sys.path.insert(0,str(BASE/'work'));sys.argv=['probe','--native','--rom',str(romfile),'--out',str(out)]
header=(BASE/'work/gameplay_probe.py').read_text().split('try:\n for index,step in enumerate(steps[:-1]):')[0].replace('BASE=Path(__file__).resolve().parent.parent','BASE=Path.cwd()')
header=header.replace("exec(compile(src,'local-emulator-setup','exec'),globals())",'''src=src.replace('def audio(l,r):pass', 'def audio(l,r):\\n if audio_file is not None:audio_file.write(struct.pack("<hh",l,r))')
src=src.replace('def batch(data,frames):return frames', 'def batch(data,frames):\\n if audio_file is not None:audio_file.write(C.string_at(data,frames*4))\\n return frames')
exec(compile(src,'local-emulator-setup','exec'),globals())''')
audio_file=None;exec(compile(header,'long-fight-setup','exec'),globals());encoder=None
names=['Goku','Gohan','Piccolo','Vegeta','Trunks','Cell','A18','Krilin','Freezer','Recoome','Ginyu']
class Pilot:
 def __init__(self,b,other,aggressive):self.b=b;self.other=other;self.aggressive=aggressive;self.seq=[];self.next=0;self.lastHP=0;self.hits=0;self.phase=0;self.started=0;self.lastOwnHP=200;self.combos=0
 def keys(self,f):
  b=self.b;o=self.other;act=rb(b+0x5b);oa=rb(o+0x5b);hp=rw(o+0x24);ownHP=rw(b+0x24);dist=rw(o+0xa)-rw(b+0xa);forward='RIGHT' if dist>0 else 'LEFT';back='LEFT' if dist>0 else 'RIGHT'
  if hp<self.lastHP and self.phase and f-self.started<180 and oa in [11,12]:
   self.hits+=1
   if self.hits==1:self.next=f+9;self.phase=2
   elif self.hits==2:self.next=f+9;self.phase=3
   elif self.hits==3:
    self.combos+=1;self.next=f+3;self.phase=4
  self.lastHP=hp
  if ownHP<self.lastOwnHP:self.phase=0;self.seq=[];self.next=f+25
  self.lastOwnHP=ownHP
  if self.seq:return self.seq.pop(0)
  if ownHP==0 or hp==0:return []
  if self.phase and (f-self.started>200 or (oa not in [11,12] and self.hits>0 and self.phase!=5)):
   self.phase=0;self.next=max(self.next,f+12)
  if self.phase in [2,3,4] and f>=self.next:
   if self.phase==2:self.seq=[['B']]*4;self.phase=5
   elif self.phase==3:self.seq=[['A']]*4;self.phase=5
   else:
    # Native technique B10; occasionally a longer Goku Meteor or native flurry.
    if rb(b+0x58)==0 and self.combos%3==0:dirs=[[forward],[forward,'DOWN'],['DOWN'],[back,'DOWN'],[back],[forward]]
    elif rb(b+0x58) in [0,1,7] and self.combos%3==2:dirs=[[back],[back,'DOWN'],['DOWN'],[forward,'DOWN'],[forward]]
    else:dirs=[[forward],['DOWN']]
    self.seq=[k for k in dirs for _ in range(4)]+[dirs[-1]+['B']]*4;self.phase=5
   return self.seq.pop(0)
  if self.phase:return []
  if f<self.next:return []
  if act not in list(range(9))+[13,14]:return []
  if rw(b+0x28)<125:
   if abs(dist)<110:return [back] if f%180<70 else ['A','B']
   return ['A','B']
  if abs(dist)>43:return [forward]
  # The second controller counters and guards, leaving different exchanges.
  if not self.aggressive and f%420<100:return [back]
  if not self.aggressive and f%113<30:return []
  self.phase=1;self.started=f;self.hits=0;self.lastHP=hp;self.seq=[['A']]*6;self.next=f+100
  return self.seq.pop(0)
try:
 for j,step in enumerate(steps[:-1]):
  if j in [9,11]:
   selected=cid1 if j==9 else cid2
   for direction,count in [('DOWN',selected//3),('RIGHT',selected%3)]:
    for _ in range(count):
     for _ in range(4):tick([direction])
     for _ in range(16):tick()
  if j==15:
   for _ in range(stage):
    for _ in range(4):tick(['RIGHT'])
    for _ in range(12):tick()
  for _ in range(step.get('frames',1)):tick([] if j==11 else step.get('buttons',[]))
 assert (rb(P1+0x58),rb(P2+0x58))==(cid1,cid2),(cid1,cid2,rb(P1+0x58),rb(P2+0x58))
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(60):tick()
 title=f'COMBOS V3 | {names[cid1]} vs {names[cid2]}'
 vf="scale=640:448:flags=neighbor,pad=640:496:0:48:color=0x10151c,drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='"+title+"':x=12:y=6:fontsize=19:fontcolor=white,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='ROM REAL - DOS MANDOS AUTOMATIZADOS - SIN CONTADOR':x=12:y=30:fontsize=12:fontcolor=0xbecbd8"
 encoder=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb565le','-video_size','320x224','-framerate',str(av.timing.fps),'-i','pipe:0','-vf',vf,'-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p',str(out/'silent.mp4')],stdin=subprocess.PIPE)
 audio_file=(out/'audio.pcm').open('wb');pilots=[Pilot(P1,P2,True),Pilot(P2,P1,False)];trace=[];ko=None
 for f in range(int(av.timing.fps*36)):
  a=pilots[0].keys(f);b=pilots[1].keys(f);tick(a,b);w,h,pitch,data=latest;encoder.stdin.write(b''.join(data[y*pitch:y*pitch+w*2] for y in range(h)))
  if f%3==0:trace.append({'frame':f,'keys1':a,'keys2':b,'hp1':rw(P1+0x24),'hp2':rw(P2+0x24),'action1':rb(P1+0x5b),'action2':rb(P2+0x5b),'combo1':rb(P1+0x106),'combo2':rb(P2+0x106)})
  if (rw(P1+0x24)==0 or rw(P2+0x24)==0) and ko is None:ko=f
  if ko is not None and f-ko>=180:break
 audio_file.close();audio_file=None;encoder.stdin.close();assert encoder.wait()==0;encoder=None
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(out/'silent.mp4'),'-f','s16le','-ar',str(round(av.timing.sample_rate)),'-ac','2','-i',str(out/'audio.pcm'),'-c:v','copy','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',str(out/'fight.mp4')],check=True)
 report={'romSha256':hashlib.sha256(rom).hexdigest(),'pair':[cid1,cid2],'stageSelection':stage,'frames':f+1,'fps':av.timing.fps,'seconds':(f+1)/av.timing.fps,'koFrame':ko,'comboAttempts':[p.combos for p in pilots],'finalHP':[rw(P1+0x24),rw(P2+0x24)],'fixture':'Native menus, native initial positions/HP/ki/actions/timers; both actor control flags set to human; two state-driven scripted controllers. Native sound, no postproduced hits or HUD counter. Fixed-length excerpts if no KO.','trace':trace}
 (out/'report.json').write_text(json.dumps(report,indent=2),encoding='utf8');save_image(out/'final.png');print(json.dumps({k:v for k,v in report.items() if k!='trace'}),flush=True)
finally:
 if audio_file:audio_file.close()
 if encoder:encoder.stdin.close();encoder.wait()
 core.retro_unload_game();core.retro_deinit()

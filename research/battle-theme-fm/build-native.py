from pathlib import Path
import json,struct,math,sys,hashlib
P=Path('work/battle-theme-fm');mode=sys.argv[1] if len(sys.argv)>1 else 'draft';score=json.loads((P/'score.json').read_text());fps=score['fps'];clock=53693175/7
voices=[v[:] for v in score['voices']]
if mode=='tone':voices=[[69,-1,-1,-1,-1] for _ in range(120)]
else:
 # Armonias mas estables: no rearticular una voz por una fluctuacion fugaz.
 for ch in range(2,5):
  stable=voices[0][ch];pending=stable;held=0
  for row in voices:
   if row[ch]==pending:held+=1
   else:pending=row[ch];held=1
   if held>=5:stable=pending
   row[ch]=stable
frames=[[] for _ in range(len(voices)+35)]
def event(t,port,reg,value):frames[t].append((port,reg,value,0))
def fm(t,ch,reg,value):event(t,ch//3,reg+ch%3,value)
def key(t,ch,on):event(t,0,0x28,(0xf0 if on else 0)+(ch if ch<3 else ch+1))
def frequency(t,ch,note):
 f=440*2**((note-69)/12);block=max(0,min(7,int(note)//12-1));fnum=round(f*144*2**20/clock/2**(block-1))
 assert 0<fnum<2048,(note,block,fnum)
 fm(t,ch,0xa4,(block<<3)|(fnum>>8));fm(t,ch,0xa0,fnum&255)
event(0,0,0x22,0);event(0,0,0x27,0);event(0,0,0x2b,0)
for v in [0x9f,0xbf,0xdf,0xff]:event(0,2,0,v)
presets=[dict(alg=4,feedback=4,mul=[1,2,1,1],tl=[40,49,20,25],ar=31,decay=8,sustain=0x48),dict(alg=4,feedback=3,mul=[1,2,1,1],tl=[43,53,22,30],ar=31,decay=12,sustain=0x68),dict(alg=7,feedback=0,mul=[1,2,3,1],tl=[37,49,59,55],ar=22,decay=5,sustain=0x46),dict(alg=7,feedback=0,mul=[1,2,3,1],tl=[40,52,62,58],ar=22,decay=5,sustain=0x46),dict(alg=4,feedback=2,mul=[1,1,2,1],tl=[54,61,40,46],ar=25,decay=8,sustain=0x46),dict(alg=7,feedback=0,mul=[1,1,1,1],tl=[25,127,127,127],ar=31,decay=22,sustain=0x0f)]
if mode=='tone':presets[0]=dict(alg=7,feedback=0,mul=[1,1,1,1],tl=[30,127,127,127],ar=31,decay=0,sustain=0x0f)
for ch,p in enumerate(presets):
 key(0,ch,False);fm(0,ch,0xb0,(p['feedback']<<3)|p['alg']);fm(0,ch,0xb4,[0xc0,0xc0,0x80,0x40,0xc0,0xc0][ch])
 for op,off in enumerate([0,4,8,12]):
  for reg,value in [(0x30,p['mul'][op]),(0x40,p['tl'][op]),(0x50,p['ar']),(0x60,p['decay']),(0x70,0),(0x80,p['sustain']),(0x90,0)]:fm(0,ch,reg+off,value)
last=[-1]*5
for i,row in enumerate(voices):
 t=i+3
 for ch,note in enumerate(row):
  if note!=last[ch]:
   key(t,ch,False)
   if note>=0:frequency(t,ch,note);key(t,ch,True)
   last[ch]=note
if mode!='tone':
 for i in score['kick']:
  t=i+3;key(t,5,False);frequency(t,5,43);key(t,5,True)
  if t+4<len(frames):frequency(t+2,5,34);key(t+4,5,False)
 for i in score['hat']:
  t=i+3;event(t,2,0,0xe4);event(t,2,0,0xf9);event(t+2,2,0,0xff)
 for i in score['snare']:
  t=i+3;event(t,2,0,0xe5);event(t,2,0,0xf6)
  for j,volume in [(2,10),(3,12),(5,15)]:event(t+j,2,0,0xf0|volume)
for ch in range(6):key(len(voices)+3,ch,False)
event(len(voices)+3,2,0,0xff)
data=b''.join(struct.pack('>H',len(e))+b''.join(bytes(v) for v in e) for e in frames)+b'\xff\xff'
r=bytearray(b'\xff'*max(0x20000,((0x1000+len(data)+65535)//65536)*65536))
for at in range(0,0x100,4):struct.pack_into('>I',r,at,0x200)
struct.pack_into('>II',r,0,0x00fffffc,0x200)
r[0x100:0x110]=b'SEGA MEGA DRIVE '
r[0x110:0x120]=b'(C)ALEX LLAO 26 '
title=b'BATTLE THEME FM - INDEPENDENT AUDIO STUDY'.ljust(48)
for at in [0x120,0x150]:r[at:at+48]=title
r[0x180:0x18e]=b'GM 00000000-00';r[0x190:0x1a0]=b'J'.ljust(16)
struct.pack_into('>4I',r,0x1a0,0,len(r)-1,0xff0000,0xffffff)
r[0x1f0:0x200]=b'JUE'.ljust(16)
code=(P/'player.bin').read_bytes();assert len(code)<0xe00;r[0x200:0x200+len(code)]=code;r[0x1000:0x1000+len(data)]=data
struct.pack_into('>H',r,0x18e,sum(struct.unpack('>'+str((len(r)-512)//2)+'H',r[512:]))&65535)
(P/(mode+'.bin')).write_bytes(r)
(P/(mode+'-stream.json')).write_text(json.dumps(dict(mode=mode,romSha256=hashlib.sha256(r).hexdigest(),frames=len(frames),seconds=len(frames)/fps,registerWrites=sum(len(e) for e in frames),maxWritesPerFrame=max(len(e) for e in frames),scoreVoices=voices,scope='Standalone original test cartridge, not Buyuu Retsuden. No source MP3 samples stored or played. Notes interpreted by YM2612/PSG register writes.'),indent=1))
print(mode,'bytes',len(r),'events',sum(len(e) for e in frames),'frames',len(frames))

from pathlib import Path
from collections import Counter
import sys
sys.path.insert(0,str(Path('work/namek-simulation').resolve()))
from vdp import layers,np,VOFF
from PIL import Image

class Composite:
 def __init__(self,art_path):
  self.art=np.asarray(Image.open(art_path).convert('RGB').resize((512,512),Image.Resampling.NEAREST))
  r=Path('work/combo-startup/candidate.bin').read_bytes();fullmap=np.frombuffer(r,dtype='>u2',count=4096,offset=0x19851a).reshape(64,64);self.original=fullmap&0x1fff
  keys={}
  for y in range(64):
   for x in range(64):
    k=tuple(int(self.original[y,(x+i)%64]) for i in range(5));keys.setdefault(k,[]).append((x,y))
  self.anchors={k:v[0] for k,v in keys.items() if len(v)==1};self.cache={};self.last=[(52,16),(52,16)]
  ss=Path('work/namek-simulation/ground.state').read_bytes();v=np.frombuffer(ss,dtype=np.uint8,count=65536,offset=VOFF).reshape(-1,2)[:,::-1].ravel();patterns=np.stack((v>>4,v&15),axis=1).reshape(2048,8,8)
  yy,xx=np.mgrid[0:512,0:512];attr=fullmap[yy//8,xx//8];px=np.where(attr&0x800,7-(xx&7),xx&7);py=np.where(attr&0x1000,7-(yy&7),yy&7)
  self.worldIndex=((attr>>13)&3)*16+patterns[attr&2047,py,px]
  self.hashCache={};self.rasterLast={}
 def registration(self,words,base,p):
  m=words[base//2:base//2+4096].reshape(64,64)&0x1fff;khash=hash(m.tobytes())
  if khash in self.cache:return self.cache[khash]
  offsets=Counter()
  for y in range(0,64,2):
   for x in range(0,60,3):
    k=tuple(int(v) for v in m[y,x:x+5]);old=self.anchors.get(k)
    if old is not None:offsets[((x-old[0])%64,(y-old[1])%64)]+=1
  best=offsets.most_common(1)[0][0] if offsets else self.last[p];self.last[p]=best
  self.cache[khash]=best;return best
 def frame(self,state,latest,raster=False):
  w,h,pitch,data=latest;raw=np.frombuffer(data,dtype='<u2').reshape(h,pitch//2)[:,:w]
  rgb=np.stack((((raw>>11)&31)*255//31,((raw>>5)&63)*255//63,(raw&31)*255//31),axis=-1).astype(np.uint8)
  ly=layers(state);words=np.frombuffer(state,dtype='<u2',count=32768,offset=VOFF);r=ly['regs'];bases=[(int(r[2])&0x38)<<10,(int(r[4])&7)<<13];uv=[];offsets=[]
  for p,(x,y) in enumerate([(ly['ax'],ly['ay']),(ly['bx'],ly['by'])]):
   dx,dy=self.registration(words,bases[p],p);offsets.append([dx,dy]);uv.append(((x-dx*8)%512,(y-dy*8)%512))
  useA=ly['owner']==0;wx=np.where(useA,uv[0][0],uv[1][0]);wy=np.where(useA,uv[0][1],uv[1][1])
  corrected=0
  if raster:
   # HBlank cinematics can change scroll within a frame. Recover those
   # vertical camera bands from read-only native background row matching.
   cram=np.frombuffer(state,dtype='<u2',count=64,offset=VOFF+65536)
   rl=np.array([0,4,8,12,17,21,25,29],np.uint16);gl=np.array([0,8,17,25,34,42,51,59],np.uint16)
   palette=(rl[cram&7]<<11)|(gl[(cram>>3)&7]<<5)|rl[(cram>>6)&7];world=palette[self.worldIndex]
   self.debug=dict(raw=raw.copy(),foreground=ly['foreground'].copy(),world=world,wx=wx.copy(),wy=wy.copy())
   paletteKey=hash(palette.tobytes());points=[(0,0),(0,7),(0,15),(2,5),(4,11),(6,3)];prime=1099511628211;mask64=(1<<64)-1
   lookup=self.hashCache.get(paletteKey)
   if lookup is None:
    hashes=np.full((512,512),1469598103934665603,np.uint64)
    for dy,dx in points:hashes=(hashes^np.roll(world,(-dy,-dx),(0,1)))*np.uint64(prime)
    flat=hashes.ravel();order=np.argsort(flat);sortedKeys=flat[order];starts=np.r_[0,np.flatnonzero(sortedKeys[1:]!=sortedKeys[:-1])+1];ends=np.r_[starts[1:],len(order)]
    lookup={int(sortedKeys[a]):order[a:z].tolist() for a,z in zip(starts,ends) if z-a<=16};self.hashCache[paletteKey]=lookup
   for lo,hi in [(0,160),(160,320)]:
    bandOffsets={};previousBand=None
    for top in range(32,224,8):
     votes=Counter()
     for x in range(lo,hi-15,8):
      if any(ly['foreground'][top+dy,x+dx] for dy,dx in points):continue
      signature=1469598103934665603
      for dy,dx in points:signature=((signature^int(raw[top+dy,x+dx]))*prime)&mask64
      for pos in lookup.get(signature,[]):votes[((pos%512-x)%512,(pos//512-top)%512)]+=1
     if not votes:continue
     best=max(votes.values());choices=[v for v,n in votes.items() if n==best]
     predicted=((int(wx[top,(lo+hi)//2])-(lo+hi)//2)%512,(int(wy[top,(lo+hi)//2])-top)%512);reference=previousBand if previousBand is not None else self.rasterLast.get((lo,top),predicted)
     dist=lambda v:sum(min((v[i]-reference[i])%512,(reference[i]-v[i])%512) for i in [0,1]);dx,dy=min(choices,key=dist);self.rasterLast[(lo,top)]=(dx,dy);bandOffsets[top]=(dx,dy);previousBand=(dx,dy)
     for y in range(top,top+8):wx[y,lo:hi]=(np.arange(lo,hi)+dx)%512;wy[y,lo:hi]=(y+dy)%512
     corrected+=8
    for top in range(32,224,8):
     if top in bandOffsets or not bandOffsets:continue
     near=min(bandOffsets,key=lambda t:abs(t-top));dx,dy=bandOffsets[near]
     for y in range(top,top+8):wx[y,lo:hi]=(np.arange(lo,hi)+dx)%512;wy[y,lo:hi]=(y+dy)%512
  # Artistic framing for this simulation, not a certified ROM camera mapping.
  sx=wx.astype(np.int32)%512;sy=np.clip(np.rint(130+(wy.astype(np.float32)-248)*1.4),0,511).astype(np.int32)
  self.coordinates=(sx,sy,ly['foreground']);self.blank=(not int(r[1])&64 or np.count_nonzero(raw!=raw[100,100])<100)
  background=self.art[sy,sx];proposal=np.where(ly['foreground'][:,:,None],rgb,background)
  if not int(r[1])&64 or np.count_nonzero(raw!=raw[100,100])<100:proposal=rgb.copy()
  return rgb,proposal,dict(registration=offsets,sprites=ly['spriteCount'],hscroll=[int(words[0xa800//2]),int(words[0xa800//2+1])],vscroll=[int.from_bytes(state[VOFF+0x10080+i*2:VOFF+0x10082+i*2],'little') for i in range(2)],foregroundFraction=float(ly['foreground'].mean()),rasterRowsCorrected=corrected)

import sys
from pathlib import Path
sys.path.insert(0,str(Path('work/simulation-deps').resolve()))
import numpy as np
VOFF=0x12425
Y,X=np.mgrid[0:224,0:320]

def layers(state):
 v=np.frombuffer(state,dtype=np.uint8,count=65536,offset=VOFF)
 words=np.frombuffer(state,dtype='<u2',count=32768,offset=VOFF)
 native=v.reshape(-1,2)[:,::-1].ravel()
 patterns=np.stack((native>>4,native&15),axis=1).reshape(2048,8,8)
 regs=np.frombuffer(state,dtype=np.uint8,count=32,offset=VOFF+0x10100)
 vs=np.frombuffer(state,dtype='<u2',count=64,offset=VOFF+0x10080)
 width=32<<(int(regs[16])&3);height=32<<((int(regs[16])>>4)&3)
 hb=(int(regs[13])&63)<<10;hm=int(regs[11])&3
 hoff=(Y if hm==3 else Y&~7 if hm==2 else np.zeros_like(Y))*4
 def plane(p):
  base=((int(regs[2])&0x38)<<10) if p==0 else ((int(regs[4])&7)<<13)
  h=words[((hb+hoff+p*2)//2)&32767]
  vv=vs[((X//16)*2+p)%64] if int(regs[11])&4 else int(vs[p])
  wx=(X-h.astype(np.int32))%(width*8);wy=(Y+vv)%(height*8)
  attr=words[(base//2+(wy//8)*width+wx//8)&32767]
  return sample(attr,wx,wy),wx,wy
 def sample(attr,xx,yy):
  px=xx&7;py=yy&7;px=np.where(attr&0x800,7-px,px);py=np.where(attr&0x1000,7-py,py)
  pix=patterns[attr&0x7ff,py,px];return dict(valid=pix!=0,priority=(attr&0x8000)!=0,foreground=(attr&0x7ff)>=0x300,color=((attr>>13)&3)*16+pix,attr=attr)
 A,ax,ay=plane(0);B,bx,by=plane(1)
 # The window replaces plane A in the hardware's horizontal/vertical union.
 hx=(int(regs[17])&31)*16;vy=(int(regs[18])&31)*8
 winx=(X>=hx) if int(regs[17])&128 else (X<hx)
 winy=(Y>=vy) if int(regs[18])&128 else (Y<vy)
 win=winx|winy;wwidth=64 if int(regs[12])&1 else 32;wb=(int(regs[3])&(0x3c if wwidth==64 else 0x3e))<<10
 wa=words[(wb//2+(Y//8)*wwidth+X//8)&32767];W=sample(wa,X,Y)
 for k in A:A[k]=np.where(win,W[k],A[k])
 sv=np.zeros((224,320),bool);sp=np.zeros_like(sv);sc=np.zeros((224,320),np.uint8)
 sb=(int(regs[5])&(0x7e if int(regs[12])&1 else 0x7f))<<9;n=0;seen=set()
 for _ in range(80):
  if n in seen:break
  seen.add(n);i=(sb//2+n*4)&32767;sy,sz,attr,sx=[int(x) for x in words[i:i+4]];sx=(sx&511)-128;sy=(sy&511)-128;w=((sz>>10)&3)+1;h=((sz>>8)&3)+1
  xx=np.arange(w*8)[None,:];yy=np.arange(h*8)[:,None];tx=(w*8-1-xx) if attr&0x800 else xx;ty=(h*8-1-yy) if attr&0x1000 else yy
  p=patterns[((attr&2047)+(tx//8)*h+ty//8)&2047,ty%8,tx%8]
  x0=max(0,sx);y0=max(0,sy);x1=min(320,sx+w*8);y1=min(224,sy+h*8)
  if x1>x0 and y1>y0:
   src=p[y0-sy:y1-sy,x0-sx:x1-sx];dest=sv[y0:y1,x0:x1];use=(src!=0)&~dest;dest[use]=True;sp[y0:y1,x0:x1][use]=bool(attr&0x8000);sc[y0:y1,x0:x1][use]=(((attr>>13)&3)*16+src)[use]
  n=sz&127
  if n==0:break
 # All sprites are foreground, but retain plane priority / occlusion.
 rank=np.zeros((224,320),np.uint8);fg=np.zeros_like(sv);color=np.full((224,320),int(regs[7])&63,np.uint8);owner=np.full((224,320),1,np.uint8)
 for plane,data,rlo,rhi in [(1,B,1,4),(0,A,2,5),(2,dict(valid=sv,priority=sp,foreground=np.ones_like(sv),color=sc),3,6)]:
  level=np.where(data['priority'],rhi,rlo).astype(np.uint8);use=data['valid']&(level>rank);rank[use]=level[use];fg[use]=data['foreground'][use];color[use]=data['color'][use];owner[use]=plane
 fg[:32]=True
 return dict(foreground=fg,color=color,owner=owner,ax=ax,ay=ay,bx=bx,by=by,regs=regs,spriteCount=len(seen))

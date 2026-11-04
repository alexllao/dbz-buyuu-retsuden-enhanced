from pathlib import Path
import struct,json,hashlib,sys
sys.path.insert(0,'work/auras');sys.path.insert(0,'work/auras/v2')
from pack_flame import pack_flame
from pack_c2 import load,tile
from build_c2 import be,sprite,lz_literal
ROOT=Path('work/auras/v2')

def effect(name,w,h):
 raw=(ROOT/(name+'.rgba')).read_bytes();p=[]
 for i in range(0,len(raw),4):
  r,g,b,a=raw[i:i+4]
  if name=='bolt':v=15 if a>=160 and min(r,g,b)>225 else 0
  else:v=0 if a<200 else 8 if r-g>35 else 7
  p.append(v)
 if name=='bolt':
  # Quantization of a thin source can leave isolated dots. Trace its main
  # path and connect it on the native grid, retaining a readable two-pixel arc.
  points=[];previous=w//2
  for y in range(h):
   xs=[x for x in range(w) if p[y*w+x]]
   if xs:
    previous=min(xs,key=lambda x:abs(x-previous));points.append((previous,y))
  assert points
  points=[(points[0][0],0)]+points+[(points[-1][0],h-1)]
  connected=[0]*(w*h)
  for (x0,y0),(x1,y1) in zip(points,points[1:]):
   steps=max(abs(x1-x0),y1-y0,1)
   for k in range(steps+1):
    x=round(x0+(x1-x0)*k/steps);y=round(y0+(y1-y0)*k/steps)
    connected[y*w+x]=15
    connected[y*w+min(w-1,x+1)]=15
  p=connected
 return p
def pack(p,w,h):return b''.join(tile(p,w,x,y) for x in range(0,w,8) for y in range(0,h,8))

def build():
 atlas,cs=pack_flame();flame_tiles=len(atlas)//32
 pixels=load(64,112)
 bolt_tile=0x513+len(atlas)//32;atlas+=pack(effect('bolt',8,32),8,32)
 dp=effect('dust',8,8);dust_tile=0x513+len(atlas)//32;atlas+=pack(dp,8,8)
 for size in (6,4):
  small=[0]*64
  for y in range(size):
   for x in range(size):small[(8-size+y)*8+(8-size)//2+x]=dp[min(7,y*8//size)*8+min(7,x*8//size)]
  atlas+=pack(small,8,8)
 assert len(atlas)<=1440;atlas=atlas.ljust(1440,b'\0');(ROOT/'tiles.bin').write_bytes(atlas)
 def locate(data):return 0x513+next(i for i in range(0,len(atlas)-len(data)+1,32) if atlas[i:i+len(data)]==data)//32
 large=[]
 def add(x,y,hs,data):
  # The central strip is repeated to widen the flame by16px, with no new tiles.
  positions=[x-40] if x!=24 else ([-8] if y<0 else [-8,-16])
  for px in positions:
   for flip in (False,True):large.append((locate(data),-px-8 if flip else px,y-104,hs,flip))
 for x,y,hs,data in cs:
  assert y>=64 or y+hs<=64
  add(x,y-16 if y<64 else y,hs,data)
 # Insert a16px horizontal band at mid-height; base stays on the same ground.
 for x in range(0,32,8):
  data=tile(pixels,64,x,64)+tile(pixels,64,x,72);yy=48
  while data and not any(data[:32]):yy+=8;data=data[32:]
  while data and not any(data[-32:]):data=data[:-32]
  if data:add(x,yy,len(data)//4,data)
 maps=[]
 for airborne in (False,True):
  for frame in range(8):
   for lightning in range(2):
    for scale in (1,.75,.5,.25):
     entries=[]
     if lightning and scale>=.5 and frame in (0,1,4,5):
      # Two long arcs, visible in brief paired bursts with changing origins.
      for j,(x,y) in enumerate([(-36,-111),(28,-67)] if frame<4 else [(-38,-77),(30,-116)]):
       entries.append(sprite(0xe000|bolt_tile|(0x800 if (j+frame)%2 else 0)|(0x1000 if frame&1 else 0),round(x*scale),round(y*scale),1,4))
     if not airborne and scale>=.5:
      for cohort in (0,):
       age=(frame+cohort)%8
       for side in (-1,1):
        radius=20+age*4
        x=side*radius-4;y=4-[0,1,3,5,4,2,1,0][age]
        t=dust_tile+(2 if age in (0,7) else 1 if age in (1,6) else 0)
        entries.append(sprite(0xe000|t|(0x800 if side<0 else 0),x,y,1,1))
     if scale==1:
      flame=large
     else:
      # Use progressively fewer native pieces; collapsing every full-size
      # sprite would exceed the VDP's per-scanline limits during the exit.
      selected=cs if scale==.75 else [c for c in cs if (c[0]==0 or c[0]==24 and c[1] in (0,64,96))] if scale==.5 else [c for c in cs if c[0]==0 and c[1]>=64 or c[0]==24 and c[1]==96]
      flame=[]
      for x,y,hs,data in selected:
       for flip in (False,True):
        px=x-32 if not flip else 24-x;py=y-104
        if scale==.75:nx=px;ny=py-4
        else:nx=round((px+4)*scale)-4;ny=round((py+hs)*scale)-hs
        flame.append((locate(data),nx,ny,hs,flip))
     for tid,x,y,hs,flip in flame:
      nx=x;ny=y
      if frame&1 and abs(x)>=24:nx+=-1 if x<0 else 1
      if frame in (2,3,6,7) and abs(x)<16:ny-=1
      entries.append(sprite(0xe000|tid|(0x800 if flip else 0),nx,ny,1,hs//8))
     maps.append(be(len(entries))+b''.join(entries))
 code=bytearray((ROOT/'aura_hook.bin').read_bytes());labels=dict((k,int(v,16)) for k,v in (s.split('=') for s in (ROOT/'aura_hook.labels.txt').read_text().splitlines()))
 source=Path('outputs/dbz-jugabilidad-v1/Buyuu_Retsuden_Jugabilidad_v1_Colores_v1.bin').read_bytes();rom=bytearray(source)
 assert source[0x9ece:0x9ed4].hex()=='4a2800bd6734'
 assert source[0x9994:0x999a].hex()=='41fa1d5a4e71'
 regions=[(0x7b800,0x7d800),(0x1b7c40,0x1c0000)];ri=0;at=regions[0][0];ptrs=[]
 for data in maps:
  if at+len(data)>regions[ri][1]:ri+=1;at=regions[ri][0]
  assert at+len(data)<=regions[ri][1]
  assert set(source[at:at+len(data)])=={255}
  ptrs.append(at);rom[at:at+len(data)]=data;at+=len(data)
 assert len(ptrs)==128
 table=labels['aura_map_table']-0x7b400;code[table:table+512]=struct.pack('>128I',*ptrs)
 assert 0x7b400+len(code)<=0x7b800
 rom[0x7b400:0x7b400+len(code)]=code;rom[0x9ece:0x9ed4]=bytes.fromhex('4ef9')+struct.pack('>I',labels['aura_entry'])
 compressed=lz_literal(atlas);rom[0x7d800:0x7d800+len(compressed)]=compressed
 rom[0x9994:0x999a]=bytes.fromhex('41f9')+struct.pack('>I',0x7d800)
 struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>1048320H',rom[512:]))&65535)
 path=Path('work/rom/auras-c2-v2.bin');path.write_bytes(rom)
 record=dict(status='Experimental C2v2 pending runtime validation',rom=str(path),sha256=hashlib.sha256(rom).hexdigest(),code_bytes=len(code),flame_tiles=flame_tiles,tile_bytes=len(atlas),flame_dimensions=[80,128],previous_dimensions=[64,112],original_dimensions=[80,112],max_sprites=max(int.from_bytes(m[:2],'big') for m in maps),animation_frames=8,maps=[hex(p) for p in ptrs],dust='Two moving ground puffs; three native sizes; no airborne dust',lightning='Two32px white arcs; brief bursts onlyGohanSSJ2/Cell; native shared index15',known_ground_y='0x1C0')
 (ROOT/'build.json').write_text(json.dumps(record,indent=2));print(json.dumps({k:v for k,v in record.items() if k!='maps'},indent=2))
if __name__=='__main__':build()

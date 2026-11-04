from pathlib import Path
from collections import deque
import sys,json
sys.path.insert(0,'work');sys.path.insert(0,'work/auras')
import extract_sprite as e
from pack_c2 import merge_tiles
ROOT=Path('work/auras/v3')
def prepare():
 raw=(ROOT/'snes-aura-source.rgba').read_bytes();pixels=[]
 colors=[(255,255,255),(255,240,0),(255,145,0)]
 for i in range(0,len(raw),4):
  r,g,b,a=raw[i:i+4]
  pixels.append(0 if a<128 else [7,11,8][min(range(3),key=lambda c:sum((raw[i+k]-colors[c][k])**2 for k in range(3)))])
 for y in range(128):
  for x in range(40):pixels[y*80+79-x]=pixels[y*80+x]
 # Native alpha normalization: only enclosed holes are filled, external gaps
 # between pointed flame tongues retain the reference outline.
 outside=set();queue=deque()
 for y in range(128):
  for x in range(80):
   if (x in (0,79) or y in (0,127)) and not pixels[y*80+x]:outside.add((x,y));queue.append((x,y))
 while queue:
  x,y=queue.popleft()
  for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
   if 0<=xx<80 and 0<=yy<128 and not pixels[yy*80+xx] and (xx,yy) not in outside:outside.add((xx,yy));queue.append((xx,yy))
 holes=[(x,y) for y in range(128) for x in range(80) if not pixels[y*80+x] and (x,y) not in outside]
 for x,y in holes:pixels[y*80+x]=7
 def tile(x,y):return bytes(pixels[(y+dy)*80+x+dx]<<4|pixels[(y+dy)*80+x+dx+1] for dy in range(8) for dx in range(0,8,2))
 chunks=[]
 for x in range(0,40,8):
  for y in range(0,128,32):
   data=b''.join(tile(x,y+dy) for dy in range(0,32,8));yy=y
   while data and not any(data[:32]):yy+=8;data=data[32:]
   while data and not any(data[-32:]):data=data[:-32]
   if data:chunks.append((x,yy,len(data)//4,data))
 atlas=merge_tiles(sorted(set(c[3] for c in chunks)))
 assert len(atlas)%32==0
 pal=[0]*6+[e.u16(0x9102+2*i) for i in range(10)]
 e.png(ROOT/'C2-v3-direct-contour.png',80,128,pixels,pal,scale=6)
 (ROOT/'direct-flame-tiles.bin').write_bytes(atlas)
 record=dict(width=80,height=128,flame_tiles=len(atlas)//32,flame_sprites=2*len(chunks),pixels=pixels,filled_enclosed_alpha_pixels=len(holes),source='User-supplied SNES aura, native palette conversion and mirrored left outline',parts=[dict(x=x,y=y,height=hs,tile=next(i//32 for i in range(0,len(atlas)-len(data)+1,32) if atlas[i:i+len(data)]==data)) for x,y,hs,data in chunks])
 (ROOT/'direct-art.json').write_text(json.dumps(record,indent=2));print({k:v for k,v in record.items() if k not in ('pixels','parts')})
 return atlas,record
if __name__=='__main__':prepare()

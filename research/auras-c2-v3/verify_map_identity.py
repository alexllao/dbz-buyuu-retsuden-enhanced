from pathlib import Path
from collections import deque
import json

root=Path('work/auras/v3')
rom=Path('work/rom/auras-c2-v3.bin').read_bytes();atlas=(root/'tiles.bin').read_bytes()
build=json.loads((root/'build.json').read_text());art=json.loads((root/'direct-art.json').read_text())
target=art['pixels'];counts=[]
for ptr in build['map_addresses']:
 a=int(ptr,16);n=int.from_bytes(rom[a:a+2],'big');pixels=[0]*(80*128);flames=0
 for i in range(n):
  q=a+2+6*i;attr=int.from_bytes(rom[q:q+2],'big');tid=attr&0x7ff
  assert tid!=0x540
  if tid>=0x54b:continue
  flames+=1
  hi=rom[q+4];x=((hi&15)<<8)|rom[q+2];y=((hi>>4)<<8)|rom[q+3]
  if x&0x800:x-=4096
  if y&0x800:y-=4096
  size=rom[q+5];w=((size>>2)&3)+1;h=(size&3)+1
  for dy in range(h*8):
   for dx in range(w*8):
    sx=w*8-1-dx if attr&0x800 else dx;sy=h*8-1-dy if attr&0x1000 else dy
    physical=tid+(sx//8)*h+sy//8
    assert physical!=0x540
    logical=physical-0x513-(physical>=0x541)
    off=logical*32+(sy%8)*4+(sx%8)//2
    color=(atlas[off]>>(0 if sx&1 else 4))&15
    xx=x+40+dx;yy=y+120+dy
    assert 0<=xx<80 and 0<=yy<128
    if color:pixels[yy*80+xx]=color
 assert pixels==target,(ptr,sum(a!=b for a,b in zip(pixels,target)))
 counts.append(flames)
outside=set();queue=deque()
for y in range(128):
 for x in range(80):
  if (x in (0,79) or y in (0,127)) and not target[y*80+x]:outside.add((x,y));queue.append((x,y))
while queue:
 x,y=queue.popleft()
 for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
  if 0<=xx<80 and 0<=yy<128 and not target[yy*80+xx] and (xx,yy) not in outside:outside.add((xx,yy));queue.append((xx,yy))
holes=sum(not target[y*80+x] and (x,y) not in outside for y in range(128) for x in range(80))
report={'maps_checked':len(counts),'flame_sprites_per_map':sorted(set(counts)),'pixel_identity_with_indexed_source':True,'enclosed_alpha_holes':holes,'reserved_tile540_references':0,'method':'Independent decode of384actualROMsprite maps, remap physical tile gap and reconstruct80x128flame bitmap; compare every palette-index pixel against direct-art.json.'}
assert holes==0
(root/'qa-map-identity.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))

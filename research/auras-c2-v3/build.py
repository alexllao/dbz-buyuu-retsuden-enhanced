from pathlib import Path
import struct,json,hashlib,sys
sys.path.insert(0,'work/auras');sys.path.insert(0,'work/auras/v3')
from build_c2 import be,sprite,lz_literal
from pack_direct import prepare
ROOT=Path('work/auras/v3')
BASE=0x513
def physical(logical):return BASE+logical+(logical>=45)
def unpack_pattern(data):return [data[y*4+x//2]>>(0 if x&1 else 4)&15 for y in range(16) for x in range(8)]
def pack_pattern(p):return bytes(p[y*8+x]<<4|p[y*8+x+1] for y in range(16) for x in range(0,8,2))
def build():
 atlas,art=prepare();assert len(atlas)==55*32
 old=Path('work/auras/v2/tiles.bin').read_bytes();ray=old[38*32:42*32]
 patterns=[unpack_pattern(ray[:64]),unpack_pattern(ray[64:]),[0]*128]
 patterns[2]=[patterns[0][y*8+7-x] for y in range(16) for x in range(8)]
 assert len({pack_pattern(p) for p in patterns})==3
 for p in patterns:atlas+=pack_pattern(p)
 atlas+=old[42*32:45*32];assert len(atlas)==64*32
 (ROOT/'tiles.bin').write_bytes(atlas)
 body=[]
 for part in art['parts']:
  start=part['tile'];remaining=part['height']//8;y=part['y']
  while remaining:
   take=min(remaining,45-start) if start<45 else remaining
   for flip in (False,True):
    x=part['x']-40 if not flip else 32-part['x']
    body.append((physical(start),x,y-120,take,flip))
   start+=take;remaining-=take;y+=take*8
 # Decode the assembled body and compare every indexed pixel with the source.
 target=art['pixels'];render=[0]*(80*128)
 for tid,x,y,tiles_h,flip in body:
  logical=tid-BASE-(tid>0x540)
  for dy in range(tiles_h*8):
   for dx in range(8):
    sx=7-dx if flip else dx;off=(logical+dy//8)*32+dy%8*4+sx//2;v=atlas[off]>>(0 if sx&1 else 4)&15
    if v:render[(y+120+dy)*80+x+40+dx]=v
 assert render==target,'Native map introduced a hole or changed a flame pixel'
 def endpoint(pattern,row,flip):
  xs=[x for x in range(8) if pattern[row*8+x]];x=xs[len(xs)//2]
  return 7-x if flip else x
 maps=[]
 for airborne in (False,True):
  for frame in range(24):
   for lightning in range(2):
    for fade in range(4):
     entries=[];age=frame%8
     if lightning and fade<2 and (frame//3)%2==0:
      state=frame%3
      for j,(x,y) in enumerate([(-36,-108),(28,-72)] if (frame//6)%2==0 else [(-38,-78),(30,-112)]):
       first=state;second=(state+1)%3;flip1=bool((j+frame)&1);flip2=not flip1
       dx=endpoint(patterns[first],15,flip1)-endpoint(patterns[second],0,flip2)
       entries.append(sprite(0xe000|physical(55+first*2)|(0x800 if flip1 else 0),x,y,1,2))
       entries.append(sprite(0xe000|physical(55+second*2)|(0x800 if flip2 else 0),x+dx,y+16,1,2))
     if not airborne and fade<3:
      for side in (-1,1):
       radius=20+age*4;y=4-[0,1,3,5,4,2,1,0][age];size=2 if age in (0,7) else 1 if age in (1,6) else 0
       entries.append(sprite(0xe000|physical(61+size)|(0x800 if side<0 else 0),side*radius-4,y,1,1))
     for tid,x,y,hs,flip in body:entries.append(sprite(0xe000|tid|(0x800 if flip else 0),x,y,1,hs))
     maps.append(be(len(entries))+b''.join(entries))
 code=bytearray((ROOT/'aura_hook.bin').read_bytes());labels=dict((k,int(v,16)) for k,v in (s.split('=') for s in (ROOT/'aura_hook.labels.txt').read_text().splitlines()))
 source=Path('outputs/dbz-jugabilidad-v1/Buyuu_Retsuden_Jugabilidad_v1_Colores_v1.bin').read_bytes();rom=bytearray(source)
 # Keep a whole tile containing the two native horizontal-scroll words intact.
 streams=[(0x7d800,atlas[:45*32]),(0x7e000,atlas[45*32:])]
 for at,data in streams:
  encoded=lz_literal(data);assert set(source[at:at+len(encoded)])=={255};rom[at:at+len(encoded)]=encoded
 regions=[(0x7c000,0x7d800),(0x1b7c40,0x1c0000),(0x1c515a,0x1c8000),(0x1df222,0x1e0000)]
 ri=0;at=regions[0][0];seen={};ptrs=[];storage=[]
 for data in maps:
  if data not in seen:
   if at+len(data)>regions[ri][1]:ri+=1;at=regions[ri][0]
   assert at+len(data)<=regions[ri][1]
   assert set(source[at:at+len(data)])=={255}
   seen[data]=at;storage.append(dict(address=hex(at),bytes=len(data)));rom[at:at+len(data)]=data;at+=len(data)
  ptrs.append(seen[data])
 assert len(ptrs)==384
 table=labels['aura_map_table']-0x7b400;code[table:table+1536]=struct.pack('>384I',*ptrs)
 assert 0x7b400+len(code)<=0x7c000
 rom[0x7b400:0x7b400+len(code)]=code
 assert source[0x9ece:0x9ed4].hex()=='4a2800bd6734'
 rom[0x9ece:0x9ed4]=bytes.fromhex('4ef9')+struct.pack('>I',labels['aura_entry'])
 expected={0x9994:'41fa1d5a4e71327ca2604eb9000015d2',0x1c2dc:'41f90000b6f0327ca2604eb9000015d2',0x28718:'41f90000b6f0327ca2604eb9000015d2'}
 for addr,original in expected.items():
  assert source[addr:addr+16].hex()==original,hex(addr)
  rom[addr:addr+16]=bytes.fromhex('4eb9')+struct.pack('>I',labels['aura_load_graphics'])+bytes.fromhex('4e71')*5
 struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>1048320H',rom[512:]))&65535)
 path=Path('work/rom/auras-c2-v3.bin');path.write_bytes(rom)
 record=dict(status='Experimental contour repair, awaiting runtime validation',rom=str(path),sha256=hashlib.sha256(rom).hexdigest(),source_sha256=hashlib.sha256(source).hexdigest(),code_bytes=len(code),allocated_tiles=64,flame_tiles=55,lightning_frames=3,dust_tiles=3,max_aura_sprites=max(int.from_bytes(m[:2],'big') for m in maps),flame_sprites=len(body),dimensions=[80,128],map_addresses=[hex(p) for p in ptrs],unique_map_storage=storage,graphics_segments=[dict(vram='0xA260',bytes=1440,tiles=['0x513','0x53F']),dict(vram='0xA820',bytes=608,tiles=['0x541','0x553'])],reserved_scroll_tile='0x540',loader_hooks=[hex(a) for a in expected],lightning_physical_tiles=['0x54B','0x550'],dust_physical_tiles=['0x551','0x553'],source_pixel_identity=True,enclosed_alpha_holes=0,fade='12 game ticks, temporal density4/4->3/4->2/4->1/4; full connected contour on each visible frame, no tile contraction or live decompression')
 (ROOT/'build.json').write_text(json.dumps(record,indent=2));print(json.dumps({k:v for k,v in record.items() if k not in ('map_addresses','unique_map_storage')},indent=2))
if __name__=='__main__':build()

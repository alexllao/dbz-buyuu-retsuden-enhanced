from pathlib import Path
import sys,json,struct,hashlib
sys.path.insert(0,'work/auras')
from build_c2 import lz_literal,sprite,be
ROOT=Path('work/auras/colors-v4');ROOT.mkdir(exist_ok=True)
art=json.loads(Path('work/auras/v3/direct-art.json').read_text())
flame=Path('work/auras/v3/tiles.bin').read_bytes()[:55*32]
dust=Path('work/auras/v3/tiles.bin').read_bytes()[61*32:64*32]
source=Path('work/auras/v3/aura_hook.asm').read_text(encoding='utf-8')
# Keep the accepted lifecycle and replace only selection, lookup and loader.
source=source[source.index('aura_entry:'):source.index('aura_map_table:')]
source=source.replace('aura_entry:\n','''aura_entry:
 tst.b (0xffffe874).w
 beq.w @aura_resources_ready
 tst.w (0xffffe9c4).w
 bne.w @aura_skip_busy
 tst.b (0xffffe73c).w
 bne.w @aura_skip_busy
 jsr @aura_load_graphics.l
aura_resources_ready:
''',1)
start=source.index(' cmpi.b #0x01,(0x58,A0)')
end=source.index('aura_animation:',start)
source=source[:start]+source[end:]
source=source.replace(' lsl.w #0x5,D6',' lsl.w #0x4,D6')
source=source.replace(' addi.w #0x0300,D5',' addi.w #0x0180,D5')
source=source.replace('aura_ground_map:\n','''aura_ground_map:
 moveq #0,D7
 cmpa.w #0xe886,A0
 bne.w @aura_player_ready
 move.w #0x0600,D7
aura_player_ready:
 moveq #0,D6
 move.b (0x58,A0),D6
 cmpi.w #0x02,D6
 beq.w @aura_actor_palette
 cmpi.w #0x06,D6
 beq.w @aura_actor_palette
 cmpi.w #0x08,D6
 beq.w @aura_actor_palette
 cmpi.w #0x09,D6
 beq.w @aura_actor_palette
 cmpi.w #0x0a,D6
 bne.w @aura_palette_ready
aura_actor_palette:
 addi.w #0x0300,D7
aura_palette_ready:
 add.w D7,D5
''')
source+='''
aura_skip_busy:
 clr.b (0x111,A0)
 jmp 0x00009f08.l

; Each actor gets a resident flame atlas. All native temporary effect loaders
; retain their graphics. Dirty resources wait for both native scene flags.
aura_load_graphics:
 .hex 48e7fffe
 tst.w (0xffffe9c4).w
 bne.w @aura_loader_defer
 tst.b (0xffffe73c).w
 bne.w @aura_loader_defer
 moveq #0,D0
 move.b (0xffffe7b6).w,D0
 cmpi.w #0x0b,D0
 bcs.w @aura_loader_p1_valid
 moveq #0,D0
aura_loader_p1_valid:
 lsl.w #0x3,D0
 lea (0x00280000).l,A2
 adda.w D0,A2
 movea.l (A2)+,A0
 movea.w #0xa260,A1
 move.l A2,-(SP)
 jsr 0x000015d2.l
 movea.l (SP)+,A2
 movea.l (A2),A0
 movea.w #0xa820,A1
 jsr 0x000015d2.l
 moveq #0,D0
 move.b (0xffffe8de).w,D0
 cmpi.w #0x0b,D0
 bcs.w @aura_loader_p2_valid
 moveq #0,D0
aura_loader_p2_valid:
 cmpi.w #0x09,D0
 bne.w @aura_loader_p2_normal
 cmpi.b #0x09,(0xffffe7b6).w
 bne.w @aura_loader_p2_normal
 moveq #0x0b,D0
aura_loader_p2_normal:
 mulu.w #0x000c,D0
 lea (0x00280100).l,A2
 adda.w D0,A2
 movea.l (A2)+,A0
 movea.w #0xa960,A1
 move.l A2,-(SP)
 jsr 0x000015d2.l
 movea.l (SP)+,A2
 movea.l (A2)+,A0
 movea.w #0x5c00,A1
 move.l A2,-(SP)
 jsr 0x000015d2.l
 movea.l (SP)+,A2
 movea.l (A2),A0
 movea.w #0xae80,A1
 jsr 0x000015d2.l
 lea (0x00280300).l,A0
 movea.w #0xaec0,A1
 jsr 0x000015d2.l
 clr.b (0xffffe874).w
 bra.w @aura_loader_return
aura_loader_defer:
 move.b #0x01,(0xffffe874).w
aura_loader_return:
 .hex 4cdf7fff
 rts

; Reproduce native decompression before invalidating the shared aura atlases.
aura_native_effect_load:
 jsr 0x000015d2.l
 move.b #0x01,(0xffffe874).w
 rts

recoome_select_table:
 lea (0x00080000).l,A0
  .hex 20704000
 cmpi.w #0x0024,D4
 bne.w @recoome_table_done
 cmpa.w #0xe390,A4
 bne.w @recoome_table_normal
 cmpi.b #0x09,(0xffffe7b6).w
 beq.w @recoome_table_done
recoome_table_normal:
 lea (0x00227314).l,A0
recoome_table_done:
 rts

aura_map_table:
'''+(' .hex '+('00'*16)+'\n')*(4*192*4//16)
(ROOT/'aura.asm').write_text(source,encoding='utf-8')

def physical(logical):
 if logical<45:return 0x513+logical
 if logical<76:return 0x541+logical-45
 if logical<108:return 0x2e0+logical-76
 return 0x574+logical-108

styles={i:dict(name='gold',roles={7:7,11:11,8:8},palette='common') for i in range(11)}
styles.update({2:dict(name='Piccolo cool white',roles={7:15,11:14,8:7},palette='actor'),6:dict(name='A18 cool white',roles={7:11,11:9,8:8},palette='actor'),7:dict(name='Krillin white',roles={7:15,11:6,8:13},palette='common'),8:dict(name='Freezer cool white',roles={7:15,11:2,8:1},palette='actor'),9:dict(name='Recoome white violet',roles={7:15,11:14,8:6},palette='actor'),10:dict(name='Ginyu lilac',roles={7:15,11:3,8:4},palette='actor')})
def reindex(data,mapping):return bytes((mapping.get(b>>4,b>>4)<<4)|mapping.get(b&15,b&15) for b in data)
chunks={};streamAt=0x280400;operations=[]
def alloc(data):
 global streamAt
 if data not in chunks:
  encoded=lz_literal(data);chunks[data]=streamAt;operations.append(dict(address=streamAt,data=encoded.hex(),kind='aura_graphics_stream'));streamAt+=len(encoded)
 return chunks[data]
p1=[];p2=[]
for cid in range(11):
 data=reindex(flame,styles[cid]['roles']);p1.extend([alloc(data[:45*32]),alloc(data[45*32:])]);p2.extend([alloc(data[:21*32]),alloc(data[21*32:53*32]),alloc(data[53*32:])])
data=reindex(flame,{7:15,11:14,8:11});p2.extend([alloc(data[:21*32]),alloc(data[21*32:53*32]),alloc(data[53*32:])])
operations+=[dict(address=0x280000,data=struct.pack('>22I',*p1).hex(),kind='P1_stream_table'),dict(address=0x280100,data=struct.pack('>36I',*p2).hex(),kind='P2_stream_table'),dict(address=0x280300,data=lz_literal(dust).hex(),kind='dust_stream')]

maps=[];mapAt=0x290000;unique={};storage=[]
for player in range(2):
 for own in range(2):
  base=player*55;palette=(player<<13 if own else 0x6000)|0x8000
  body=[];render=[0]*10240
  for part in art['parts']:
   tile=part['tile'];remaining=part['height']//8;y=part['y']
   while remaining:
    n=1
    while n<remaining and physical(base+tile+n)==physical(base+tile)+n:n+=1
    for flip in [False,True]:
     x=part['x']-40 if not flip else 32-part['x'];body.append((tile,physical(base+tile),x,y-120,n,flip))
    remaining-=n;tile+=n;y+=n*8
  # Verify alpha and role pixels against accepted source after physical splits.
  for tile,physicalTile,x,y,height,flip in body:
   for dy in range(height*8):
    for dx in range(8):
     sx=7-dx if flip else dx;off=(tile+dy//8)*32+dy%8*4+sx//2;v=flame[off]>>(0 if sx&1 else 4)&15
     if v:render[(y+120+dy)*80+x+40+dx]=v
  assert render==art['pixels']
  for air in range(2):
   for frame in range(24):
    for fade in range(4):
     entries=[];age=frame%8
     if not air and fade<3:
      for side in (-1,1):
       radius=20+age*4;y=4-[0,1,3,5,4,2,1,0][age];size=2 if age in (0,7) else 1 if age in (1,6) else 0
       entries.append(sprite(0xe000|physical(110+size)|(0x800 if side<0 else 0),side*radius-4,y,1,1))
     for _,tile,x,y,height,flip in body:entries.append(sprite(palette|tile|(0x800 if flip else 0),x,y,1,height))
     data=be(len(entries))+b''.join(entries)
     if data not in unique:
      unique[data]=mapAt;storage.append(dict(address=hex(mapAt),bytes=len(data),sprites=len(entries)));operations.append(dict(address=mapAt,data=data.hex(),kind='aura_sprite_map'));mapAt+=len(data)
     maps.append(unique[data])
assert len(maps)==768 and streamAt<0x290000 and mapAt<0x2a0000
record=dict(styles=styles,physical_tiles=[physical(i) for i in range(113)],map_pointers=maps,map_storage=storage,operations=operations,graphics_end=hex(streamAt),maps_end=hex(mapAt),map_pixel_identity=True,lightning=False,shared_regions=['5C00..6000 (native temporary effect preserved with dirty guard)','A260..A800','A820..AC00','AE80..AF20'])
(ROOT/'resources.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print('Prepared',len(maps),'map pointers;',len(unique),'maps; graphics end',hex(streamAt),'maps end',hex(mapAt))

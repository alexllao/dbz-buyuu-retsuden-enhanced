from pathlib import Path
import json,struct,hashlib
P=Path('work/namek-menu');parent=Path('work/namek-native/assets-rom.bin').read_bytes();rom=bytearray(parent);labels={k:int(v,16) for k,v in (line.split('=') for line in (P/'menu.labels.txt').read_text().splitlines())};ops=[]
def put(at,data,why):
 data=bytes(data);ops.append(dict(offset=at,before=parent[at:at+len(data)].hex(),data=data.hex(),why=why));rom[at:at+len(data)]=data
code=(P/'menu.bin').read_bytes();assert set(parent[0x330000:0x330000+len(code)])=={255};put(0x330000,code,'Ayudas de carga y selector; F7C0 guarda la variante y E741 sigue fisico')
def jump(at,label,n=6,jsr=False):put(at,bytes.fromhex('4eb9' if jsr else '4ef9')+struct.pack('>I',labels[label])+bytes.fromhex('4e71')*((n-6)//2),label)
for at,label,n in [(0x90b0,'load_graphics',8),(0x90ca,'load_palette',6),(0x9116,'load_map',8),(0xa3e8,'load_map_a1',6),(0x369aa,'load_map_menu',6),(0x3a93a,'select_previous',8),(0x3a9f2,'select_next',10),(0x3ac24,'draw_stage_label',6)]:jump(at,label,n)
jump(0x3c2f8,'assign_story_stage',6,True)
for i,at in enumerate([0x307000,0x317000,0x327000]):put(0x332000+i*16,struct.pack('>4I',at,at,at,0xffffffff),'Lista de franjas nativas de la variante')
font={
'A':['01110','10001','10001','11111','10001','10001','10001'],
'D':['11110','10001','10001','10001','10001','10001','11110'],
'E':['11111','10000','10000','11110','10000','10000','11111'],
'G':['01110','10001','10000','10111','10001','10001','01110'],
'I':['11111','00100','00100','00100','00100','00100','11111'],
'N':['10001','11001','11001','10101','10011','10011','10001'],
'O':['01110','10001','10001','10001','10001','10001','01110'],
'R':['11110','10001','10001','11110','10100','10010','10001'],
'S':['01111','10000','10000','01110','00001','00001','11110'],
'U':['10001','10001','10001','10001','10001','10001','01110'],
'V':['10001','10001','10001','10001','10001','01010','00100'],
' ':['00000']*7}
for vi,text in enumerate(['NUEVO','RUINAS','DRAGON']):
 atlas=bytearray()
 for ch in text.ljust(6):
  pixels=[[0]*16 for _ in range(16)];lit=set()
  for y,row in enumerate(font[ch]):
   for x,bit in enumerate(row):
    if bit=='1':
     for dy in range(2):
      for dx in range(2):lit.add((3+x*2+dx,1+y*2+dy))
  for x,y in lit:
   for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
    if 0<=x+dx<16 and 0<=y+dy<16:pixels[y+dy][x+dx]=14
  for x,y in lit:pixels[y][x]=1
  for tx in range(2):
   for ty in range(2):
    for y in range(8):
     for x in range(0,8,2):atlas.append(pixels[ty*8+y][tx*8+x]<<4|pixels[ty*8+y][tx*8+x+1])
 assert len(atlas)==0x300;put(0x331000+vi*0x300,atlas,'Rotulo nativo '+text);put(0x332100+vi*8,bytes(range(len(text)))+b'\xff'+bytes(7-len(text)),'Indice de glifos '+text)
struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
(P/'candidate.bin').write_bytes(rom);(P/'operations.json').write_text(json.dumps(dict(sourceSha256=hashlib.sha256(parent).hexdigest(),targetSha256=hashlib.sha256(rom).hexdigest(),operations=ops,ramVariant='F7C0',physicalStageIds='0..8; variants1..3 use physical6',menuVirtualIds='0..11, extras9..11'),indent=2));print('BUILT MENU',len(code),hashlib.sha256(rom).hexdigest())

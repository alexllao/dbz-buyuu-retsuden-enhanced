from pathlib import Path
import struct,json,hashlib
p=Path('work/intro-characters');basepath=Path('outputs/intro-paleta-G-v6-1/Buyuu_Retsuden_Enhanced_v6_1.bin');base=basepath.read_bytes();rom=bytearray(base)
tiles=Path('work/gameplay-review/title-all-tiles.bin').read_bytes();old=base[0x1adfb2:0x1adff6];native=[0]*(96*16)
for i in range(4):
 attr,x,y,hi,size=struct.unpack_from('>HBBBB',old,2+i*6);x|=(hi&15)<<8
 if x&0x800:x-=4096
 w=((size>>2)&3)+1;h=(size&3)+1
 for yy in range(h*8):
  for xx in range(w*8):
   t=(attr&0x7ff)+(xx//8)*h+yy//8;v=(tiles[t*32+(yy%8)*4+xx%8//2]>>(4 if xx%2==0 else 0))&15;native[yy*96+x+56+xx]=v
def glyph(x0):return {(x-x0,y) for y in range(16) for x in range(x0,x0+8) if native[y*96+x]==1}
A=glyph(24);nine=glyph(72)
font={' ':set(),'A':A,'9':nine}
font['0']={(x,y) for y in range(2,15) for x in range(8) if (y in [2,14] and 2<=x<=5) or (3<=y<=13 and x in [1,6])}
font['6']={(7-x,16-y) for x,y in nine}
font['2']={(x,y) for y in range(2,15) for x in range(8) if (y==2 and 2<=x<=5) or (y==3 and x in [1,6]) or (4<=y<=6 and x==6) or (7<=y<=11 and x==12-y) or (y in [12,13] and x==1) or (y==14 and 1<=x<=6)}
font['E']={(x,y) for y in range(2,15) for x in range(6) if x==0 or y in [2,8,14]}
font['L']={(x,y) for y in range(2,15) for x in range(6) if x==0 or y==14}
font['X']={(x,y) for y in range(2,15) for x in range(6) if x in ([0,5] if y<=4 or y>=12 else [1,4] if y<=6 or y>=10 else [2,3])}
font['O']=set(font['0']);font['-']={(x,8) for x in range(6)}
text='- 2026 ALEX LLAO';W=128;H=16;white={(j*8+x+1,y) for j,c in enumerate(text) for x,y in font[c]}
outline=white|{(x+dx,y+dy) for x,y in white for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]}
pix=[0]*(W*H)
for x,y in outline:
 if 0<=x<W and 0<=y<H:pix[y*W+x]=5
for x,y in white:pix[y*W+x]=1
raw=bytearray()
for strip in range(4):
 for tx in range(4):
  for ty in range(2):
   for y in range(8):
    for x in range(0,8,2):
     xx=strip*32+tx*8+x;yy=ty*8+y;raw.append(pix[yy*W+xx]*16+pix[yy*W+xx+1])
resource=struct.pack('<H',len(raw)-1)+b''.join(b'\xff'+raw[i:i+8] for i in range(0,len(raw),8));assert len(resource)<0x500
mapping=bytearray(struct.pack('>H',15))
for i in range(4):
 x=-8+i*32;y=16;hi=((y>>8)&15)<<4|((x>>8)&15);mapping.extend(struct.pack('>HBBBB',0xa680+i*8,x&255,y&255,hi,13))
for i in range(11):
 entry=bytearray(old[2+i*6:2+(i+1)*6])
 if i<4:
  x=((entry[4]&15)<<8)|entry[2]
  if x&0x800:x-=4096
  x=(x-56)&0xfff;entry[2]=x&255;entry[4]=(entry[4]&0xf0)|(x>>8)
 mapping.extend(entry)
assert len(mapping)==92
ops=[]
for a,data,label in [(0x3f0000,resource,'Native-height credit glyph extension, same white stroke/black cross-outline style'),(0x3f0800,mapping,'Preserve original copyright sprites; BANDAI and ALEX same row, native16pixel height'),(0x78096,struct.pack('>I',0x3f0800),'Redirect credit map away from enlarged font resource')]:
 rom[a:a+len(data)]=data;ops.append({'address':a,'data':bytes(data).hex(),'label':label})
struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
(p/'font-candidate.bin').write_bytes(rom)
report={'sourceSha256':hashlib.sha256(base).hexdigest(),'targetSha256':hashlib.sha256(rom).hexdigest(),'fontMetrics':{'cell':[8,16],'whiteCapRows':[2,14],'whiteStrokePixels':1,'outline':'4-neighbour black outline using same palette indices as native copyright','originalAWhiteMaskReused':True,'nativeDigit9BasisForNewDigits':True},'nativeBandaiSpritesUnchangedExceptPosition':True,'newGlyphs':'Letters missing from BANDAI1994 are extensions drawn with its cell, cap height and stroke; not an external compact font','operations':ops}
(p/'font-operations.json').write_text(json.dumps(report,indent=2));print(report['targetSha256'])

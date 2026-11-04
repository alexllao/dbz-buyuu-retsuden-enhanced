from pathlib import Path
import json,struct,hashlib
P=Path('work/gameplay-review');base=Path('work/auras/colors-v4/candidate.bin').read_bytes();rom=bytearray(base)
font={
'-':['00000','00000','00000','11111','00000','00000','00000'],
' ':['00000']*7,
'2':['01110','10001','00001','00010','00100','01000','11111'],
'0':['01110','10001','10011','10101','11001','10001','01110'],
'6':['00110','01000','10000','11110','10001','10001','01110'],
'A':['01110','10001','10001','11111','10001','10001','10001'],
'L':['10000','10000','10000','10000','10000','10000','11111'],
'E':['11111','10000','10000','11110','10000','10000','11111'],
'X':['10001','10001','01010','00100','01010','10001','10001'],
'O':['01110','10001','10001','10001','10001','10001','01110']}
text='- 2026 ALEX LLAO';W=96;H=16;mask=set()
for c,ch in enumerate(text):
 for y in range(10):
  for x,v in enumerate(font[ch][y*7//10]):
   if v=='1':mask.add((c*6+x+1,y+3))
pix=[0]*(W*H)
for x,y in mask:
 for dx in [-1,0,1]:
  for dy in [-1,0,1]:
   xx=x+dx;yy=y+dy
   if 0<=xx<W and 0<=yy<H:pix[yy*W+xx]=5
for x,y in mask:pix[y*W+x]=1
tiles=bytearray()
for strip in range(3):
 for tx in range(4):
  for ty in range(2):
   for y in range(8):
    for x in range(0,8,2):
     xx=strip*32+tx*8+x;yy=ty*8+y;tiles.append(pix[yy*W+xx]*16+pix[yy*W+xx+1])
resource=struct.pack('<H',len(tiles)-1)+b''.join(b'\xff'+tiles[i:i+8] for i in range(0,len(tiles),8))
# Keep all eleven original copyright sprites, moving their two lines up sixteen pixels.
old=base[0x1adfb2:0x1adff6];newmap=bytearray(struct.pack('>H',14))
for i in range(3):
 x=-48+i*32;y=16;hi=((y>>8)&15)<<4|((x>>8)&15)
 newmap.extend(struct.pack('>HBBBB',0xa680+i*8,x&255,y&255,hi,13))
for i in range(11):
 entry=bytearray(old[2+i*6:2+(i+1)*6]);y=((entry[4]>>4)<<8)|entry[3]
 if y&0x800:y-=0x1000
 y=(y-16)&0xfff;entry[3]=y&255;entry[4]=((y>>8)<<4)|(entry[4]&15)
 newmap.extend(entry)
assert len(newmap)==86
ops=[]
def put(a,d,label):
 ops.append(dict(address=a,data=bytes(d).hex(),label=label));rom[a:a+len(d)]=d
assert all(x==255 for x in base[0x3f0000:0x3f0800])
put(0x3f0000,resource,'New outlined credit glyphs, native compressed resource')
put(0x3f0400,newmap,'Credit map: three new sprites plus all eleven original Japanese and BANDAI copyright sprites, original lines moved up16px')
# Preserve all registers around native VRAM decompression, then reproduce displaced title init instruction.
code=bytes.fromhex('48e7fffe41f9003f0000327cd0004eb9000015d24cdf7fff31fc0050e9e64e75')
put(0x3f0500,code,'Title-only load helper at VRAM D000; native renderer SAT is DC00')
assert base[0x77bd0:0x77bd6].hex()=='31fc0050e9e6'
put(0x77bd0,bytes.fromhex('4eb9003f0500'),'Title init hook')
assert base[0x78096:0x7809a].hex()=='001adfb2'
put(0x78096,struct.pack('>I',0x3f0400),'Redirect copyright sprite map')
put(0x1ade32,Path('work/rom/presentation-shadows-G.bin').read_bytes()[0x1ade32:0x1ade52],'Approved presentation palette G, sixteen words only')
cs=sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535;put(0x18e,struct.pack('>H',cs),'Mega Drive checksum')
(P/'title-credits.bin').write_bytes(rom)
report=dict(status='Built; real title capture pending',text=text,sourceSha256=hashlib.sha256(base).hexdigest(),targetSha256=hashlib.sha256(rom).hexdigest(),paletteSource='work/rom/presentation-shadows-G.bin',paletteRange='0x1ADE32..0x1ADE51',vramNewTiles='0xD000..0xD2FF',originalCreditRow='All original Japanese and BANDAI 1994 copyright sprites and graphics preserved; original two lines moved up16px; mod credit appended on separate third line',creditLineNativeY={'japanese':168,'bandai1994':184,'alexLlao':200},patchOperations=ops,unchangedOutsideOperations=all(any(o['address']<=i<o['address']+len(bytes.fromhex(o['data'])) for o in ops) for i,(a,b) in enumerate(zip(base,rom)) if a!=b))
(P/'title-credits.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
steps=json.loads(Path('work/emulator/steps-presentation-lighter.json').read_text());steps[-1]['save']=str(P/'title-credits-preserve-bandai.png');(P/'title-steps.json').write_text(json.dumps(steps));print(report['targetSha256'])

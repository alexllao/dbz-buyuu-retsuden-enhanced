from pathlib import Path
import json,sys,zlib,struct,binascii,hashlib,shutil
sys.path.insert(0,'work/intro-body-refined');from extract import extract
P=Path('work/intro-body-refined');R=Path('repository');O=Path('outputs/intro-personajes-corregidos-v6-5');B=Path('work/intro-consistency/boot/Buyuu_Retsuden_Enhanced_v6_4');N=P/'runtime/Buyuu_Retsuden_Enhanced_v6_5'
def read(p):
 b=p.read_bytes();i=8;raw=b''
 while i<len(b):
  n=int.from_bytes(b[i:i+4],'big');k=b[i+4:i+8];d=b[i+8:i+8+n];i+=n+12
  if k==b'IHDR':w,h,depth,col,*_=struct.unpack('>IIBBBBB',d);assert(depth,col)==(8,6)
  if k==b'IDAT':raw+=d
 raw=zlib.decompress(raw);assert all(raw[y*(w*4+1)]==0 for y in range(h));return w,h,[raw[y*(w*4+1)+1:(y+1)*(w*4+1)] for y in range(h)]
def png(p,w,rows):
 def ch(k,d):return struct.pack('>I',len(d))+k+d+struct.pack('>I',binascii.crc32(k+d)&0xffffffff)
 p.write_bytes(b'\x89PNG\r\n\x1a\n'+ch(b'IHDR',struct.pack('>IIBBBBB',w,len(rows),8,6,0,0,0))+ch(b'IDAT',zlib.compress(b''.join(b'\0'+row for row in rows)))+ch(b'IEND',b''))
source=Path('outputs/intro-paleta-G-v6-1/Buyuu_Retsuden_Enhanced_v6_1.bin');e=extract(source);ops=json.loads((P/'operations.json').read_text());native=json.loads((N/'report.json').read_text());lut=json.loads(Path('work/intro-characters/native-qa.json').read_text())['nativeBodyColorConversionLut']
checks=[]
for f in [720,840,960,1080,1200,1800]:
 w,h,a=read(B/f'F{f:04}.png');ww,hh,b=read(N/f'F{f:04}.png');assert(w,h)==(ww,hh);changed=outside=0
 for y in range(h):
  for x in range(w):
   if a[y][x*4:x*4+4]!=b[y][x*4:x*4+4]:
    changed+=1
    if e['pixelOwnerCIDs'][(y//2)*320+x//2]<0:outside+=1
 assert outside==0,(f,outside)
 if f in [720,840,1800]:assert changed==0,(f,changed)
 checks.append({'frame':f,'changedPixels':changed,'outsideOriginalBodyMaskChangedPixels':outside})
_,_,image=read(N/'F0960.png');errors={str(c):0 for c in range(1,11)}
for at,(cid,bank,index) in enumerate(zip(e['pixelOwnerCIDs'],e['pixelBanks'],e['pixelIndices'])):
 if cid<0:continue
 x=at%320;y=at//320;word=ops['targetMapping'][str(cid)][f'{bank}:{index}'];expected=bytes(lut[c][str(word>>s&7)] for c,s in enumerate([1,5,9]));actual=image[y*2][x*8:x*8+3]
 if expected!=actual:errors[str(cid)]+=1
assert not any(errors.values()),errors
assert native['satMax']['count']<=80 and native['satMax']['lineSprites']<=20 and native['satMax']['linePixels']<=320
old=Path('outputs/intro-contraste-anime-v6-4/Buyuu_Retsuden_Enhanced_v6_4.bin').read_bytes();rom=(O/'Buyuu_Retsuden_Enhanced_v6_5.bin').read_bytes()
unchanged={}
for key,a,z in [('battlePalettes',0x80064,0x80064+11*32),('stagePalettes',0x19e51e,0x19e51e+9*48),('controls',0x7b000,0x7b400),('sideSwitch',0x3e0000,0x3e0800),('creditResource',0x3f0000,0x3f0900),('openingGokuPalette',0x1addb2,0x1addd2),('titleGokuPalette',0x1ade32,0x1ade52)]:unchanged[key]=rom[a:z]==old[a:z]
assert all(unchanged.values())
report={'sourceSha256':hashlib.sha256(old).hexdigest(),'targetSha256':hashlib.sha256(rom).hexdigest(),'checks':unchanged,'nativeFrameChecks':checks,'nativeBodyRGBErrorsPerCID':errors,'satMax':native['satMax'],'resourceStats':ops['stats'],'scope':'Restore gray material shading; tiny near-black/trim harmonizations instead of collapsed gray ramps; Cell shares Piccolo greens, Recoome shares human skin ramp for readability. Combat unchanged.','status':'Native verified; lineup user visual approval pending; warm Goku face approved from v6.4','limits':['No new full-game or hardware test','Battle palettes are reference for intro adaptation, not exact same palette words for every material','Modified ASM study map remains tied to v6.2']}
(P/'native-validation.json').write_text(json.dumps(report,indent=2)+'\n')
_,_,a=read(B/'F0960.png');_,_,b=read(N/'F0960.png');png(O/'Personajes-antes-arriba-despues-abajo.png',640,a[208:]+b[208:])
for f,name in [('F0960.png','Intro-personajes-corregidos.png'),('F1800.png','Titulo-contraste-anime-conservado.png')]:shutil.copyfile(N/f,O/name)
print(json.dumps({'bodyErrors':errors,'satMax':native['satMax'],'unchanged':unchanged}))

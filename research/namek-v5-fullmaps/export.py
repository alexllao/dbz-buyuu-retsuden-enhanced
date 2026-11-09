from pathlib import Path
import sys,json,hashlib,struct,zipfile,shutil
sys.path.insert(0,'work/simulation-deps');sys.path.insert(0,'work/namek-simulation')
import numpy as np
from PIL import Image
from vdp import layers,VOFF
P=Path('work/namek-native-v5');O=Path('outputs/Namek-V5-PNG-completos');M=Path('repository/assets/media/namek-v5-fullmaps')
for d in [O,M,O/'ampliados-4x']:d.mkdir(parents=True,exist_ok=True)
rom=(P/'integrated.bin').read_bytes();sha=hashlib.sha256(rom).hexdigest();assert sha=='ed28bb56d207f0d0fd12f1cd1e6eff5597c0f8344e6a7bcf39c8b4017c89f2a8'
def unpack(at):
 size=int.from_bytes(rom[at:at+2],'little');assert not size&0x8000;size+=1;at+=2;out=bytearray()
 while len(out)<size:
  flags=rom[at];at+=1
  for bit in range(8):
   if flags>>bit&1:out.append(rom[at]);at+=1
   else:
    token=int.from_bytes(rom[at:at+2],'little');at+=2;distance=token>>4
    for _ in range((token&15)+3):
     pos=len(out)-distance;assert pos<len(out);out.append(out[pos] if pos>=0 else 0)
   if len(out)>=size:break
 return bytes(out)
r5=np.array([0,4,8,12,17,21,25,29],np.uint16);g6=np.array([0,8,17,25,34,42,51,59],np.uint16)
def rgb565_colors(cram):
 return np.stack([r5[cram&7]*255//31,g6[(cram>>3)&7]*255//63,r5[(cram>>6)&7]*255//31],axis=-1).astype(np.uint8)
names={'normal':'01-Namek-normal-V5','aldea':'02-Namek-devastado-V5','porunga':'03-Namek-Porunga-V5'};records=[]
for k,(slug,name) in enumerate(names.items()):
 block=0x300000+k*0x10000;packed=unpack(block);assert packed==(P/slug/'tiles.bin').read_bytes()
 assert int.from_bytes(rom[block+0x7000:block+0x7002],'big')==64
 mapdata=rom[block+0x7002:block+0x7002+8192];assert mapdata==(P/slug/'map.bin').read_bytes()
 attrs=np.frombuffer(mapdata,'>u2').reshape(64,64);raw=np.frombuffer(packed,np.uint8);tiles=np.stack((raw>>4,raw&15),axis=1).reshape(-1,8,8)
 yy,xx=np.indices((512,512));a=attrs[yy//8,xx//8];index=tiles[a&2047,np.where(a&0x1000,7-(yy&7),yy&7),np.where(a&0x800,7-(xx&7),xx&7)];assert not (index==0).any()
 state=(P/slug/'seed-0.state').read_bytes();cram=np.frombuffer(state,'<u2',count=64,offset=VOFF+65536);lut=rgb565_colors(cram)
 words=np.frombuffer(rom,'>u2',count=22,offset=block+0x9100);expected=((words>>1)&7)|(((words>>5)&7)<<3)|(((words>>9)&7)<<6);assert np.array_equal(cram[32:54],expected)
 globalColor=(((a>>13)&3)*16+index);image=Image.fromarray(lut[globalColor]);path=O/(name+'-512x512.png');image.save(path)
 image.resize((2048,2048),Image.Resampling.NEAREST).save(O/'ampliados-4x'/(name+'-2048x2048.png'))
 # Verificación del color frente al PNG de captura, excluyendo HUD y sprites.
 ly=layers(state);screenshot=np.asarray(Image.open(P/slug/'native-ground.png').convert('RGB'))[::2,::2]
 mask=(~ly['foreground'])&(ly['color']>=32);predicted=lut[ly['color']];matches=np.all(predicted[mask]==screenshot[mask],axis=1)
 assert matches.all(),(slug,int((~matches).sum()))
 shutil.copy2(path,M/(slug+'.png'));shutil.copy2(O/'ampliados-4x'/(name+'-2048x2048.png'),M/(slug+'-4x.png'))
 records.append(dict(variant=slug,file=path.name,width=512,height=512,nativePixelScale=1,backgroundOnly=True,gameAndCompilationResampling=False,palette='Genesis Plus GX RGB565, same conversion as native PNG captures',verifiedBackgroundPixels=int(mask.sum()),colorMatchesCaptureExactly=True,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
 print('EXPORTED',slug,'512x512 and4x; native color checks',int(mask.sum()),flush=True)
manifest=dict(version='V5',buildId='20261109-093419',romSha256=sha,source='Integrated ROM graphics/map and verified native CRAM snapshots',images=records,noRomIncluded=True)
(O/'manifest.json').write_text(json.dumps(manifest,indent=2));shutil.copy2(O/'manifest.json',M/'manifest.json')
(O/'LEEME.txt').write_text('FONDOS COMPLETOS NAMEK V5\n\nTres mapas512x512, sin HUD ni personajes, decodificados del build093419.\nLos PNG principales estan a escala1:1; no son capturas parciales de320x224.\nColores iguales a la captura RGB565 del emulador, comprobados contra el fondo visible.\nLa carpeta ampliados-4x contiene copias2048x2048 por vecino mas proximo, sin suavizado.\nNo se cambian dibujos ni colores. Toda la zona de cielo/suelo incluida en el mapa se conserva.\nEl juego reutiliza franjas del mapa durante el scroll. Estos PNG muestran el mapa base completo.\nNo incluyen ROM, estados ni parches.\n',encoding='utf-8')
with zipfile.ZipFile(O/'Namek-V5-PNG-completos.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(O.rglob('*')):
  if f.is_file() and f.suffix in ['.png','.json','.txt']:z.write(f,f.relative_to(O).as_posix())
print('PNG bundle ready')

"""Casa con alfa/contorno, cielo nocturno sin franjas y Porunga legible.

Adaptación sobre R7; no se redimensiona ni filtra el fotograma del juego.
Los recursos finales son opacos y se empaquetan en patrones nativos de8x8.
"""
from pathlib import Path
import sys,json,struct,hashlib
from collections import deque
sys.path.insert(0,'work/namek-native-r6')
import build as h
np,Image=h.np,h.Image
sys.path.insert(0,'work/namek-native-r7')
P=Path('work/namek-native-r8');OLD=Path('work/namek-native-r7');A=Path('repository/assets/concepts/namek-native-r8')
DRAGON_POS=(176,284);DRAGON_SIZE=(72,60)
def load(slug):
 attrs=np.frombuffer((OLD/slug/'map.bin').read_bytes(),'>u2').reshape(64,64)
 ix,bank=h.decode((OLD/slug/'tiles.bin').read_bytes(),attrs)
 palette=(OLD/slug/'palette.bin').read_bytes();words=list(struct.unpack('>24H',palette))[:22]+h.COMMON
 pal=np.array([h.rgb(w) for w in words],np.uint8).reshape(2,16,3)
 return ix,bank,palette,pal
def pack(ix,banks):
 ids={};atlas=[];mapped=np.zeros((64,64),np.uint16)
 for y in range(64):
  for x in range(64):
   tile=ix[y*8:y*8+8,x*8:x*8+8]
   data,flip=min(((t.tobytes(),f) for t,f in h.flips(tile)),key=lambda v:v[0])
   if data not in ids:ids[data]=len(atlas);atlas.append(data)
   mapped[y,x]=((int(banks[y,x])+2)<<13)|ids[data]|flip
 return atlas,mapped
def components(mask):
 seen=np.zeros_like(mask,bool);out=[]
 for sy,sx in zip(*np.where(mask)):
  if seen[sy,sx]:continue
  todo=[(int(sy),int(sx))];seen[sy,sx]=True;pts=[]
  while todo:
   y,x=todo.pop();pts.append((y,x))
   for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
    yy,xx=y+dy,x+dx
    if 0<=yy<mask.shape[0] and 0<=xx<mask.shape[1] and mask[yy,xx] and not seen[yy,xx]:seen[yy,xx]=True;todo.append((yy,xx))
  ys,xs=zip(*pts);out.append((len(pts),(min(xs),min(ys),max(xs)+1,max(ys)+1),pts))
 return sorted(out,reverse=True)
def native_sprite(path,size,pal,allowed,house=False):
 source=Image.open(path).convert('RGBA');alpha=source.getchannel('A');box=alpha.point(lambda a:255 if a>=192 else 0).getbbox();assert box
 source=source.crop(box);rgba=np.asarray(source.resize(size,Image.Resampling.BOX));mask=rgba[:,:,3]>=160
 allowed=np.array(allowed,np.uint8);ix=allowed[h.nearest(rgba[:,:,:3],pal[0,allowed])]
 if house:
  original=np.asarray(source);dark=(original[:,:,:3].max(-1)<90)&(original[:,:,3]>=192)
  density=np.asarray(Image.fromarray((dark*255).astype(np.uint8)).resize(size,Image.Resampling.BOX))
  ix[mask&(density>=38)]=10
  # Recuperar un contorno nativo definido después de la reducción de alfa.
  padded=np.pad(mask,1);interior=mask.copy()
  for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:interior&=padded[1+dy:1+dy+size[1],1+dx:1+dx+size[0]]
  ix[mask&~interior]=10
 return pal[0,ix],mask,rgba,box
NORMAL,NORMALBANK,_,NORMALPAL=load('normal')
normalRGB=NORMALPAL[NORMALBANK,NORMAL]
cloudMask=np.isin(NORMAL,[14,15]);cloudMask[280:]=False
clouds=[c for c in components(cloudMask) if c[0]>20 and c[1][2]-c[1][0]<=100 and c[1][3]-c[1][1]<=40]
assert clouds
def cloud_template():
 _,(x0,y0,x1,y1),pts=clouds[0];x0=x0//8*8;y0=y0//8*8;x1=(x1+7)//8*8;y1=(y1+7)//8*8
 shape=np.zeros((y1-y0,x1-x0),bool)
 for y,x in pts:shape[y-y0,x-x0]=True
 return shape
CLOUD=cloud_template()
def put_cloud(world,air,pal,x,y,night=False,flip=False):
 shape=CLOUD[:,::-1] if flip else CLOUD;hh,ww=shape.shape;assert x+ww<=512 and y+hh<=352
 use=shape&air[y:y+hh,x:x+ww];view=world[y:y+hh,x:x+ww]
 if night:
  rgb,cloudMask,_,_=native_sprite(A/'cloud-guide.png',(96,32),pal,[11,12])
  # Conservar la nube principal; descartar píxeles aislados de alfa al importar.
  largest=components(cloudMask)[0];clean=np.zeros_like(cloudMask)
  for cy,cx in largest[2]:clean[cy,cx]=True
  cloudMask=clean
  if flip:rgb=rgb[:,::-1];cloudMask=cloudMask[:,::-1]
  hh,ww=cloudMask.shape;use=cloudMask&air[y:y+hh,x:x+ww]
  world[y:y+hh,x:x+ww][use]=rgb[use]
 else:view[use]=pal[0,15]
 return use
def ground_connected_foreground(candidate):
 connected=np.zeros_like(candidate,bool);todo=deque()
 for x in range(512):
  if candidate[511,x]:connected[511,x]=True;todo.append((511,x))
 while todo:
  y,x=todo.popleft()
  for dy in (-1,0,1):
   for dx in (-1,0,1):
    yy,xx=y+dy,x+dx
    if 0<=yy<512 and 0<=xx<512 and candidate[yy,xx] and not connected[yy,xx]:connected[yy,xx]=True;todo.append((yy,xx))
 return connected
def build(slug,compact_clouds=False):
 out=P/slug;out.mkdir(parents=True,exist_ok=True)
 before,oldBank,palette,pal=load(slug);beforeRGB=pal[oldBank,before]
 world=beforeRGB.copy();banks=oldBank[::8,::8].copy();edited=np.zeros((512,512),bool)
 yy=np.indices((512,512))[0]
 # Limpiar antes de colocar nubes: la casa nueva las ocluye con su alfa,
 # nunca con un rectángulo vacío alrededor de la arquitectura.
 sky=pal[0,11] if slug=='normal' else pal[0,13] if slug=='aldea' else pal[0,1]
 world[280:311,335:410]=sky;edited[280:314,335:410]=True
 for y in range(311,314):world[y,335:410]=world[y,334].copy()
 if slug=='porunga':
  # Recuperar el fondo detrás de la figura vieja y conservar el resto del
  # paisaje nocturno. No arrastrar restos verdes de la niebla sobre la roca.
  air=np.isin(NORMAL,[11,12,13,14,15])&(yy<352);air[:280]=True
  # Los bordes grises aislados de nubes antiguas no son paisaje. Conservar
  # únicamente el primer plano conectado al terreno, incluidos los árboles.
  fore=ground_connected_foreground(~air);air=(~fore)&(yy<352)
  air[280:311,335:410]=True;air[311:314,335:410]=False
  world[278:344,156:240]=pal[0,NORMAL[278:344,156:240]];edited[278:344,156:240]=True
  repair=np.isin(before,[11,12,13])&~air&(yy<352);world[repair]=pal[0,NORMAL[repair]];edited|=repair
  world[air]=pal[0,1];edited|=air
  cloudInk=np.zeros_like(air)
  for x,y,flip in [(24,32,False),(336,80,True),(144,176,False),(256,280,True),(24,304,False)]:
   ink=put_cloud(world,air,pal,x,y,True,flip);cloudInk[y:y+ink.shape[0],x:x+ink.shape[1]]|=ink
  plainSky=air&~cloudInk
  rgb,mask,rgba,box=native_sprite(A/'porunga-guide.png',DRAGON_SIZE,pal,[1,6,7,8,9,10,11,12,13,14,15])
  x0,y0=DRAGON_POS;region=world[y0:y0+60,x0:x0+72];region[mask]=rgb[mask];edited[y0:y0+60,x0:x0+72]|=mask
  plainSky[y0:y0+60,x0:x0+72][mask]=False
  # Los ojos usan rojo de la paleta común, sin alterar ningún color compartido.
  red=(rgba[:,:,0].astype(int)>rgba[:,:,1].astype(int)*1.5)&(rgba[:,:,0]>65)&mask
  region[red]=pal[1,10]
  for y,x in zip(*np.where(red)):banks[(y+y0)//8,(x+x0)//8]=1
  # Elegir banco1 solo si reproduce todos los colores del tile exactamente.
  shared={tuple(c) for c in pal[1,1:]}
  for ty in range(44):
   for tx in range(64):
    tile=world[ty*8:ty*8+8,tx*8:tx*8+8]
    if all(tuple(c) in shared for c in np.unique(tile.reshape(-1,3),axis=0)):banks[ty,tx]=1
  Image.fromarray(np.dstack((rgb,mask.astype(np.uint8)*255))).save(out/'porunga-native.png')
  (out/'porunga-import.json').write_text(json.dumps(dict(sourceBox=box,position=[x0,y0],size=[72,60],redEyePixels=int(red.sum())),indent=2))
 elif compact_clouds:
  # Reutilizar nubes enteras a1x; reservar detalle a casa y roca.
  air=np.zeros((512,512),bool);air[:256]=True
  world[:256]=pal[0,11] if slug=='normal' else pal[1,2]
  for x,y,flip in [(104,24,False),(352,64,True),(24,136,False),(240,208,True)]:
   if slug=='normal':put_cloud(world,air,pal,x,y,False,flip)
   else:
    shape=CLOUD[:,::-1] if flip else CLOUD;hh,ww=shape.shape;world[y:y+hh,x:x+ww][shape]=pal[1,5]
  edited[:256]=True
 house,hm,_,box=native_sprite(A/'house-source.png',(58,32),pal,[1,2,3,4,5,6,7,8,9,10,14,15],True)
 x0,y0=345,282;world[y0:y0+32,x0:x0+58][hm]=house[hm];banks[35:40,42:51]=0
 if slug=='porunga':plainSky[y0:y0+32,x0:x0+58][hm]=False
 edited[y0:y0+32,x0:x0+58]|=hm
 Image.fromarray(np.dstack((house,hm.astype(np.uint8)*255))).save(out/'house-native.png')
 # Convertir solo a bancos explícitos; no elegir colores por cobertura local.
 ix=np.zeros((512,512),np.uint8);bankFull=np.repeat(np.repeat(banks,8,0),8,1)
 for b in (0,1):
  q=h.nearest(world,pal[b,1:])+1;ix[bankFull==b]=q[bankFull==b]
 preview=pal[bankFull,ix];atlas,mapped=pack(ix,banks)
 print(slug,'patterns',len(atlas),'compact clouds',compact_clouds,flush=True)
 if len(atlas)>736 and slug!='porunga' and not compact_clouds:return build(slug,True)
 assert len(atlas)<=736,(slug,len(atlas))
 assert not (ix==0).any()
 quantError=(preview!=world).any(-1)
 spriteBox=np.zeros((512,512),bool);dx,dy=DRAGON_POS;spriteBox[dy:dy+60,dx:dx+72]=True
 assert not (quantError&~spriteBox).any(),'palette seam outside dragon'
 nightRun=0
 if slug=='porunga':
  assert (preview[plainSky]==pal[0,1]).all(),'stray pixels in empty sky'
  np.save(out/'plain-sky-mask.npy',plainSky)
  green=np.zeros((512,512),bool)
  for color in pal[0,[11,12,13]]:green|=(preview==color).all(-1)
  green&=air
  for row in green[:352]:
   run=0
   for val in row:
    run=run+1 if val else 0;nightRun=max(nightRun,run)
  assert nightRun<=96,('unexpected horizontal sky strip',nightRun)
 packed=b''.join(bytes(p[i]<<4|p[i+1] for i in range(0,64,2)) for p in atlas).ljust(24576,b'\0')
 decoded,decodedBank=h.decode(packed,mapped);assert np.array_equal(decoded,ix);assert np.array_equal(decodedBank,bankFull)
 literal=struct.pack('<H',24575)+b''.join(b'\xff'+packed[i:i+8] for i in range(0,24576,8));mapbytes=mapped.astype('>u2').tobytes()
 for name,data in [('tiles.bin',packed),('gfx.lz',literal),('map.bin',mapbytes),('map-header.bin',struct.pack('>H',64)+mapbytes),('palette.bin',palette)]: (out/name).write_bytes(data)
 Image.fromarray(preview).save(out/'compiled-map.png');np.save(out/'indices.npy',ix);np.save(out/'banks.npy',banks)
 assert np.array_equal(preview[~edited],beforeRGB[~edited])
 report=dict(variant=slug,tiles=len(atlas),limit=736,losslessPacking=True,compactWholeClouds=compact_clouds,paletteR7Exact=True,houseSourceAlphaBox=box,housePosition=[345,282],houseSize=[58,32],houseColorSha256=hashlib.sha256(preview[282:314,345:403][hm].tobytes()).hexdigest(),outsideEditedRegionsChangedPixels=int((preview[~edited]!=beforeRGB[~edited]).any(-1).sum()),paletteErrorsOutsideDragon=int((quantError&~spriteBox).sum()),dragonPaletteApproximationPixels=int(quantError.sum()),longestNightSkyGreenRun=nightRun if slug=='porunga' else None,nativeApprovalPending=True)
 (out/'build.json').write_text(json.dumps(report,indent=2))
if __name__=='__main__':
 for slug in sys.argv[1:] or ['normal','aldea','porunga']:build(slug)

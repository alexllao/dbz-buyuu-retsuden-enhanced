"""Montaje nativo a un píxel, sin miniatura ampliada ni filtro de salida.

El suelo usa patrones nativos reutilizables, conservados exactamente. Montañas
y casa se remuestrean directamente a la rejilla final; las nubes de Porunga
son un recurso reutilizado sin escalado. No modifica lógica de combate.
"""
from pathlib import Path
import sys,json,struct,hashlib
from datetime import datetime,timezone,timedelta
sys.path.insert(0,'work/simulation-deps')
import numpy as np
from PIL import Image
P=Path('work/namek-native-v3');AS=Path('repository/assets/concepts/namek-native-v1')
BASE=Path('work/combo-startup/candidate.bin').read_bytes()
assert hashlib.sha256(BASE).hexdigest()=='68f838f7ce1fcf0f237d56c09826a359d26931d331cc1ec9716b9d321654ffab'
def cram(c):return sum(int(c[k])*2<<(k*4) for k in range(3))
def rgb(v):return tuple(((v>>s)&7)*255//7 for s in [1,5,9])
def nearest(pixels,palette):
 d=pixels.astype(np.int32)[...,None,:]-palette.astype(np.int32);err=(d*d*np.array([2,3,1])).sum(axis=-1);idx=err.argmin(axis=-1).astype(np.uint8)
 return idx,np.take_along_axis(err,idx[...,None],axis=-1)[...,0]
BG=[(0,0,0),(0,1,2),(0,2,4),(0,3,5),(0,4,6),(1,5,7),(7,5,3),(5,3,1),(4,2,1),(2,1,1),(1,1,1),(0,5,2),(1,6,3),(2,5,4),(7,6,4),(7,7,6)]
COMMON=list(struct.unpack_from('>10H',BASE,0x9102))

def unpack(at):
 size=int.from_bytes(BASE[at:at+2],'little');assert not size&0x8000;size+=1;at+=2;out=bytearray()
 while len(out)<size:
  flags=BASE[at];at+=1
  for bit in range(8):
   if flags>>bit&1:out.append(BASE[at]);at+=1
   else:
    token=int.from_bytes(BASE[at:at+2],'little');at+=2;distance=token>>4
    for _ in range((token&15)+3):
     pos=len(out)-distance;assert pos<len(out);out.append(out[pos] if pos>=0 else 0)
   if len(out)>=size:break
 return out

def material(col):
 r,g,b=[col[:,:,i].astype(int) for i in range(3)]
 return np.where((b>r*1.3)&(b>g*1.12),1,np.where((g>r*1.3)&(g>=b*.90),2,np.where((r>g*1.1)&(r>b*1.3),3,np.where((r>160)&(g>160)&(b>100),4,5)))).astype(np.uint8)

def flips(a):return [(a,0),(a[:,::-1],0x800),(a[::-1],0x1000),(a[::-1,::-1],0x1800)]

def native_ground():
 # Reutilizar la textura nativa a un píxel; no ampliarla desde una miniatura.
 # El espejo de una franja de128 conserva continuidad en ambos extremos.
 packed=unpack(0x1863ac);raw=np.frombuffer(packed,np.uint8)
 tiles=np.stack((raw>>4,raw&15),axis=1).reshape(-1,8,8)
 attrs=np.frombuffer(BASE,'>u2',count=4096,offset=0x19851a).reshape(64,64)
 yy,xx=np.indices((512,512));a=attrs[yy//8,xx//8]
 ix=tiles[a&2047,np.where(a&0x1000,7-(yy&7),yy&7),np.where(a&0x800,7-(xx&7),xx&7)]
 strip=ix[:,208:336];return np.concatenate((strip,strip[:,::-1],strip,strip[:,::-1]),axis=1)

def native_sky(index):
 # Extraer una nube completa como recurso reutilizable de tiles nativos.
 # Nunca reducir sus píxeles a una cuadrícula más gruesa.
 mask=index!=1;visited=np.zeros_like(mask);components=[]
 for sy,sx in zip(*np.where(mask)):
  if visited[sy,sx]:continue
  todo=[(int(sy),int(sx))];visited[sy,sx]=True;points=[]
  while todo:
   y,x=todo.pop();points.append((y,x))
   for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
    ny,nx=y+dy,x+dx
    if 0<=ny<len(mask) and 0<=nx<512 and mask[ny,nx] and not visited[ny,nx]:visited[ny,nx]=True;todo.append((ny,nx))
  if len(points)<100:continue
  ys,xs=zip(*points);x0,x1=min(xs)//8*8,(max(xs)//8+1)*8;y0,y1=min(ys)//8*8,(max(ys)//8+1)*8
  if 40<=x1-x0<=208 and 16<=y1-y0<=88:components.append((len(points),x0,y0,x1,y1,points))
 assert components,'no isolated complete cloud resource'
 _,x0,y0,x1,y1,points=max(components)
 cloud=np.ones((y1-y0,x1-x0),np.uint8)
 for y,x in points:cloud[y-y0,x-x0]=index[y,x]
 sky=np.ones_like(index)
 for x,y,flip in [(24,24,False),(288,96,True),(96,184,False)]:
  patch=cloud[:,::-1] if flip else cloud;h,w=patch.shape
  assert y+h<=280 and x+w<=512,(x,y,w,h)
  sky[y:y+h,x:x+w]=patch
 print('CLOUD',dict(sourceBox=[x0,y0,x1,y1],size=list(cloud.shape[::-1]),placements=3),flush=True)
 return sky

def compile_variant(slug):
 out=P/slug;out.mkdir(parents=True,exist_ok=True)
 art=Image.open(AS/(slug+'-sans-house.png')).convert('RGB').resize((512,512),Image.Resampling.BOX)
 # Cada tramo se remuestrea por área una vez, sin aliasing vecino más próximo.
 worldImage=Image.new('RGB',(512,512))
 worldImage.paste(art.crop((0,0,512,130)).resize((512,248),Image.Resampling.BOX),(0,0))
 worldImage.paste(art.crop((0,130,512,500)).resize((512,264),Image.Resampling.BOX),(0,248))
 world=np.asarray(worldImage).copy()
 # Casa compartida: no hereda el muestreo del panorama ni cambia entre variantes.
 house=Image.open(AS/'house.png').convert('RGBA');box=house.getchannel('A').point(lambda a:255 if a>=192 else 0).getbbox()
 house=np.asarray(house.crop(box).resize((58,23),Image.Resampling.BOX));alpha=house[:,:,3]>=192;hm=np.zeros((512,512),bool)
 world[291:314,345:403][alpha]=house[:,:,:3][alpha];hm[291:314,345:403]=alpha
 sky={'normal':[(0,0,0),(0,5,2),(1,6,3),(0,4,2),(2,5,4),(7,7,6)],'aldea':[(0,0,0),(1,1,2),(3,3,3),(5,5,5),(0,5,2),(7,7,6)],'porunga':[(0,0,0),(0,1,2),(0,2,2),(0,3,2),(1,4,2),(7,7,6)]}[slug]
 bg=list(BG)
 if slug=='aldea':bg[11:14]=[(3,3,3),(5,5,5),(1,1,2)]
 if slug=='porunga':bg[11:14]=[(0,2,2),(0,3,2),(2,6,3)]
 words=[cram(c) for c in bg+sky]+COMMON;pal=np.array([rgb(v) for v in words],np.uint8).reshape(2,16,3)
 indices=[];errors=[]
 for b in range(2):
  i,e=nearest(world,pal[b,1:]);indices.append(i+1);errors.append(e)
 if slug=='porunga':
  i,_=nearest(world[:280],pal[1,1:5]);indices[1][:280]=i+1
  indices[1][:280][indices[1][:280]==2]=3
  indices[1][:280]=native_sky(indices[1][:280]);world[:280]=pal[1,indices[1][:280]]
  band=indices[0][280:344];drop=band==11
  figure=world[288:344,160:240];figureMask=(figure[:,:,0]>35)|(figure[:,:,1]>140)
  for row in range(len(figureMask)):
   hit=np.flatnonzero(figureMask[row])
   if len(hit):figureMask[row,hit[0]:hit[-1]+1]=True
  drop[8:64,160:240]&=~figureMask;band[drop]=12
 # Las entradas variables del cielo no se usan en la casa compartida.
 allowed=np.array([1,2,3,4,5,6,7,8,9,10,14,15]);fixed,_=nearest(world,pal[0,allowed]);indices[0][hm]=allowed[fixed[hm]]
 native=native_ground();indices[0][376:]=native[376:]
 world[376:]=pal[0,native[376:]]
 # El suelo nativo alcanza el horizonte sin cortar las bases de las montañas.
 # Conservar el contorno cálido y rellenar sus sombras dentro de cada ladera.
 r,g,bl=[world[352:376,:,i].astype(int) for i in range(3)]
 keep=(r>g*.9)&(r>bl*1.1)
 for row in range(24):
  for lo,hi in [(65,235),(280,480)]:
   hit=np.flatnonzero(keep[row,lo:hi])
   if len(hit):keep[row,lo+hit[0]:lo+hit[-1]+1]=True
 patch=indices[0][352:376];patch[~keep]=native[352:376][~keep]
 world[352:376][~keep]=pal[0,native[352:376][~keep]]
 # Siempre la misma paleta para la casa, nunca el color local de otro cielo.
 groups={};tiles=[];sourceRGB=np.empty_like(world);sourceMat=np.zeros((512,512),np.uint8)
 for ty in range(64):
  for tx in range(64):
   ys=slice(ty*8,ty*8+8);xs=slice(tx*8,tx*8+8);protected=hm[ys,xs].any()
   # Un material no cambia de banco cada8px: ésa era otra fuente de parches.
   b=0 if protected or ty>=35 or slug=='normal' else 1
   tile=indices[b][ys,xs];mat=material(pal[b,tile]);sourceRGB[ys,xs]=pal[b,tile]
   if 35<=ty<47 and b==0:
    mat[(tile>=6)&(tile<=10)]=3
   if slug=='porunga':
    if b==1:mat[tile<=4]=tile[tile<=4]+16
    else:
     green=(tile>=11)&(tile<=13);mat[green]=tile[green]+32
   sourceMat[ys,xs]=mat
   if int(tile.min())==int(tile.max()):protected=True
   if ty>=47:protected=True
   # Normalizar por el contorno primero. Solo simetrías con material idéntico.
   opts=[(m.tobytes(),t.tobytes(),f) for (m,f),(t,_) in zip(flips(mat),flips(tile))]
   mask,data,flip=min(opts,key=lambda v:(v[0],v[1]));region=0 if ty<38 else 1;key=(b,region,mask,data if protected else None)
   g=groups.setdefault(key,{'b':b,'items':{},'mask':mask,'fixed':bool(protected),'rows':set()});g['rows'].add(ty)
   g['items'][data]=g['items'].get(data,0)+1;tiles.append((key,data,flip))
 print('REGIONS',slug,{name:sum(bool(set(range(lo,hi))&g['rows']) for g in groups.values()) for name,lo,hi in [('sky',0,35),('horizon',35,44),('base',44,47),('grass',47,64)]},flush=True)
 assert len(groups)<=736,(slug,'too many protected topologies',len(groups))
 # Dentro de cada contorno se aproxima únicamente el sombreado del material.
 # Bordes y media tienen más peso para impedir saltos de color entre bloques.
 border=np.ones((8,8),np.float32);border[[0,-1],:]=12;border[:,[0,-1]]=12
 featureWeight=np.sqrt(border[:,:,None]*np.array([2,3,1],np.float32)).reshape(-1)
 for g in groups.values():
  g['patterns']=list(g['items']);g['counts']=np.array(list(g['items'].values()),np.float32)
  cols=np.stack([pal[g['b'],np.frombuffer(p,np.uint8)].reshape(8,8,3) for p in g['patterns']]).astype(np.float32)/255
  g['features']=np.concatenate([cols.reshape(len(cols),-1)*featureWeight,cols.mean(axis=(1,2))*32],axis=1)
  average=np.average(g['features'],axis=0,weights=g['counts']);first=int(((g['features']-average)**2).sum(axis=1).argmin())
  g['selected']=[];g['distance']=np.full(len(cols),np.inf,np.float32);g['labels']=np.zeros(len(cols),int)
  choose(g,first)
 while sum(len(g['selected']) for g in groups.values())<min(736,sum(len(g['patterns']) for g in groups.values())):
  key=max(groups,key=lambda k:float(np.max(groups[k]['distance']*np.sqrt(groups[k]['counts']))))
  g=groups[key];pick=int(np.argmax(g['distance']*np.sqrt(g['counts'])));choose(g,pick)
 atlas=[];lut={}
 for key,g in groups.items():
  base=len(atlas);atlas.extend(g['patterns'][i] for i in g['selected'])
  for i,p in enumerate(g['patterns']):lut[(key,p)]=base+int(g['labels'][i])
 attrs=np.array([((key[0]+2)<<13)|lut[(key,data)]|flip for key,data,flip in tiles],dtype='>u2').reshape(64,64)
 packed=b''.join(bytes(p[i]<<4|p[i+1] for i in range(0,64,2)) for p in atlas).ljust(24576,b'\0')
 literal=struct.pack('<H',24575)+b''.join(b'\xff'+packed[i:i+8] for i in range(0,24576,8))
 # Vista decodificada del recurso final, no del arte antes de comprimir.
 v=np.stack([np.frombuffer(p,np.uint8).reshape(8,8) for p in atlas]);yy,xx=np.indices((512,512));a=attrs.astype(np.uint16)[yy//8,xx//8]
 pix=v[a&2047,np.where(a&0x1000,7-(yy&7),yy&7),np.where(a&0x800,7-(xx&7),xx&7)];bank=((a>>13)&3)-2;preview=pal[bank,pix]
 postMat=material(preview);postMat[(bank==0)&(yy>=280)&(yy<376)&(pix>=6)&(pix<=10)]=3
 if slug=='porunga':
  sk=(bank==1)&(pix<=4);postMat[sk]=pix[sk]+16
  gr=(bank==0)&(pix>=11)&(pix<=13);postMat[gr]=pix[gr]+32
 assert not (pix==0).any();mismatch=postMat!=sourceMat;assert not mismatch.any()
 changed=(preview!=sourceRGB).any(axis=2);grass=(material(sourceRGB)==1)&(yy>=352)
 assert not (changed&grass&(yy>=376)).any(),'foreground blue texture changed'
 rom=bytearray(BASE);rom[0x300000:0x300000+len(literal)]=literal;struct.pack_into('>I',rom,0x1769e2,0x300000)
 rom[0x19851a:0x19a51a]=attrs.tobytes();palette=struct.pack('>22H',*words[:22])+BASE[0x19e66a:0x19e66e];rom[0x19e63e:0x19e66a]=palette[:44]
 bid=datetime.now(timezone(timedelta(hours=1))).strftime('%Y%m%d-%H%M%S');title=('DBZ V1.0 NAMEK3 '+slug+' '+bid).upper()[:48].encode().ljust(48,b' ')
 for off in [0x120,0x150]:rom[off:off+48]=title
 struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
 for name,data in [('candidate.bin',rom),('tiles.bin',packed),('gfx.lz',literal),('map.bin',attrs.tobytes()),('map-header.bin',struct.pack('>H',64)+attrs.tobytes()),('palette.bin',palette)]: (out/name).write_bytes(data)
 for name,img in [('source-layout.png',world),('quantized-source.png',sourceRGB),('compiled-map.png',preview)]:Image.fromarray(img).save(out/name)
 assert not changed[376:].any(),'native foreground texture altered'
 report=dict(variant=slug,buildId=bid,sourceSampling='Direct area projection to512; native one-pixel terrain128-wide mirrored and repeated; foreground y376:512 exact; shared house58x23 at345,291; Porunga cloud resource reused unscaled',coarseGridUpscaling=False,tiles=len(atlas),limit=736,topologyGroups=len(groups),patternsBefore=sum(len(g['patterns']) for g in groups.values()),opaquePixels=int((pix>0).sum()),materialBoundaryChanges=int(mismatch.sum()),textureChangedPixels=int(changed.sum()),grassTextureChangedPixels=int((changed&grass).sum()),foregroundTextureChangedPixels=int(changed[376:].sum()),foregroundBlueTextureChangedPixels=int((changed&grass&(yy>=376)).sum()),houseColorSha256=hashlib.sha256(preview[hm].tobytes()).hexdigest(),porungaAnimated=False,experimental=True,userApprovalPending=True,parentSha256=hashlib.sha256(BASE).hexdigest(),targetSha256=hashlib.sha256(rom).hexdigest())
 (out/'build.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)

def choose(g,pick):
 slot=len(g['selected']);g['selected'].append(pick);d=((g['features']-g['features'][pick])**2).sum(axis=1);better=d<g['distance'];g['labels'][better]=slot;g['distance']=np.minimum(g['distance'],d)

if __name__=='__main__':
 for slug in sys.argv[1:] or ['normal','aldea','porunga']:compile_variant(slug)

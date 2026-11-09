"""Adaptación técnica de los maestros R6 aprobados; conservar arte original.

Cuantización CRAM en rejilla nativa, deduplicación con reflejos y presupuesto
de 736 patrones. No usa sustitución global de tiles ni arcos del suelo V5.
"""
from pathlib import Path
import sys,json,struct,hashlib
sys.path.insert(0,'work/simulation-deps')
import numpy as np
from PIL import Image,ImageFilter
P=Path('work/namek-native-r6'); A=Path('repository/assets/concepts/namek-revision-r6')
BASE=Path('work/combo-startup/candidate.bin').read_bytes()
assert hashlib.sha256(BASE).hexdigest()=='68f838f7ce1fcf0f237d56c09826a359d26931d331cc1ec9716b9d321654ffab'
FILES={'normal':'normal-aprobado.png','aldea':'aldea-lava-aprobado.png','porunga':'porunga-propuesta.png'}
COMMON=list(struct.unpack_from('>10H',BASE,0x9102))
BG=[(0,0,0),(0,1,2),(0,2,4),(0,3,5),(0,4,6),(1,5,7),(6,5,4),(4,4,3),(3,3,2),(2,2,2),(1,1,1),(1,5,2),(1,5,2),(2,5,4),(6,6,5),(7,7,6)]
def cram(c):return sum(int(c[k])*2<<(k*4) for k in range(3))
def rgb(v):
 r,g,b=[(v>>s)&7 for s in (1,5,9)]
 return (int([0,4,8,12,17,21,25,29][r]*255//31),int([0,8,17,25,34,42,51,59][g]*255//63),int([0,4,8,12,17,21,25,29][b]*255//31))
def flips(a):return [(a,0),(a[:,::-1],0x800),(a[::-1],0x1000),(a[::-1,::-1],0x1800)]
def nearest(src,pal):
 d=src.astype(np.int32)[...,None,:]-pal.astype(np.int32)
 return ((d*d)*np.array([2,3,1])).sum(-1).argmin(-1).astype(np.uint8)
def decode(packed,attrs):
 t=np.frombuffer(packed,np.uint8);t=np.stack((t>>4,t&15),-1).reshape(-1,8,8)
 yy,xx=np.indices((512,512));a=attrs[yy//8,xx//8]
 ix=t[a&2047,np.where(a&0x1000,7-(yy&7),yy&7),np.where(a&0x800,7-(xx&7),xx&7)]
 return ix,((a>>13)&3)-2
def original_ground():
 at=0x1863ac;size=int.from_bytes(BASE[at:at+2],'little')+1;at+=2;out=bytearray()
 while len(out)<size:
  flags=BASE[at];at+=1
  for bit in range(8):
   if flags>>bit&1:out.append(BASE[at]);at+=1
   else:
    token=int.from_bytes(BASE[at:at+2],'little');at+=2;distance=token>>4
    for _ in range((token&15)+3):
     pos=len(out)-distance;out.append(out[pos] if pos>=0 else 0)
   if len(out)>=size:break
 attrs=np.frombuffer(BASE,'>u2',count=4096,offset=0x19851a).reshape(64,64)
 return decode(bytes(out),attrs)[0]
def material_mask(tile,bank,slug,strict=False):
 if bank==1:
  # Contornos de nube/humo/cielo intactos; el sombreado puede compartir tile.
  if slug=='porunga':return np.where(tile<=1,1,np.where(tile<=5,2,3)).astype(np.uint8)
  return np.where(tile<=2,1,np.where(tile<=4,2,3)).astype(np.uint8)
 mask=np.where(tile<=5,1,np.where(tile<=10,2,np.where(tile<=13,3,4))).astype(np.uint8)
 if strict:
  for shade in [6,7,8,9,10]:mask[tile==shade]=shade+24
 if slug=='aldea':
  mask[(tile>=11)&(tile<=12)]=tile[(tile>=11)&(tile<=12)]+8
  mask[tile==13]=2
 return mask
def compress_tiles(indices,banks,pal,slug,src):
 groups={};placements=[]
 for ty in range(64):
  for tx in range(64):
   bank=int(banks[ty,tx]);tile=indices[bank][ty*8:ty*8+8,tx*8:tx*8+8];mask=material_mask(tile,bank,slug,strict=35<=ty<49)
   fixed=(ty>=54) or (36<=ty<=39 and 42<=tx<=51) or (slug=='porunga' and 35<=ty<=38 and 20<=tx<=27) or (tile.min()==tile.max())
   opts=[(m.tobytes(),t.tobytes(),f) for (m,f),(t,_) in zip(flips(mask),flips(tile))]
   shape,data,flip=min(opts,key=lambda o:(o[0],o[1]))
   patch=src[ty*8:ty*8+8,tx*8:tx*8+8].astype(int)
   neutral=((patch.max(-1)-patch.min(-1))<14).mean()>.85
   region=0 if bank==1 or (ty<44 and neutral) else 1 if ty<49 else 2
   key=(bank,region,shape,data if fixed else None)
   g=groups.setdefault(key,dict(bank=bank,patterns={},fixed=fixed));g['patterns'][data]=g['patterns'].get(data,0)+1
   placements.append((key,data,flip))
 print(slug,'contour groups',len(groups),flush=True)
 assert len(groups)<=736,(slug,'too many distinct contours',len(groups))
 border=np.ones((8,8),np.float32);border[[0,-1]]=12;border[:,[0,-1]]=12
 weight=np.sqrt(border[:,:,None]*np.array([2,3,1],np.float32)).ravel()
 def choose(g,pick):
  slot=len(g['selected']);g['selected'].append(pick);dist=((g['features']-g['features'][pick])**2).sum(-1);better=dist<g['distance'];g['labels'][better]=slot;g['distance']=np.minimum(g['distance'],dist)
 for g in groups.values():
  g['data']=list(g['patterns']);g['counts']=np.array(list(g['patterns'].values()),np.float32)
  colors=np.stack([pal[g['bank'],np.frombuffer(d,np.uint8)].reshape(8,8,3) for d in g['data']]).astype(np.float32)/255
  g['features']=np.concatenate((colors.reshape(len(colors),-1)*weight,colors.mean((1,2))*32),axis=1)
  avg=np.average(g['features'],axis=0,weights=g['counts']);g['selected']=[];g['distance']=np.full(len(colors),np.inf,np.float32);g['labels']=np.zeros(len(colors),int)
  choose(g,int(((g['features']-avg)**2).sum(-1).argmin()))
 while sum(len(g['selected']) for g in groups.values())<min(736,sum(len(g['data']) for g in groups.values())):
  g=max(groups.values(),key=lambda g:float(np.max(g['distance']*np.sqrt(g['counts']))));choose(g,int(np.argmax(g['distance']*np.sqrt(g['counts']))))
 atlas=[];lookup={}
 for key,g in groups.items():
  start=len(atlas);atlas.extend(g['data'][i] for i in g['selected'])
  for i,data in enumerate(g['data']):lookup[(key,data)]=start+int(g['labels'][i])
 attrs=np.array([((key[0]+2)<<13)|lookup[(key,data)]|flip for key,data,flip in placements],np.uint16).reshape(64,64)
 return atlas,attrs,len(groups)
def build(slug):
 out=P/slug;out.mkdir(parents=True,exist_ok=True)
 src=np.asarray(Image.open(A/FILES[slug]).convert('RGB').resize((512,512),Image.Resampling.NEAREST)).copy()
 bg=list(BG)
 sky={'normal':[(0,0,0),(1,5,2),(1,5,2),(1,5,2),(6,6,5),(7,7,6)],'aldea':[(0,0,0),(1,1,1),(2,2,2),(3,3,3),(4,4,4),(5,5,5)],'porunga':[(0,0,0),(0,1,2),(0,2,2),(0,3,2),(2,5,3),(7,7,6)]}[slug]
 if slug=='aldea':bg[11:14]=[(7,2,0),(7,6,1),(3,3,3)]
 if slug=='porunga':bg[11:14]=[(0,2,2),(0,3,2),(2,5,3)]
 words=[cram(c) for c in bg+sky]+COMMON;pal=np.array([rgb(w) for w in words],np.uint8).reshape(2,16,3)
 indices=[nearest(src,pal[b,1:])+1 for b in range(2)]
 if slug!='normal':
  indices[1][:280]=np.asarray(Image.fromarray(indices[1][:280]).filter(ImageFilter.ModeFilter(3)))
 if slug=='porunga':
  # Reutilizar una nube entera, sin miniaturizarla ni aproximar sus tiles.
  cloud=indices[1][24:104,24:224].copy();indices[1][:264]=1
  for x,y,flip in [(24,24,False),(288,104,True),(96,184,False)]:
   indices[1][y:y+80,x:x+200]=cloud[:,::-1] if flip else cloud
 if slug=='aldea':
  cloud=indices[1][16:64,96:192].copy();cloud[cloud<3]=2
  indices[1][:256]=2
  for x,y,flip in [(96,16,False),(352,48,True),(288,96,False),(16,136,True),(240,184,False)]:
   indices[1][y:y+48,x:x+96]=cloud[:,::-1] if flip else cloud
  haze=indices[1][256:280,:64].copy();pair=np.concatenate((haze,haze[:,::-1]),axis=1)
  indices[1][256:280]=np.tile(pair,(1,4))
 if slug=='aldea':
  gray=(src.max(-1).astype(int)-src.min(-1).astype(int))<14
  allowed=np.array([9,10,13]);mono=allowed[nearest(src,pal[0,allowed])]
  indices[0][gray]=mono[gray]
 # Las tres variantes usan las mismas mesetas: una única geometría y
 # sombreado nativos, sin variaciones accidentales entre generaciones.
 if slug!='normal':
  common=np.asarray(Image.open(A/FILES['normal']).convert('RGB').resize((512,512),Image.Resampling.NEAREST))
  rr,gg,bb=[common[:,:,i].astype(int) for i in range(3)]
  stone=(rr>bb*1.1)&(rr>gg*.85)
  rr,gg,bb=[src[:,:,i].astype(int) for i in range(3)]
  oldstone=(rr>bb*1.1)&(rr>gg*.85)
  boxes=np.zeros((512,512),bool);boxes[333:376,56:224]=True;boxes[314:376,272:464]=True
  cp=stone&boxes;drop=oldstone&boxes&~stone
  commonIndex=nearest(common,pal[0,1:])+1
  indices[0][cp]=commonIndex[cp];src[cp]=common[cp]
  yy=np.indices((512,512))[0];indices[0][drop&(yy<352)]=13 if slug=='aldea' else 12
  indices[0][drop&(yy>=352)]=4
 # Consolidar ruido de un píxel dentro de roca; no alterar su silueta.
 rock=np.isin(indices[0],np.array([6,7,8,9,10]))
 filtered=np.asarray(Image.fromarray(indices[0]).filter(ImageFilter.ModeFilter(3)))
 use=rock&np.isin(filtered,np.array([6,7,8,9,10]));use[:296]=False;use[392:]=False
 indices[0][use]=filtered[use]
 # Cielo plano en su tono dominante; las nubes mantienen contornos nativos.
 # Eliminar solamente el gradiente suave de la generación, no sus siluetas.
 if slug=='normal':
  r,g,b=[src[:,:,i].astype(int) for i in range(3)]
  green=(g>r*1.5)&(g>b*1.2)
  indices[0][:330][green[:330]]=11
 # Recuperar la textura original completa a escala 1:1 desde Y392.
 # No se reutilizan los arcos de acantilado que causaban errores en V5.
 native=original_ground();strip=native[:,208:336];native=np.concatenate((strip,strip[:,::-1],strip,strip[:,::-1]),axis=1)
 for y in range(392,512):
  original=indices[0][y].copy();indices[0][y]=native[y]
  # La casa y las grietas del dibujo aprobado tienen prioridad sobre el suelo.
  if slug=='aldea' and y<424:indices[0][y,:128]=original[:128]
 # Casa compartida: índices exactos del normal, máscara de arquitectura y
 # detalles de ventana. No copiar el cielo circundante de otro escenario.
 normal=np.asarray(Image.open(A/FILES['normal']).convert('RGB').resize((512,512),Image.Resampling.NEAREST))
 patch=normal[291:314,340:405]; rr,gg,bb=[patch[:,:,i].astype(int) for i in range(3)]
 hm=(rr>75)&(gg>65)&(rr>bb*.85)
 # Interiores oscuros/ventanas se incluyen entre extremos de cada fila.
 for row in hm:
  hit=np.flatnonzero(row)
  if len(hit):row[hit[0]:hit[-1]+1]=True
 fixed=nearest(patch,pal[0,np.array([1,2,3,4,5,6,7,8,9,10,14,15])])
 fixed=np.array([1,2,3,4,5,6,7,8,9,10,14,15],np.uint8)[fixed]
 indices[0][291:314,340:405][hm]=fixed[hm]
 banks=np.zeros((64,64),np.uint8)
 if slug!='normal':banks[:35]=1
 # Todo el horizonte comparte banco: cambiarlo por cobertura de cada tile
 # producía escalones rectangulares en la niebla. El gris13 coincide con
 # el gris3 del cielo, de modo que la unión no depende de bloques de8px.
 # Incluso los tiles mayormente vacíos junto a los cuernos deben usar
 # el mismo banco que la arquitectura de las otras variantes.
 banks[36:40,42:51]=0
 atlas=[];ids={};attrs=np.empty((64,64),np.uint16);tileRows=[]
 for ty in range(64):
  for tx in range(64):
   bank=int(banks[ty,tx]);tile=indices[bank][ty*8:ty*8+8,tx*8:tx*8+8]
   data,flip=min(((t.tobytes(),f) for t,f in flips(tile)),key=lambda v:v[0])
   if data not in ids:ids[data]=len(atlas);atlas.append(data)
   attrs[ty,tx]=((bank+2)<<13)|ids[data]|flip
  tileRows.append(len(atlas))
 print(slug,'exact tiles',len(atlas),'cumulative',[(y,tileRows[y]) for y in [34,39,43,47,52,63]],flush=True)
 np.save(out/'source-indices.npy',np.stack(indices));np.save(out/'banks.npy',banks)
 Image.fromarray(np.array([pal[int(banks[y//8,x//8]),indices[int(banks[y//8,x//8])][y,x]] for y in range(512) for x in range(512)],np.uint8).reshape(512,512,3)).save(out/'quantized-source.png')
 atlas,attrs,groupCount=compress_tiles(indices,banks,pal,slug,src)
 packed=b''.join(bytes(p[i]<<4|p[i+1] for i in range(0,64,2)) for p in atlas).ljust(24576,b'\0')
 literal=struct.pack('<H',24575)+b''.join(b'\xff'+packed[i:i+8] for i in range(0,24576,8))
 palette=struct.pack('>22H',*words[:22])+BASE[0x19e66a:0x19e66e]
 ix,bank=decode(packed,attrs);preview=pal[bank,ix];Image.fromarray(preview).save(out/'compiled-map.png')
 assert not (ix==0).any()
 for name,data in [('tiles.bin',packed),('gfx.lz',literal),('map.bin',attrs.astype('>u2').tobytes()),('map-header.bin',struct.pack('>H',64)+attrs.astype('>u2').tobytes()),('palette.bin',palette)]: (out/name).write_bytes(data)
 expected=np.where(np.repeat(np.repeat(banks,8,0),8,1)==0,indices[0],indices[1]);changed=(ix!=expected)
 expectedMaterials=np.empty_like(expected);actualMaterials=np.empty_like(expected)
 for b in (0,1):
  use=bank==b;expectedMaterials[use]=material_mask(expected,b,slug)[use];actualMaterials[use]=material_mask(ix,b,slug)[use]
 assert np.array_equal(expectedMaterials,actualMaterials),'contour changed during tile sharing'
 yy=np.indices(ix.shape)[0];rockShades=(bank==0)&(yy>=280)&(yy<392)&(np.isin(expected,[6,7,8,9,10])|np.isin(ix,[6,7,8,9,10]))
 assert np.array_equal(ix[rockShades],expected[rockShades]),'rock shade boundary changed'
 assert np.array_equal(ix[432:],native[432:]),'native combat-floor texture changed'
 (out/'build.json').write_text(json.dumps(dict(variant=slug,tiles=len(atlas),limit=736,contourGroups=groupCount,materialBoundaryChanges=int((expectedMaterials!=actualMaterials).sum()),rockShadeBoundaryChanges=int((ix[rockShades]!=expected[rockShades]).sum()),nativeForegroundExactFromY=432,nativeGroundModuleX=[208,336],textureChangedPixels=int(changed.sum()),paletteOwnedEntries=22,commonUntouched=True,sourceSha256=hashlib.sha256((A/FILES[slug]).read_bytes()).hexdigest(),houseColorSha256=hashlib.sha256(preview[291:314,340:405][hm].tobytes()).hexdigest(),nativeApprovalPending=True),indent=2))
if __name__=='__main__':
 for slug in sys.argv[1:] or FILES:build(slug)

"""Conversión nativa: contornos de materiales exactos, texturas con presupuesto.

No se mezclan tiles con límites de suelo, roca o cielo diferentes. La reducción
de resolución es continua antes de dividir en tiles; la casa se codifica aparte
a la misma escala para los tres escenarios. No modifica lógica de combate.
"""
from pathlib import Path
import sys,json,struct,hashlib
from datetime import datetime,timezone,timedelta
sys.path.insert(0,'work/simulation-deps')
import numpy as np
from PIL import Image
P=Path('work/namek-native-v2');AS=Path('repository/assets/concepts/namek-native-v1')
BASE=Path('work/combo-startup/candidate.bin').read_bytes()
assert hashlib.sha256(BASE).hexdigest()=='68f838f7ce1fcf0f237d56c09826a359d26931d331cc1ec9716b9d321654ffab'
env={};exec(Path('work/namek-native/build.py').read_text().split('def compile_variant')[0],env)
cram,rgb,nearest=[env[n] for n in ['cram','rgb','nearest']]
BG=[(0,0,0),(0,1,2),(0,2,4),(0,3,5),(0,4,6),(0,5,2),(0,3,2),(1,6,3),(2,1,1),(3,2,2),(4,3,2),(5,3,1),(6,4,2),(7,5,3),(7,6,4),(7,7,6)]
COMMON=env['COMMON']

def material(col):
 r,g,b=[col[:,:,i].astype(int) for i in range(3)]
 return np.where((b>r*1.3)&(b>g*1.12),1,np.where((g>r*1.3)&(g>=b*.90),2,np.where((r>g*1.1)&(r>b*1.3),3,np.where((r>160)&(g>160)&(b>100),4,5)))).astype(np.uint8)

def flips(a):return [(a,0),(a[:,::-1],0x800),(a[::-1],0x1000),(a[::-1,::-1],0x1800)]

def compile_variant(slug):
 out=P/slug;out.mkdir(parents=True,exist_ok=True)
 art=Image.open(AS/(slug+'-sans-house.png')).convert('RGB').resize((512,512),Image.Resampling.BOX)
 # Cada tramo se remuestrea por área una vez, sin aliasing vecino más próximo.
 worldImage=Image.new('RGB',(512,512))
 worldImage.paste(art.crop((0,0,512,130)).resize((512,248),Image.Resampling.BOX),(0,0))
 worldImage.paste(art.crop((0,130,512,500)).resize((512,264),Image.Resampling.BOX),(0,248))
 world=np.asarray(worldImage.resize((256,256),Image.Resampling.BOX).resize((512,512),Image.Resampling.NEAREST)).copy()
 if slug in ['porunga','aldea']:
  # Las nubes lejanas no deben agotar el atlas del suelo y las montañas.
  world[:280]=np.asarray(worldImage.resize((128,128),Image.Resampling.BOX).resize((512,512),Image.Resampling.NEAREST))[:280]
 # El horizonte y las montañas conservan la rejilla nativa de un píxel.
 # La textura fina del primer plano usa el muestreo continuo de dos píxeles.
 if slug in ['aldea','porunga']:
  world[304:376,320:464]=np.asarray(worldImage)[304:376,320:464]
  if slug=='porunga':world[288:344,160:240]=np.asarray(worldImage)[288:344,160:240]
 else:world[288:376]=np.asarray(worldImage)[288:376]
 # Casa compartida: no hereda el muestreo del panorama ni cambia entre variantes.
 house=Image.open(AS/'house.png').convert('RGBA');box=house.getchannel('A').point(lambda a:255 if a>=192 else 0).getbbox()
 house=np.asarray(house.crop(box).resize((58,23),Image.Resampling.BOX));alpha=house[:,:,3]>=192;hm=np.zeros((512,512),bool)
 world[291:314,345:403][alpha]=house[:,:,:3][alpha];hm[291:314,345:403]=alpha
 sky={'normal':[(0,0,0),(0,5,2),(1,6,3),(0,3,2),(3,6,3),(7,7,5)],'aldea':[(0,0,0),(1,1,2),(3,3,3),(5,5,5),(0,5,2),(7,7,5)],'porunga':[(0,0,0),(0,1,2),(0,2,2),(0,3,2),(1,4,2),(7,7,5)]}[slug]
 bg=list(BG)
 if slug=='aldea':bg[6:8]=[(3,3,3),(5,5,5)]
 words=[cram(c) for c in bg+sky]+COMMON;pal=np.array([rgb(v) for v in words],np.uint8).reshape(2,16,3)
 indices=[];errors=[]
 for b in range(2):
  i,e=nearest(world,pal[b,1:]);indices.append(i+1);errors.append(e)
 if slug in ['aldea','porunga']:
  # Dos azules contiguos del césped nocturno/humeante se unifican antes del
  # troceado; así las sombras siguen siendo continuas y liberan patrones.
  ground=indices[0][376:];ground[ground==4]=3
 if slug=='porunga':
  i,_=nearest(world[:280],pal[1,1:5]);indices[1][:280]=i+1
 # Las dos entradas variables del humo no se usan en la casa compartida.
 allowed=np.array([1,2,3,4,5,8,9,10,11,12,13,14,15]);fixed,_=nearest(world,pal[0,allowed]);indices[0][hm]=allowed[fixed[hm]]
 # Siempre la misma paleta para la casa, nunca el color local de otro cielo.
 groups={};tiles=[];sourceRGB=np.empty_like(world)
 for ty in range(64):
  for tx in range(64):
   ys=slice(ty*8,ty*8+8);xs=slice(tx*8,tx*8+8);protected=hm[ys,xs].any()
   b=0 if protected else (int(slug!='normal') if ty<35 else int(errors[1][ys,xs].sum()<errors[0][ys,xs].sum()))
   tile=indices[b][ys,xs];mat=material(pal[b,tile]);sourceRGB[ys,xs]=pal[b,tile]
   if ty>=47:
    # En el primer plano también son contornos las bandas de sombra azules.
    # Mantenerlas exactas evita que una sombra se convierta en un cuadrado.
    blue=mat==1;mat[blue]=tile[blue]+16
   # Normalizar por el contorno primero. Solo simetrías con material idéntico.
   opts=[(m.tobytes(),t.tobytes(),f) for (m,f),(t,_) in zip(flips(mat),flips(tile))]
   mask,data,flip=min(opts,key=lambda v:(v[0],v[1]));key=(b,mask,data if protected else None)
   g=groups.setdefault(key,{'b':b,'items':{},'mask':mask,'fixed':bool(protected)})
   g['items'][data]=g['items'].get(data,0)+1;tiles.append((key,data,flip))
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
 assert not (pix==0).any();mismatch=material(preview)!=material(sourceRGB);assert not mismatch.any()
 changed=(preview!=sourceRGB).any(axis=2);grass=(material(sourceRGB)==1)&(yy>=352)
 assert not (changed&grass&(yy>=376)).any(),'foreground blue texture changed'
 rom=bytearray(BASE);rom[0x300000:0x300000+len(literal)]=literal;struct.pack_into('>I',rom,0x1769e2,0x300000)
 rom[0x19851a:0x19a51a]=attrs.tobytes();palette=struct.pack('>22H',*words[:22])+BASE[0x19e66a:0x19e66e];rom[0x19e63e:0x19e66a]=palette[:44]
 bid=datetime.now(timezone(timedelta(hours=1))).strftime('%Y%m%d-%H%M%S');title=('DBZ V1.0 NAMEK2 '+slug+' '+bid).upper()[:48].encode().ljust(48,b' ')
 for off in [0x120,0x150]:rom[off:off+48]=title
 struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
 for name,data in [('candidate.bin',rom),('tiles.bin',packed),('gfx.lz',literal),('map.bin',attrs.tobytes()),('map-header.bin',struct.pack('>H',64)+attrs.tobytes()),('palette.bin',palette)]: (out/name).write_bytes(data)
 for name,img in [('source-layout.png',world),('quantized-source.png',sourceRGB),('compiled-map.png',preview)]:Image.fromarray(img).save(out/name)
 report=dict(variant=slug,buildId=bid,sourceSampling='Area-filtered projection; continuous256 raster; normal horizon512; ruins/Porunga main cliff512 and clouds128; Porunga figure512; shared house58x23 at345,291',tiles=len(atlas),limit=736,topologyGroups=len(groups),patternsBefore=sum(len(g['patterns']) for g in groups.values()),opaquePixels=int((pix>0).sum()),materialBoundaryChanges=int(mismatch.sum()),textureChangedPixels=int(changed.sum()),grassTextureChangedPixels=int((changed&grass).sum()),foregroundBlueTextureChangedPixels=int((changed&grass&(yy>=376)).sum()),houseColorSha256=hashlib.sha256(preview[hm].tobytes()).hexdigest(),experimental=True,userApprovalPending=True,parentSha256=hashlib.sha256(BASE).hexdigest(),targetSha256=hashlib.sha256(rom).hexdigest())
 (out/'build.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)

def choose(g,pick):
 slot=len(g['selected']);g['selected'].append(pick);d=((g['features']-g['features'][pick])**2).sum(axis=1);better=d<g['distance'];g['labels'][better]=slot;g['distance']=np.minimum(g['distance'],d)

if __name__=='__main__':
 for slug in sys.argv[1:] or ['normal','aldea','porunga']:compile_variant(slug)

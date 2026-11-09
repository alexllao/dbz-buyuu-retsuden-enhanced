from pathlib import Path
import sys,json,struct,hashlib,os
from datetime import datetime,timezone,timedelta
from zoneinfo import ZoneInfo
sys.path.insert(0,str(Path('work/simulation-deps').resolve()))
import numpy as np
from PIL import Image
P=Path('work/namek-native');P.mkdir(exist_ok=True);AS=Path('repository/assets/concepts/namek-native-v1')
BASE=Path('work/combo-startup/candidate.bin').read_bytes();assert hashlib.sha256(BASE).hexdigest()=='68f838f7ce1fcf0f237d56c09826a359d26931d331cc1ec9716b9d321654ffab'

def cram(c):return sum(int(c[k])*2<<(k*4) for k in range(3))
def rgb(v):return tuple(((v>>s)&7)*255//7 for s in [1,5,9])
BG=[(0,0,0),(0,1,2),(0,2,3),(0,3,2),(0,5,3),(2,6,3),(5,7,3),(0,2,4),(0,4,6),(1,5,7),(2,3,3),(3,2,1),(5,3,1),(7,5,2),(7,6,4),(7,7,6)]
COMMON=list(struct.unpack_from('>10H',BASE,0x9102));SHARED=[cram(c) for c in [(0,0,0),(7,7,6),(5,4,3),(0,1,2),(0,4,4)]]

def nearest(pixels,palette):
 d=pixels.astype(np.int32)[...,None,:]-palette.astype(np.int32);err=(d*d*np.array([2,3,1])).sum(axis=-1);idx=err.argmin(axis=-1).astype(np.uint8);return idx,np.take_along_axis(err,idx[...,None],axis=-1)[...,0]

def ordered_dither(pixels,palette,base_index,mask):
 # Tramado Bayer 4x4 alineado con los tiles: mezcla dos colores reales de CRAM.
 # No se difuminan ni se cambian los contornos; la casa usa cuantizacion fija aparte.
 shape=pixels.shape[:2];src=pixels.astype(np.float32).reshape(-1,3);cols=palette.astype(np.float32);weight=np.array([2,3,1],np.float32)
 delta=src[:,None,:]-cols[None,:,:];dist=(delta*delta*weight).sum(axis=-1);near=np.argsort(dist,axis=1)[:,:4]
 best=dist.min(axis=1);p0=base_index.ravel().copy();p1=p0.copy();fraction=np.zeros(len(src),np.float32)
 for i in range(4):
  for j in range(i+1,4):
   ia,ib=near[:,i],near[:,j];a,b=cols[ia],cols[ib];line=b-a;den=(line*line*weight).sum(axis=1);t=np.clip(((src-a)*line*weight).sum(axis=1)/np.maximum(den,1),0,1);res=src-(a+t[:,None]*line);err=(res*res*weight).sum(axis=1)
   better=(err<best*.85)&(t>.06)&(t<.94);best[better]=err[better];p0[better]=ia[better];p1[better]=ib[better];fraction[better]=t[better]
 bayer=np.array([[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]],np.float32);yy,xx=np.indices(shape);threshold=(bayer[yy%4,xx%4]+.5)/16;result=np.where(fraction.reshape(shape)>threshold,p1.reshape(shape),p0.reshape(shape)).astype(np.uint8)
 return np.where(mask,result,base_index).astype(np.uint8)

def canonical(tile):
 choices=[(tile,0),(tile[:,::-1],0x800),(tile[::-1,:],0x1000),(tile[::-1,::-1],0x1800)]
 return min(((a.tobytes(),flip) for a,flip in choices),key=lambda item:item[0])

def reduce_patterns(patterns,counts,palette,budget):
 # Medoid representatives remain real palette-index tiles, not RGB averages.
 if len(patterns)<=budget:return list(range(len(patterns))),np.arange(len(patterns))
 data=np.stack([palette[np.frombuffer(p,np.uint8)].ravel() for p in patterns]).astype(np.float32)/255
 weights=np.tile(np.sqrt([2,3,1]),64).astype(np.float32);data*=weights
 norm=(data*data).sum(axis=1);selected=[];distance=np.full(len(data),np.inf,np.float32);score=np.array(counts,dtype=np.float32)**0.4
 pick=int(np.argmax(counts))
 for k in range(budget):
  selected.append(pick);delta=((data-data[pick])**2).sum(axis=1);distance=np.minimum(distance,delta);distance[selected]=0;pick=int(np.argmax(distance*score))
 for iteration in range(3):
  centers=data[selected];cost=np.maximum(norm[:,None]+(centers*centers).sum(axis=1)[None,:]-2*(data@centers.T),0);labels=cost.argmin(axis=1)
  for k in range(len(selected)):
   members=np.flatnonzero(labels==k)
   if not len(members):continue
   centroid=np.average(data[members],axis=0,weights=np.array(counts)[members]);selected[k]=int(members[np.argmin(((data[members]-centroid)**2).sum(axis=1))])
 centers=data[selected];cost=np.maximum(norm[:,None]+(centers*centers).sum(axis=1)[None,:]-2*(data@centers.T),0);return selected,cost.argmin(axis=1)

def compile_variant(slug):
 out=P/slug;out.mkdir(exist_ok=True)
 src=AS/(slug+'-sans-house.png');src=src if src.exists() else Path('repository/assets/concepts/namek-three-v1')/(slug+'.png')
 art=np.asarray(Image.open(src).convert('RGB').resize((512,512),Image.Resampling.NEAREST)).copy();house_mask=np.zeros((512,512),bool)
 hp=AS/'house.png'
 if hp.exists():
  house=Image.open(hp).convert('RGBA');box=house.getchannel('A').point(lambda a:255 if a>=192 else 0).getbbox();house=house.crop(box).resize((58,32),Image.Resampling.NEAREST);rgba=np.asarray(house);alpha=rgba[:,:,3]>=192;x0,y0=345,190;area=art[y0:y0+32,x0:x0+58];area[alpha]=rgba[:,:,:3][alpha];house_mask[y0:y0+32,x0:x0+58]=alpha
 worldY=np.arange(512);yy=np.clip(np.rint(np.where(worldY<248,worldY*130/248,130+(worldY-248)*1.4)),0,511).astype(int);world=art[yy];hm=house_mask[yy];Image.fromarray(world).save(out/'source-layout.png')
 targetColors=[(8,25,38),(15,53,61),(18,70,47),(44,112,65),(97,168,70),(179,218,94),(4,49,83),(3,81,126),(0,121,171),(2,156,210),(49,35,32),(98,68,46),(153,101,57),(201,143,78),(239,195,125)]
 bgwords=[0]+[cram(c) for c in np.rint(np.asarray(targetColors)/255*7).astype(int)];bgcols=np.asarray([rgb(v) for v in bgwords]);sky=np.median(art[180:190,343:405],axis=(0,1));localword=bgwords[int(((bgcols-sky)**2).sum(axis=1).argmin())];words=bgwords+SHARED+[localword]+COMMON
 pal=np.array([rgb(v) for v in words],np.uint8).reshape(2,16,3);indices=[];errors=[]
 for bank in range(2):
  ix,err=nearest(world,pal[bank]);indices.append(ix);errors.append(err)
 ditherEnabled=os.environ.get('NAMEK_DITHER','1')!='0';ditherMask=np.zeros((512,512),bool)
 if ditherEnabled:
  smooth=(np.abs(world.astype(int)-np.roll(world.astype(int),1,axis=0)).mean(axis=2)+np.abs(world.astype(int)-np.roll(world.astype(int),1,axis=1)).mean(axis=2))<20
  nativeIndex=indices[0];boundary=np.zeros_like(hm)
  for shift in [-8,-4,4,8]:boundary|=(nativeIndex!=np.roll(nativeIndex,shift,axis=0))|(nativeIndex!=np.roll(nativeIndex,shift,axis=1))
  ditherMask=(np.indices((512,512))[0]<286)&smooth&boundary&~hm
  indices[0]=ordered_dither(world,pal[0],indices[0],ditherMask)
 house_fixed,_=nearest(world,pal[1]);house_fixed,_=nearest(world,np.delete(pal[1],5,axis=0));house_fixed=house_fixed+(house_fixed>=5)
 maps=[];dictionaries=[{},{}];patterns=[[],[]];counts=[[],[]];protected=[set(),set()]
 for ty in range(64):
  for tx in range(64):
   ys=slice(ty*8,ty*8+8);xs=slice(tx*8,tx*8+8);is_house=bool(hm[ys,xs].any());tileRGB=world[ys,xs].astype(int);bright=((tileRGB[:,:,0]>205)&(tileRGB[:,:,1]>205)&(tileRGB[:,:,2]>120)).mean()>0.35;gray=((tileRGB.max(axis=2)-tileRGB.min(axis=2)<24)&(tileRGB.mean(axis=2)>50)).mean()>0.6;bank=1 if is_house or ((bright or gray) and errors[1][ys,xs].sum()<errors[0][ys,xs].sum()) else 0
   tile=indices[bank][ys,xs].copy()
   if is_house:tile[hm[ys,xs]]=house_fixed[ys,xs][hm[ys,xs]]
   data,flip=canonical(tile);idx=dictionaries[bank].get(data)
   if idx is None:idx=len(patterns[bank]);dictionaries[bank][data]=idx;patterns[bank].append(data);counts[bank].append(0)
   counts[bank][idx]+=1
   # Preserve the shared house and the small dragon instead of approximating these features.
   is_dragon=slug=='porunga' and 19<=tx<=29 and 35<=ty<=43
   if is_house or is_dragon:protected[bank].add(idx)
   maps.append((bank,idx,flip))
 fixed=sum(len(p) for p in protected);remaining=736-fixed;budgets=[]
 need=[len(patterns[b])-len(protected[b]) for b in range(2)];total=sum(need)
 for b in range(2):budgets.append(min(need[b],round(remaining*need[b]/max(1,total))))
 while sum(budgets)>remaining:budgets[0]-=1
 while sum(budgets)<min(remaining,total):
  for b in range(2):
   if budgets[b]<need[b] and sum(budgets)<remaining:budgets[b]+=1
 atlas=[];lut=[{},{}];cluster=[]
 for b in range(2):
  for idx in sorted(protected[b]):lut[b][idx]=len(atlas);atlas.append(patterns[b][idx])
  free=[i for i in range(len(patterns[b])) if i not in protected[b]];chosen,assign=reduce_patterns([patterns[b][i] for i in free],[counts[b][i] for i in free],pal[b],budgets[b]);base=len(atlas)
  atlas.extend(patterns[b][free[i]] for i in chosen)
  for i,idx in enumerate(free):lut[b][idx]=base+int(assign[i])
  cluster.append(dict(bank=b+2,uniqueBefore=len(patterns[b]),fixed=len(protected[b]),representatives=len(chosen)))
 assert len(atlas)<=736
 attrs=np.array([((b+2)<<13)|lut[b][idx]|flip for b,idx,flip in maps],dtype='>u2').reshape(64,64)
 packed=b''.join(bytes(int(t[i])<<4|int(t[i+1]) for i in range(0,64,2)) for t in atlas);packed=packed.ljust(24576,b'\0')
 literal=struct.pack('<H',len(packed)-1)+b''.join(b'\xff'+packed[i:i+8] for i in range(0,len(packed),8))
 rom=bytearray(BASE);at=0x300000;assert set(BASE[at:at+len(literal)])=={255};rom[at:at+len(literal)]=literal;struct.pack_into('>I',rom,0x1769ca+24,at);rom[0x19851a:0x19851a+8192]=attrs.tobytes();rom[0x19e63e:0x19e63e+44]=struct.pack('>22H',*words[:22])
 now=datetime.now(timezone(timedelta(hours=1)));bid=now.strftime('%Y%m%d-%H%M%S');title=('DBZ V1.0 NAMEK '+slug.upper()+' '+now.strftime('%Y%m%d %H%M'))[:48]
 for offset in [0x120,0x150]:rom[offset:offset+48]=title.encode().ljust(48,b' ')
 struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
 allowed=[(0x120,96),(0x18e,2),(0x1769ca+24,4),(0x19851a,8192),(0x19e63e,44),(at,len(literal))]
 assert all(any(a<=i<a+n for a,n in allowed) for i,(x,y) in enumerate(zip(BASE,rom)) if x!=y)
 (out/'candidate.bin').write_bytes(rom);(out/'tiles.bin').write_bytes(packed);(out/'map.bin').write_bytes(attrs.tobytes());(out/'gfx.lz').write_bytes(literal);(out/'map-header.bin').write_bytes(struct.pack('>H',64)+attrs.tobytes());(out/'palette.bin').write_bytes(struct.pack('>22H',*words[:22])+BASE[0x19e66a:0x19e66e])
 report=dict(version='1.0',buildId=bid,variant=slug,parentSha256=hashlib.sha256(BASE).hexdigest(),targetSha256=hashlib.sha256(rom).hexdigest(),tiles=len(atlas),limit=736,paletteOwnedWords=22,sharedPaletteUntouched=True,clusters=cluster,houseAssetShared=hp.exists(),houseArtPosition=[345,190],houseArtDimensions=[58,32],allowedChanges=allowed,sourceImage=src.as_posix(),sourceImageSha256=hashlib.sha256(src.read_bytes()).hexdigest(),dithering=dict(enabled=ditherEnabled,pattern='Bayer4x4',region='smooth sky palette boundaries only, native worldY<286; house excluded',pixels=int(ditherMask.sum())),integrated=True,experimental=True,stageSlot=6,newStageSlotAdded=False)
 (out/'house-mask.bits').write_bytes(np.packbits(hm).tobytes());(out/'house-indices.bin').write_bytes(house_fixed[hm].tobytes())
 (out/'build.json').write_text(json.dumps(report,indent=2));print('BUILT',slug,report['tiles'],cluster,flush=True)
 # Decode the actual packed map/tiles as a static compiler check.
 v=np.stack([np.frombuffer(p,np.uint8).reshape(8,8) for p in atlas]);iy,ix=np.mgrid[:512,:512];attr=attrs.astype(np.uint16)[iy//8,ix//8];px=np.where(attr&0x800,7-(ix&7),ix&7);py=np.where(attr&0x1000,7-(iy&7),iy&7);color=v[attr&2047,py,px];bank=((attr>>13)&3)-2;preview=pal[bank,color];Image.fromarray(preview).save(out/'compiled-map.png')
 return report
if __name__=='__main__':
 for slug in sys.argv[1:] or ['porunga']:compile_variant(slug)

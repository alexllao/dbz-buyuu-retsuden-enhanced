"""Native resource fixes: opaque glass, whole clouds, shared clean floor.

Deterministic import and editing of existing indexed assets; no generated art.
"""
from pathlib import Path
import sys,json,struct,hashlib,importlib.util
sys.path.insert(0,'work/namek-native-r6')
import build as h
np,Image=h.np,h.Image
spec=importlib.util.spec_from_file_location('r9_helpers','work/namek-native-r9/build.py');r9=importlib.util.module_from_spec(spec);spec.loader.exec_module(r9)
P=Path('work/namek-native-r10');OLD=Path('work/namek-native-r9')

def load(slug):
 attrs=np.frombuffer((OLD/slug/'map.bin').read_bytes(),'>u2').reshape(64,64)
 ix,bank=h.decode((OLD/slug/'tiles.bin').read_bytes(),attrs)
 palette=(OLD/slug/'palette.bin').read_bytes();words=list(struct.unpack('>24H',palette))[:22]+h.COMMON
 pal=np.array([h.rgb(w) for w in words],np.uint8).reshape(2,16,3)
 return ix,bank,palette,pal

NORMAL,NB,_,NP=load('normal');Y,X=np.indices((512,512))
air=np.isin(NORMAL,[11,12,13,14,15])&(Y<352);air[:280]=True
air=(~r9.ground_connected_foreground(~air))&(Y<352)
cloudSource=Path('repository/assets/concepts/namek-native-r9/cloud-guide.png')
houseSource=Path('repository/assets/concepts/namek-native-r9/house-source.png')

def house(pal):
 im=Image.open(houseSource).convert('RGBA');rgba=np.array(im);rgb=rgba[:,:,:3].astype(int);alpha=rgba[:,:,3].copy()
 blue=(rgb[:,:,2]>rgb[:,:,0]*1.3)&(rgb[:,:,2]>rgb[:,:,1]*1.05)
 # Existing keying leaked through gaps around blue glass and an open doorway.
 # Include blue inside the warm wall envelope without filling green sky gaps.
 envelope=np.zeros_like(blue)
 for y,row in enumerate(alpha>=192):
  xs=np.flatnonzero(row)
  if len(xs):envelope[y,xs[0]:xs[-1]+1]=True
 repaired=blue&envelope&(alpha<255);rgba[:,:,3][blue&envelope]=255
 fixed=Image.fromarray(rgba);out=P/'house-import-repaired.png';fixed.save(out)
 colors,mask,reduced,box=r9.native_sprite(out,(58,32),pal,[1,2,3,4,5,6,7,8,9,14,15],False)
 # Verify the large circular blue window retained opaque source glass.
 glass=blue&envelope;nativeGlass=np.asarray(Image.fromarray((glass*255).astype(np.uint8)).resize((58,32),Image.Resampling.BOX))>=192
 assert mask[nativeGlass].all()
 return colors,mask,dict(repairedSourcePixels=int(repaired.sum()),opaqueNativeGlassPixels=int(nativeGlass.sum()),glassMask=nativeGlass)

def cloud(pal,size,kind):
 source=Image.open(cloudSource).convert('RGBA');box=source.getchannel('A').point(lambda a:255 if a>=192 else 0).getbbox();source=source.crop(box)
 rgba=np.asarray(source.resize(size,Image.Resampling.BOX));mask=rgba[:,:,3]>=160
 # Same complete native cloud silhouette, two color levels per atmosphere.
 if kind=='normal':bank,allowed=0,[14,15]
 elif kind=='aldea':bank,allowed=1,[4,5]
 else:bank,allowed=0,[11,12]
 light=rgba[:,:,:3].astype(int).sum(-1);vals=light[mask];threshold=float(np.median(vals))
 ix=np.where(light>threshold,allowed[1],allowed[0]);rgb=pal[bank,ix]
 return rgb,mask

def build(slug):
 out=P/slug;out.mkdir(parents=True,exist_ok=True)
 before,banks,palette,pal=load(slug);world=pal[banks,before].copy();original=world.copy();edited=np.zeros((512,512),bool)
 bank8=banks[::8,::8].copy();keep=np.zeros((512,512),bool)
 # Preserve destruction effects and the accepted dragon while clearing old sky.
 if slug=='aldea':keep=air&(Y>=280)&(banks==0)&np.isin(before,[9,10,11,12])
 if slug=='porunga':
  figure=np.asarray(Image.open(OLD/'porunga/porunga-native.png').getchannel('A'))>0
  keep[286:366,240:297]|=figure
 clear=air&~keep;sky=11 if slug=='normal' else 13 if slug=='aldea' else 1
 world[clear]=pal[0,sky];edited|=clear
 # Complete clouds live above the tree line, with a visible depth gap.
 positions=[(24,40,(96,32),False),(336,128,(72,24),True),(160,280,(56,24),False)]
 if slug=='aldea':positions=[(24,40,(72,24),False),(336,128,(72,24),True),(160,280,(56,24),False)]
 cloudInk=np.zeros((512,512),bool)
 for x,y,size,flip in positions:
  rgb,mask=cloud(pal,size,slug)
  if flip:rgb=rgb[:,::-1];mask=mask[:,::-1]
  w,hh=size;use=mask&clear[y:y+hh,x:x+w]
  world[y:y+hh,x:x+w][use]=rgb[use];cloudInk[y:y+hh,x:x+w]|=use
  if slug=='aldea':bank8[y//8:(y+hh+7)//8,x//8:(x+w+7)//8]=1
  edited[y:y+hh,x:x+w]|=use
 assert np.argwhere(cloudInk)[:,0].max()<304
 # Use the accepted, non-rectangular normal floor on all variants. Preserve
 # actual ruined architecture/smoke on the left, not the repeated soil tile.
 floor=np.zeros((512,512),bool);floor[392:]=True
 ruin=(slug=='aldea')&(X<128)&(Y>=392)&(Y<424)&np.isin(before,[6,9,10,13,14,15])
 cleanFloor=floor&~ruin;world[cleanFloor]=pal[0,NORMAL[cleanFloor]];edited|=cleanFloor;bank8[49:]=0
 hrgb,hm,glass=house(pal);x0,y0=345,282
 world[y0:y0+32,x0:x0+58][hm]=hrgb[hm];edited[y0:y0+32,x0:x0+58]|=hm;bank8[35:40,42:51]=0
 bankFull=np.repeat(np.repeat(bank8,8,0),8,1);ix=np.zeros((512,512),np.uint8)
 for b in [0,1]:
  q=h.nearest(world,pal[b,1:])+1;ix[bankFull==b]=q[bankFull==b]
 preview=pal[bankFull,ix];assert np.array_equal(preview,world),'palette conversion changed a pixel'
 atlas,mapped=r9.pack(ix,bank8);print(slug,'patterns',len(atlas),flush=True);assert len(atlas)<=736
 assert np.array_equal(preview[~edited],original[~edited]);assert not (ix==0).any()
 packed=b''.join(bytes(t[i]<<4|t[i+1] for i in range(0,64,2)) for t in atlas).ljust(24576,b'\0')
 decoded,db=h.decode(packed,mapped);assert np.array_equal(decoded,ix);assert np.array_equal(db,bankFull)
 literal=struct.pack('<H',24575)+b''.join(b'\xff'+packed[i:i+8] for i in range(0,24576,8));mb=mapped.astype('>u2').tobytes()
 for name,data in [('tiles.bin',packed),('gfx.lz',literal),('map.bin',mb),('map-header.bin',struct.pack('>H',64)+mb),('palette.bin',palette)]: (out/name).write_bytes(data)
 Image.fromarray(preview).save(out/'compiled-map.png');Image.fromarray(np.dstack((preview[282:314,345:403],hm.astype(np.uint8)*255))).save(out/'house-native.png')
 if slug=='porunga':
  alpha=np.asarray(Image.open(OLD/'porunga/porunga-native.png').getchannel('A'));Image.fromarray(np.dstack((preview[286:366,240:297],alpha))).save(out/'porunga-native.png')
 np.save(out/'indices.npy',ix);np.save(out/'banks.npy',bank8);np.save(out/'edited-mask.npy',edited)
 report=dict(variant=slug,tiles=len(atlas),limit=736,losslessPacking=True,paletteR9Exact=True,housePosition=[345,282],houseSize=[58,32],houseColorSha256=hashlib.sha256(preview[282:314,345:403][hm].tobytes()).hexdigest(),repairedSourceGlassPixels=glass['repairedSourcePixels'],opaqueNativeGlassPixels=glass['opaqueNativeGlassPixels'],cloudMaxY=int(np.argwhere(cloudInk)[:,0].max()),cloudsAboveY304=True,cleanFloorNormalExact=bool(np.array_equal(ix[cleanFloor],NORMAL[cleanFloor])),outsideEditedRegionsChangedPixels=0,nativeApprovalPending=True)
 (out/'build.json').write_text(json.dumps(report,indent=2))

if __name__=='__main__':
 for slug in sys.argv[1:] or ['normal','aldea','porunga']:build(slug)

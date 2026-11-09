"""Refinar únicamente las texturas de roca sobre los recursos nativos R6."""
from pathlib import Path
import sys,json,struct,hashlib
sys.path.insert(0,'work/namek-native-r6')
import build as h
np,Image=h.np,h.Image
P=Path('work/namek-native-r7');OLD=Path('work/namek-native-r6')
GUIDE=Path('repository/assets/concepts/namek-rock-r7/guia-textura.png')
def pack(ix,banks):
 atlas=[];ids={};mapped=np.zeros((64,64),np.uint16)
 for ty in range(64):
  for tx in range(64):
   tile=ix[ty*8:ty*8+8,tx*8:tx*8+8]
   data,flip=min(((t.tobytes(),f) for t,f in h.flips(tile)),key=lambda v:v[0])
   if data not in ids:ids[data]=len(atlas);atlas.append(data)
   mapped[ty,tx]=((int(banks[ty,tx])+2)<<13)|ids[data]|flip
 return atlas,mapped
def fit_one_pattern(ix,banks8,mask,pal):
 atlas,mapped=pack(ix,banks8);changes=0
 while len(atlas)>736:
  uses={i:np.argwhere((mapped&2047)==i) for i in range(len(atlas))}
  eligible=[]
  for i,data in enumerate(atlas):
   pix=np.frombuffer(data,np.uint8).reshape(8,8)
   if not np.isin(pix,[6,7,8,9,10]).all():continue
   if not all(mask[y*8:y*8+8,x*8:x*8+8].all() for y,x in uses[i]):continue
   eligible.append(i)
  best=None;border=np.ones((8,8),np.float32);border[[0,-1]]=16;border[:,[0,-1]]=16
  for i in eligible:
   a=np.frombuffer(atlas[i],np.uint8).reshape(8,8);ac=pal[0,a].astype(int)
   for j in eligible:
    if i==j:continue
    b=np.frombuffer(atlas[j],np.uint8).reshape(8,8);d=ac-pal[0,b].astype(int)
    error=float(((d*d*np.array([2,3,1])).sum(-1)*border).sum())*len(uses[i])
    candidate=(error,i,j)
    if best is None or candidate<best:best=candidate
  assert best is not None
  _,source,target=best;tile=np.frombuffer(atlas[target],np.uint8).reshape(8,8)
  for y,x in uses[source]:
   attr=int(mapped[y,x]);patch=tile[:,::-1] if attr&0x800 else tile
   if attr&0x1000:patch=patch[::-1]
   old=ix[y*8:y*8+8,x*8:x*8+8];changes+=int((old!=patch).sum());old[:]=patch
  atlas,mapped=pack(ix,banks8)
 return atlas,mapped,changes
def build(slug):
 out=P/slug;out.mkdir(parents=True,exist_ok=True)
 attrs=np.frombuffer((OLD/slug/'map.bin').read_bytes(),'>u2').reshape(64,64)
 before,banks=h.decode((OLD/slug/'tiles.bin').read_bytes(),attrs);ix=before.copy()
 palette=(OLD/slug/'palette.bin').read_bytes();words=list(struct.unpack('>24H',palette))[:22]+h.COMMON
 pal=np.array([h.rgb(w) for w in words],np.uint8).reshape(2,16,3)
 guide=np.asarray(Image.open(GUIDE).convert('RGB').resize((512,512),Image.Resampling.NEAREST))
 shades=np.array([6,7,8,9,10],np.uint8);detail=shades[h.nearest(guide,pal[0,shades])]
 normalAttrs=np.frombuffer((OLD/'normal/map.bin').read_bytes(),'>u2').reshape(64,64)
 normalPixels,_=h.decode((OLD/'normal/tiles.bin').read_bytes(),normalAttrs)
 # La silueta y arquitectura nativas quedan intactas. Solo sustituir roca.
 rockMask=np.zeros((512,512),bool);rockMask[314:376,272:464]=True;rockMask[333:376,56:224]=True
 rockMask&=(banks==0)&np.isin(before,shades)&np.isin(normalPixels,shades)
 ix[rockMask]=detail[rockMask]
 treeMask=np.zeros_like(rockMask)
 for x0,y0,x1,y1 in [(7,326,42,352),(213,328,230,340),(456,332,470,342),(279,336,289,344)]:treeMask[y0:y1,x0:x1]=True
 treeMask&=(banks==0)&np.isin(before,[1,2,3,4,5])&np.isin(normalPixels,[1,2,3,4,5])
 blues=np.array([1,2,3,4,5],np.uint8);treeDetail=blues[h.nearest(guide,pal[0,blues])]
 ix[treeMask]=treeDetail[treeMask];mask=rockMask|treeMask
 banks8=banks[::8,::8];atlas,mapped=pack(ix,banks8);exactCount=len(atlas)
 imported=ix.copy();atlas,mapped,budgetWrites=fit_one_pattern(ix,banks8,mask,pal)
 budgetPixels=int((ix!=imported).sum())
 preview=pal[banks,ix];Image.fromarray(preview).save(out/'exact-preview.png')
 print(slug,'exact patterns',exactCount,'final',len(atlas),'budget pixels',budgetPixels,'changed',int((ix!=before).sum()),flush=True)
 np.save(out/'indices.npy',ix);np.save(out/'mask.npy',mask)
 if len(atlas)>736:return
 packed=b''.join(bytes(p[i]<<4|p[i+1] for i in range(0,64,2)) for p in atlas).ljust(24576,b'\0')
 decoded,bank=h.decode(packed,mapped);assert np.array_equal(decoded,ix);assert np.array_equal(bank,banks)
 literal=struct.pack('<H',24575)+b''.join(b'\xff'+packed[i:i+8] for i in range(0,24576,8));mapbytes=mapped.astype('>u2').tobytes()
 for name,data in [('tiles.bin',packed),('gfx.lz',literal),('map.bin',mapbytes),('map-header.bin',struct.pack('>H',64)+mapbytes),('palette.bin',palette)]: (out/name).write_bytes(data)
 Image.fromarray(preview).save(out/'compiled-map.png')
 assert np.array_equal(ix[~mask],before[~mask])
 assert np.array_equal(ix[291:314,340:405],before[291:314,340:405])
 assert palette==(OLD/slug/'palette.bin').read_bytes()
 report=dict(variant=slug,patternsBefore=exactCount,tiles=len(atlas),limit=736,budgetAdjustmentPixels=budgetPixels,budgetAdjustmentWrites=budgetWrites,losslessPatternPackingAfterAdjustment=True,paletteR6Exact=True,changedPixels=int((ix!=before).sum()),rockChangedPixels=int((ix[rockMask]!=before[rockMask]).sum()),treeChangedPixels=int((ix[treeMask]!=before[treeMask]).sum()),outsideEditedRegionsChangedPixels=int((ix[~mask]!=before[~mask]).sum()),sourceGuideSha256=hashlib.sha256(GUIDE.read_bytes()).hexdigest(),houseColorSha256=json.loads((OLD/slug/'build.json').read_text())['houseColorSha256'],nativeApprovalPending=True)
 (out/'build.json').write_text(json.dumps(report,indent=2))
if __name__=='__main__':
 for slug in sys.argv[1:] or ['normal','aldea','porunga']:build(slug)

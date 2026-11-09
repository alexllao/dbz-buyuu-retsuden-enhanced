"""Eliminar restos de árboles del módulo de suelo; conservar paletas V4.

Se editan los tiles nativos antes de repetirlos. La limpieza no desplaza ni
remuestrea el escenario. Se protegen laderas y árboles completos del diseño.
"""
from pathlib import Path
import sys,json,struct,hashlib
from datetime import datetime,timezone,timedelta
sys.path.insert(0,'work/simulation-deps')
import numpy as np
from PIL import Image
P=Path('work/namek-native-v5');OLD=Path('work/namek-native-v4');AS=Path('repository/assets/concepts/namek-native-v1')
BASE=Path('work/combo-startup/candidate.bin').read_bytes()
helpers={'__name__':'native_v4_helpers'};exec(compile((OLD/'build.py').read_text(),'v4-index-decoder','exec'),helpers)
decode,flips,rgb,hm=[helpers[n] for n in ['decode','flips','rgb','hm']]
assert hashlib.sha256(BASE).hexdigest()=='68f838f7ce1fcf0f237d56c09826a359d26931d331cc1ec9716b9d321654ffab'
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
 return bytes(out)
def module():
 attrs=np.frombuffer(BASE,'>u2',count=4096,offset=0x19851a).reshape(64,64)
 whole=decode(unpack(0x1863ac),attrs);before=whole[:,208:336].copy();after=before.copy()
 # Dos árboles del gráfico antiguo perdían su copa al recortar desdeY352.
 # Sustituir sus fragmentos por tiles vecinos del mismo suelo, a escala1:1.
 after[352:376,0:8]=before[352:376,8:16]
 after[352:360,24:32]=before[352:360,32:40]
 def repeat(s):return np.concatenate((s,s[:,::-1],s,s[:,::-1]),axis=1)
 return repeat(before),repeat(after)
originalNative,cleanNative=module()
def keep_concept(slug):
 art=Image.open(AS/(slug+'-sans-house.png')).convert('RGB').resize((512,512),Image.Resampling.BOX)
 band=np.asarray(art.crop((0,130,512,500)).resize((512,264),Image.Resampling.BOX))[104:128]
 r,g,b=[band[:,:,i].astype(int) for i in range(3)];keep=(r>g*.9)&(r>b*1.1)
 for y in range(24):
  for lo,hi in [(65,235),(280,480)]:
   hit=np.flatnonzero(keep[y,lo:hi])
   if len(hit):keep[y,lo+hit[0]:lo+hit[-1]+1]=True
 return keep
def build(slug):
 out=P/slug;out.mkdir(parents=True,exist_ok=True)
 attrs=np.frombuffer((OLD/slug/'map.bin').read_bytes(),'>u2').reshape(64,64).astype(np.uint16)
 source=decode((OLD/slug/'tiles.bin').read_bytes(),attrs);edited=source.copy()
 connected=np.isin(source[340:352],range(1,11)).sum(axis=0)>=10
 target=(originalNative[352:376]!=cleanNative[352:376])&~keep_concept(slug)&~connected[None,:]
 edited[352:376][target]=cleanNative[352:376][target]
 allowed=np.zeros_like(source,bool);allowed[352:376]=target
 assert np.array_equal(source[~allowed],edited[~allowed])
 palette=(OLD/slug/'palette.bin').read_bytes();words=list(struct.unpack('>24H',palette));common=list(struct.unpack_from('>10H',BASE,0x9102));pal=np.array([rgb(v) for v in words[:22]+common],np.uint8).reshape(2,16,3)
 atlas=[];ids={};mapped=np.zeros_like(attrs)
 for ty in range(64):
  for tx in range(64):
   tile=edited[ty*8:ty*8+8,tx*8:tx*8+8];data,flip=min(((t.tobytes(),f) for t,f in flips(tile)),key=lambda v:v[0])
   if data not in ids:ids[data]=len(atlas);atlas.append(data)
   mapped[ty,tx]=(int(attrs[ty,tx])&0xe000)|ids[data]|flip
 assert len(atlas)<=736,(slug,len(atlas))
 packed=b''.join(bytes(p[i]<<4|p[i+1] for i in range(0,64,2)) for p in atlas).ljust(24576,b'\0')
 result=decode(packed,mapped);assert np.array_equal(result,edited);assert not (result==0).any()
 yy,xx=np.indices((512,512));bank=((mapped[yy//8,xx//8]>>13)&3)-2;preview=pal[bank,result];oldrgb=pal[bank,source]
 assert np.array_equal(preview[hm],oldrgb[hm])
 Image.fromarray(oldrgb).save(out/'previous-map.png');Image.fromarray(preview).save(out/'compiled-map.png')
 Image.fromarray(preview[320:392,192:288]).resize((768,576),Image.Resampling.NEAREST).save(out/'junction-inspect.png')
 literal=struct.pack('<H',24575)+b''.join(b'\xff'+packed[i:i+8] for i in range(0,24576,8));mapbytes=mapped.astype('>u2').tobytes()
 rom=bytearray(BASE);rom[0x300000:0x300000+len(literal)]=literal;struct.pack_into('>I',rom,0x1769e2,0x300000);rom[0x19851a:0x19a51a]=mapbytes;rom[0x19e63e:0x19e66e]=palette
 bid=datetime.now(timezone(timedelta(hours=1))).strftime('%Y%m%d-%H%M%S');title=('DBZ V1.0 NAMEK5 '+slug+' '+bid).upper()[:48].encode().ljust(48,b' ')
 for at in [0x120,0x150]:rom[at:at+48]=title
 struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
 for name,data in [('tiles.bin',packed),('gfx.lz',literal),('map.bin',mapbytes),('map-header.bin',struct.pack('>H',64)+mapbytes),('palette.bin',palette),('candidate.bin',rom)]: (out/name).write_bytes(data)
 changed=result!=source
 report=dict(variant=slug,buildId=bid,tiles=len(atlas),limit=736,spatialResampling=False,losslessPacking=True,paletteV4Exact=palette==(OLD/slug/'palette.bin').read_bytes(),paletteSha256=hashlib.sha256(palette).hexdigest(),changedPixels=int(changed.sum()),outsideCleanupChangedPixels=int(changed[~allowed].sum()),houseColorSha256=hashlib.sha256(preview[hm].tobytes()).hexdigest(),protectedConnectedColumns=np.flatnonzero(connected).tolist(),cleanupSource=dict(nativeModuleX=[208,336],primary=dict(dst=[0,352,8,376],src=[8,352,16,376]),secondary=dict(dst=[24,352,32,360],src=[32,352,40,360]),mirroredRepeats=True),targetSha256=hashlib.sha256(rom).hexdigest(),userApprovalPending=True)
 (out/'build.json').write_text(json.dumps(report,indent=2));print(slug,'tiles',len(atlas),'changed',report['changedPixels'],'palette exact',report['paletteV4Exact'],flush=True)
if __name__=='__main__':
 for slug in sys.argv[1:] or ['normal','aldea','porunga']:build(slug)

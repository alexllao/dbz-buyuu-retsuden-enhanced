"""Revisión de color: tierras neutras, casa marfil y cielo continuo.

Parte de los índices ya aprobados en definición V3. No vuelve a remuestrear
el dibujo ni a aproximar texturas. Solo recolorea la casa y deduplica tiles
idénticos para codificar el resultado exactamente.
"""
from pathlib import Path
import sys,json,struct,hashlib
from datetime import datetime,timezone,timedelta
sys.path.insert(0,'work/simulation-deps')
import numpy as np
from PIL import Image
P=Path('work/namek-native-v4');OLD=Path('work/namek-native-v3')
BASE=Path('work/combo-startup/candidate.bin').read_bytes()
assert hashlib.sha256(BASE).hexdigest()=='68f838f7ce1fcf0f237d56c09826a359d26931d331cc1ec9716b9d321654ffab'
def cram(c):return sum(int(c[k])*2<<(k*4) for k in range(3))
def rgb(v):return tuple(((v>>s)&7)*255//7 for s in [1,5,9])
def flips(a):return [(a,0),(a[:,::-1],0x800),(a[::-1],0x1000),(a[::-1,::-1],0x1800)]
def decode(data,attrs):
 raw=np.frombuffer(data,np.uint8);tiles=np.stack((raw>>4,raw&15),axis=1).reshape(-1,8,8)
 yy,xx=np.indices((512,512));a=attrs[yy//8,xx//8]
 return tiles[a&2047,np.where(a&0x1000,7-(yy&7),yy&7),np.where(a&0x800,7-(xx&7),xx&7)]
house=Image.open('repository/assets/concepts/namek-native-v1/house.png').convert('RGBA')
box=house.getchannel('A').point(lambda a:255 if a>=192 else 0).getbbox()
hm=np.zeros((512,512),bool);hm[291:314,345:403]=np.asarray(house.crop(box).resize((58,23),Image.Resampling.BOX))[:,:,3]>=192
EARTH={6:(6,5,4),7:(4,4,3),8:(3,3,2),9:(2,2,2),14:(6,6,5)}
HOUSE_REMAP={6:15,7:14,8:6,9:8}

def build(slug):
 out=P/slug;out.mkdir(parents=True,exist_ok=True)
 attrs=np.frombuffer((OLD/slug/'map.bin').read_bytes(),'>u2').reshape(64,64).astype(np.uint16)
 source=decode((OLD/slug/'tiles.bin').read_bytes(),attrs);edited=source.copy()
 for a,b in HOUSE_REMAP.items():edited[hm&(source==a)]=b
 assert np.array_equal(source[~hm],edited[~hm])
 oldPalette=(OLD/slug/'palette.bin').read_bytes();words=list(struct.unpack('>24H',oldPalette))
 for at,c in EARTH.items():words[at]=cram(c)
 if slug=='normal':words[11]=words[12]=cram((1,5,2))
 common=list(struct.unpack_from('>10H',BASE,0x9102));before=np.array([rgb(v) for v in list(struct.unpack('>22H',oldPalette[:44]))+common],np.uint8).reshape(2,16,3)
 pal=np.array([rgb(v) for v in words[:22]+common],np.uint8).reshape(2,16,3)
 atlas=[];ids={};mapped=np.zeros_like(attrs)
 for ty in range(64):
  for tx in range(64):
   tile=edited[ty*8:ty*8+8,tx*8:tx*8+8];data,flip=min(((t.tobytes(),f) for t,f in flips(tile)),key=lambda v:v[0])
   if data not in ids:ids[data]=len(atlas);atlas.append(data)
   mapped[ty,tx]=(int(attrs[ty,tx])&0xe000)|ids[data]|flip
 assert len(atlas)<=736,(slug,len(atlas))
 packed=b''.join(bytes(p[i]<<4|p[i+1] for i in range(0,64,2)) for p in atlas).ljust(24576,b'\0')
 result=decode(packed,mapped);assert np.array_equal(result,edited)
 assert not (result==0).any()
 iy,ix=np.indices((512,512));bank=((mapped[iy//8,ix//8]>>13)&3)-2
 oldRGB=before[bank,source];newRGB=pal[bank,result]
 Image.fromarray(oldRGB).save(out/'previous-map.png');Image.fromarray(newRGB).save(out/'compiled-map.png')
 green=(bank==0)&np.isin(source,[11,12])&(iy<328)
 skyTransitions=(green[1:]&green[:-1]&(source[1:]!=source[:-1]))
 if slug=='normal':
  assert skyTransitions.sum()>0
  assert not np.any((newRGB[1:]!=newRGB[:-1])[skyTransitions])
 literal=struct.pack('<H',24575)+b''.join(b'\xff'+packed[i:i+8] for i in range(0,24576,8))
 mapbytes=mapped.astype('>u2').tobytes();palette=struct.pack('>24H',*words)
 rom=bytearray(BASE);rom[0x300000:0x300000+len(literal)]=literal;struct.pack_into('>I',rom,0x1769e2,0x300000)
 rom[0x19851a:0x19a51a]=mapbytes;rom[0x19e63e:0x19e66e]=palette
 bid=datetime.now(timezone(timedelta(hours=1))).strftime('%Y%m%d-%H%M%S');title=('DBZ V1.0 NAMEK4 '+slug+' '+bid).upper()[:48].encode().ljust(48,b' ')
 for at in [0x120,0x150]:rom[at:at+48]=title
 struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
 for name,data in [('tiles.bin',packed),('gfx.lz',literal),('map.bin',mapbytes),('map-header.bin',struct.pack('>H',64)+mapbytes),('palette.bin',palette),('candidate.bin',rom)]: (out/name).write_bytes(data)
 report=dict(variant=slug,buildId=bid,tiles=len(atlas),limit=736,recompressedLosslessly=True,source='V3 indices; no spatial resampling',outsideHouseIndicesChanged=int((source[~hm]!=result[~hm]).sum()),houseChangedPixels=int((source[hm]!=result[hm]).sum()),houseColorSha256=hashlib.sha256(newRGB[hm].tobytes()).hexdigest(),earthPalette={str(k):list(v) for k,v in EARTH.items()},houseRemap=HOUSE_REMAP,normalSky=dict(continuous=slug=='normal',paletteIndices=[11,12],color9bit=[1,5,2],previousTransitionPixels=int(skyTransitions.sum()) if slug=='normal' else None),sharedPaletteUntouched=common==list(struct.unpack_from('>10H',BASE,0x9102)),targetSha256=hashlib.sha256(rom).hexdigest(),userApprovalPending=True)
 (out/'build.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
if __name__=='__main__':
 for slug in sys.argv[1:] or ['normal','aldea','porunga']:build(slug)

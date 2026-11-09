from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,'work/simulation-deps')
import numpy as np
s=Path('work/namek-native/build.py').read_text();env={'__name__':'audit_defs'};exec(s.split('def compile_variant')[0],env)
start=s.index(" art=np.asarray",s.index('def compile_variant'));end=s.index(' fixed=sum',start);part=s[start:end];part='\n'.join(line[1:] for line in part.splitlines());part=part.replace(";Image.fromarray(world).save(out/'source-layout.png')",'')
env.update(slug='porunga',src=Path('repository/assets/concepts/namek-native-v1/porunga-sans-house.png'),out=Path('work/namek-quality-audit'));exec(part,env)
patterns=env['patterns'];maps=env['maps'];world=env['world'];pal=env['pal'];pre=np.zeros((512,512),np.uint8);prebank=np.zeros_like(pre)
for j,(bank,ix,flip) in enumerate(maps):
 tile=np.frombuffer(patterns[bank][ix],np.uint8).reshape(8,8)
 if flip&0x800:tile=tile[:,::-1]
 if flip&0x1000:tile=tile[::-1]
 y,x=divmod(j,64);pre[y*8:y*8+8,x*8:x*8+8]=tile;prebank[y*8:y*8+8,x*8:x*8+8]=bank
attrs=np.frombuffer(Path('work/namek-native/porunga/map.bin').read_bytes(),dtype='>u2').reshape(64,64);raw=np.frombuffer(Path('work/namek-native/porunga/tiles.bin').read_bytes(),dtype=np.uint8);tiles=np.stack((raw>>4,raw&15),axis=1).reshape(-1,8,8);yy,xx=np.indices((512,512));a=attrs[yy//8,xx//8];px=np.where(a&0x800,7-(xx&7),xx&7);py=np.where(a&0x1000,7-(yy&7),yy&7);post=tiles[a&2047,py,px];postbank=((a>>13)&3)-2
changed=post!=pre;rgbpre=pal[prebank,pre].astype(int);rgbpost=pal[postbank,post].astype(int);err=((rgbpost-rgbpre)**2).mean(axis=2)
report={}
for name,mask in [('all',np.ones_like(pre,dtype=bool)),('sky',yy<280),('grass',yy>=352),('rocks', (yy>=280)&(yy<352))]:
 idx=np.where(mask);tilechange=changed.reshape(64,8,64,8).transpose(0,2,1,3).any(axis=(2,3));tm=mask.reshape(64,8,64,8).transpose(0,2,1,3).any(axis=(2,3))
 report[name]=dict(pixels=int(mask.sum()),vqChangedPixels=int(changed[mask].sum()),vqChangedFraction=float(changed[mask].mean()),tiles=int(tm.sum()),tilesWithVqPixelChanges=int((tilechange&tm).sum()),postZeroPixels=int(((post==0)&mask).sum()),preZeroPixels=int(((pre==0)&mask).sum()),vqRGB_RMSE=float(np.sqrt(err[mask].mean())))
report.update(uniqueBefore=[len(p) for p in patterns],afterTiles=736,sourceDimensions=list(env['Image'].open(env['src']).size),sampling='non-integer nearest resize to512; piecewise y resample; per-tile canonical flips and medoid substitution')
Path('work/namek-quality-audit/pattern-audit.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

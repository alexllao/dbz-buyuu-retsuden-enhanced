from pathlib import Path
import json,zlib,struct,sys,hashlib
sys.path.insert(0,'work/intro-characters');from extract import extract
P=Path('work/intro-characters');old=Path('work/intro-consistency/boot/candidate');new=P/'runtime/candidate';source=Path('outputs/intro-paleta-G-v6-1/Buyuu_Retsuden_Enhanced_v6_1.bin');e=extract(source)
def read(p):
 b=p.read_bytes();i=8;raw=b''
 while i<len(b):
  n=int.from_bytes(b[i:i+4],'big');t=b[i+4:i+8];d=b[i+8:i+8+n];i+=n+12
  if t==b'IHDR':w,h,depth,col,*_=struct.unpack('>IIBBBBB',d);assert depth==8 and col==6
  if t==b'IDAT':raw+=d
 raw=zlib.decompress(raw);assert all(raw[y*(w*4+1)]==0 for y in range(h));return w,h,[raw[y*(w*4+1)+1:(y+1)*(w*4+1)] for y in range(h)]
checks=[]
for f in [720,840,960,1080,1200,1800]:
 w,h,a=read(old/f'F{f:04}.png');ww,hh,b=read(new/f'F{f:04}.png');assert (w,h)==(ww,hh);delta=[];outside=[]
 for y in range(h):
  for x in range(w):
   if a[y][x*4:x*4+4]!=b[y][x*4:x*4+4]:
    delta.append((x,y))
    if e['pixelOwnerCIDs'][(y//2)*320+x//2]<0:outside.append((x,y))
 checks.append(dict(frame=f,fullFrameEqual=not delta,changedPixels=len(delta),outsideBodyOwnerMaskChangedPixels=len(outside)))
print(checks)
# Derive actual libretro channel level conversion from baseline's native body pixels.
_,_,a=read(old/'F0960.png');lut=[{0:0} for _ in range(3)];conflicts=[]
for at,(cid,bank,index) in enumerate(zip(e['pixelOwnerCIDs'],e['pixelBanks'],e['pixelIndices'])):
 if cid<0:continue
 x=at%320;y=at//320;rgb=a[y*2][x*8:x*8+3];word=e['report']['palettes'][bank][index]
 for channel,shift in enumerate([1,5,9]):
  level=word>>shift&7
  if level in lut[channel] and lut[channel][level]!=rgb[channel]:conflicts.append((at,channel,level,lut[channel][level],rgb[channel]))
  lut[channel][level]=rgb[channel]
print('lut',lut,'conflicts',len(conflicts))
r=json.loads((P/'operations.json').read_text());_,_,b=read(new/'F0960.png');errors={};counts={}
for at,(cid,bank,index) in enumerate(zip(e['pixelOwnerCIDs'],e['pixelBanks'],e['pixelIndices'])):
 if cid<0:continue
 x=at%320;y=at//320;word=r['targetMapping'][str(cid)][f'{bank}:{index}'];expected=bytes(lut[c][word>>s&7] for c,s in enumerate([1,5,9]));actual=b[y*2][x*8:x*8+3];counts[cid]=counts.get(cid,0)+1
 if expected!=actual:errors[cid]=errors.get(cid,0)+1
print('nativebodyerrors',errors)
protected=json.loads((P/'material-plan.json').read_text())['protected_three_shade_material_ramps'];initial=json.loads((P/'target-mapping.json').read_text());assert all(r['targetMapping'][str(g['cid'])][key]==initial[str(g['cid'])][key] for g in protected for key in g['source'])
qa=dict(sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),targetSha256=hashlib.sha256((P/'candidate.bin').read_bytes()).hexdigest(),frames=checks,nativeBodyColorConversionLut=lut,nativeLutConflictPixels=len(conflicts),nativeFullbodyF960PerCIDPixels=counts,nativeFullbodyF960PerCIDRGBErrors={str(cid):errors.get(cid,0) for cid in counts},protectedMaterialRampsPreserved=len(protected),satMax=json.loads((new/'report.json').read_text())['satMax'],method='Cold boot2000displayframes, no buttons/RAM writes, before attractCPU. Pixel comparisons use sourceV6.1 for approvedG face, unchangedtitle, and body ownership; intro sourcebodypalette NOT approval reference. BodyexpectedRGB usesexplicitbattle-derived material targets after disclosedsecondaryadaptations.',limits=['No physical hardware test.','Secondary gray/trim shades simplified as listed in operations.json; final visual approval pending.'])
assert all(x['fullFrameEqual'] for x in checks if x['frame'] in [720,840,1800]);assert all(x['outsideBodyOwnerMaskChangedPixels']==0 for x in checks if x['frame'] in [960,1080,1200]);assert not errors and not conflicts
(P/'native-qa.json').write_text(json.dumps(qa,indent=2));r['nativeQA']='native-qa.json';r['status']='Native boot verified: approvedG face/title unchanged, exact disclosedbodytargets, visual review pending';(P/'operations.json').write_text(json.dumps(r,indent=2))


from pathlib import Path
import struct,json,hashlib
P=Path('work/knockdown-k2');P.mkdir(parents=True,exist_ok=True);base=Path('work/knockdown-k1/candidate.bin').read_bytes();r=bytearray(base);edits=[]
for program in [0xbf,0xc0,0xc1,0xc2]:
 a=0x1eb26+program*2;t=a+struct.unpack_from('>h',base,a)[0];j=t+2
 while base[j]!=0:j+=1
 weights=list(base[t+2:j]);before=int.from_bytes(base[t:t+2],'big');after=sum(x for x in weights if x<128)*4;r[t:t+2]=after.to_bytes(2,'big');edits.append(dict(program=hex(program),address=t,bytes=2,beforeDuration=before,afterDuration=after,timeUnitBefore=3,timeUnitAfter=4))
header='DBZ BUYUU V1.0 K2 2026-11-07 09:00Z'
for a in [0x120,0x150]:r[a:a+48]=header.encode().ljust(48,b' ')
struct.pack_into('>H',r,0x18e,sum(struct.unpack('>'+str((len(r)-512)//2)+'H',r[512:]))&65535);allowed=[(0x120,96),(0x18e,2)]+[(e['address'],2) for e in edits];assert all(any(a<=i<a+n for a,n in allowed) for i,(x,y) in enumerate(zip(base,r)) if x!=y)
(P/'candidate.bin').write_bytes(r);(P/'build.json').write_text(json.dumps(dict(version='1.0',variant='K2',buildId='20261107-100046',headerTitle=header,sourceSha256=hashlib.sha256(base).hexdigest(),targetSha256=hashlib.sha256(r).hexdigest(),mainRomUnchanged=True,experimental=True,edits=edits,allowed=allowed),indent=2));print(hashlib.sha256(r).hexdigest())

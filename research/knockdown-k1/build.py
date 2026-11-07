from pathlib import Path
import struct,json,hashlib
P=Path('work/knockdown-k1');base=Path('work/meteor-hits/candidate.bin').read_bytes();r=bytearray(base);edits=[]
for program,weights,unit in [(0xa1,[1,4,2,128,3,1,1],4),(0xa4,[1,1,4,2,128,1,3,1],4),(0xa5,[1,4,2,128,2,1,1,1],4),(0xbf,[2,1,2],3),(0xc0,[1,2,2],3),(0xc1,[2,1,1],3),(0xc2,[1,2,2],3)]:
 a=0x1eb26+program*2;t=a+struct.unpack_from('>h',base,a)[0];j=t+2
 while base[j]!=0:j+=1
 old=list(base[t+2:j]);assert len(old)==len(weights);newDuration=sum(x for x in weights if x<128)*unit;r[t:t+2]=newDuration.to_bytes(2,'big');r[t+2:j]=bytes(weights);edits.append(dict(program=hex(program),address=t,bytes=j-t,beforeDuration=int.from_bytes(base[t:t+2],'big'),afterDuration=newDuration,beforeWeights=old,afterWeights=weights,timeUnit=unit))
header='DBZ BUYUU V1.0 K1 2026-11-07 08:48Z'
for a in [0x120,0x150]:r[a:a+48]=header.encode().ljust(48,b' ')
struct.pack_into('>H',r,0x18e,sum(struct.unpack('>'+str((len(r)-512)//2)+'H',r[512:]))&65535);allowed=[(0x120,96),(0x18e,2)]+[(x['address'],x['bytes']) for x in edits];assert all(any(a<=i<a+n for a,n in allowed) for i,(x,y) in enumerate(zip(base,r)) if x!=y)
(P/'candidate.bin').write_bytes(r);(P/'build.json').write_text(json.dumps(dict(version='1.0',variant='K1 trial',buildId='20261107-094832',headerTitle=header,sourceSha256=hashlib.sha256(base).hexdigest(),targetSha256=hashlib.sha256(r).hexdigest(),experimental=True,mainRomUnchanged=True,edits=edits,allowed=allowed),indent=2));print(hashlib.sha256(r).hexdigest())

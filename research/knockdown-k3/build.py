from pathlib import Path
import struct,json,hashlib
P=Path('work/knockdown-k3');base=Path('work/knockdown-k1/candidate.bin').read_bytes();original=Path('work/meteor-hits/candidate.bin').read_bytes();r=bytearray(base);edits=[]
for program in [0xbf,0xc0,0xc1,0xc2]:
 a=0x1eb26+program*2;t=a+struct.unpack_from('>h',base,a)[0];before=int.from_bytes(base[t:t+2],'big');r[t:t+2]=original[t:t+2];edits.append(dict(program=hex(program),address=t,bytes=2,beforeDuration=before,afterDuration=int.from_bytes(r[t:t+2],'big')))
header='DBZ BUYUU V1.0 K3 2026-11-07 09:14Z'
for a in [0x120,0x150]:r[a:a+48]=header.encode().ljust(48,b' ')
struct.pack_into('>H',r,0x18e,sum(struct.unpack('>'+str((len(r)-512)//2)+'H',r[512:]))&65535);allowed=[(0x120,96),(0x18e,2)]+[(e['address'],2) for e in edits];assert all(any(a<=i<a+n for a,n in allowed) for i,(x,y) in enumerate(zip(base,r)) if x!=y)
(P/'candidate.bin').write_bytes(r);(P/'build.json').write_text(json.dumps(dict(version='1.0',variant='K3',buildId='20261107-101421',headerTitle=header,sourceSha256=hashlib.sha256(base).hexdigest(),targetSha256=hashlib.sha256(r).hexdigest(),mainRomUnchanged=True,experimental=True,originalGetupTiming=True,edits=edits,allowed=allowed),indent=2));print(hashlib.sha256(r).hexdigest())
s=Path('work/knockdown-k2/record.py').read_text().replace("root=baseDir/'work/knockdown-k2/comparison'/which", "root=baseDir/'work/knockdown-k3/comparison'/which").replace("rompath='work/knockdown-k2/candidate.bin' if which=='after' else 'work/knockdown-k1/candidate.bin'", "rompath='work/knockdown-k3/candidate.bin'").replace("[(0,'Goku'),(4,'Trunks'),(2,'Piccolo'),(5,'Cell'),(9,'Recoome')]", "[(0,'Goku'),(5,'Cell')]")
# Conservar los mismos estados de K1/K2 para aislar la incorporacion.
s=s.replace("if which=='before':", "if False:")
(P/'record.py').write_text(s)
s=Path('work/knockdown-k2/measure.py').read_text().replace('work/knockdown-k2','work/knockdown-k3').replace("romBuild='K2 trial'","romBuild='K3 trial'");(P/'measure.py').write_text(s)

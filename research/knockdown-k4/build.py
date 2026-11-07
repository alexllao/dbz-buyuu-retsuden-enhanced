from pathlib import Path
from datetime import datetime,timezone
import struct,json,hashlib
P=Path('work/knockdown-k4');P.mkdir(exist_ok=True)
base=Path('work/knockdown-k3/candidate.bin').read_bytes();r=bytearray(base);edits=[]
for program in [0xa1,0xa4,0xa5]:
 a=0x1eb26+program*2;t=a+struct.unpack_from('>h',base,a)[0];j=t+2
 while base[j]:j+=1
 weights=list(base[t+2:j]);unit=int.from_bytes(base[t:t+2],'big')//sum(x for x in weights if x<128)
 assert unit==4
 # Alargar exclusivamente la ultima pose tumbada. Mantener la unidad de
 # tiempo conserva los segmentos previos de caida y rebote.
 old=weights[-1];weights[-1]+=4
 r[t:t+2]=(sum(x for x in weights if x<128)*unit).to_bytes(2,'big');r[t+2:j]=bytes(weights)
 edits.append(dict(program=hex(program),address=t,bytes=j-t,oldLastWeight=old,newLastWeight=weights[-1],timeUnit=unit,extraNativeUpdates=16))
now=datetime.now(timezone.utc);bid=now.astimezone().strftime('%Y%m%d-%H%M%S');header='DBZ BUYUU V1.0 K4 '+now.strftime('%Y-%m-%d %H:%MZ')
for a in [0x120,0x150]:r[a:a+48]=header.encode().ljust(48,b' ')
struct.pack_into('>H',r,0x18e,sum(struct.unpack('>'+str((len(r)-512)//2)+'H',r[512:]))&65535)
allowed=[(0x120,96),(0x18e,2)]+[(e['address'],e['bytes']) for e in edits]
assert all(any(a<=i<a+n for a,n in allowed) for i,(x,y) in enumerate(zip(base,r)) if x!=y)
(P/'candidate.bin').write_bytes(r);(P/'build.json').write_text(json.dumps(dict(version='1.0',variant='K4',buildId=bid,headerTitle=header,sourceSha256=hashlib.sha256(base).hexdigest(),targetSha256=hashlib.sha256(r).hexdigest(),experimental=True,mainRomUnchanged=True,edits=edits,allowed=allowed),indent=2))
for name in ['measure.py','record.py']:
 s=Path('work/knockdown-k3',name).read_text().replace('knockdown-k3','knockdown-k4').replace('K3 trial','K4 trial')
 (P/name).write_text(s)
print(bid,hashlib.sha256(r).hexdigest())

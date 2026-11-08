from pathlib import Path
import hashlib,struct,json
from datetime import datetime,timezone,timedelta
P=Path('work/input-links');base=Path('work/basic-chains/candidate.bin').read_bytes();r=bytearray(base)
assert hashlib.sha256(base).hexdigest()=='ed43838799a67b29ff72d84ea9fc096ba46a0df3a60031d70c63cd23bd5416f1'
code=(P/'inputs.bin').read_bytes();assert len(code)<0x1000 and set(base[0x3de000:0x3de000+len(code)])=={255}
labels={k:int(v,16) for k,v in (l.split('=') for l in (P/'inputs.labels.txt').read_text().splitlines())}
old={k:int(v,16) for k,v in (l.split('=') for l in Path('work/input-v2/inputs.labels.txt').read_text().splitlines())}
allowed=[(0x3de000,len(code)),(0x120,96),(0x18e,2)];r[0x3de000:0x3de000+len(code)]=code
for at,label in [(0x3d0000,'frame_entry'),(0x9264,'matcher'),(0x922a,'history_direction'),(0x73f4,'round_reset')]:
 op=bytes.fromhex('4eb9' if at==0x73f4 else '4ef9');assert base[at:at+6]==op+struct.pack('>I',old[label]);r[at:at+6]=op+struct.pack('>I',labels[label]);allowed.append((at,6))
now=datetime.now(timezone(timedelta(hours=1)));bid=now.strftime('%Y%m%d-%H%M%S');head='DBZ V1.0 INPUT LINK '+now.strftime('%Y%m%d %H%M')
for at in [0x120,0x150]:r[at:at+48]=head.encode().ljust(48,b' ')
struct.pack_into('>H',r,0x18e,sum(struct.unpack('>'+str((len(r)-512)//2)+'H',r[512:]))&65535)
assert all(any(a<=i<a+n for a,n in allowed) for i,(x,y) in enumerate(zip(base,r)) if x!=y)
(P/'candidate.bin').write_bytes(r);(P/'build.json').write_text(json.dumps(dict(version='1.0',buildId=bid,sourceSha256=hashlib.sha256(base).hexdigest(),targetSha256=hashlib.sha256(r).hexdigest(),codeBytes=len(code),allowed=allowed,queueState='F72D/E and F73D/E, unused bytes in existing recognizer state'),indent=2));print(bid,hashlib.sha256(r).hexdigest())

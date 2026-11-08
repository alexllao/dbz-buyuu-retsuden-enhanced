from pathlib import Path
import struct,json,hashlib
from datetime import datetime,timezone,timedelta
P=Path('work/basic-chains');base=Path('work/throw-links/candidate.bin').read_bytes();r=bytearray(base);code=(P/'chain.bin').read_bytes();assert len(code)<0x800 and set(base[0x3dd000:0x3dd000+len(code)])=={255};assert base[0x20b7e:0x20b86].hex()=='1141005b0c010020';r[0x3dd000:0x3dd000+len(code)]=code;r[0x20b7e:0x20b86]=bytes.fromhex('4eb9')+struct.pack('>I',0x3dd000)+bytes.fromhex('4e71');now=datetime.now(timezone(timedelta(hours=1)));bid=now.strftime('%Y%m%d-%H%M%S');head='DBZ V1.0 GOKU CHAIN '+now.strftime('%Y%m%d %H%M')
for a in [0x120,0x150]:r[a:a+48]=head.encode().ljust(48,b' ')
struct.pack_into('>H',r,0x18e,sum(struct.unpack('>'+str((len(r)-512)//2)+'H',r[512:]))&65535);allowed=[(0x120,96),(0x18e,2),(0x3dd000,len(code)),(0x20b7e,8)];assert all(any(a<=i<a+n for a,n in allowed) for i,(x,y) in enumerate(zip(base,r)) if x!=y)
(P/'candidate.bin').write_bytes(r);(P/'build.json').write_text(json.dumps(dict(version='1.0',buildId=bid,headerTitle=head,sourceSha256=hashlib.sha256(base).hexdigest(),targetSha256=hashlib.sha256(r).hexdigest(),codeBytes=len(code),allowed=allowed,scope='Goku only: second confirmed A -> native401, third confirmed B -> native404. Existing cap3basics+1finisher retained.'),indent=2));print(bid,hashlib.sha256(r).hexdigest())

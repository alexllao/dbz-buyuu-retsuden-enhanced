from pathlib import Path
import json,struct,hashlib
from datetime import datetime,timezone,timedelta
P=Path('work/throw-links');base=Path('work/barrage-roster/candidate.bin').read_bytes();r=bytearray(base);labels={k:int(v,16) for k,v in (s.split('=') for s in (P/'throw.labels.txt').read_text().splitlines())};code=(P/'throw.bin').read_bytes();assert len(code)<0x800 and set(base[0x3dc000:0x3dc000+len(code)])=={255};r[0x3dc000:0x3dc000+len(code)]=code;edits=[]
for a,label,expected in [(0x1ad3e,'capture','4eb900020ca4'),(0x1ae2c,'impact','4eb9000219e4')]:
 assert base[a:a+6].hex()==expected;edits.append(dict(address=a,before=expected,label=label));r[a:a+6]=bytes.fromhex('4eb9')+struct.pack('>I',labels[label])
now=datetime.now(timezone(timedelta(hours=1)));bid=now.strftime('%Y%m%d-%H%M%S');head='DBZ V1.0 THROW LINK '+now.strftime('%Y%m%d %H%M')
for a in [0x120,0x150]:r[a:a+48]=head.encode().ljust(48,b' ')
struct.pack_into('>H',r,0x18e,sum(struct.unpack('>'+str((len(r)-512)//2)+'H',r[512:]))&65535);allowed=[(0x120,96),(0x18e,2),(0x3dc000,len(code))]+[(x['address'],6) for x in edits];assert all(any(a<=i<a+n for a,n in allowed) for i,(x,y) in enumerate(zip(base,r)) if x!=y)
(P/'candidate.bin').write_bytes(r);(P/'build.json').write_text(json.dumps(dict(version='1.0',buildId=bid,headerTitle=head,sourceSha256=hashlib.sha256(base).hexdigest(),targetSha256=hashlib.sha256(r).hexdigest(),edits=edits,allowed=allowed,ram='F7A0..F7AF, cached thrown attack type/power per victim',codeBytes=len(code)),indent=2));print(bid,hashlib.sha256(r).hexdigest())

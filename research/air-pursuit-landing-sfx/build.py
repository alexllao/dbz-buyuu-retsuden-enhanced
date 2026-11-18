from pathlib import Path
from datetime import datetime,timezone,timedelta
import struct,json,hashlib
P=Path('work/air-pursuit-landing-sfx');base=Path('work/menu-japanese/candidate.bin').read_bytes();r=bytearray(base)
assert hashlib.sha256(base).hexdigest()=='666135fff3069ecd06d25bab945b43970d929fea5d3493b88ff1fe6a54ca1f7f'
labels={k:int(v,16) for k,v in (l.split('=') for l in (P/'pursuit.labels.txt').read_text().splitlines())};code=(P/'pursuit.bin').read_bytes();assert len(code)<0x2000 and set(base[0x3e5000:0x3e5000+len(code)])=={255};r[0x3e5000:0x3e5000+len(code)]=code
hooks=[(0x3d0000,'frame_entry','4ef9003de000','4ef9'),(0x13020,'dispatch','43fa6bac3010','4ef9'),(0x11c1e,'boxes','4ef9003e1148','4ef9'),(0x11e14,'damage_p1','4eb9003d038e','4eb9'),(0x11ff8,'damage_p2','4eb9003d039a','4eb9'),(0x73f4,'round_reset','4eb9003e128e','4eb9'),(0x9264,'matcher','4ef9003de0e2','4ef9'),(0x2121a,'ground_gate','303c01c00828','4ef9')]
for at,label,old,op in hooks:
 assert base[at:at+6].hex()==old,(hex(at),base[at:at+6].hex())
 r[at:at+6]=bytes.fromhex(op)+struct.pack('>I',labels[label])
assert base[0x21220:0x21224].hex()=='0004001e'
r[0x21220:0x21224]=bytes.fromhex('4e714e71')
bid=datetime.now(timezone(timedelta(hours=1))).strftime('%Y%m%d-%H%M%S');title=('DBZ V1.0 AIR PURSUIT '+bid).encode().ljust(48,b' ')
for at in [0x120,0x150]:r[at:at+48]=title
struct.pack_into('>H',r,0x18e,sum(struct.unpack('>'+str((len(r)-512)//2)+'H',r[512:]))&65535)
allowed=[(0x3e5000,len(code)),(0x120,96),(0x18e,2),(0x21220,4)]+[(at,6) for at,*_ in hooks]
assert all(any(a<=i<a+n for a,n in allowed) for i,(x,y) in enumerate(zip(base,r)) if x!=y)
assert r[0x300000:0x330000]==base[0x300000:0x330000]
(P/'candidate.bin').write_bytes(r);(P/'build.json').write_text(json.dumps(dict(version='1.0',buildId=bid,sourceSha256=hashlib.sha256(base).hexdigest(),targetSha256=hashlib.sha256(r).hexdigest(),codeBytes=len(code),hooks=hooks,allowed=allowed,status='Internal prototype, not validated',ram='F800..F87F, two64-byte slots',command='UP+C after own native throw, Goku/Vegeta human, normal speed;16KI; at most2air basics'),indent=2))
print(bid,len(code),hashlib.sha256(r).hexdigest())




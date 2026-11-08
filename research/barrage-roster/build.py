from pathlib import Path
import struct,json,hashlib
from datetime import datetime,timezone,timedelta
P=Path('work/barrage-roster');base=Path('work/knockdown-k4/candidate.bin').read_bytes();r=bytearray(base);labels={k:int(v,16) for k,v in (s.split('=') for s in (P/'helpers.labels.txt').read_text().splitlines())};code=(P/'helpers.bin').read_bytes();assert set(base[0x3da200:0x3db400])=={255};r[0x3da200:0x3da200+len(code)]=code
edits=[]
def hook(a,n,label):
 edits.append(dict(address=a,before=base[a:a+n].hex(),helper=label));r[a:a+n]=bytes.fromhex('4eb9')+struct.pack('>I',labels[label])+bytes.fromhex('4e71')*((n-6)//2)
hook(0x1d33e,6,'advance');hook(0x20a7a,6,'animation');hook(0x1d36e,4+4,'slot')
# La carga original 1D36E mide 4 bytes; incluir BSR 1D372 y ejecutarlo
# despues desde el helper evita ocupar el incremento de 1D376.
hook(0x1d37a,6,'debit');hook(0x22066,8,'damage')
animations=[]
for cid,poses in [(0,[51,52,58,59,60,52,58,59,60,52,51]),(3,[58,59,58,57,58,59,58,57,58,59,58]),(5,[51,52,51,52,51,52,51,52,51,52,51]),(6,[51,52,51,52,51,52,51,52,51,52,51]),(7,[51,52,59,60,59,52,59,60,59,52,51]),(9,[51,52,51,52,51,52,51,52,51,52,51])]:
 weights=[1]*10+[6];unit=8;anim=b'\x00\x02'+(sum(weights)*unit).to_bytes(2,'big')+bytes(weights)+b'\0'+bytes(poses);at=0x3db000+cid*64;r[at:at+len(anim)]=anim;animations.append(dict(cid=cid,address=at,bytes=len(anim),weights=weights,poses=poses,timeUnit=unit))
now=datetime.now(timezone(timedelta(hours=1)));bid=now.strftime('%Y%m%d-%H%M%S');header='DBZ BUYUU V1.0 FIVE6 '+now.strftime('%Y%m%d %H%M')
for a in [0x120,0x150]:r[a:a+48]=header.encode().ljust(48,b' ')
struct.pack_into('>H',r,0x18e,sum(struct.unpack('>'+str((len(r)-512)//2)+'H',r[512:]))&65535)
allowed=[(0x120,96),(0x18e,2),(0x3da200,len(code)),*[(x['address'],x['bytes']) for x in animations]]+[(e['address'],len(bytes.fromhex(e['before']))) for e in edits];assert all(any(a<=i<a+n for a,n in allowed) for i,(x,y) in enumerate(zip(base,r)) if x!=y)
(P/'candidate.bin').write_bytes(r);(P/'build.json').write_text(json.dumps(dict(version='1.0',variant='Six native five-shot barrages on K4',buildId=bid,headerTitle=header,sourceSha256=hashlib.sha256(base).hexdigest(),targetSha256=hashlib.sha256(r).hexdigest(),edits=edits,allowed=allowed,animations=animations,codeBytes=len(code)),indent=2));print(bid,hashlib.sha256(r).hexdigest())

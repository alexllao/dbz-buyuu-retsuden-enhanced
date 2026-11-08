from pathlib import Path
from datetime import datetime,timezone,timedelta
import struct,hashlib,json
P=Path('work/combo-startup');base=Path('work/input-links/candidate.bin').read_bytes();r=bytearray(base);assert hashlib.sha256(base).hexdigest()=='7e60aa9b967f9c647bfd77992afbcca2e8261f5e2f63a6534838872aa02c7cc4'
code=(P/'startup.bin').read_bytes();assert len(code)<0x1000 and set(base[0x3df000:0x3df000+len(code)])=={255};r[0x3df000:0x3df000+len(code)]=code
labels={k:int(v,16) for k,v in (l.split('=') for l in (P/'startup.labels.txt').read_text().splitlines())};assert base[0x20a7a:0x20a80].hex()=='4eb9003da272';r[0x20a7a:0x20a80]=bytes.fromhex('4eb9')+struct.pack('>I',labels['entry'])
old={k:int(v,16) for k,v in (l.split('=') for l in Path('work/input-links/inputs.labels.txt').read_text().splitlines())};assert base[0x73f4:0x73fa]==bytes.fromhex('4eb9')+struct.pack('>I',old['round_reset']);r[0x73f4:0x73fa]=bytes.fromhex('4eb9')+struct.pack('>I',labels['round_reset'])
now=datetime.now(timezone(timedelta(hours=1)));bid=now.strftime('%Y%m%d-%H%M%S');title='DBZ V1.0 COMBO KI '+now.strftime('%Y%m%d %H%M')
for at in [0x120,0x150]:r[at:at+48]=title.encode().ljust(48,b' ')
struct.pack_into('>H',r,0x18e,sum(struct.unpack('>'+str((len(r)-512)//2)+'H',r[512:]))&65535)
allowed=[(0x3df000,len(code)),(0x20a7a,6),(0x73f4,6),(0x120,96),(0x18e,2)];assert all(any(a<=i<a+n for a,n in allowed) for i,(x,y) in enumerate(zip(base,r)) if x!=y)
(P/'candidate.bin').write_bytes(r);(P/'build.json').write_text(json.dumps(dict(version='1.0',buildId=bid,headerTitle=title,sourceSha256=hashlib.sha256(base).hexdigest(),targetSha256=hashlib.sha256(r).hexdigest(),codeBytes=len(code),allowed=allowed,state='F7B0..F7B7, selected program and latched flag per player; spare byte reserved'),indent=2));print(bid,hashlib.sha256(r).hexdigest())

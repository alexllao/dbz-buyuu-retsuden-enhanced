from pathlib import Path
import json,struct,hashlib
from datetime import datetime,timezone,timedelta
P=Path('work/namek-native-r10');base=Path('work/combo-startup/candidate.bin').read_bytes();rom=bytearray(base);resources=[]
for k,slug in enumerate(['normal','aldea','porunga']):
 for file,off in [('gfx.lz',0),('map-header.bin',0x7000),('palette.bin',0x9100)]:
  at=0x300000+k*0x10000+off;data=(P/slug/file).read_bytes();assert set(base[at:at+len(data)])=={255};rom[at:at+len(data)]=data;resources.append(dict(variant=slug,path=file,address=at,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
ops=json.loads(Path('work/namek-menu/operations.json').read_text())['operations']
for op in ops:
 at=op['offset'];data=bytes.fromhex(op['data']);assert rom[at:at+len(data)]==bytes.fromhex(op['before']);rom[at:at+len(data)]=data
bid=datetime.now(timezone(timedelta(hours=1))).strftime('%Y%m%d-%H%M%S');title=('DBZ V1.0 NAMEK10 '+bid).encode().ljust(48,b' ')
for at in [0x120,0x150]:rom[at:at+48]=title
struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
allowed=[(0x120,96),(0x18e,2)]+[(r['address'],r['bytes']) for r in resources]+[(o['offset'],len(bytes.fromhex(o['data']))) for o in ops]
assert all(any(a<=i<a+n for a,n in allowed) for i,(x,y) in enumerate(zip(base,rom)) if x!=y)
for a,n in [(0x1769ca,36),(0x198518,8194),(0x19e63e,48),(0x9102,20)]:assert rom[a:a+n]==base[a:a+n]
assert len({json.loads((P/s/'build.json').read_text())['houseColorSha256'] for s in ['normal','aldea','porunga']})==1
(P/'integrated.bin').write_bytes(rom)
report=dict(buildId=bid,sha256=hashlib.sha256(rom).hexdigest(),parentSha256=hashlib.sha256(base).hexdigest(),allowedChanges=allowed,resources=resources,originalNamekUntouched=True,gameplayUntouched=True,sharedHouseExact=True,userApprovalPending=True)
(P/'integrated-build.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)

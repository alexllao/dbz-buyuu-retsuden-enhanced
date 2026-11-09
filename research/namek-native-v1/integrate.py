from pathlib import Path
import struct,json,hashlib
from datetime import datetime,timezone,timedelta
P=Path('work/namek-native');rom=bytearray((P/'assets-rom.bin').read_bytes());base=Path('work/combo-startup/candidate.bin').read_bytes();ops=json.loads(Path('work/namek-menu/operations.json').read_text())
for op in ops['operations']:
 at=op['offset'];data=bytes.fromhex(op['data']);assert rom[at:at+len(data)]==bytes.fromhex(op['before']),hex(at);rom[at:at+len(data)]=data
now=datetime.now(timezone(timedelta(hours=1)));bid=now.strftime('%Y%m%d-%H%M%S');title='DBZ V1.0 EXTRA NAMEK '+now.strftime('%Y%m%d %H%M')
for at in [0x120,0x150]:rom[at:at+48]=title.encode().ljust(48,b' ')
struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
resources=json.loads((P/'resources.json').read_text());allowed=[(0x120,96),(0x18e,2)]+[(int(r['address'],16),r['bytes']) for r in resources['resources']]+[(o['offset'],len(bytes.fromhex(o['data']))) for o in ops['operations']]
assert all(any(a<=i<a+n for a,n in allowed) for i,(x,y) in enumerate(zip(base,rom)) if x!=y)
for at,n in [(0x1769ca,36),(0x198518,8194),(0x19e63e,48),(0x9102,20)]:assert rom[at:at+n]==base[at:at+n]
(P/'integrated.bin').write_bytes(rom);(P/'integrated-build.json').write_text(json.dumps(dict(version='1.0',buildId=bid,headerTitle=title,parentSha256=hashlib.sha256(base).hexdigest(),targetSha256=hashlib.sha256(rom).hexdigest(),targetBytes=len(rom),experimental=True,userApprovalPending=True,physicalConsoleTested=False,originalStage6DataAndSharedColorsUntouched=True,menuOperations=ops,resources=resources,allowedChanges=allowed),indent=2));print('INTEGRATED',bid,hashlib.sha256(rom).hexdigest())

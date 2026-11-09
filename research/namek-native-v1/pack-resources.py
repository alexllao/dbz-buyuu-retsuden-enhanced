from pathlib import Path
import json,hashlib
P=Path('work/namek-native');base=Path('work/combo-startup/candidate.bin').read_bytes();rom=bytearray(base);records=[]
for k,slug in enumerate(['normal','aldea','porunga']):
 block=0x300000+k*0x10000
 for name,offset in [('gfx.lz',0),('map-header.bin',0x7000),('palette.bin',0x9100)]:
  data=(P/slug/name).read_bytes();at=block+offset;assert set(base[at:at+len(data)])=={255};rom[at:at+len(data)]=data;records.append(dict(variant=slug,file=name,address=hex(at),bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
for a,n in [(0x1769ca,36),(0x198518,8194),(0x19e63e,48)]:assert rom[a:a+n]==base[a:a+n]
(P/'assets-rom.bin').write_bytes(rom);(P/'resources.json').write_text(json.dumps(dict(baseSha256=hashlib.sha256(base).hexdigest(),resources=records,originalStage6DataAndPointersUntouched=True),indent=2));print('RESOURCES READY',hashlib.sha256(rom).hexdigest())

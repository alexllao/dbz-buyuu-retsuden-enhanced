from pathlib import Path
import json,struct,hashlib
p=Path('work/intro-consistency');source=Path('outputs/cambio-de-lado-v6/Buyuu_Retsuden_Enhanced_v6.bin');base=source.read_bytes();rom=bytearray(base)
assert hashlib.sha256(base).hexdigest()=='a6d472c58c2f9cf8b39ba3f8cad46ada784dac91f83cc7421b461fcfb537eccb'
changes=[]
def put(a,data,role):
 before=bytes(rom[a:a+len(data)]);rom[a:a+len(data)]=data;changes.append({'address':hex(a),'before':before.hex(),'after':bytes(data).hex(),'role':role})
# Keep the distinct blue backdrop entry of the opening scene.
put(0x1addb4,base[0x1ade34:0x1ade52],'Opening Goku palette entries1..15: exact approved G title colors; entry0 preserved')
for a,old,new,role in [(0x1adde4,0x8ce,0xcce,'body bank1 skin light'),(0x1adde8,0x48e,0x68a,'body bank1 skin mid'),(0x1addde,0x26c,0x246,'body bank1 skin shadow'),(0x1addf8,0x8ce,0xcce,'body bank2 skin light'),(0x1addfa,0x48e,0x68a,'body bank2 skin mid'),(0x1addfc,0x26c,0x246,'body bank2 skin shadow')]:
 assert struct.unpack_from('>H',rom,a)[0]==old
 put(a,struct.pack('>H',new),role+'; source approved G skin ramp')
put(0x18e,struct.pack('>H',sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535),'Genesis checksum')
allowed=set()
for x in changes:allowed.update(range(int(x['address'],16),int(x['address'],16)+len(bytes.fromhex(x['after']))))
assert all(i in allowed for i,(a,b) in enumerate(zip(base,rom)) if a!=b)
assert rom[0x1addb2:0x1addb4]==base[0x1addb2:0x1addb4]
assert rom[0x1addb4:0x1addd2]==rom[0x1ade34:0x1ade52]
(p/'candidate.bin').write_bytes(rom)
report={'sourceSha256':hashlib.sha256(base).hexdigest(),'targetSha256':hashlib.sha256(rom).hexdigest(),'changes':changes,'changedBytes':sum(a!=b for a,b in zip(base,rom)),'scope':'Only opening face palette duplicate,6shared full-body skin entries andchecksum. Approved title G, credit, gameplay, ki, graphics/mapping and timing unchanged. Shared colors can also shade boots or armor.'}
(p/'build.json').write_text(json.dumps(report,indent=2));print(json.dumps({'targetSha256':report['targetSha256'],'changedBytes':report['changedBytes']}))

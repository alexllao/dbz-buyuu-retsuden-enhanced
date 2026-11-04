from pathlib import Path
import struct,hashlib,json
p=Path('work/gameplay-review')
rom=bytearray(Path('work/auras/colors-v4/candidate.bin').read_bytes())
code=(p/'controls-v2.bin').read_bytes()
labels={k:int(v,16) for k,v in (l.split('=') for l in (p/'controls-v2.labels.txt').read_text().splitlines())}
assert len(code)<0x400
rom[0x7b000:0x7b400]=b'\xff'*0x400
rom[0x7b000:0x7b000+len(code)]=code
for a,label,n in [(0x8f58,'input_entry',8),(0x209dc,'animation_entry',8),(0x20a46,'animation_exit',6)]:
 rom[a:a+n]=bytes.fromhex('4ef9')+struct.pack('>I',labels[label])+bytes.fromhex('4e71')*((n-6)//2)
struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
(p/'candidate-v2.bin').write_bytes(rom)
print(json.dumps({'sha256':hashlib.sha256(rom).hexdigest(),'bytes':len(code),'labels':labels}))

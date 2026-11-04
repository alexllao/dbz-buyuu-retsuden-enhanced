from pathlib import Path
import json,hashlib,struct,sys
sys.path.insert(0,str(Path(__file__).parent/'deps'))
from capstone import *

original=Path('work/rom/original.bin').read_bytes()
assert hashlib.sha256(original).hexdigest()=='217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557'
code=Path('work/controls_v1.bin').read_bytes()
labels={k:int(v,16) for k,v in (line.split('=') for line in Path('work/controls_v1.labels.txt').read_text().splitlines())}
assert len(code)<0x3000
assert set(original[0x7b000:0x7b000+len(code)])=={255}
patches=[
 (0x8f58,bytes.fromhex('4a38e7446600000a'),bytes.fromhex('4ef9')+struct.pack('>I',labels['input_entry'])+bytes.fromhex('4e71')),
 (0x209dc,bytes.fromhex('48e700606100006a'),bytes.fromhex('4ef9')+struct.pack('>I',labels['animation_entry'])+bytes.fromhex('4e71')),
 (0x20a46,bytes.fromhex('4cdf06004e75'),bytes.fromhex('4ef9')+struct.pack('>I',labels['animation_exit'])),
]
rom=bytearray(original)
for address,expected,replacement in patches:
 assert rom[address:address+len(expected)]==expected,(hex(address),rom[address:address+len(expected)].hex())
 rom[address:address+len(expected)]=replacement
rom[0x7b000:0x7b000+len(code)]=code
rom[0x18e:0x190]=struct.pack('>H',sum(struct.unpack('>'+str((len(rom)-0x200)//2)+'H',rom[0x200:]))&0xffff)
dest=Path('work/rom/controls-v1.bin');dest.write_bytes(rom)
dis=Cs(CS_ARCH_M68K,CS_MODE_BIG_ENDIAN|CS_MODE_M68K_000)
instructions=list(dis.disasm(code,0x7b000))
assert sum(i.size for i in instructions)==len(code)
assert not any(i.mnemonic in ('illegal','dc.w') for i in instructions)
Path('work/controls-capstone-check.txt').write_text('\n'.join(f'{i.address:08x}: {i.bytes.hex():24} {i.mnemonic} {i.op_str}' for i in instructions),encoding='utf-8')
record={'source_sha256':hashlib.sha256(original).hexdigest(),'output_sha256':hashlib.sha256(rom).hexdigest(),'rom_size':len(rom),'code_range':[hex(0x7b000),hex(0x7b000+len(code))],'code_bytes':len(code),'labels':{k:hex(v) for k,v in labels.items()},'hooks':[{'offset':hex(a),'original':e.hex(),'replacement':r.hex()} for a,e,r in patches],'checksum':rom[0x18e:0x190].hex(),'scratch':'Per actor 0x108..0x10F in the unused gap before native 0x118 timer fields; initialized at first human-input tick. Magic stability checked across 11 characters and both speeds.','status':'Experimental internal build pending emulator checks'}
Path('work/controls-build.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps({k:record[k] for k in ('rom_size','code_bytes','output_sha256','status')}))

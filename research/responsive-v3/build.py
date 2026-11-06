from pathlib import Path
import json,hashlib,struct
P=Path('work/responsive-v3');base=Path('work/input-v2/candidate.bin').read_bytes();rom=bytearray(base);sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(base)=='17c1d2789c095cba7d3e66ec7c16af24503899f195b3ca4e9be4fc26889aff74'
labels={k:int(v,16) for k,v in (l.split('=') for l in (P/'response.labels.txt').read_text().splitlines())};code=(P/'response.bin').read_bytes()
assert len(code)<0x1000 and set(base[0x3d4000:0x3d4000+len(code)])=={255}
rom[0x3d4000:0x3d4000+len(code)]=code
allowed=[(0x3d4000,len(code)),(0x18e,2)]
version=json.loads((P/'version.json').read_text(encoding='utf8'))
title=version['headerTitle'].encode('ascii').ljust(48,b' ')
assert len(title)==48
rom[0x120:0x150]=title;rom[0x150:0x180]=title
allowed.extend([(0x120,48),(0x150,48)])
for address,original,label in [(0x8f68,'41f8e75e43f8e886','input_p1'),(0x8fdc,'41f8e88643f8e75e','input_p2')]:
 assert base[address:address+8].hex()==original
 rom[address:address+8]=b'\x4e\xf9'+struct.pack('>I',labels[label])+b'\x4e\x71';allowed.append((address,8))
assert base[0x8d0a:0x8d10].hex()=='4a38e73c660a'
rom[0x8d0a:0x8d10]=b'\x4e\xf9'+struct.pack('>I',labels['poll_gate']);allowed.append((0x8d0a,6))
assert base[0x3b02f4:0x3b02fa].hex()=='4eb9003b02da'
rom[0x3b02f4:0x3b02fa]=b'\x4e\xf9'+struct.pack('>I',labels['counter_tick']);allowed.append((0x3b02f4,6))
struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
assert all(any(a<=i<a+n for a,n in allowed) for i,(x,y) in enumerate(zip(base,rom)) if x!=y)
(P/'candidate.bin').write_bytes(rom)
meta=dict(sourceSha256=sha(base),targetSha256=sha(rom),codeBytes=len(code),allowed=allowed,status='Release candidate',version=version)
(P/'build.json').write_text(json.dumps(meta,indent=2)+'\n');print(meta)

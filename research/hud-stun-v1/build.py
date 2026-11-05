from pathlib import Path
import struct,hashlib,json,re
P=Path('work/stun-hud');sourceText=(P/'hud.asm').read_text(encoding='utf-8-sig');assert set(re.findall(r'@([a-zA-Z0-9_]+)',sourceText)) <= set(re.findall(r'^([a-zA-Z0-9_]+):',sourceText,re.M));base=Path('work/native-stun-fix/candidate.bin').read_bytes();rom=bytearray(base);code=(P/'hud.bin').read_bytes();assets=(P/'resources.bin').read_bytes();assert len(code)<0x4000 and len(assets)==0x1740
assert set(base[0x3b0000:0x3c0000])=={255};assert base[0x706e:0x7078].hex()=='23fc6c00000200c00004'
labels={k:int(v,16) for k,v in (line.split('=') for line in (P/'hud.labels.txt').read_text().splitlines())}
for address,label in [(0x6f28,'entry'),(0x701c,'entry_sat')]:
 assert base[address:address+6].hex()=='4df900c00004'
 rom[address:address+6]=bytes.fromhex('4ef9')+struct.pack('>I',labels[label])
for address in [0x6eb8]:
 assert base[address:address+6].hex()=='4eb9001ae356'
 rom[address:address+6]=bytes.fromhex('4eb9')+struct.pack('>I',labels['pixels_entry'])
rom[0x706e:0x7078]=bytes.fromhex('4ef9')+struct.pack('>I',labels['entry_direct'])+bytes.fromhex('4e714e71');rom[0x3b0000:0x3b0000+len(code)]=code;rom[0x3b4000:0x3b4000+len(assets)]=assets
struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535);(P/'candidate.bin').write_bytes(rom);(P/'build.json').write_text(json.dumps({'sourceSha256':hashlib.sha256(base).hexdigest(),'targetSha256':hashlib.sha256(rom).hexdigest(),'codeBytes':len(code),'resourcesBytes':len(assets),'vram':'AF20..AFA0: four pattern tiles, no labels','sat':'Two sprites prepended during native transfer, native head clear/attribute preserved afterwards; no persistent game RAM reserved'},indent=2));print('BUILT',len(code),hashlib.sha256(rom).hexdigest())

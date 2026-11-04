from pathlib import Path
import json,hashlib,struct
p=Path('work/combos');source=Path('outputs/intro-personajes-originales-v6-6/Buyuu_Retsuden_Enhanced_v6_6.bin');base=source.read_bytes();rom=bytearray(base);code=(p/'combo-v1.bin').read_bytes()
assert len(code)<0x1000 and set(base[0x3d0000:0x3d0000+len(code)])=={255}
assert base[0x8dcc:0x8dd2].hex()=='4eb9003e0000'
rom[0x8dcc:0x8dd2]=bytes.fromhex('4eb9003d0000');rom[0x3d0000:0x3d0000+len(code)]=code
labels={k:int(v,16) for k,v in (line.split('=') for line in (p/'combo-v1.labels.txt').read_text().splitlines())}
for address,label,opcode in [(0x11e14,'damage_p1','4eb9'),(0x11ff8,'damage_p2','4eb9'),(0x11ef4,'repeat_p1','4ef9'),(0x120d4,'repeat_p2','4ef9')]:
 rom[address:address+6]=bytes.fromhex(opcode)+struct.pack('>I',labels[label])
struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
(p/'candidate.bin').write_bytes(rom)
meta={'sourceSha256':hashlib.sha256(base).hexdigest(),'targetSha256':hashlib.sha256(rom).hexdigest(),'codeBytes':len(code),'hook':'0x8DCC after native A/B matcher, before side switch/native dispatch','codeBase':'0x3D0000','scratch':'Goku/Vegeta human actors only,104..107; separate from controls108..10F and auras110..117; bounded static scan and dynamic audit','allowedChanges':['checksum 0x18E','hook 0x8DCC','new code 0x3D0000','contact checks 0x11E14/11FF8/11EF4/120D4'],'status':'Experimental internal candidate, tests pending'}
(p/'build.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta))

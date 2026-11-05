from pathlib import Path
import struct,hashlib,json,re
P=Path('work/teleport-advantage');base=Path('work/stun-break/candidate.bin').read_bytes();code=(P/'side.bin').read_bytes();labels={k:int(v,16) for k,v in (l.split('=') for l in (P/'side.labels.txt').read_text().splitlines())}
assert len(code)<0x1000 and labels['adv_update']%2==0
assert set(re.findall(r'@([a-zA-Z0-9_]+)',(P/'side.asm').read_text()))<=set(labels)
rom=bytearray(base);rom[0x3e0000:0x3e1000]=b'\xff'*0x1000;rom[0x3e0000:0x3e0000+len(code)]=code
needle=bytes.fromhex('4eb9003e01f4');a=base.find(needle,0x7b000,0x7b400);assert a>=0 and base.find(needle,a+1,0x7b400)<0
rom[a:a+6]=bytes.fromhex('4eb9')+struct.pack('>I',labels['pre_input'])
struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
(P/'candidate.bin').write_bytes(rom);(P/'build.json').write_text(json.dumps(dict(sourceSha256=hashlib.sha256(base).hexdigest(),targetSha256=hashlib.sha256(rom).hexdigest(),codeBytes=len(code),relinkedControlCall=hex(a),preInput=hex(labels['pre_input']),windowInputUpdates=6,newActorBytes=['117'],preservedAuraDirty='P1+116 E874 untouched',behavior='After new C side switch finishes successfully across opponent, delay opponent new A/B for six eligible input updates. Guard, movement and C counter remain. No guaranteed hit, animation speed or damage change.'),indent=2));print('BUILD',len(code),hashlib.sha256(rom).hexdigest())

from pathlib import Path
import struct,hashlib,json,re
P=Path('work/hits-hud');base=Path('work/teleport-advantage/candidate.bin').read_bytes();rom=bytearray(base);code=(P/'hud.bin').read_bytes();font=(P/'font.bin').read_bytes();labels={k:int(v,16) for k,v in (line.split('=') for line in (P/'hud.labels.txt').read_text().splitlines())}
assert len(code)<0x4000 and len(font)==9600
assert set(re.findall(r'@([a-zA-Z0-9_]+)',(P/'hud.asm').read_text()))<=set(labels)
for at,label,op in [(0x6f28,'entry','4ef9'),(0x701c,'entry_sat','4ef9'),(0x6eb8,'pixels_entry','4eb9'),(0x21a0e,'break_stun_on_hit','4ef9')]:rom[at:at+6]=bytes.fromhex(op)+struct.pack('>I',labels[label])
rom[0x706e:0x7078]=bytes.fromhex('4ef9')+struct.pack('>I',labels['entry_direct'])+bytes.fromhex('4e714e71')
assert base[0x20b7a:0x20b82].hex()=='b05067201141005b'
cinematicCalls=[]
for at in range(0x13000,0x1eb26,2):
 if base[at:at+6] in [bytes.fromhex('4eb900020b7a'),bytes.fromhex('4ef900020b7a')]:
  rom[at+2:at+6]=struct.pack('>I',labels['cinematic_entry']);cinematicCalls.append(at)
assert cinematicCalls
assert rom[0x20b7a:0x20b82]==base[0x20b7a:0x20b82]
(P/'cinematic-calls.json').write_text(json.dumps(cinematicCalls))
assert base[0x73f4:0x73fa].hex()=='117c00ff0083'
rom[0x73f4:0x73fa]=bytes.fromhex('4eb9')+struct.pack('>I',labels['round_counter_reset'])
assert base[0x3e0000:0x3e0006].hex()=='48e7fffe40e7'
rom[0x3e0000:0x3e0006]=bytes.fromhex('4ef9')+struct.pack('>I',labels['frame_entry'])
assert set(base[0x3b6000:0x3b6000+len(font)])=={255}
rom[0x3b0000:0x3b0000+len(code)]=code;rom[0x3b6000:0x3b6000+len(font)]=font
struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
(P/'candidate.bin').write_bytes(rom);(P/'build.json').write_text(json.dumps(dict(sourceSha256=hashlib.sha256(base).hexdigest(),targetSha256=hashlib.sha256(rom).hexdigest(),codeBytes=len(code),fontBytes=len(font),hud='Native counter, one latest attacking side visible, three unused pattern tiles AFA0..B000; original stun bar graphics unchanged',state='Actor120..125, preserving native126 and aura116/advantage117',stunFix='Native accumulation inactivity counter32 resets on accepted unblocked hit; no periodic clear in middle of recent hits'),indent=2));print(len(code),hashlib.sha256(rom).hexdigest())

from pathlib import Path
import hashlib,json,struct
P=Path('work/responsive-cancels-v1')
base=Path('work/hits-hud-v3/candidate.bin').read_bytes();rom=bytearray(base)
assert hashlib.sha256(base).hexdigest()=='2907df9f27139b6bfa8c646aca7a92f61ee2aa9f38b6924b6238b4f8548cf748'
labels={k:int(v,16) for k,v in (line.split('=') for line in (P/'responsive.labels.txt').read_text().splitlines())}
old={k:int(v,16) for k,v in (line.split('=') for line in Path('work/native-stun-fix/combos-v5.labels.txt').read_text().splitlines())}
code=(P/'responsive.bin').read_bytes();assert set(base[0x3d2000:0x3d2000+len(code)])=={255}
rom[0x3d2000:0x3d2000+len(code)]=code
def jump(at,label):rom[at:at+6]=b'\x4e\xf9'+struct.pack('>I',labels[label])
assert base[0x3d0000:0x3d0006].hex()=='48e7fffe40e7'
jump(0x3d0000,'entry')
jump(old['common_cancel'],'cancel_basic')
assert base[0x7b012:0x7b018].hex()=='4eb900008f68'
rom[0x7b012:0x7b018]=b'\x4e\xb9'+struct.pack('>I',labels['input_restore'])
assert base[0x9264:0x926c].hex()=='43fa014261000114'
jump(0x9264,'matcher');rom[0x926a:0x926c]=b'\x4e\x71'
jump(0x7b4a2,'aura_residual')
assert base[0x922a:0x9230].hex()=='0c2800000059'
jump(0x922a,'history_direction')
assert base[0x2108a:0x21090].hex()=='082900040020'
jump(0x2108a,'throw_special_gate')
# Acortar sólo la preparación de carga: 4 unidades a 1. Incrementos nativos.
assert base[0x1f2ed]==4
rom[0x1f2ed]=1
struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
(P/'candidate.bin').write_bytes(rom)
preserved={name:base[a:z]==rom[a:z] for name,a,z in [('hits-stun',0x3b0000,0x3b9000),('aura-before-routing',0x7b400,0x7b4a2),('aura-after-routing',0x7b4b2,0x7d000),('side',0x3e0000,0x3e1000),('damage',0x21b4e,0x21b54),('stun-break',0x20914,0x209dc)]}
assert all(preserved.values())
meta=dict(sourceSha256=hashlib.sha256(base).hexdigest(),targetSha256=hashlib.sha256(rom).hexdigest(),preserved=preserved,codeBytes=len(code),status='internal candidate')
(P/'build.json').write_text(json.dumps(meta,indent=2));print(meta)

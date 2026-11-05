from pathlib import Path
import struct,hashlib,json
P=Path('work/stun-break');base=Path('work/stun-hud/candidate.bin').read_bytes();code=(P/'hud.bin').read_bytes();old=Path('work/stun-hud/hud.bin').read_bytes()
assert code[:len(old)]==old and len(code)-len(old)==32
assert base[0x21a0e:0x21a14].hex()=='0c68007d0028'
labels={k:int(v,16) for k,v in (line.split('=') for line in (P/'hud.labels.txt').read_text().splitlines())}
rom=bytearray(base);rom[0x3b0000:0x3b0000+len(code)]=code;rom[0x21a0e:0x21a14]=bytes.fromhex('4ef9')+struct.pack('>I',labels['break_stun_on_hit'])
struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
target=hashlib.sha256(rom).hexdigest();assert target=='c62d48cff3a76a1f2edcbde3e1bbf99e3bf856f824686467db8c07eb5989a46c'
(P/'candidate.bin').write_bytes(rom);print(target)

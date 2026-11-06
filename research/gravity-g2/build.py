from pathlib import Path
import hashlib,json,struct
P=Path('work/gravity-g2');base=Path('work/gohan-hits/candidate.bin').read_bytes();r=bytearray(base)
lab={k:int(v,16) for k,v in (s.split('=') for s in (P/'gravity.labels.txt').read_text().splitlines())};code=(P/'gravity.bin').read_bytes()
assert set(r[0x3d6000:0x3d6000+len(code)])=={255};r[0x3d6000:0x3d6000+len(code)]=code
for a,name,op in [(0x3d3000,'frame_entry','4ef9'),(0x20a90,'duration','4eb9'),(0x13110,'vertical','4eb9')]:r[a:a+6]=bytes.fromhex(op)+struct.pack('>I',lab[name])
r[0x3d348a:0x3d348c]=bytes.fromhex('7013')
# Menos tiempo en el aire: acortar recorrido normal para conservar velocidad horizontal.
old=struct.unpack_from('>H',base,0x1a1f8)[0];struct.pack_into('>H',r,0x1a1f8,round(old*2/3))
head='DBZ BUYUU V1.0 G2 GOKU 2026-11-06 15:49Z'
for a in [0x120,0x150]:r[a:a+48]=head.encode().ljust(48,b' ')
struct.pack_into('>H',r,0x18e,sum(struct.unpack('>'+str((len(r)-512)//2)+'H',r[512:]))&65535)
assert r[0x16b01:0x16b19]==base[0x16b01:0x16b19] and r[0x18af0:0x18b08]==base[0x18af0:0x18b08]
(P/'candidate.bin').write_bytes(r);(P/'build.json').write_text(json.dumps(dict(buildId='20261106-164956',header=head,sha256=hashlib.sha256(r).hexdigest(),baseSha256=hashlib.sha256(base).hexdigest(),scope='Goku only normal and running jump; baseline Piccolo Meteor; shared dash fix'),indent=2))
s=Path('work/gravity-probe/test.py').read_text().replace("f\"rompath='work/gravity-probe/{variant}.bin'\"", "\"rompath='work/gravity-g2/candidate.bin'\"").replace("Path(f'work/gravity-probe/{variant}","Path(f'work/gravity-g2/{variant}")
(P/'test.py').write_text(s)

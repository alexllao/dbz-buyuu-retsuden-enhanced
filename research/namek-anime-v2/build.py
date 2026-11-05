from pathlib import Path
import struct,hashlib,json
P=Path('work/namek-anime-v2');base=Path('work/stun-break/candidate.bin').read_bytes();rom=bytearray(base)
# Azul para terreno y copas; roca ocre/beige; cielo verde con luces amarillentas.
values=[0x0000,0x0620,0x0a40,0x0c62,0x0c84,0x0ea8,0x08ac,0x068a,0x0468,0x0246,0x0224,0x0262,0x04a4,0x08ec,0x0620,0x0eee,0x0444,0x0262,0x04a4,0x08ec,0x0eee,0x00e0]
a=0x19e63e;before=[int.from_bytes(base[a+i*2:a+i*2+2],'big') for i in range(22)];rom[a:a+44]=struct.pack('>22H',*values)
struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
assert all(0x18e<=i<0x190 or a<=i<a+44 for i,(x,y) in enumerate(zip(base,rom)) if x!=y)
(P/'proposal.bin').write_bytes(rom)
(P/'palette.json').write_text(json.dumps(dict(status='Visual proposal pending user selection; previous pink proposal rejected',stage=6,offset=hex(a),sourceSha256=hashlib.sha256(base).hexdigest(),targetSha256=hashlib.sha256(rom).hexdigest(),before=[f'{v:04X}' for v in before],after=[f'{v:04X}' for v in values],onlyStage6ColorsAndChecksumChanged=True,reference='Three new user images: blue grass and tree crowns, beige/ochre rock, green sky and yellowish highlights. No pink rock.'),indent=2)+'\n',encoding='utf-8')

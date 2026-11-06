from pathlib import Path
import hashlib,json,struct
P=Path('work/gohan-hits');base=Path('work/piccolo-hits/candidate.bin').read_bytes();rom=bytearray(base);sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(base)=='d3ea94bb78553b545b1db56da8e67a87b69ca8fa67621b6597a31b5ec75e813a'
code=(P/'contact.bin').read_bytes();assert len(code)<256 and set(base[0x3d5100:0x3d5100+len(code)])=={255};assert base[0x168c0:0x168c8].hex()=='13fc0047ffff5000'
rom[0x3d5100:0x3d5100+len(code)]=code;rom[0x168c0:0x168c8]=bytes.fromhex('4eb9003d51004e71')
v=dict(version='1.0',buildId='20261106-124607',buildDate='2026-11-06',buildTimestamp='2026-11-06T12:46:07+01:00',timezone='Europe/Madrid',headerTitle='DBZ BUYUU ENHANCED V1.0 2026-11-06 11:46Z',filename='DBZ_Buyuu_Retsuden_Enhanced_v1.0_build_20261106-124607.bin')
for a in [0x120,0x150]:rom[a:a+48]=v['headerTitle'].encode().ljust(48,b' ')
struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
allowed=[(0x120,96),(0x18e,2),(0x168c0,8),(0x3d5100,len(code))];assert all(any(a<=i<a+n for a,n in allowed) for i,(x,y) in enumerate(zip(base,rom)) if x!=y)
(P/'candidate.bin').write_bytes(rom);(P/'version.json').write_text(json.dumps(v,indent=2)+'\n');(P/'build.json').write_text(json.dumps(dict(sourceSha256=sha(base),targetSha256=sha(rom),codeBytes=len(code),allowed=allowed),indent=2)+'\n');print(sha(rom))

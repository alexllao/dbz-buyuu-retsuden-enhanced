from pathlib import Path
import hashlib,json,struct
P=Path('work/piccolo-hits');base=Path('work/ki-startup/candidate.bin').read_bytes();rom=bytearray(base);sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(base)=='4e6e2c7422b54e1bfaa9e2a94ba8632d8d7a4bc4a0c50c0a3bda591754b29bb0'
code=(P/'contact.bin').read_bytes();assert len(code)<256 and set(base[0x3d5000:0x3d5000+len(code)])=={255};assert base[0x16b34:0x16b3c].hex()=='13fc0047ffff5000'
rom[0x3d5000:0x3d5000+len(code)]=code;rom[0x16b34:0x16b3c]=bytes.fromhex('4eb9003d50004e71')
v=dict(version='1.0',buildId='20261106-105411',buildDate='2026-11-06',buildTimestamp='2026-11-06T10:54:11+01:00',timezone='Europe/Madrid',headerTitle='DBZ BUYUU ENHANCED V1.0 2026-11-06 09:54Z',filename='DBZ_Buyuu_Retsuden_Enhanced_v1.0_build_20261106-105411.bin')
for a in [0x120,0x150]:rom[a:a+48]=v['headerTitle'].encode().ljust(48,b' ')
struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
allowed=[(0x120,96),(0x18e,2),(0x16b34,8),(0x3d5000,len(code))];assert all(any(a<=i<a+n for a,n in allowed) for i,(x,y) in enumerate(zip(base,rom)) if x!=y)
(P/'candidate.bin').write_bytes(rom);(P/'version.json').write_text(json.dumps(v,indent=2)+'\n');(P/'build.json').write_text(json.dumps(dict(sourceSha256=sha(base),targetSha256=sha(rom),codeBytes=len(code),allowed=allowed),indent=2)+'\n');print(sha(rom))

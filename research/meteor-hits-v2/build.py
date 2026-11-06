from pathlib import Path
import json,hashlib,struct
P=Path('work/meteor-hits');base=Path('work/gohan-hits/candidate.bin').read_bytes();r=bytearray(base);labels={k:int(v,16) for k,v in (s.split('=') for s in (P/'contacts.labels.txt').read_text().splitlines())};code=(P/'contacts.bin').read_bytes();assert len(code)<256 and set(base[0x3da000:0x3da000+len(code)])=={255};r[0x3da000:0x3da000+len(code)]=code;allowed=[(0x3da000,len(code)),(0x120,96),(0x18e,2)]
for at,label in [(0x175ee,'a18'),(0x17bea,'freezer'),(0x191fe,'krilin'),(0x18d50,'trunks')]:
 assert base[at:at+8].hex()=='13fc0047ffff5000';r[at:at+8]=bytes.fromhex('4eb9')+struct.pack('>I',labels[label])+bytes.fromhex('4e71');allowed.append((at,8))
header='DBZ BUYUU ENHANCED V1.0 2026-11-06 16:42Z'
for at in [0x120,0x150]:r[at:at+48]=header.encode().ljust(48,b' ')
struct.pack_into('>H',r,0x18e,sum(struct.unpack('>'+str((len(r)-512)//2)+'H',r[512:]))&65535)
assert all(any(a<=i<a+n for a,n in allowed) for i,(x,y) in enumerate(zip(base,r)) if x!=y)
for a,n in [(0x70,4),(0x7640,6),(0x7686,6),(0x7240,8),(0x8d32,6),(0x3b035c,6)]:assert r[a:a+n]==base[a:a+n]
assert set(r[0x3d8000:0x3d9000])=={255}
(P/'candidate.bin').write_bytes(r);(P/'build.json').write_text(json.dumps(dict(version='1.0',buildId='20261106-174207',headerTitle=header,sourceSha256=hashlib.sha256(base).hexdigest(),targetSha256=hashlib.sha256(r).hexdigest(),allowed=allowed,addedMeteorShake=False,gravityG1G2=False),indent=2));print(hashlib.sha256(r).hexdigest())
s=Path('work/meteor-impact/roster.py').read_text().replace("rompath='work/meteor-impact/candidate.bin'", "rompath='work/meteor-hits/candidate.bin'").replace("P=Path('work/meteor-impact')", "P=Path('work/meteor-hits')");(P/'roster.py').write_text(s)

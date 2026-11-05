from pathlib import Path
import hashlib,json,struct
P=Path('work/input-v2');base=Path('work/responsive-cancels-v1/candidate.bin').read_bytes();rom=bytearray(base)
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(base)=='065f87ddd8ba76e64fde764d381463d1fb6da710fdd788f3364ddd02270549f9'
labels={k:int(v,16) for k,v in (l.split('=') for l in (P/'inputs.labels.txt').read_text().splitlines())};code=(P/'inputs.bin').read_bytes()
assert len(code)<0x1000 and set(base[0x3d3000:0x3d3000+len(code)])=={255}
rom[0x3d3000:0x3d3000+len(code)]=code
patches=[]
for address,label in [(0x3d0000,'frame_entry'),(0x9264,'matcher'),(0x922a,'history_direction'),(0x73f4,'round_reset')]:
 rom[address:address+6]=(b'\x4e\xb9' if address==0x73f4 else b'\x4e\xf9')+struct.pack('>I',labels[label]);patches.append((address,6))
exec(compile(Path('work/input-v2/relocate.py').read_text(encoding='utf8'),'relocate-mod-state','exec'),globals())
# Saltos voluntarios: altura 3/4 y paso temporal 3 en lugar de4.
for at in [0x1ee62,0x1ee6f,0x1ee7c,0x1ee89,0x1ee96,0x1eea3]:
 assert base[at:at+2].hex()=='0036'
 rom[at:at+2]=bytes.fromhex('002a');patches.append((at,2))
for at in range(0x13138,0x13164,2):
 value=int.from_bytes(base[at:at+2],'big')
 rom[at:at+2]=(value*3//4).to_bytes(2,'big')
patches.append((0x13138,0x2c))
struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
(P/'candidate.bin').write_bytes(rom)
preserved={n:base[a:z]==rom[a:z] for n,a,z in [('hits-tiles',0x3b4000,0x3b9000),('native-projectiles',0x123f2,0x1291e),('native-hit-dispatch',0x11d24,0x1216a),('damage-calculation',0x21b4e,0x21b54),('original-reactions',0x216ee,0x21a0e)]};assert all(preserved.values())
allowed=patches+[(r['address'],r['bytes']) for r in relocations]+[(0x18e,2),(0x3d3000,len(code))];assert all(any(a<=i<a+n for a,n in allowed) for i,(x,y) in enumerate(zip(base,rom)) if x!=y)
meta=dict(sourceSha256=sha(base),targetSha256=sha(rom),codeBytes=len(code),preserved=preserved,allowed=allowed,state='F710/F714 walk coast; F720/F730 Goku recognizer, separate from v1 F700..F70F',status='Internal candidate, runtime validation required')
(P/'build.json').write_text(json.dumps(meta,indent=2));print({k:v for k,v in meta.items() if k!='allowed'})

from pathlib import Path
import struct,hashlib,json
P=Path('work/meteor-impact');base=Path('work/gohan-hits/candidate.bin').read_bytes();r=bytearray(base);lab={k:int(v,16) for k,v in (s.split('=') for s in (P/'impact.labels.txt').read_text().splitlines())};code=(P/'impact.bin').read_bytes();assert set(base[0x3d8000:0x3d8000+len(code)])=={255};r[0x3d8000:0x3d8000+len(code)]=code
for a,name,old in [(0x7640,'main_pre','31fc0200e75a'),(0x7686,'main_pre','31fc0200e75a'),(0x3b035c,'event_entry','48e7fffe40e7')]:
 assert base[a:a+6].hex()==old,(hex(a),base[a:a+6].hex());r[a:a+6]=bytes.fromhex('4ef9')+struct.pack('>I',lab[name])
assert base[0x7240:0x7248].hex()=='42401039ffff5000';r[0x7240:0x7248]=bytes.fromhex('4eb9')+struct.pack('>I',lab['cue_entry'])+bytes.fromhex('4e71')
assert base[0x8d32:0x8d38].hex()=='4eb900007136';r[0x8d32:0x8d38]=bytes.fromhex('4eb9')+struct.pack('>I',lab['scroll'])
assert base[0x70:0x74].hex()=='0000723a';r[0x70:0x74]=struct.pack('>I',lab['hint'])
head='DBZ BUYUU V1.0 IMPACT 2026-11-06 16:25Z'
for a in [0x120,0x150]:r[a:a+48]=head.encode().ljust(48,b' ')
struct.pack_into('>H',r,0x18e,sum(struct.unpack('>'+str((len(r)-512)//2)+'H',r[512:]))&65535);(P/'candidate.bin').write_bytes(r);(P/'build.json').write_text(json.dumps(dict(buildId='20261106-172551',version='1.0',variant='meteor-impact',header=head,sha256=hashlib.sha256(r).hexdigest(),baseSha256=hashlib.sha256(base).hexdigest(),codeBytes=len(code)),indent=2));print(hashlib.sha256(r).hexdigest())

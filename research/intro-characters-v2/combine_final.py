from pathlib import Path
import json,struct,hashlib
p=Path('work/intro-characters');base=Path('outputs/intro-paleta-G-v6-1/Buyuu_Retsuden_Enhanced_v6_1.bin').read_bytes();rom=bytearray(base);used=[]
assert hashlib.sha256(base).hexdigest()=='5dbd8871d8d5d75694e7d14ff6da2f2003f0b32e239c84e037d4d562fe9769ca'
for component,path in [('body',p/'operations.json'),('font',p/'font-operations.json')]:
 d=json.loads(path.read_text());assert d['sourceSha256']==hashlib.sha256(base).hexdigest()
 for op in d['operations']:
  a=op['address'];b=bytes.fromhex(op['data'])
  if a==0x18e:continue
  assert all(not(a<x+len(y) and x<a+len(b)) for x,y in used),(component,hex(a))
  rom[a:a+len(b)]=b;used.append((a,b))
struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
out=Path('outputs/intro-personajes-v6-2');out.mkdir(parents=True,exist_ok=True);f=out/'Buyuu_Retsuden_Enhanced_v6_2.bin';f.write_bytes(rom)
report={'sourceSha256':hashlib.sha256(base).hexdigest(),'targetSha256':hashlib.sha256(rom).hexdigest(),'target':str(f),'bodySourceSha256':json.loads((p/'operations.json').read_text())['targetSha256'],'fontSourceSha256':json.loads((p/'font-operations.json').read_text())['targetSha256'],'operationRanges':[(hex(a),len(b)) for a,b in used],'gameplayCodeUnchanged':all(rom[a:z]==base[a:z] for a,z in [(0x7b000,0x7b400),(0x3e0000,0x3e0800)]),'scope':'Intro resources/pointers, body palette packing and native-height credit bitmap/map; no gameplay changes; background face approved, full-body and font review pending'}
(p/'combined.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))

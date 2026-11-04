from pathlib import Path
import json,hashlib,struct
R=Path('repository');P=Path('work/intro-body-refined');O=Path('outputs/intro-personajes-corregidos-v6-5');O.mkdir(parents=True,exist_ok=True)
base=Path('outputs/intro-contraste-anime-v6-4/Buyuu_Retsuden_Enhanced_v6_4.bin').read_bytes();rom=bytearray(base);d=json.loads((P/'operations.json').read_text())
for op in d['operations']:
 a=op['address'];b=bytes.fromhex(op['data'])
 if a!=0x18e:rom[a:a+len(b)]=b
struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
sha=lambda b:hashlib.sha256(b).hexdigest()
assert rom[0x1addb2:0x1addd2]==base[0x1addb2:0x1addd2]
assert rom[0x1ade32:0x1ade52]==base[0x1ade32:0x1ade52]
assert rom[0x3ca000:0x3ca040]==base[0x3ca000:0x3ca040]
(O/'Buyuu_Retsuden_Enhanced_v6_5.bin').write_bytes(rom)
p=(R/'patches/review-v6-4/enhanced-v6-4.ips').read_bytes();assert p[-6:-3]==b'EOF';p=bytearray(p[:-6]);i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 a=i
 while i<len(rom) and rom[i]!=base[i] and i-a<65535:i+=1
 p+=a.to_bytes(3,'big')+(i-a).to_bytes(2,'big')+rom[a:i]
p+=b'EOF'+len(rom).to_bytes(3,'big')
folder=R/'patches/review-v6-5';folder.mkdir(parents=True,exist_ok=True);(folder/'enhanced-v6-5.ips').write_bytes(p)
m={'source':{'sha256':'217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557','bytes':2097152},'baseReviewSha256':sha(base),'target':{'filename':'Buyuu_Retsuden_Enhanced_v6_5.bin','sha256':sha(rom),'bytes':len(rom)},'patch':{'path':'patches/review-v6-5/enhanced-v6-5.ips','sha256':sha(p)},'scope':'Restore intro lineup trouser/armor shading and readable Recoome skin. Keep user-approved warm-C Goku face and title, all combat changes. Native/user visual review pending.','inheritsGameplay':'patches/review-v3/manifest.json'}
(folder/'manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
print('v6.5',sha(rom))

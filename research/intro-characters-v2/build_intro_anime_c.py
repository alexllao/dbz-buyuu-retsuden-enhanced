from pathlib import Path
import struct,json,hashlib
R=Path('repository');O=Path('outputs/intro-contraste-anime-v6-4');O.mkdir(parents=True,exist_ok=True)
base=Path('outputs/intro-original-v6-3/Buyuu_Retsuden_Enhanced_v6_3.bin').read_bytes();rom=bytearray(base)
ops=[]
def put(a,d,label):rom[a:a+len(d)]=d;ops.append({'address':a,'data':bytes(d).hex(),'label':label})
body=json.loads((R/'src/intro/characters-v2/operations.json').read_text(encoding='utf-8'))
for op in body['operations']:
 if op['address']!=0x18e:put(op['address'],bytes.fromhex(op['data']),op['label'])
# Deterministic 16-color adaptation of selected concept C. Warm peach base,
# cream highlights, coral shadows, black outlines and stronger golden hair.
# These are real Mega Drive color words, not sampled AI-generated RGB pixels.
pal=[0x0000,0x0002,0x0642,0x0002,0x04ae,0x046c,0x0420,0x04a4,0x0068,0x0ace,0x08ae,0x0862,0x02ae,0x0262,0x08ee,0x0eee]
d=struct.pack('>16H',*pal)
put(0x1addb4,d[2:],'Opening warm-C Goku palette, keep original backdrop entry0')
put(0x1ade32,d,'Title warm-C Goku palette, same visible ramp as opening')
struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
sha=lambda b:hashlib.sha256(b).hexdigest()
checks={}
for key,a,z in [('battlePalettes',0x80064,0x80064+11*32),('stagePalettes',0x19e51e,0x19e51e+9*48),('controls',0x7b000,0x7b400),('sideSwitch',0x3e0000,0x3e0800),('creditResource',0x3f0000,0x3f0900),('titleBackgroundCopy',0x3ca000,0x3ca040),('titleBackgroundPointer',0x77b80,0x77b84)]:
 checks[key+'Unchanged']=rom[a:z]==base[a:z]
assert all(checks.values())
(O/'Buyuu_Retsuden_Enhanced_v6_4.bin').write_bytes(rom)
folder=R/'src/intro/anime-c-v1';folder.mkdir(parents=True,exist_ok=True)
(folder/'operations.json').write_text(json.dumps({'sourceSha256':sha(base),'targetSha256':sha(rom),'paletteWords':[f'{v:04X}' for v in pal],'operations':ops,'checks':checks,'scope':'Concept C adaptation in native palette words; body resources reuse audited battle-derived v6.2; native visual review pending'},indent=2)+'\n',encoding='utf-8')
p=(R/'patches/review-v6-3/enhanced-v6-3.ips').read_bytes();assert p[-6:-3]==b'EOF';p=bytearray(p[:-6]);i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 a=i
 while i<len(rom) and rom[i]!=base[i] and i-a<65535:i+=1
 p+=a.to_bytes(3,'big')+(i-a).to_bytes(2,'big')+rom[a:i]
p+=b'EOF'+len(rom).to_bytes(3,'big')
folder=R/'patches/review-v6-4';folder.mkdir(parents=True,exist_ok=True);(folder/'enhanced-v6-4.ips').write_bytes(p)
manifest={'source':{'sha256':'217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557','bytes':2097152},'baseReviewSha256':sha(base),'target':{'filename':'Buyuu_Retsuden_Enhanced_v6_4.bin','sha256':sha(rom),'bytes':len(rom)},'patch':{'path':'patches/review-v6-4/enhanced-v6-4.ips','sha256':sha(p)},'scope':'Warm anime-contrast C palette applied to opening and credit/title screen. Opening lineup uses battle-derived v6.2 resources. Battle palettes, stages, ki, gameplay and credits retained. Native visual review pending.','inheritsGameplay':'patches/review-v3/manifest.json'}
(folder/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('v6.4',sha(rom))

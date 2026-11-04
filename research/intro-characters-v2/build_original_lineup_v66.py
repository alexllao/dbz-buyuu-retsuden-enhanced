from pathlib import Path
import json,hashlib,struct
R=Path('repository');O=Path('outputs/intro-personajes-originales-v6-6');O.mkdir(parents=True,exist_ok=True)
base=Path('outputs/intro-personajes-corregidos-v6-5/Buyuu_Retsuden_Enhanced_v6_5.bin').read_bytes()
reference=Path('outputs/intro-original-v6-3/Buyuu_Retsuden_Enhanced_v6_3.bin').read_bytes()
original=Path('work/rom/original.bin').read_bytes();rom=bytearray(base);operations=[]
for op in json.loads((R/'src/intro/body-refined-v1/operations.json').read_text(encoding='utf-8'))['operations']:
 a=op['address'];n=len(bytes.fromhex(op['data']))
 if a==0x18e:continue
 rom[a:a+n]=reference[a:a+n];operations.append({'address':a,'bytes':n,'purpose':'Restore original intro lineup resource, pointer or palette'})
struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
checks={'originalBodyPaletteBanks':rom[0x1addd2:0x1ade32]==original[0x1addd2:0x1ade32]}
for a in [0x778be,0x778ee,0x77fd0,0x77fe8]:checks[f'originalPointer{a:X}']=rom[a:a+4]==original[a:a+4]
for name,a,z in [('openingGokuPalette',0x1addb2,0x1addd2),('titleGokuPalette',0x1ade32,0x1ade52),('credits',0x3f0000,0x3f0900),('titleBackground',0x3ca000,0x3ca040),('battlePalettes',0x80064,0x80064+11*32),('stagePalettes',0x19e51e,0x19e51e+9*48),('controls',0x7b000,0x7b400),('sideSwitch',0x3e0000,0x3e0800)]:checks[name+'Unchanged']=rom[a:z]==base[a:z]
assert all(checks.values());sha=lambda b:hashlib.sha256(b).hexdigest()
(O/'Buyuu_Retsuden_Enhanced_v6_6.bin').write_bytes(rom)
p=(R/'patches/review-v6-5/enhanced-v6-5.ips').read_bytes();assert p[-6:-3]==b'EOF';p=bytearray(p[:-6]);i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 a=i
 while i<len(rom) and rom[i]!=base[i] and i-a<65535:i+=1
 p+=a.to_bytes(3,'big')+(i-a).to_bytes(2,'big')+rom[a:i]
p+=b'EOF'+len(rom).to_bytes(3,'big')
folder=R/'patches/review-v6-6';folder.mkdir(parents=True,exist_ok=True);(folder/'enhanced-v6-6.ips').write_bytes(p)
m={'source':{'sha256':sha(original),'bytes':len(original)},'baseReviewSha256':sha(base),'target':{'filename':'Buyuu_Retsuden_Enhanced_v6_6.bin','sha256':sha(rom),'bytes':len(rom)},'patch':{'path':'patches/review-v6-6/enhanced-v6-6.ips','sha256':sha(p)},'scope':'Original full-body intro lineup restored. Warm-C large Goku face and title retained. Combat changes and both credits retained.','inheritsGameplay':'patches/review-v3/manifest.json'}
(folder/'manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
e=R/'evidence/intro-original-lineup-v6-6';e.mkdir(parents=True,exist_ok=True);(e/'restoration.json').write_text(json.dumps({'sourceSha256':sha(base),'targetSha256':sha(rom),'checks':checks,'operations':operations},indent=2)+'\n',encoding='utf-8')
print('v6.6',sha(rom))

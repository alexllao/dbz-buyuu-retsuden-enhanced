from pathlib import Path
import hashlib,json,struct
R=Path('repository');O=Path('outputs/intro-original-v6-3');O.mkdir(parents=True,exist_ok=True)
original=Path('work/rom/original.bin').read_bytes()
base=Path('outputs/intro-personajes-v6-2/Buyuu_Retsuden_Enhanced_v6_2.bin').read_bytes()
previous=Path('outputs/intro-paleta-G-v6-1/Buyuu_Retsuden_Enhanced_v6_1.bin').read_bytes()
rom=bytearray(base);ops=[]
# Undo body recomposition, including resource pointers, to keep original indexed
# artwork and original palettes together. Credit resources are independent.
for op in json.loads((R/'src/intro/characters-v2/operations.json').read_text(encoding='utf-8'))['operations']:
 a=op['address'];n=len(bytes.fromhex(op['data']))
 if a==0x18e:continue
 rom[a:a+n]=previous[a:a+n];ops.append({'address':a,'bytes':n,'purpose':'Undo v6.2 body recomposition'})
# Four opening banks plus title Goku bank. Restore full original words.
a=0x1addb2;n=160;rom[a:a+n]=original[a:a+n]
ops.append({'address':a,'bytes':n,'purpose':'Original opening and title palettes, all five banks'})
# Title copies 16 longwords from the tournament palette at 0x77B7E.
# Give this loader its own original 64-byte copy; combat keeps selected colors.
assert original[0x77b7e:0x77b84].hex()=='43f90019e51e'
rom[0x3ca000:0x3ca040]=original[0x19e51e:0x19e55e]
rom[0x77b80:0x77b84]=(0x3ca000).to_bytes(4,'big')
ops.extend([{'address':0x3ca000,'bytes':64,'purpose':'Original title background palette copy, isolated from combat'}, {'address':0x77b80,'bytes':4,'purpose':'Title-only palette source pointer'}])
struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
sha=lambda b:hashlib.sha256(b).hexdigest()
assert rom[a:a+n]==original[a:a+n]
for ptr in [0x778be,0x778ee,0x77fd0,0x77fe8]:assert rom[ptr:ptr+4]==original[ptr:ptr+4]
font=json.loads((R/'src/title/credit-v2/operations.json').read_text(encoding='utf-8'))
for op in font['operations']:
 p=op['address'];d=bytes.fromhex(op['data'])
 if p!=0x18e:assert rom[p:p+len(d)]==base[p:p+len(d)]
(O/'Buyuu_Retsuden_Enhanced_v6_3.bin').write_bytes(rom)
p=(R/'patches/review-v6-2/enhanced-v6-2.ips').read_bytes();assert p[-6:-3]==b'EOF';p=bytearray(p[:-6]);i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 start=i
 while i<len(rom) and rom[i]!=base[i] and i-start<65535:i+=1
 p+=start.to_bytes(3,'big')+(i-start).to_bytes(2,'big')+rom[start:i]
p+=b'EOF'+len(rom).to_bytes(3,'big')
folder=R/'patches/review-v6-3';folder.mkdir(parents=True,exist_ok=True);(folder/'enhanced-v6-3.ips').write_bytes(p)
manifest={'source':{'sha256':sha(original),'bytes':len(original)},'baseReviewSha256':sha(base),'target':{'filename':'Buyuu_Retsuden_Enhanced_v6_3.bin','sha256':sha(rom),'bytes':len(rom)},'patch':{'path':'patches/review-v6-3/enhanced-v6-3.ips','sha256':sha(p)},'scope':'Original opening and title palettes and original full-body resources restored. Bandai and ALEX LLAO credit retained. Gameplay and other visual changes retained.','inheritsGameplay':'patches/review-v3/manifest.json'}
(folder/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
e=R/'evidence/intro-original-v6-3';e.mkdir(parents=True,exist_ok=True)
(e/'restoration.json').write_text(json.dumps({'sourceSha256':sha(base),'targetSha256':sha(rom),'operations':ops,'checks':{'allFivePaletteBanksEqualOriginal':True,'allFourBodyResourcePointersEqualOriginal':True,'creditOperationsUnchanged':True,'gameplayCodeUnchanged':all(rom[a:z]==base[a:z] for a,z in [(0x7b000,0x7b400),(0x3e0000,0x3e0800)])}},indent=2)+'\n',encoding='utf-8')
print('Built v6.3',sha(rom))

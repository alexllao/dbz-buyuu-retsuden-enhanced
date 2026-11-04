from pathlib import Path
import json,struct,hashlib,shutil
p=Path('work/gameplay-review');base=Path('work/auras/colors-v4/candidate.bin').read_bytes();rom=bytearray((p/'candidate-v2.bin').read_bytes())
title=json.loads((p/'title-credits.json').read_text());knock=json.loads((p/'knockdown/candidate-build.json').read_text())
for op in title['patchOperations']:
 if op['address']!=0x18e:
  a=op['address'];d=bytes.fromhex(op['data']);assert rom[a:a+len(d)]==base[a:a+len(d)];rom[a:a+len(d)]=d
for op in knock['patches']:
 a=int(op['offset'],16)
 if a==0x18e:continue
 d=bytes.fromhex(op['after']);assert rom[a:a+len(d)]==bytes.fromhex(op['before']);rom[a:a+len(d)]=d
struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
out=Path('outputs/revision-jugabilidad-v2');out.mkdir(parents=True,exist_ok=True)
target=out/'Buyuu_Retsuden_Enhanced_v5.bin';target.write_bytes(rom)
patch=Path('repository/patches/auras-c2-v4/auras-c2.ips').read_bytes();assert patch[-6:-3]==b'EOF';patch=bytearray(patch[:-6]);ops=[];i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 start=i;i+=1
 while i<len(rom) and rom[i]!=base[i] and i-start<65535:i+=1
 d=bytes(rom[start:i]);patch.extend(start.to_bytes(3,'big')+len(d).to_bytes(2,'big')+d);ops.append({'address':start,'data':d.hex()})
patch.extend(b'EOF'+len(rom).to_bytes(3,'big'));(out/'Buyuu_Retsuden_Enhanced_v5.ips').write_bytes(patch)
shutil.copyfile(p/'title-credits-preserve-bandai.png',out/'Presentacion-G-ALEX-LLAO.png')
for f in (p/'knockdown').glob('Comparacion-*.mp4'):shutil.copyfile(f,out/f.name)
manifest={'source':{'sha256':hashlib.sha256(Path('work/rom/original.bin').read_bytes()).hexdigest(),'bytes':2097152},'target':{'filename':target.name,'sha256':hashlib.sha256(rom).hexdigest(),'bytes':len(rom)},'patch':{'path':'patches/review-v2/enhanced-v5.ips','sha256':hashlib.sha256(patch).hexdigest()},'components':['gameplay v2: native locomotion with original inertia; v1 basic recovery/input queue retained','ground knockdown A1 42->30 ticks; A4 54->30 ticks; A5 unchanged30','approved title G and - 2026 ALEX LLAO','character/stage colors v1 and Ki v4 without lightning'],'limits':['Manual feel remains for user review','No physical console validation','No new CPU autoplay; earlier comparison belongs to previous v4 build','HUD H4, selection portraits and stage10 still not integrated']}
(p/'combined-manifest.json').write_text(json.dumps(manifest,indent=2))
(p/'combined-operations.json').write_text(json.dumps(ops,indent=2))
(out/'Informe.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print(json.dumps(manifest['target']))

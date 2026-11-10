from pathlib import Path
import json,hashlib,shutil
P=Path('work/menu-japanese');R=Path('repository');O=Path('outputs/Selector-Namek-japones');sha=lambda b:hashlib.sha256(b).hexdigest()
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8',newline='\n')
m=json.loads((P/'build.json').read_text(encoding='utf-8'));base=Path('work/combo-charge-all/candidate.bin').read_bytes();rom=(P/'candidate.bin').read_bytes();assert sha(rom)==m['targetSha256'] and sha(base)==m['sourceSha256']
for path in [P/'validation.json',P/'validation-modes.json',O/'procedencia.json']:assert json.loads(path.read_text())['romSha256']==sha(rom)
patch=bytearray(b'PATCH');i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 start=i
 while i<len(rom) and rom[i]!=base[i] and i-start<65535:i+=1
 patch+=start.to_bytes(3,'big')+(i-start).to_bytes(2,'big')+rom[start:i]
patch+=b'EOF'+len(rom).to_bytes(3,'big')
bid=m['buildId'];pn=f'Selector-japones-sobre-cargas-combo-build-{bid}.ips';pp=R/'patches/menu-japanese'/pn;pp.parent.mkdir(parents=True,exist_ok=True);pp.write_bytes(patch);cp(pp,O/pn)
verify=bytearray(base);pos=5
while patch[pos:pos+3]!=b'EOF':
 at=int.from_bytes(patch[pos:pos+3],'big');n=int.from_bytes(patch[pos+3:pos+5],'big');pos+=5;assert n;verify[at:at+n]=patch[pos:pos+n];pos+=n
assert verify==rom
name=f'DBZ_Enhanced_v1.0_Namek_JP_build_{bid}.bin';cp(P/'candidate.bin',O/name)
manifest=dict(version='1.0',buildId=bid,source=dict(build='20261110-120502',sha256=sha(base)),target=dict(filename=name,sha256=sha(rom),bytes=len(rom)),patch=dict(path=pp.relative_to(R).as_posix(),sha256=sha(patch),scope='Delta against combo-charge build 20261110-120502, not original retail ROM'),changes='Japanese native-font names for the three extra Namek stages; combat and stage graphics unchanged',userVisualReviewPending=True)
write(R/'patches/menu-japanese/manifest.json',json.dumps(manifest,indent=2)+'\n');write(O/'version.json',json.dumps(manifest,indent=2)+'\n')
write(O/'LEEME.txt',f'v1.0 build {bid}. Selector de los tres Namek extra con nombres y fuente japoneses originales. Conserva R10 y las cargas minimas en combo del build 120502.\nArrancar desde cero; no cargar estados de otra version. El IPS solo se aplica al build 20261110-120502.\n')
for n in ['build.py','capture.py','validate.py','validate-modes.py','package.py']:cp(P/n,R/'research/menu-japanese'/n)
for n in ['build.json','validation.json','validation-modes.json']:cp(P/n,R/'evidence/menu-japanese'/n)
cp(O/'procedencia.json',R/'evidence/menu-japanese/captures.json')
for slug in ['original','normal','aldea','porunga']:cp(O/(slug+'.png'),R/'assets/media/menu-japanese'/(slug+'.png'))
print('PACKAGED',bid,sha(rom),name)

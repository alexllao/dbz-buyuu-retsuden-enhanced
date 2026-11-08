from pathlib import Path
import json,hashlib,shutil,gzip,zipfile
P=Path('work/barrage-five');R=Path('repository');O=Path('outputs/rafaga-cinco-Goku');sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf8',newline='\n')
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
m=json.loads((P/'build.json').read_text());rom=(P/'candidate.bin').read_bytes();base=Path('work/knockdown-k4/candidate.bin').read_bytes();assert sha(rom)==m['targetSha256'];validation=json.loads((P/'validation-after.json').read_text());assert validation['passed'] and validation['romSha256']==sha(rom) and len(validation['cases'])==32
assert json.loads((P/'extra-before.json').read_text())==json.loads((P/'extra-after.json').read_text())
assert rom[0x1f39f:0x1f3d8]==base[0x1f39f:0x1f3d8] and rom[0x1f4b3:0x1f4d7]==base[0x1f4b3:0x1f4d7]
patch=bytearray(next((R/'patches/knockdown-k4').glob('*.ips')).read_bytes());assert patch[-6:-3]==b'EOF';patch=patch[:-6];i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 start=i
 while i<len(rom) and rom[i]!=base[i] and i-start<65535:i+=1
 patch+=start.to_bytes(3,'big')+(i-start).to_bytes(2,'big')+rom[start:i]
patch+=b'EOF'+len(rom).to_bytes(3,'big');bid=m['buildId'];filename=f'DBZ_Enhanced_v1.0_K4_Goku_5_disparos_build_{bid}.bin';patchname=f'Goku-5-disparos-build-{bid}.ips';pp=R/'patches/barrage-five'/patchname;pp.parent.mkdir(parents=True,exist_ok=True);pp.write_bytes(patch)
manifest=dict(version='1.0',variant='Goku five-shot barrage on approved K4',buildId=bid,headerTitle=m['headerTitle'],source=dict(sha256='217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557',bytes=2097152),target=dict(filename=filename,sha256=sha(rom),bytes=len(rom)),patch=dict(path=pp.relative_to(R).as_posix(),sha256=sha(patch)),experimental=True,userApprovalPending=True)
write(R/'patches/barrage-five/manifest.json',json.dumps(manifest,indent=2)+'\n')
for n in ['build.json','validation-before.json','validation-after.json','energy.json','video-cases.json']:cp(P/n,R/'evidence/barrage-five'/n)
for f in P.glob('test-after-*.json'):(R/'evidence/barrage-five'/(f.stem+'.json.gz')).write_bytes(gzip.compress(f.read_bytes(),mtime=0))
summary=dict(passed=True,romSha256=sha(rom),casesAfter=32,casesBefore=32,energyCases=5,extraTracesIdentical=['Goku Kamehameha','Goku standing punch','Vegeta standing kick'],k4ReactionDataIdentical=True,fiveShotsAreNativeProjectiles=True,fullBarrageNominalKiCost=60,hitDamageScale='3/5 after native defense calculation, before downstream native modifiers',maximumObservedDamage=30,gameplayVideoSpeedScaling=False,limits=['Five impacts confirmed at distances32/64/120 in both ports/directions; at180+ some projectiles miss.','P2 facing right at240/360 is invalidated by the native camera boundary; it also misses in baseline.','Holding A does not repeat the barrage in the bounded test; no exhaustive infinite/combo-balance proof.','Throw plus barrage at tested delay48 misses; no guaranteed aerial conversion implemented.','Technique animation lasts about0.45s longer overall despite shorter shot intervals.','Normal-speed emulator only; hardware/turbo and other characters not integrated.'])
write(R/'evidence/barrage-five/summary.json',json.dumps(summary,indent=2)+'\n')
for n in ['helpers.asm','helpers.listing.txt','helpers.labels.txt','build.py','test.py','energy.py','extra.py','probe.py','record.py','record-far.py','edit.py','package.py','assemble.ps1']:cp(P/n,R/'research/barrage-five'/n)
write(R/'research/barrage-five/helpers.hex',(P/'helpers.bin').read_bytes().hex()+'\n');cp(Path('work/scripts/AssembleBarrage.java'),R/'research/barrage-five/AssembleBarrage.java')
cp(O/'Goku-rafaga-3-vs-5-comparacion.mp4',R/'assets/media/barrage-five/comparacion.mp4');cp(O/'comparacion.png',R/'assets/media/barrage-five/captura.png');cp(P/'candidate.bin',O/filename);cp(pp,O/patchname);write(O/'version.json',json.dumps(manifest,indent=2)+'\n');write(O/'LEEME.txt',f'Prueba Goku 5 disparos sobre K4 aprobada. v1.0 build {bid}.\nComando: abajo, diagonal abajo-delante, delante + A.\n5 proyectiles; 60 ki nominales en total. Cerca pueden conectar los cinco; lejos no se garantizan.\nArrancar desde cero, velocidad normal, sin estados de otras ROM.\n')
with zipfile.ZipFile(O/'ROM-prueba-Goku-5-disparos-sobre-K4.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in [O/filename,O/patchname,O/'version.json',O/'LEEME.txt']:z.write(f,f.name)
print('Packaged',bid,sha(rom))

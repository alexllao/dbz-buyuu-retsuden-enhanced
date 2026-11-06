from pathlib import Path
import json,hashlib,shutil,zipfile
P=Path('work/gravity-g2');R=Path('repository');O=Path('outputs/saltos-gravedad-G2');sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf8',newline='\n')
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
m=json.loads((P/'build.json').read_text());rom=(P/'candidate.bin').read_bytes();base=Path('work/gohan-hits/candidate.bin').read_bytes();assert sha(rom)==m['sha256'];patch=bytearray((R/'patches/release-v1-0-build-20261106-124607/DBZ-Enhanced-v1.0-build-20261106-124607.ips').read_bytes());assert patch[-6:-3]==b'EOF';patch=patch[:-6];i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 start=i
 while i<len(rom) and rom[i]!=base[i] and i-start<65535:i+=1
 patch+=start.to_bytes(3,'big')+(i-start).to_bytes(2,'big')+rom[start:i]
patch+=b'EOF'+len(rom).to_bytes(3,'big');patchpath=R/'patches/gravity-g2/DBZ-Enhanced-v1.0-G2-build-20261106-164956.ips';patchpath.parent.mkdir(parents=True,exist_ok=True);patchpath.write_bytes(patch)
filename='DBZ_Buyuu_Retsuden_Enhanced_v1.0_G2_build_20261106-164956.bin'
manifest=dict(version='1.0',variant='G2 - prueba solo Goku',buildId=m['buildId'],headerTitle=m['header'],source=dict(sha256='217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557',bytes=2097152),target=dict(filename=filename,sha256=sha(rom),bytes=len(rom)),patch=dict(path=patchpath.relative_to(R).as_posix(),sha256=sha(patch)),experimental=True)
write(R/'patches/gravity-g2/manifest.json',json.dumps(manifest,indent=2)+'\n');cp(O/'Goku-G2-saltos-antes-despues.mp4',R/'assets/media/gravity-g2/comparacion.mp4');cp(O/'comparacion.png',R/'assets/media/gravity-g2/captura.png')
cases=[]
for port in [1,2]:cases+=json.loads((P/f'validation-port{port}.json').read_text())
assert len(cases)==20 and all(t['landed'] for t in cases)
evidence=dict(passed=True,sha256=sha(rom),scope='Goku only',cases=cases,baseline=json.loads(Path('work/gravity-probe/dash-fix-0-summary.json').read_text()),trial=json.loads((P/'G2-0-summary.json').read_text()),video=dict(path='assets/media/gravity-g2/comparacion.mp4',sha256=sha((O/'Goku-G2-saltos-antes-despues.mp4').read_bytes())),limitations=['Normal speed in emulator, not turbo or hardware.','Comparison begins from compatible deterministic snapshots; validation20cases uses fresh boot in each player port.','Piccolo Meteor unchanged from124607; G1 trial did not convince user.','Shared dash fix retained in both sides. No default ROM changed.'])
write(R/'evidence/gravity-g2/validation.json',json.dumps(evidence,indent=2)+'\n')
for f in P.glob('*.json'):cp(f,R/'evidence/gravity-g2'/f.name)
for f in P.glob('*.py'):cp(f,R/'research/gravity-g2'/f.name)
for n in ['gravity.asm','gravity.labels.txt','gravity.listing.txt']:cp(P/n,R/'src/gameplay/gravity-g2'/n)
write(R/'src/gameplay/gravity-g2/gravity.hex',(P/'gravity.bin').read_bytes().hex()+'\n')
cp(P/'candidate.bin',O/filename);write(O/'version.json',json.dumps(manifest,indent=2)+'\n');write(O/'LEEME.txt','Prueba G2 SOLO GOKU. v1.0 build20261106-164956.\nSalto normal mas bajo y corto; carrera con salto mas alto, misma duracion y recorrido.\nPiccolo Meteor conserva version anterior124607. No cambia la version principal.\nArrancar desde cero, velocidad normal, sin estados anteriores.\n')
with zipfile.ZipFile(O/'ROM-prueba-G2-Goku.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in [O/filename,O/'version.json',O/'LEEME.txt']:z.write(f,f.name)
print('G2 package',sha(rom))

from pathlib import Path
import json,hashlib,shutil,gzip,zipfile
P=Path('work/combo-startup');R=Path('repository');O=Path('outputs/Especiales-rapidos-en-combo');sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(exist_ok=True,parents=True);p.write_text(s,encoding='utf-8')
def cp(a,b):b.parent.mkdir(exist_ok=True,parents=True);shutil.copyfile(a,b)
m=json.loads((P/'build.json').read_text());rom=(P/'candidate.bin').read_bytes();base=Path('work/input-links/candidate.bin').read_bytes();assert sha(rom)==m['targetSha256']
a=json.loads((P/'matrix/before.json').read_text());b=json.loads((P/'matrix/after.json').read_text());assert len(a['cases'])==len(b['cases'])==168 and b['romSha256']==sha(rom)
key=lambda t:(t['cid'],t['port'],t['side'],t['context'],t['speed']);assert [key(t) for t in a['cases']]==[key(t) for t in b['cases']]
assert all(x['damage']==y['damage'] and (x['accepted'] is None)==(y['accepted'] is None) for x,y in zip(a['cases'],b['cases']))
assert all(not t['fastUsed'] for t in b['cases'] if t['context'] in ['solo','guard','whiff','late'])
assert all(t['returnedToIdle'] for t in b['cases']);assert sum(t['fastUsed'] for t in b['cases'])==32
inputs=json.loads((P/'input-matrix.json').read_text());assert len(inputs)==200 and all(t['ok'] for t in inputs)
neg=json.loads((P/'negative-checks.json').read_text());assert neg['romSha256']==sha(rom) and all(t['passed'] for t in neg['cases'])
assert all(t['meteor'] for t in json.loads((P/'chords.json').read_text()));assert len(json.loads((P/'extra-runtime.json').read_text()))==5
repeat=json.loads((P/'repeated-cast.json').read_text());assert len(repeat)==2 and all(t['firstFast'] and not t['secondSoloFast'] for t in repeat)
for at,z in [(0x1eb26,0x20500),(0x123f2,0x1291e),(0x216ee,0x21b54),(0x3d0000,0x3df000),(0x7b190,0x7b278)]:assert rom[at:z]==base[at:z] or at==0x3d0000 and rom[at:z]==base[at:z]
patch=bytearray(next((R/'patches/input-links').glob('*.ips')).read_bytes());assert patch[-6:-3]==b'EOF';patch=patch[:-6];i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 start=i
 while i<len(rom) and rom[i]!=base[i] and i-start<65535:i+=1
 patch+=start.to_bytes(3,'big')+(i-start).to_bytes(2,'big')+rom[start:i]
patch+=b'EOF'+len(rom).to_bytes(3,'big');bid=m['buildId'];name=f'DBZ_Enhanced_v1.0_Especiales_en_combo_build_{bid}.bin';pn=f'Especiales-en-combo-build-{bid}.ips';pp=R/'patches/combo-startup'/pn;pp.parent.mkdir(exist_ok=True);pp.write_bytes(patch)
manifest=dict(version='1.0',buildId=bid,headerTitle=m['headerTitle'],variant='Gohan Masenko and Vegeta Final Flash: shorter preparation after confirmed combo only',source=json.loads((R/'patches/input-links/manifest.json').read_text())['source'],target=dict(filename=name,bytes=len(rom),sha256=sha(rom)),patch=dict(path=pp.relative_to(R).as_posix(),sha256=sha(patch)),experimental=True,userApprovalPending=True)
write(R/'patches/combo-startup/manifest.json',json.dumps(manifest,indent=2)+'\n')
E=R/'evidence/combo-startup';E.mkdir(exist_ok=True)
for n in ['build.json','before-probe.json','after-probe.json','input-matrix.json','negative-checks.json','chords.json','repeated-cast.json']:cp(P/n,E/n)
cp(P/'matrix/before.json',E/'matrix-before.json');cp(P/'matrix/after.json',E/'matrix-after.json')
for v in ['before','after']:cp(P/f'video/{v}/metrics.json',E/f'video-{v}.json')
for f in (P/'matrix').glob('after-*.json'):(E/(f.stem+'.json.gz')).write_bytes(gzip.compress(f.read_bytes(),mtime=0))
(E/'extra-runtime.json.gz').write_bytes(gzip.compress((P/'extra-runtime.json').read_bytes(),mtime=0))
soloDeltas=[y['startup']-x['startup'] for x,y in zip(a['cases'],b['cases']) if x['context']=='solo' and x['startup'] is not None and y['startup'] is not None]
kiDiff=[dict(case=key(x),before=x['kiDebits'],after=y['kiDebits']) for x,y in zip(a['cases'],b['cases']) if x['kiDebits']!=y['kiDebits']]
summary=dict(romSha256=sha(rom),buildId=bid,casesEach=168,damageDifferences=0,lostStarts=0,fastCases=32,soloGuardWhiffLateFastCases=0,soloFrameDeltaRange=[min(soloDeltas),max(soloDeltas)],kiTraceDifferences=kiDiff,nominalKiCostTablesUntouched=True,projectileAndDamageCodeUntouched=True,releaseAnimationUnitUntouched=True,inputCasesPassed=200,meteorChordsPassed=10,negativeSelectionPassed=7,extraRuntimeChecks=5,repeatedCastChecks=repeat,scope='Two human characters, normal speed. No new hitstun or guaranteed combo certification. Prototype pending gamepad review.')
write(E/'validation.json',json.dumps(summary,indent=2)+'\n')
for n in ['startup.asm','startup.labels.txt','startup.listing.txt','prepare.py','build.py','probe.py','matrix.py','record.py','edit.py','regression.py','repeat.py','analyze.py','inspect.py','package.py','assemble.ps1']:cp(P/n,R/'research/combo-startup'/n)
write(R/'research/combo-startup/startup.hex',(P/'startup.bin').read_bytes().hex()+'\n');cp(Path('work/scripts/AssembleComboStartup.java'),R/'research/combo-startup/AssembleComboStartup.java')
cp(O/'Gohan-Vegeta-especiales-en-combo-antes-despues.mp4',R/'assets/media/combo-startup/comparacion.mp4');cp(O/'comparacion.png',R/'assets/media/combo-startup/comparacion.png')
cp(P/'candidate.bin',O/name);cp(pp,O/pn);write(O/'version.json',json.dumps(manifest,indent=2));write(O/'LEEME.txt',f'v1.0 build {bid}. PRUEBA: Masenko de Gohan y Final Flash de Vegeta con preparacion abreviada al empezar dentro de una cadena confirmada.\nSueltos usan tablas nativas; no cambia velocidad del proyectil, dano o comandos.\nConserva K4, seis rafagas, correccion de lanzamiento, basicos y buffer de Goku.\nArrancar desde cero, sin estados de otra version. Pendiente de valorar con mando.\n')
with zipfile.ZipFile(O/'ROM-prueba-especiales-rapidos-en-combo.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in [O/name,O/pn,O/'version.json',O/'LEEME.txt']:z.write(f,f.name)
print('Packaged',bid,sha(rom),summary['soloFrameDeltaRange'])

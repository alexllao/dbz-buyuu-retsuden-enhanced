from pathlib import Path
import json,hashlib,gzip,shutil,zipfile
P=Path('work/barrage-roster');R=Path('repository');O=Path('outputs/rafagas-cinco-plantel');sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf8',newline='\n')
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
m=json.loads((P/'build.json').read_text());rom=(P/'candidate.bin').read_bytes();base=Path('work/knockdown-k4/candidate.bin').read_bytes();assert sha(rom)==m['targetSha256'];cases=[]
for port in ['port1','port2']:
 before=json.loads((P/port/'validation-before.json').read_text());after=json.loads((P/port/'validation-after.json').read_text());assert before['passed'] and after['passed'] and after['romSha256']==sha(rom) and len(after['cases'])==60
 for a,b in zip(before['cases'],after['cases']):
  assert all(a[k]==b[k] for k in ['cid','facing','distance','mode']);assert len(a['shots'])==3 and len(b['shots'])==5 and b['returned'];assert not any(x['previousType'] in [32,33] for x in b['shots'])
  if b['distance']==120 and b['mode']=='hit':assert b['maxHits']==5 and len(b['events'])==5 and sum(x['damage'] for x in b['events'])<=sum(x['damage'] for x in a['events'])
  if b['mode']=='guard':assert b['maxHits']==0
  cases.append(dict(port=port,reference=a,trial=b))
assert len(cases)==120
assert json.loads((P/'extra-before.json').read_text())==json.loads((P/'extra-after.json').read_text())
assert rom[0x1f39f:0x1f3d8]==base[0x1f39f:0x1f3d8] and rom[0x1f4b3:0x1f4d7]==base[0x1f4b3:0x1f4d7]
patch=bytearray(next((R/'patches/knockdown-k4').glob('*.ips')).read_bytes());assert patch[-6:-3]==b'EOF';patch=patch[:-6];i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 start=i
 while i<len(rom) and rom[i]!=base[i] and i-start<65535:i+=1
 patch+=start.to_bytes(3,'big')+(i-start).to_bytes(2,'big')+rom[start:i]
patch+=b'EOF'+len(rom).to_bytes(3,'big');bid=m['buildId'];filename=f'DBZ_Enhanced_v1.0_K4_Rafagas_6_personajes_build_{bid}.bin';patchname=f'Rafagas-6-personajes-build-{bid}.ips';pp=R/'patches/barrage-roster'/patchname;pp.parent.mkdir(parents=True,exist_ok=True);pp.write_bytes(patch)
manifest=dict(version='1.0',variant='Five native shots for Goku Vegeta Cell A18 Krilin Recoome on K4',buildId=bid,headerTitle=m['headerTitle'],source=dict(sha256='217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557',bytes=2097152),target=dict(filename=filename,sha256=sha(rom),bytes=len(rom)),patch=dict(path=pp.relative_to(R).as_posix(),sha256=sha(patch)),experimental=True,userApprovalPending=True)
write(R/'patches/barrage-roster/manifest.json',json.dumps(manifest,indent=2)+'\n');write(R/'evidence/barrage-roster/validation.json',json.dumps(dict(passed=True,romSha256=sha(rom),referenceCases=120,trialCases=120,cases=cases,k4DataUnchanged=True,otherSampledTechniquesIdentical=True,newMovesAdded=[],newGraphicsAdded=[],limits=['Grounded normal-speed emulator fixtures only.','Other-plane test is a fixture; no broad aerial conversion was implemented.','Farther distances can lose impacts; damage depends on rival and integer rounding.','Bounded defense tests do not prove absence of infinite pressure.','No exhaustive turbo/hardware/other-technique regression audit.']),indent=2)+'\n')
cp(P/'build.json',R/'evidence/barrage-roster/build.json');cp(P/'video-cases.json',R/'evidence/barrage-roster/video-cases.json')
for port in ['port1','port2']:
 for f in (P/port).glob('trace-after-*.json'):(R/'evidence/barrage-roster'/(port+'-'+f.stem+'.json.gz')).write_bytes(gzip.compress(f.read_bytes(),mtime=0))
for n in ['prepare.py','helpers.asm','helpers.listing.txt','helpers.labels.txt','build.py','test.py','seeds.py','extra.py','record.py','edit.py','package.py','assemble.ps1']:cp(P/n,R/'research/barrage-roster'/n)
write(R/'research/barrage-roster/helpers.hex',(P/'helpers.bin').read_bytes().hex()+'\n');cp(O/'Rafagas-3-vs-5-seis-personajes.mp4',R/'assets/media/barrage-roster/comparacion.mp4');cp(O/'comparacion.png',R/'assets/media/barrage-roster/captura.png');cp(P/'candidate.bin',O/filename);cp(pp,O/patchname);write(O/'version.json',json.dumps(manifest,indent=2)+'\n');write(O/'LEEME.txt',f'v1.0 K4 + rafagas de cinco, seis personajes. Build {bid}.\nGoku: abajo, diagonal abajo-delante, delante + A.\nVegeta, Cell, A18, Krilin y Recoome: comando original, mantener abajo y abajo-diagonal atras-atras + A.\nNo se anade un movimiento ni comando nuevo. Otros personajes sin ampliar.\nK4 conservada; propuesta de rafagas pendiente de valoracion. Arrancar desde cero, normal, sin estados antiguos.\n')
with zipfile.ZipFile(O/'ROM-prueba-rafagas-cinco-6-personajes-K4.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in [O/filename,O/patchname,O/'version.json',O/'LEEME.txt']:z.write(f,f.name)
print('Packaged',bid,sha(rom),len(cases))

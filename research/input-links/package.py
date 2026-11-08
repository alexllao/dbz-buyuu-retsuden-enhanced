from pathlib import Path
import json,hashlib,shutil,zipfile,gzip
P=Path('work/input-links');R=Path('repository');O=Path('outputs/Buffer-enlaces-v1');sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
m=json.loads((P/'build.json').read_text());rom=(P/'candidate.bin').read_bytes();base=Path('work/basic-chains/candidate.bin').read_bytes();assert sha(rom)==m['targetSha256']
a=json.loads((P/'before-matrix.json').read_text());b=json.loads((P/'after-matrix.json').read_text());assert len(a)==len(b)==180 and sum(t['started'] for t in a)==160 and all(t['started'] for t in b)
assert all(not x['started'] or y['started'] for x,y in zip(a,b))
inputs=json.loads((P/'input-matrix.json').read_text());assert len(inputs)==200 and all(t['ok'] for t in inputs)
assert all(t['meteor'] for t in json.loads((P/'chords.json').read_text()))
neg=json.loads((P/'negative-checks.json').read_text());assert neg['romSha256']==sha(rom) and all(t['passed'] for t in neg['cases'])
assert all(not t['specialStarted'] and t['queueExpired'] for t in json.loads((P/'negative-links.json').read_text()))
limits=json.loads((P/'after-limits.json').read_text());oldlimits=json.loads(Path('work/basic-chains/after-limits.json').read_text());assert limits['romSha256']==sha(rom) and limits['otherCharacters']==oldlimits['otherCharacters']
sig=lambda t:(t['mode'],len(t['contacts']),t['damage'],t['maxHits'],len(t['assistedStarts']))
assert [sig(t) for t in limits['cases']]==[sig(t) for t in oldlimits['cases']]
for port in ['port1','port2']:
 d=json.loads((P/port/'validation-after.json').read_text());assert d['passed'] and d['romSha256']==sha(rom) and len(d['cases'])==48
guard=[]
for speed in [2,3,4,5,6]:
 r=json.loads((P/f'guard-kame-{speed}.json').read_text());guard.append(dict(speed=speed,started=any(t['p']['program']==0xc04 for t in r),damage=r[0]['e']['hp']-r[-1]['e']['hp'],maxHits=max(t['p']['hits'] for t in r)))
assert next(t for t in guard if t['speed']==4)['maxHits']==3
for at,z in [(0x13138,0x13164),(0x1f8ba,0x2025c),(0x21b4e,0x21b54),(0x216ee,0x21a0e),(0x3da200,0x3dd800)]:assert rom[at:z]==base[at:z]
patch=bytearray(next((R/'patches/basic-chains').glob('*.ips')).read_bytes());assert patch[-6:-3]==b'EOF';patch=patch[:-6];i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 start=i
 while i<len(rom) and rom[i]!=base[i] and i-start<65535:i+=1
 patch+=start.to_bytes(3,'big')+(i-start).to_bytes(2,'big')+rom[start:i]
patch+=b'EOF'+len(rom).to_bytes(3,'big');bid=m['buildId'];name=f'DBZ_Enhanced_v1.0_Buffer_enlaces_build_{bid}.bin';pn=f'Buffer-enlaces-build-{bid}.ips';pp=R/'patches/input-links'/pn;pp.parent.mkdir(exist_ok=True);pp.write_bytes(patch)
manifest=dict(version='1.0',buildId=bid,variant='Goku recognized-special recovery buffer; 6 recognizer updates',source=json.loads((R/'patches/basic-chains/manifest.json').read_text())['source'],target=dict(filename=name,sha256=sha(rom),bytes=len(rom)),patch=dict(path=pp.relative_to(R).as_posix(),sha256=sha(patch)),experimental=True,userApprovalPending=True)
write(R/'patches/input-links/manifest.json',json.dumps(manifest,indent=2)+'\n')
E=R/'evidence/input-links';E.mkdir(exist_ok=True)
for n in ['build.json','before-matrix.json','after-matrix.json','input-matrix.json','negative-checks.json','negative-links.json','chords.json','charge-double.json','after-limits.json']:cp(P/n,E/n)
for n in ['extra-runtime.json','before-critical-trace.json','after-critical-trace.json']:(E/(n+'.gz')).write_bytes(gzip.compress((P/n).read_bytes(),mtime=0))
for port in ['port1','port2']:cp(P/port/'validation-after.json',E/(port+'-basics.json'))
report=dict(romSha256=sha(rom),buildId=bid,finisherStarts=dict(before=160,after=180,casesEach=180,regressions=0,matchup='Goku vs Goku, normal speed, high ki, neutral rival, 2 ports x 2 facing x 5 rhythms x 3 delays x 3 techniques'),inputCasesPassed=200,meteorChordsPassed=10,negativeSelectionPassed=7,chargeChoices=2,extraChecks=5,basicsPassed=96,limitsPreserved=True,otherTenCharactersDamageHitsPreserved=True,guardAfterThird=guard,protectedTablesPreserved=True,remaining=['Kamehameha at5frames/direction afterAAB vsVegeta still fails in the separate trace. Not all transitions are fixed.','No hardware/turbo/full matchup certification; no universal no-infinites claim.','A started finisher is not necessarily an unavoidable combo.'])
write(E/'validation.json',json.dumps(report,indent=2)+'\n')
for n in ['inputs.asm','inputs.labels.txt','inputs.listing.txt','assemble.ps1','build.py','matrix.py','regression.py','basic-regression.py','trace-link.py','guarded-link.py','negative-links.py','record.py','edit.py','seed.py','package.py']:cp(P/n,R/'research/input-links'/n)
write(R/'research/input-links/inputs.hex',(P/'inputs.bin').read_bytes().hex()+'\n');cp(Path('work/scripts/AssembleInputLinks.java'),R/'research/input-links/AssembleInputLinks.java');cp(Path('work/control-audit/prepare-fix.py'),R/'research/input-links/prepare-fix.py')
cp(O/'Buffer-Kamehameha-antes-despues.mp4',R/'assets/media/input-links/comparacion.mp4');cp(O/'comparacion.png',R/'assets/media/input-links/comparacion.png');cp(P/'video/metrics.json',E/'video.json')
cp(P/'candidate.bin',O/name);cp(pp,O/pn);write(O/'version.json',json.dumps(manifest,indent=2));write(O/'LEEME.txt',f'v1.0 build {bid}. Buffer breve de especiales reconocidos al terminar basicos de Goku.\nConserva K4, seis rafagas, correccion del lanzamiento y variantes de basicos.\nNo incluye el ensayo pendiente de dos saltos. No todos los enlaces son combos inevitables.\nPrueba pendiente de valorar con mando. Arrancar desde cero, sin estados de otra version.\n')
with zipfile.ZipFile(O/'ROM-prueba-buffer-enlaces.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in [O/name,O/pn,O/'version.json',O/'LEEME.txt']:z.write(f,f.name)
print('Packaged',bid,sha(rom),guard)

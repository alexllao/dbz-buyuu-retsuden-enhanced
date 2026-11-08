from pathlib import Path
import json,hashlib,gzip,shutil,zipfile
P=Path('work/jump-two');R=Path('repository');O=Path('outputs/Goku-dos-saltos');sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf8',newline='\n')
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
m=json.loads((P/'build.json').read_text());rom=(P/'candidate.bin').read_bytes();base=Path('work/barrage-roster/candidate.bin').read_bytes();target=next(x for x in m['variants'] if x['variant']=='candidate');assert sha(rom)==target['sha256'];checks={}
for variant in ['control','candidate']:
 d=json.loads((P/f'validation-{variant}.json').read_text());assert d['passed'] and len(d['cases'])==40 and d['romSha256']==sha((P/f'{variant}.bin').read_bytes());checks[variant]=d
for t in checks['candidate']['cases']:
 if t['mode'] in ['vertical','forward','backward']:assert 59<=t['height']<=62 and t['airFrames']<=26
 if t['mode'] in ['running','backrun']:assert t['run'] and 85<=t['height']<=88
others=[]
for cid in [1,2,3,5,6,7,9]:
 a=json.loads((P/f'other-control-{cid}.json').read_text());b=json.loads((P/f'other-candidate-{cid}.json').read_text());key=lambda x:(x['p']['program'],x['p']['cursor'],x['p']['x'],x['p']['y']);pathA=list(dict.fromkeys(map(key,a)));pathB=list(dict.fromkeys(map(key,b)));assert pathA==pathB;others.append(dict(cid=cid,fullTraceIdentical=a==b,uniqueMotionSequenceIdentical=True))
rafagas=json.loads((P/'port1/validation-after-quick.json').read_text());assert rafagas['passed'] and rafagas['romSha256']==sha(rom) and len(rafagas['cases'])==6 and all(x['maxHits']==5 for x in rafagas['cases'])
for a,n in [(0x1f39f,0x39),(0x1f4b3,0x24),(0x3da200,0x400),(0x3db000,0x400)]:assert rom[a:a+n]==base[a:a+n]
patch=bytearray(next((R/'patches/barrage-roster').glob('*.ips')).read_bytes());assert patch[-6:-3]==b'EOF';patch=patch[:-6];i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 start=i
 while i<len(rom) and rom[i]!=base[i] and i-start<65535:i+=1
 patch+=start.to_bytes(3,'big')+(i-start).to_bytes(2,'big')+rom[start:i]
patch+=b'EOF'+len(rom).to_bytes(3,'big');bid=m['buildId'];filename=f'DBZ_Enhanced_v1.0_Goku_dos_saltos_build_{bid}.bin';patchname=f'Goku-dos-saltos-build-{bid}.ips';pp=R/'patches/jump-two'/patchname;pp.parent.mkdir(parents=True,exist_ok=True);pp.write_bytes(patch)
manifest=dict(version='1.0',variant='Goku short normal jump and long running jump; K4 and six barrages retained',buildId=bid,headerTitle=target['header'],source=dict(sha256='217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557',bytes=2097152),target=dict(filename=filename,sha256=sha(rom),bytes=len(rom)),patch=dict(path=pp.relative_to(R).as_posix(),sha256=sha(patch)),experimental=True,userApprovalPending=True)
write(R/'patches/jump-two/manifest.json',json.dumps(manifest,indent=2)+'\n');write(R/'evidence/jump-two/validation.json',json.dumps(dict(passed=True,romSha256=sha(rom),comparisonVariants=checks,otherCharacters=others,sixBarrages=rafagas,approvedK4AndBarrageBytesPreserved=True,videoCases=json.loads((P/'video-cases.json').read_text()),videoSpeedScaling=False,limits=['Goku only; human ports normal-speed fixtures, not hardware/turbo certification.','Both comparison sides include Goku dash repair; raw approved base did not run with the test double tap.','A18 has one extra displayed frame in a regression clip; deduplicated motion sequence is identical.','Air attacks can extend airtime; no full ballistic physics replacement.','No broad obstacle/juggle/AI/balance audit.']),indent=2)+'\n');cp(P/'build.json',R/'evidence/jump-two/build.json')
for f in P.glob('trace-candidate-*.json'):(R/'evidence/jump-two'/(f.stem+'.json.gz')).write_bytes(gzip.compress(f.read_bytes(),mtime=0))
for n in ['prepare.py','jump.asm','jump.listing.txt','jump.labels.txt','build.py','probe.py','test.py','record.py','edit.py','rafagas.py','package.py','assemble.ps1']:cp(P/n,R/'research/jump-two'/n)
write(R/'research/jump-two/jump.hex',(P/'jump.bin').read_bytes().hex()+'\n');cp(Path('work/scripts/AssembleGravity.java'),R/'research/jump-two/AssembleGravity.java');cp(O/'Goku-salto-normal-y-largo-antes-despues.mp4',R/'assets/media/jump-two/comparacion.mp4');cp(O/'comparacion.png',R/'assets/media/jump-two/captura.png');cp(P/'candidate.bin',O/filename);cp(pp,O/patchname);write(O/'version.json',json.dumps(manifest,indent=2)+'\n');write(O/'LEEME.txt',f'Prueba solo Goku: dos saltos. v1.0 build {bid}.\nArriba: normal mas corto. Doble toque adelante/atras, mantener y saltar: largo.\nIncluye correccion de carrera de Goku; K4 y seis rafagas aprobadas conservadas.\nOtros personajes sin nuevos arcos. Pendiente de valorar.\nArrancar desde cero, normal y sin estados de otras ROM.\n')
with zipfile.ZipFile(O/'ROM-prueba-Goku-dos-saltos-K4-y-rafagas.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in [O/filename,O/patchname,O/'version.json',O/'LEEME.txt']:z.write(f,f.name)
print('Packaged',bid,sha(rom))

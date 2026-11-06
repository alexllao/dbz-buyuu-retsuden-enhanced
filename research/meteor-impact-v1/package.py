from pathlib import Path
import json,hashlib,shutil,gzip,zipfile
P=Path('work/meteor-impact');R=Path('repository');O=Path('outputs/meteor-impact-v1');sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf8',newline='\n')
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
m=json.loads((P/'build.json').read_text());rom=(P/'candidate.bin').read_bytes();base=Path('work/gohan-hits/candidate.bin').read_bytes();assert sha(rom)==m['sha256'];patch=bytearray((R/'patches/release-v1-0-build-20261106-124607/DBZ-Enhanced-v1.0-build-20261106-124607.ips').read_bytes());assert patch[-6:-3]==b'EOF';patch=patch[:-6];i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 start=i
 while i<len(rom) and rom[i]!=base[i] and i-start<65535:i+=1
 patch+=start.to_bytes(3,'big')+(i-start).to_bytes(2,'big')+rom[start:i]
patch+=b'EOF'+len(rom).to_bytes(3,'big');patchpath=R/'patches/meteor-impact-v1/DBZ-Enhanced-v1.0-Impact-build-20261106-172551.ips';patchpath.parent.mkdir(parents=True,exist_ok=True);patchpath.write_bytes(patch)
filename='DBZ_Buyuu_Retsuden_Enhanced_v1.0_Impact_build_20261106-172551.bin';manifest=dict(version='1.0',variant='Meteor impact v1 - prueba',buildId=m['buildId'],headerTitle=m['header'],source=dict(sha256='217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557',bytes=2097152),target=dict(filename=filename,sha256=sha(rom),bytes=len(rom)),patch=dict(path=patchpath.relative_to(R).as_posix(),sha256=sha(patch)),experimental=True)
write(R/'patches/meteor-impact-v1/manifest.json',json.dumps(manifest,indent=2)+'\n');movie=O/'Meteor-impactos-reales-antes-despues.mp4';cp(movie,R/'assets/media/meteor-impact-v1/comparacion.mp4');cp(O/'comparacion.png',R/'assets/media/meteor-impact-v1/captura.png')
cases=json.loads((P/'validation-cases.json').read_text());p2=[]
for cid in [1,2]:
 t=json.loads((P/f'port2-{cid}/validation-port2.json').read_text());assert t['romSha256']==sha(rom);p2+=t['cases']
hud=json.loads((P/'hud-qa.json').read_text());assert len(cases)==60 and len(p2)==12 and hud['allExact'];comparison=[]
for name in ['Goku','Gohan','Piccolo','Vegeta','Trunks','Cell','A18','Krilin','Freezer','Recoome']:
 pair=[]
 for side in ['before','after']:
  r=json.loads((P/f'comparison/{side}/{name}.json').read_text());pair.append(dict(side=side,hits=max(t['p']['hits'] for t in r),damage=r[0]['e']['hp']-r[-1]['e']['hp'],pulses=r[-1]['events'],end=[r[-1]['p']['program'],r[-1]['e']['program']],meteorFrames=sum(0x83c<=t['p']['program']<0x860 for t in r)))
 assert pair[0]['damage']==pair[1]['damage'] and pair[0]['hits']==pair[1]['hits'] and pair[1]['pulses']>0 and pair[1]['end']==[0,0]
 comparison.append(dict(name=name,pair=pair))
evidence=dict(passed=True,romSha256=sha(rom),baseSha256=sha(base),nativeRomShake=True,postproductionShake=False,gameplayTimeScaling=False,cases=cases,player2=p2,hud=hud,comparison=comparison,chapters=json.loads((P/'chapters.json').read_text()),video=dict(path='assets/media/meteor-impact-v1/comparacion.mp4',sha256=sha(movie.read_bytes())),limitations=['Normal-speed emulator; original hardware and turbo pending.','Captured timing varies by0..6 frames from rendering/engine scheduling; no timing tables changed.','Common meter HITS and stun remain unchanged, including undercounts in Trunks/A18/Krilin/Freezer.','Ginyu Body Change is not a striking Meteor and receives no artificial shake.','General basic/guard shake remains a separate unintegrated proposal.'])
write(R/'evidence/meteor-impact-v1/validation.json',json.dumps(evidence,indent=2)+'\n');cp(P/'build.json',R/'evidence/meteor-impact-v1/build.json');cp(P/'hud-qa.json',R/'evidence/meteor-impact-v1/hud-qa.json')
for side in ['before','after']:
 for f in (P/f'comparison/{side}').glob('*.json'):
  dest=R/'evidence/meteor-impact-v1'/(side+'-'+f.stem+'.json.gz');dest.write_bytes(gzip.compress(f.read_bytes(),mtime=0))
for n in ['impact.asm','impact.labels.txt','impact.listing.txt']:cp(P/n,R/'src/gameplay/meteor-impact-v1'/n)
write(R/'src/gameplay/meteor-impact-v1/impact.hex',(P/'impact.bin').read_bytes().hex()+'\n')
for n in ['build.py','record.py','validate.py','visual-qa.py','edit.py','package.py','port2-test-1.py','port2-test-2.py','assemble.ps1']:cp(P/n,R/'research/meteor-impact-v1'/n)
cp('work/scripts/AssembleImpact.java',R/'research/meteor-impact-v1/AssembleImpact.java')
cp(P/'candidate.bin',O/filename);write(O/'version.json',json.dumps(manifest,indent=2)+'\n');write(O/'LEEME.txt','Prueba Meteor Impact v1.0 build20261106-172551.\nSacudidas dentro de la ROM en diez remates cinematograficos. HUD superior fijo.\nNo incluye propuestas G1/G2 de gravedad ni arreglos nuevos del contador HITS/stun.\nArrancar desde cero, velocidad normal, sin estados anteriores.\n')
with zipfile.ZipFile(O/'ROM-prueba-impactos-Meteor.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in [O/filename,O/'version.json',O/'LEEME.txt']:z.write(f,f.name)
print('PACKAGED',sha(rom),len(cases)+len(p2),'HUD',hud['matched'])

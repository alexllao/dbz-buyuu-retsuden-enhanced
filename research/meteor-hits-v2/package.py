from pathlib import Path
import json,hashlib,shutil,gzip,zipfile,subprocess
P=Path('work/meteor-hits');R=Path('repository');O=Path('outputs/v1.0-build-20261106-174207');folder='release-v1-0-build-20261106-174207';sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf8',newline='\n')
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
m=json.loads((P/'build.json').read_text());rom=(P/'candidate.bin').read_bytes();base=Path('work/gohan-hits/candidate.bin').read_bytes();assert sha(rom)==m['targetSha256'];patch=bytearray((R/'patches/release-v1-0-build-20261106-124607/DBZ-Enhanced-v1.0-build-20261106-124607.ips').read_bytes());assert patch[-6:-3]==b'EOF';patch=patch[:-6];i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 start=i
 while i<len(rom) and rom[i]!=base[i] and i-start<65535:i+=1
 patch+=start.to_bytes(3,'big')+(i-start).to_bytes(2,'big')+rom[start:i]
patch+=b'EOF'+len(rom).to_bytes(3,'big');patchname='DBZ-Enhanced-v1.0-build-20261106-174207.ips';patchpath=R/'patches'/folder/patchname;patchpath.parent.mkdir(parents=True,exist_ok=True);patchpath.write_bytes(patch)
filename='DBZ_Buyuu_Retsuden_Enhanced_v1.0_build_20261106-174207.bin';manifest=dict(version='1.0',buildId=m['buildId'],buildDate='2026-11-06',buildTimestamp='2026-11-06T17:42:07+01:00',timezone='Europe/Madrid',headerTitle=m['headerTitle'],source=dict(sha256='217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557',bytes=2097152),baseReviewSha256=sha(base),target=dict(filename=filename,sha256=sha(rom),bytes=len(rom)),patch=dict(path=patchpath.relative_to(R).as_posix(),sha256=sha(patch)),experimental=True,addedMeteorShake=False,gravityG1G2=False)
write(R/'patches'/folder/'manifest.json',json.dumps(manifest,indent=2)+'\n');movie=O/'Meteor-HITS-corregidos-y-Cell-11-13.mp4';dest=R/'assets/media'/folder/movie.name;cp(movie,dest);cp(O/'comparacion.png',dest.parent/'captura.png');cases=[]
for port in [1,2]:
 d=json.loads((P/f'validation-port{port}.json').read_text());assert d['romSha256']==sha(rom) and d['passed'];cases+=d['cases']
assert len(cases)==120
comparison=[]
for name,expected in [('Krilin',8),('Freezer',3),('A18',3),('Trunks',3)]:
 r=json.loads((P/f'comparison/after/{name}.json').read_text());old=json.loads(Path(f'work/meteor-impact/comparison/before/{name}.json').read_text());c=dict(name=name,before=max(t['p']['hits'] for t in old),after=max(t['p']['hits'] for t in r),damage=r[0]['e']['hp']-r[-1]['e']['hp']);assert c['before']==2 and c['after']==expected and c['damage']==old[0]['e']['hp']-old[-1]['e']['hp'];comparison.append(c)
cell=[]
for name in ['Cell13','Cell11']:
 r=json.loads((P/f'comparison/after/{name}.json').read_text());zero=next((i for i,t in enumerate(r) if t['e']['hp']==0),len(r)-1);rr=r[:zero+1];drops=[dict(frame=i,damage=a['e']['hp']-b['e']['hp']) for i,(a,b) in enumerate(zip(rr,rr[1:]),1) if b['e']['hp']<a['e']['hp']];c=dict(name=name,initialHP=rr[0]['e']['hp'],finalHP=rr[-1]['e']['hp'],contacts=len(drops),maxHits=max(t['p']['hits'] for t in rr),drops=drops);assert c['maxHits']==c['contacts'];cell.append(c)
assert [c['maxHits'] for c in cell]==[13,11]
evidence=dict(passed=True,romSha256=sha(rom),cases=cases,comparison=comparison,cellExamples=cell,cellGuardAudit=json.loads((P/'cell-audit.json').read_text()),addedMeteorShake=False,nativeShakeOnly=True,gravityG1G2=False,stunChanged=False,stunCounterProof=json.loads((P/'stun-preserved.json').read_text()),damageChanged=False,animationTablesChanged=False,video=dict(path=dest.relative_to(R).as_posix(),sha256=sha(movie.read_bytes()),seconds=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(movie)]).decode().strip())),chapters=json.loads((P/'chapters.json').read_text()),limits=['Normal speed in Genesis Plus GX. Turbo and original hardware pending.','The eleven-hit Cell example is a documented KO at63HP, not proof that this caused the users earlier observation.','Four missing contact paths corrected. General combo windows and stun remain unchanged.','Video baseline is124607 without added shake; new build also excludes Meteor impact experiment.'])
write(R/'evidence'/folder/'validation.json',json.dumps(evidence,indent=2)+'\n');write(P/'validation.json',json.dumps(evidence,indent=2)+'\n')
for n in ['build.json','validation-port1.json','validation-port2.json','cell-audit.json','cell-ko-audit.json']:cp(P/n,R/'evidence'/folder/n)
for f in list(P.glob('trace-*.json'))+list(P.glob('cell-stand-*.json'))+[P/'cell-natural-ko.json']:
 (R/'evidence'/folder/(f.stem+'.json.gz')).write_bytes(gzip.compress(f.read_bytes(),mtime=0))
for n in ['contacts.asm','contacts.labels.txt','contacts.listing.txt']:cp(P/n,R/'src/hud/meteor-hits-v2'/n)
write(R/'src/hud/meteor-hits-v2/contacts.hex',(P/'contacts.bin').read_bytes().hex()+'\n')
for n in ['build.py','validate.py','cell-audit.py','cell-ko.py','record.py','record-cell-ko.py','edit.py','package.py','assemble.ps1']:cp(P/n,R/'research/meteor-hits-v2'/n)
cp('work/scripts/AssembleMeteorHits.java',R/'research/meteor-hits-v2/AssembleMeteorHits.java');cp(P/'candidate.bin',O/filename);cp(patchpath,O/patchname);write(O/'version.json',json.dumps(manifest,indent=2)+'\n');cp(P/'validation.json',O/'validation.json');write(O/'LEEME.txt','Buyuu Retsuden Enhanced v1.0 build20261106-174207.\nMeteor: Krilin8, Freezer3, A18 3 y Trunks3 HITS en las tomas completas; resto revisado.\nCell cuenta cada contacto:13 con vida suficiente,11 en el ejemplo de KO a63HP.\nSin sacudidas de Meteor anadidas. Conserva la vibracion nativa.\nNo incluye G1/G2 de gravedad. Arrancar desde cero, velocidad normal, sin estados anteriores.\n')
with zipfile.ZipFile('outputs/ROM-v1.0-build-20261106-174207.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in [O/filename,O/patchname,O/'version.json',O/'LEEME.txt']:z.write(f,f.name)
print('PACKAGED',sha(rom),len(cases),comparison)

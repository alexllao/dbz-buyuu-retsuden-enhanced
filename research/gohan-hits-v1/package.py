from pathlib import Path
import json,hashlib,shutil,gzip,zipfile
P=Path('work/gohan-hits');R=Path('repository');v=json.loads((P/'version.json').read_text());folder='release-v1-0-build-'+v['buildId'];O=Path('outputs/v1.0-build-'+v['buildId']);sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf8',newline='\n')
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
rom=(P/'candidate.bin').read_bytes();base=Path('work/piccolo-hits/candidate.bin').read_bytes();meta=json.loads((P/'build.json').read_text());assert sha(rom)==meta['targetSha256'] and sha(base)==meta['sourceSha256'];cases=[];regression=[]
for port in [1,2]:
 for sub,target in [('',cases),('piccolo-regression/',regression)]:
  d=json.loads((P/f'{sub}validation-port{port}.json').read_text());assert d['passed'] and d['romSha256']==sha(rom);target.extend(d['cases'])
assert len(cases)==len(regression)==12
assert all(t['maxHits']==(5 if t['mode']=='hit' else 0) and (t['damage']==34 if t['mode']=='hit' else True) for t in cases)
assert all(t['maxHits']==(9 if t['mode']=='hit' else 0) for t in regression)
comparison=[]
for tag in ['before','after']:
 t=json.loads((P/f'comparison/{tag}/Gohan Meteor.json').read_text());comparison.append(dict(build=tag,maxHits=max(r['p']['hits'] for r in t),damage=t[0]['e']['hp']-t[-1]['e']['hp']))
assert [t['maxHits'] for t in comparison]==[2,5] and all(t['damage']==34 for t in comparison)
old='release-v1-0-build-20261106-105411';patch=bytearray((R/'patches'/old/'DBZ-Enhanced-v1.0-build-20261106-105411.ips').read_bytes());assert patch[-6:-3]==b'EOF';patch=patch[:-6];i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 start=i
 while i<len(rom) and rom[i]!=base[i] and i-start<65535:i+=1
 patch+=start.to_bytes(3,'big')+(i-start).to_bytes(2,'big')+rom[start:i]
patch+=b'EOF'+len(rom).to_bytes(3,'big');patchName='DBZ-Enhanced-v1.0-build-'+v['buildId']+'.ips';(R/'patches'/folder).mkdir(parents=True,exist_ok=True);(R/'patches'/folder/patchName).write_bytes(patch)
manifest=dict(**v,source=dict(sha256='217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557',bytes=2097152),baseReviewSha256=sha(base),target=dict(filename=v['filename'],sha256=sha(rom),bytes=len(rom)),patch=dict(path='patches/'+folder+'/'+patchName,sha256=sha(patch)),experimental=True,scope='Count Gohan Meteor contact cues only while victim is in885; exclude final cue after damage/reaction transition. Preserve damage, animation, previous Piccolo fix and controls.')
write(R/'patches'/folder/'manifest.json',json.dumps(manifest,indent=2)+'\n')
movie=O/f'Gohan-Meteor-HITS-antes-despues-v1.0-build-{v["buildId"]}.mp4';dest=R/'assets/media'/folder/movie.name;cp(movie,dest)
summary=dict(passed=True,romSha256=sha(rom),baseRomSha256=sha(base),version=v,gohanCases=cases,piccoloRegression=regression,comparison=comparison,damageChanged=False,animationChanged=False,controlsChanged=False,video=dict(path=dest.relative_to(R).as_posix(),sha256=sha(movie.read_bytes())),limitations=['Normal-speed emulator cases in both ports and orientations; not an exhaustive audit of all special moves or original hardware.','Earlier full presentation shows Gohan before this fix. Short contains no Gohan Meteor and keeps its source build105411.'])
write(P/'validation.json',json.dumps(summary,indent=2)+'\n')
for n in ['build.json','version.json','validation.json','validation-port1.json','validation-port2.json']:cp(P/n,R/'evidence'/folder/n)
for sub in ['', 'piccolo-regression/']:
 for f in (P/sub).glob('trace-*.json'):
  dest=R/'evidence'/folder/('piccolo-' if sub else 'gohan-');dest=dest.parent/(dest.name+f.stem+'.json.gz');dest.write_bytes(gzip.compress(f.read_bytes(),mtime=0))
for n in ['contact.asm','contact.labels.txt','contact.listing.txt']:cp(P/n,R/'src/hud/gohan-hits-v1'/n)
write(R/'src/hud/gohan-hits-v1/contact.hex',(P/'contact.bin').read_bytes().hex()+'\n')
for f in P.glob('*.py'):cp(f,R/'research/gohan-hits-v1'/f.name)
cp(P/'assemble.ps1',R/'research/gohan-hits-v1/assemble.ps1');cp('work/scripts/AssembleGohanHits.java',R/'research/gohan-hits-v1/AssembleGohanHits.java');cp(P/'piccolo-regression/test.py',R/'research/gohan-hits-v1/test-piccolo-regression.py')
cp(P/'candidate.bin',O/v['filename']);cp(R/'patches'/folder/patchName,O/patchName);write(O/'version.json',json.dumps(manifest,indent=2)+'\n');cp(P/'validation.json',O/'validation.json')
guide=f'# Buyuu Retsuden Enhanced v1.0\n\nBuild {v["buildId"]} · 6 de noviembre de 2026, 12:46:07 Madrid.\n\nCorrige el Meteor de Gohan: cinco contactos en la prueba, antes dos; mismo daño. Doce casos de Gohan y doce de Piccolo. Conserva controles, gráficos y mejoras previas. Arranca desde cero en velocidad normal, sin estados de versiones anteriores.\n\nGuía: https://github.com/alexllao/dbz-buyuu-retsuden-enhanced/blob/development/docs/gohan-hits-v1.md\n';write(O/'LEEME.md',guide)
with zipfile.ZipFile('outputs/ROM-v1.0-build-'+v['buildId']+'.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in [O/v['filename'],O/patchName,O/'version.json',O/'validation.json',O/'LEEME.md']:z.write(f,f.name)
print('PACKAGED',v['buildId'],sha(rom))

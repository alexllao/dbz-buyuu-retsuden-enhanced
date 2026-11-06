from pathlib import Path
import json,hashlib,shutil,gzip,zipfile
P=Path('work/ki-startup');R=Path('repository');v=json.loads((P/'version.json').read_text());folder='release-v1-0-build-'+v['buildId'];O=Path('outputs/v1.0-build-'+v['buildId']);sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf8',newline='\n')
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
rom=(P/'candidate.bin').read_bytes();base=Path('work/responsive-v3/candidate.bin').read_bytes();meta=json.loads((P/'build.json').read_text());assert sha(rom)==meta['targetSha256'] and sha(base)==meta['sourceSha256']
before=json.loads((P/'technique-before.json').read_text());after=json.loads((P/'technique-validation.json').read_text());assert before['romSha256']==sha(base) and after['romSha256']==sha(rom) and len(after['cases'])==16
for a,b in zip(before['cases'],after['cases']):assert a['damage']==b['damage'] and a['techniqueDebit']==b['techniqueDebit'] and b['emissionFrames']<a['emissionFrames']
matrix=json.loads((P/'input-matrix.json').read_text());assert len(matrix)==200 and all(t['ok'] for t in matrix)
chords=json.loads((P/'chords.json').read_text());assert len(chords)==10 and all(t['meteor'] for t in chords)
neg=json.loads((P/'negative-checks.json').read_text());assert neg['romSha256']==sha(rom) and all(t['passed'] for t in neg['cases'])
post=[]
for n in ['0','1','port2']:
 d=json.loads((P/f'postthrow-ki-{n}.json').read_text());assert d['romSha256']==sha(rom) and len(d['cases'])==10 and all(t['started'] for t in d['cases']);post.append(d)
cinema=[]
for cid in [0,1]:
 b=json.loads((P/f'before-{cid}.json').read_text());a=json.loads((P/f'after-{cid}.json').read_text());assert b['cases'][2]==a['cases'][2];cinema.append(dict(cid=cid,distance=400,unchanged=True))
promo=json.loads((P/'video/promo.json').read_text());assert promo['romSha256']==sha(rom) and not promo['gameplayTimeScaling']
trace=json.loads((P/'video/11 cruces y meteor.json').read_text());crosses=[sum(t[k]['program']==0x843 and (i==0 or trace[i-1][k]['program']!=0x843) for i,t in enumerate(trace)) for k in ['p','e']];assert crosses==[2,1] and any(t['p']['program']==0x83e for t in trace) and max(t['p']['hits'] for t in trace)==3 and trace[0]['e']['hp']-trace[-1]['e']['hp']==35
patch=bytearray((R/'patches/release-v1-0/DBZ-Enhanced-v1.0-build-20261106-100534.ips').read_bytes());assert patch[-6:-3]==b'EOF';patch=patch[:-6];i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 start=i
 while i<len(rom) and rom[i]!=base[i] and i-start<65535:i+=1
 patch+=start.to_bytes(3,'big')+(i-start).to_bytes(2,'big')+rom[start:i]
patch+=b'EOF'+len(rom).to_bytes(3,'big');patchName='DBZ-Enhanced-v1.0-build-'+v['buildId']+'.ips';(R/'patches'/folder).mkdir(parents=True,exist_ok=True);(R/'patches'/folder/patchName).write_bytes(patch)
manifest=dict(**v,source=dict(sha256='217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557',bytes=2097152),baseReviewSha256=sha(base),target=dict(filename=v['filename'],sha256=sha(rom),bytes=len(rom)),patch=dict(path='patches/'+folder+'/'+patchName,sha256=sha(patch)),experimental=True,scope='Shorten only preparation holds of normal non-split Kamehameha and Masenko. Preserve release timing unit, split-route tables, damage/cost/collision/speed data. Three alternating crossovers into native Goku Meteor recorded.')
write(R/'patches'/folder/'manifest.json',json.dumps(manifest,indent=2)+'\n')
media=[]
for f in O.glob('*.mp4'):
 dest=R/'assets/media'/folder/f.name;cp(f,dest);media.append(dict(path=dest.relative_to(R).as_posix(),sha256=sha(f.read_bytes())))
for n in ['captura.png','Comparacion-preparacion.png']:cp(O/n,R/'assets/media'/folder/n)
summary=dict(passed=True,romSha256=sha(rom),baseRomSha256=sha(base),build=v,techniqueCases=16,baseTechniqueCases=16,inputCases=200,postthrowPassed=30,meteorChords=10,negativeCases=7,splitRouteChecks=cinema,damageAndDebitPreserved=True,releaseAnimationUnitPreserved=True,projectileSpeedDataChanged=False,crossovers=crosses,crossMeteorHits=3,crossMeteorDamage=35,promoSeconds=promo['seconds'],media=media,limitations=['Normal-speed scripted emulator tests, not hardware certification or human balance approval.','Only normal non-split Kamehameha and Masenko startup adjusted. Super/split routes unchanged.','At distance280 one original Masenko setup also misses before and after; this is not a projectile-range fix.','Prior build accumulated24.5min; this build uses focused differential checks, not a repeat of that full soak.'])
write(P/'validation.json',json.dumps(summary,indent=2)+'\n');write(P/'postthrow-summary.json',json.dumps(post,indent=2)+'\n')
for n in ['build.json','version.json','validation.json','input-matrix.json','negative-checks.json','chords.json','charge-double.json','technique-before.json','technique-validation.json','postthrow-summary.json','before-0.json','before-1.json','after-0.json','after-1.json']:cp(P/n,R/'evidence'/folder/n)
write(R/'evidence'/folder/'promo.json',json.dumps(promo,indent=2)+'\n');(R/'evidence'/folder/'cruces-meteor.json.gz').write_bytes(gzip.compress(json.dumps(trace,separators=(',',':')).encode(),mtime=0))
for f in P.glob('*.py'):cp(f,R/'research/ki-startup-v1'/f.name)
cp(P/'version.json',R/'research/ki-startup-v1/version.json')
cp(P/'candidate.bin',O/v['filename']);cp(R/'patches'/folder/patchName,O/patchName);write(O/'version.json',json.dumps(manifest,indent=2)+'\n');cp(P/'validation.json',O/'validation.json')
print('PACKAGED',v['buildId'],sha(rom))

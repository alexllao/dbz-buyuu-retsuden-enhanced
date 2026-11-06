from pathlib import Path
import json,hashlib,shutil,gzip,zipfile
P=Path('work/responsive-v3');R=Path('repository');V=json.loads((P/'version.json').read_text());O=Path('outputs/v1.0-build-'+V['buildId']);O.mkdir(parents=True,exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf8',newline='\n')
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
rom=(P/'candidate.bin').read_bytes();base=Path('work/input-v2/candidate.bin').read_bytes();meta=json.loads((P/'build.json').read_text());assert sha(rom)==meta['targetSha256']
assert rom[0x120:0x150].decode('ascii').strip()==V['headerTitle'];assert rom[0x150:0x180]==rom[0x120:0x150]
matrix=json.loads((P/'input-matrix.json').read_text());assert len(matrix)==200 and all(c['ok'] for c in matrix)
negative=json.loads((P/'negative-checks.json').read_text());assert negative['romSha256']==sha(rom) and all(c['passed'] for c in negative['cases'])
chords=json.loads((P/'chords.json').read_text());assert len(chords)==10 and all(c['meteor'] for c in chords)
poll=json.loads((P/'poll-validation.json').read_text());assert poll['passed'] and poll['romSha256']==sha(rom)
stun=json.loads((P/'stun-validation.json').read_text());assert stun['passed'] and stun['romSha256']==sha(rom)
post=[]
for name in [str(i) for i in range(11)]+['port2']:
 d=json.loads((P/f'postthrow-ki-{name}.json').read_text());assert d['romSha256']==sha(rom) and len(d['cases'])==10 and all(c['started'] for c in d['cases']);post.append(d)
marathons=[]
for f in [P/f'marathon-{i}.json' for i in range(11)]+[P/f'stage-{i}-marathon.json' for i in range(9)]:
 d=json.loads(f.read_text());assert d['passed'] and d['romSha256']==sha(rom);marathons.append({k:v for k,v in d.items() if k!='samples'})
assert sum(d['frames'] for d in marathons)==88200
promo=json.loads((P/'video/promo.json').read_text());assert promo['romSha256']==sha(rom) and not promo['gameplayTimeScaling'];assert len(promo['chapters'])==12
clips=[]
for c in promo['chapters']:
 trace=json.loads((P/'video'/(c['label']+'.json')).read_text());events=[dict(frame=i,damage=a['e']['hp']-b['e']['hp'],hits=b['p']['hits']) for i,(a,b) in enumerate(zip(trace,trace[1:]),1) if b['e']['hp']<a['e']['hp']]
 clips.append(dict(label=c['label'],frames=len(trace),maxHits=max(t['p']['hits'] for t in trace),damageEvents=events))
 compressed=gzip.compress(json.dumps(trace,separators=(',',':')).encode(),mtime=0);out=R/'evidence/release-v1-0/traces'/(c['label']+'.json.gz');out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(compressed)
assert clips[1]['maxHits']==6 and clips[2]['maxHits']==3 and clips[4]['maxHits']==8 and clips[9]['maxHits']==13
patch=bytearray((R/'patches/responsive-v2/responsive-v2.ips').read_bytes());assert patch[-6:-3]==b'EOF';patch=patch[:-6];i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 start=i
 while i<len(rom) and rom[i]!=base[i] and i-start<65535:i+=1
 patch+=start.to_bytes(3,'big')+(i-start).to_bytes(2,'big')+rom[start:i]
patch+=b'EOF'+len(rom).to_bytes(3,'big');folder=R/'patches/release-v1-0';folder.mkdir(parents=True,exist_ok=True);patchName='DBZ-Enhanced-v1.0-build-'+V['buildId']+'.ips';(folder/patchName).write_bytes(patch)
manifest=dict(**V,source=dict(sha256='217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557',bytes=2097152),baseReviewSha256=sha(base),target=dict(filename=V['filename'],sha256=sha(rom),bytes=len(rom)),patch=dict(path='patches/release-v1-0/'+patchName,sha256=sha(patch)),experimental=True,scope='Release1.0: prior graphics/gameplay plus post-impact pad polling, throw-recovery history preservation and HITS pause during offensive ki. Version/build in both ROM header titles. No native collision/damage/stun formula changes vs Respuesta v2.')
write(folder/'manifest.json',json.dumps(manifest,indent=2)+'\n')
summary=dict(version=V,romSha256=sha(rom),passed=True,inputCases=200,postThrowKiPassed=120,characters=11,ports=2,singleFramePollTests=8,negativeCases=7,meteorChordCases=10,scriptedFrames=88200,scriptedMinutes=sum(d['seconds'] for d in marathons)/60,stages=9,nativeCollisionChanges=False,nativeDamageChanges=False,stunFormulaChanges=False,kiCounterPause=True,clips=clips,limitations=['Scripted emulator input at normal speed, not a physical controller or original hardware certification.','Accumulated runtime with restored seeds between bouts; not one continuous match.','Native impact/cinematic pauses remain. Polling every eligible combat update is not a promise that every single video-frame press during a pause is buffered.','HITS tracks the documented chain window; a counted throw-to-beam sequence can still be defended and is not proof of an unavoidable combo.','Exhaustive special-move/HITS/stun audit and human balance testing remain pending.'])
write(P/'validation.json',json.dumps(summary,indent=2)+'\n');write(P/'marathon-summary.json',json.dumps(marathons,indent=2)+'\n');write(P/'postthrow-summary.json',json.dumps(post,indent=2)+'\n')
for n in ['build.json','version.json','validation.json','input-matrix.json','negative-checks.json','chords.json','charge-double.json','poll-validation.json','marathon-summary.json','postthrow-summary.json']:cp(P/n,R/'evidence/release-v1-0'/n)
stun.pop('rows');write(R/'evidence/release-v1-0/stun-validation.json',json.dumps(stun,indent=2)+'\n');write(R/'evidence/release-v1-0/promo.json',json.dumps(promo,indent=2)+'\n')
for n in ['response.asm','response.labels.txt','response.listing.txt']:cp(P/n,R/'src/gameplay/responsive-v3'/n)
write(R/'src/gameplay/responsive-v3/response.hex',(P/'response.bin').read_bytes().hex()+'\n')
for f in P.glob('*.py'):cp(f,R/'research/responsive-v3'/f.name)
cp(P/'assemble.ps1',R/'research/responsive-v3/assemble.ps1');cp('work/scripts/AssembleResponseV3.java',R/'research/responsive-v3/AssembleResponseV3.java')
cp(P/'candidate.bin',O/V['filename']);cp(folder/patchName,O/patchName);write(O/'version.json',json.dumps(manifest,indent=2)+'\n');cp(P/'validation.json',O/'validation.json')
movie=O/Path(promo['video']['path']).name;assert sha(movie.read_bytes())==promo['video']['sha256'];cp(movie,R/promo['video']['path']);cp(O/'captura.png',R/'assets/media/release-v1-0/captura.png')
print('PACKAGED',sha(rom),V['version'],V['buildId'],summary['scriptedMinutes'])

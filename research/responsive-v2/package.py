from pathlib import Path
import json,hashlib,shutil
P=Path('work/input-v2');R=Path('repository');O=Path('outputs/respuesta-v2');O.mkdir(parents=True,exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf8',newline='\n')
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
base=Path('work/responsive-cancels-v1/candidate.bin').read_bytes();rom=(P/'candidate.bin').read_bytes();meta=json.loads((P/'build.json').read_text());assert sha(rom)==meta['targetSha256']
matrix=json.loads((P/'input-matrix.json').read_text());assert len(matrix)==200 and all(c['ok'] for c in matrix)
negative=json.loads((P/'negative-checks.json').read_text());assert negative['romSha256']==sha(rom) and all(c['passed'] for c in negative['cases'])
chords=json.loads((P/'chords.json').read_text());assert len(chords)==10 and all(c['meteor'] for c in chords)
extra=json.loads((P/'extra-runtime.json').read_text());assert len(extra)==5
choice=json.loads((P/'charge-double.json').read_text());assert 0xc05 in choice[0]['programs'] and 0x83e not in choice[0]['programs'];assert 0x83e in choice[1]['programs'] and 0xc05 not in choice[1]['programs']
marathons=[]
for f in [P/f'marathon-{cid}.json' for cid in range(11)]+[P/f'stage-{stage}-marathon.json' for stage in range(9)]:
 d=json.loads(f.read_text());assert d['passed'] and d['romSha256']==sha(rom)
 marathons.append({k:v for k,v in d.items() if k!='samples'})
assert len(marathons)==20
frames=sum(d['frames'] for d in marathons);assert frames==88200
balls=[]
for distance in [32,64,120,180]:
 d=json.loads((P/f'barrage-after-{distance}.json').read_text());contacts=[dict(frame=b['f'],hp=b['e']['hp']) for a,b in zip(d,d[1:]) if b['e']['hp']<a['e']['hp']];assert len(contacts)==3
 balls.append(dict(distance=distance,contacts=contacts))
walk=[]
for hold in [2,5,15,30,60]:
 a=json.loads((P/f'walk-{hold}.json').read_text());b=json.loads((P/f'walk-after-{hold}.json').read_text());old=a[-1]['x']-a[hold-1]['x'];new=b[-1]['x']-b[hold-1]['x'];assert 0<new<=4
 walk.append(dict(heldFrames=hold,oldCoast=old,newCoast=new))
jumpBefore=json.loads((P/'jump-before.json').read_text());jumpAfter=json.loads((P/'jump-after.json').read_text());assert all(c['height']==87 and c['airFrames']<=36 for c in jumpAfter)
summary=dict(romSha256=sha(rom),passed=True,inputCases=200,inputPassed=200,meteorChords=chords,extraChecks=list(extra),chargeCommandChoice=choice,scriptedFrames=frames,scriptedMinutes=sum(d['seconds'] for d in marathons)/60,humanCharacters=11,stages=9,walking=walk,jumpBefore=jumpBefore,jumpAfter=jumpAfter,barrage=balls,stateRelocations=168,negativeChecks=negative['cases'],counterRuleChanges=False,nativeCollisionChanges=False,limitations=['Normal-speed scripted ports with initial charged snapshots; reset after KO or every1800frames. Accumulated runtime, not a continuous human session.','Does not guarantee every physical-controller gesture or establish perfect human feel.','Diagonal components accepted; anticipatory special may redirect a simple attack before it becomes active, not cancel active techniques.','HITS/stun state relocated to avoid native projectile overlap; their counting/stun rules and native damage/reaction formulas remain pending manual review.'])
write(P/'validation.json',json.dumps(summary,indent=2)+'\n')
write(P/'marathon-summary.json',json.dumps(marathons,indent=2)+'\n')
patch=(R/'patches/responsive-v1/responsive-v1.ips').read_bytes();assert patch[-6:-3]==b'EOF';patch=bytearray(patch[:-6]);i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 start=i
 while i<len(rom) and rom[i]!=base[i] and i-start<65535:i+=1
 patch+=start.to_bytes(3,'big')+(i-start).to_bytes(2,'big')+rom[start:i]
patch+=b'EOF'+len(rom).to_bytes(3,'big');folder=R/'patches/responsive-v2';folder.mkdir(parents=True,exist_ok=True);(folder/'responsive-v2.ips').write_bytes(patch)
manifest=dict(source=dict(sha256='217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557',bytes=2097152),baseReviewSha256=sha(base),target=dict(filename='Buyuu_Retsuden_Enhanced_Respuesta_v2.bin',sha256=sha(rom),bytes=len(rom)),patch=dict(path='patches/responsive-v2/responsive-v2.ips',sha256=sha(patch)),experimental=True,defaultBuildUnchanged='v6.6',scope='Goku lenient command recognizer; half-circle Kamehameha, double half-circle Super, double half-circle A+B Meteor; shorter walking coast and lower/faster normal jumps; relocate mod state out of native third projectile. No collision/damage/counter-rule changes.')
write(folder/'manifest.json',json.dumps(manifest,indent=2)+'\n')
meta['status']='Validated scripted normal-speed candidate; human feel/balance review remains';write(P/'build.json',json.dumps(meta,indent=2)+'\n')
for n in ['build.json','validation.json','input-matrix.json','chords.json','marathon-summary.json','relocations.json','charge-double.json','negative-checks.json']:cp(P/n,R/'evidence/responsive-v2'/n)
for n in ['inputs.asm','inputs.labels.txt']:cp(P/n,R/'src/gameplay/responsive-v2'/n)
write(R/'src/gameplay/responsive-v2/inputs.hex',(P/'inputs.bin').read_bytes().hex()+'\n')
for n in ['build.py','relocate.py','test-inputs.py','test-chords.py','test-charge-choice.py','test-negative.py','test-regression.py','test-extra.py','test-basic.py','test-jump.py','marathon.py','marathon-stages.py','record.py','package.py']:cp(P/n,R/'research/responsive-v2'/n)
cp('work/scripts/AssembleInputV2.java',R/'research/responsive-v2/AssembleInputV2.java')
cp(P/'candidate.bin',O/manifest['target']['filename']);cp(folder/'responsive-v2.ips',O/'Respuesta-v2.ips');write(O/'version.json',json.dumps(manifest,indent=2));cp(P/'validation.json',O/'validation.json')
print('PACKAGE',sha(rom),'minutes',summary['scriptedMinutes'])

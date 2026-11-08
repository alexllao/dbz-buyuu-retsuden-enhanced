from pathlib import Path
import json,hashlib,gzip,shutil,zipfile
P=Path('work/throw-links');R=Path('repository');O=Path('outputs/enlaces-lanzamiento-especial');sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf8',newline='\n')
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
m=json.loads((P/'build.json').read_text());rom=(P/'candidate.bin').read_bytes();base=Path('work/barrage-roster/candidate.bin').read_bytes();assert sha(rom)==m['targetSha256'];before=[];after=[];changes=[]
for cid in range(11):
 a=json.loads((P/f'report-{cid}.json').read_text());b=json.loads((P/f'after/report-{cid}.json').read_text());assert a['baseline']['totalDamage']==b['baseline']['totalDamage'];assert b['romSha256']==sha(rom);assert all(x['accepted'] is not None for x in b['cases']);chosen=next(x for x in b['cases'] if x['delay']==b['earliestUsefulDelay'] and not x['guard']);assert len(chosen['events'])==chosen['maxHits']==2
 for x in a['cases']:
  y=next((y for y in b['cases'] if (y['delay'],y['guard'])==(x['delay'],x['guard'])),None)
  if y and x['totalDamage']!=y['totalDamage']:
   assert cid in [0,7] and x['delay']==0 and y['totalDamage']==b['baseline']['totalDamage'];changes.append(dict(cid=cid,guard=x['guard'],before=x['totalDamage'],after=y['totalDamage']))
 before.append(a);after.append(b)
assert len(changes)==4
p2=json.loads((P/'port2/summary.json').read_text());extras=json.loads((P/'port2/extras.json').read_text());assert all(x['accepted'] is not None for d in p2 for x in d['cases'] if not x['throwOnly']);assert all(x['accepted'] is not None for x in extras)
ma=json.loads((P/'meteors/before/roster-report.json').read_text());mb=json.loads((P/'meteors/after/roster-report.json').read_text());assert len(ma)==len(mb)==11 and all(x['hits']==y['hits'] and x['damage']==y['damage'] for x,y in zip(ma,mb))
for a,n in [(0x1f39f,0x39),(0x1f4b3,0x24),(0x3da200,0x400),(0x3db000,0x400)]:assert rom[a:a+n]==base[a:a+n]
patch=bytearray(next((R/'patches/barrage-roster').glob('*.ips')).read_bytes());assert patch[-6:-3]==b'EOF';patch=patch[:-6];i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 start=i
 while i<len(rom) and rom[i]!=base[i] and i-start<65535:i+=1
 patch+=start.to_bytes(3,'big')+(i-start).to_bytes(2,'big')+rom[start:i]
patch+=b'EOF'+len(rom).to_bytes(3,'big');bid=m['buildId'];filename=f'DBZ_Enhanced_v1.0_K4_Rafagas_Lanzamientos_build_{bid}.bin';patchname=f'Lanzamiento-especial-build-{bid}.ips';pp=R/'patches/throw-links'/patchname;pp.parent.mkdir(parents=True,exist_ok=True);pp.write_bytes(patch)
manifest=dict(version='1.0',variant='Throw damage source correction; K4 and six approved barrages',buildId=bid,headerTitle=m['headerTitle'],source=dict(sha256='217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557',bytes=2097152),target=dict(filename=filename,sha256=sha(rom),bytes=len(rom)),patch=dict(path=pp.relative_to(R).as_posix(),sha256=sha(patch)),experimental=True,userApprovalPending=True)
write(R/'patches/throw-links/manifest.json',json.dumps(manifest,indent=2)+'\n');counts=dict(referenceP1=sum(1+len(d['cases']) for d in before),correctedP1=sum(1+len(d['cases']) for d in after),correctedP2=sum(len(d['cases']) for d in p2),extraP2=len(extras),meteorBefore=len(ma),meteorAfter=len(mb));write(R/'evidence/throw-links/validation.json',json.dumps(dict(passed=True,romSha256=sha(rom),counts=counts,reference=before,corrected=after,secondPort=p2,secondPortExtras=extras,changedDamageCases=changes,meteorSamplesBefore=ma,meteorSamplesAfter=mb,k4AndSixBarrageDataPreserved=True,gameplayVideoSpeedScaling=False,limits=['Normal-speed scripted human ports, one principal ki special per character.','Recorded contact with HP loss occurs on the ground; no new aerial juggle system.','Not every two-impact neutral sequence is an inescapable combo; guard can reduce damage where there is a gap.','Krilin timing varies between ports/guard fixtures by several frames.','Turbo, hardware, all stages/matchups/escapes and interrupted/KO throws not exhaustively audited.','Jump-two prototype is not merged into this approved-base trial.']),indent=2)+'\n');cp(P/'build.json',R/'evidence/throw-links/build.json');cp(P/'video-cases.json',R/'evidence/throw-links/video-cases.json')
for cid in range(11):
 d=after[cid];delay=d['earliestUsefulDelay']
 for f in [P/f'trace-{cid}-0-neutral.json',P/f'after/trace-{cid}-0-neutral.json',P/f'after/trace-{cid}-{delay}-neutral.json']:
  label=('before-' if f.parent==P else 'after-')+f.stem+'.json.gz';(R/'evidence/throw-links'/label).write_bytes(gzip.compress(f.read_bytes(),mtime=0))
for name in ['throw.asm','throw.listing.txt','throw.labels.txt','build.py','audit.py','audit-after.py','extras.py','merge-extras.py','seeds-p2.py','port2.py','refine-p2.py','meteors.py','record.py','edit.py','package.py','assemble.ps1']:cp(P/name,R/'research/throw-links'/name)
cp(Path('work/scripts/AssembleThrowLinks.java'),R/'research/throw-links/AssembleThrowLinks.java');write(R/'research/throw-links/throw.hex',(P/'throw.bin').read_bytes().hex()+'\n')
for name,target in [('Lanzamiento-a-especial-once-personajes','once-personajes'),('Lanzamiento-especial-tiempo-dano-y-defensa','comparacion')]:
 for ext in ['mp4','png']:cp(O/(name+'.'+ext),R/'assets/media/throw-links'/(target+'.'+ext))
cp(P/'candidate.bin',O/filename);cp(pp,O/patchname);write(O/'version.json',json.dumps(manifest,indent=2)+'\n');write(O/'LEEME.txt',f'v1.0 build {bid}: lanzamiento y especial.\nConserva K4 y seis rafagas aprobadas. Corrige el dano del lanzamiento si se prepara otro ataque antes de caer el rival.\nNo cambia comandos ni fuerza impactos; el momento varia por personaje.\nLos saltos experimentales de Goku no se incluyen. Arrancar desde cero, normal y sin estados anteriores.\n')
with zipfile.ZipFile(O/'ROM-prueba-enlaces-lanzamiento-especial-K4.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in [O/filename,O/patchname,O/'version.json',O/'LEEME.txt']:z.write(f,f.name)
print('PACKAGED',bid,counts)

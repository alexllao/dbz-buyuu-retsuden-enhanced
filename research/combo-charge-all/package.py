from pathlib import Path
import json,hashlib,shutil
P=Path('work/combo-charge-all');R=Path('repository');O=Path('outputs/Cargas-minimas-en-combo');sha=lambda b:hashlib.sha256(b).hexdigest()
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
def write(p,text):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8',newline='\n')
m=json.loads((P/'build.json').read_text());rom=(P/'candidate.bin').read_bytes();base=Path('work/namek-native-r10/integrated.bin').read_bytes();assert sha(rom)==m['targetSha256'] and sha(base)==m['sourceSha256']
# Actualizar solo la descripcion de los campos; no reconstruir la ROM validada.
m['minimumPreparationClockTicks']=dict(singlePose=3,multiPoseEach=1)
m['state']='F7B0..F7B7: program, fast latch and phase. F7D0..F7EF: native hurt rectangles with CID/facing/plane tags; all reset each round.'
write(P/'build.json',json.dumps(m,indent=2)+'\n')
allcases=[]
for port in [1,2]:
 before=json.loads((P/f'roster-before-p{port}.json').read_text());after=json.loads((P/f'roster-after-p{port}.json').read_text());assert len(before)==len(after)==44
 for a,b in zip(before,after):
  assert (a['cid'],a['side'],a['context'])==(b['cid'],b['side'],b['context'])
  assert a['damage']==b['damage'] and b['idle']
  if b['context']=='solo':assert not b['fast']
  allcases.append(dict(port=port,cid=b['cid'],side=b['side'],context=b['context'],before=a['startup'],after=b['startup'],damage=b['damage'],fast=b['fast']))
comparison=json.loads((P/'comparison.json').read_text());assert len(comparison)==24
repeat=json.loads((P/'repeat.json').read_text());assert len(repeat)==11 and all(t['comboFast'] and not t['nextSoloFast'] for t in repeat)
video=json.loads((P/'video.json').read_text());assert video['sources'][1]['romSha256']==sha(rom)
for a,b in zip(video['sources'][0]['takes'],video['sources'][1]['takes']):assert a['damage']==b['damage'] and a['maxHits']==b['maxHits'] and b['fast']
summary=dict(buildId=m['buildId'],romSha256=sha(rom),rosterCasesEach=88,damageDifferences=0,soloFastCases=0,fastCases=sum(c['fast'] for c in allcases),notConfirmedOrExpired=[c for c in allcases if c['context']=='combo' and not c['fast']],soloFrameDeltaRange=[min(c['after']-c['before'] for c in allcases if c['context']=='solo'),max(c['after']-c['before'] for c in allcases if c['context']=='solo')],focusedContextsEach=24,repeatedCastCases=11,recordedCharacters=5,mode='Normal speed, scripted human input, two ports and two directions; not an exhaustive audit of every catalog entry or Turbo/CPU/console behavior.',catalogEntries=110)
write(P/'validation.json',json.dumps(summary,indent=2)+'\n')
bid=m['buildId'];name=f'DBZ_Enhanced_v1.0_Cargas_combo_build_{bid}.bin';cp(P/'candidate.bin',O/name)
patch=bytearray(b'PATCH');i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 start=i
 while i<len(rom) and rom[i]!=base[i] and i-start<65535:i+=1
 patch+=start.to_bytes(3,'big')+(i-start).to_bytes(2,'big')+rom[start:i]
patch+=b'EOF'+len(rom).to_bytes(3,'big')
pn=f'Cargas-en-combo-sobre-Namek-R10-build-{bid}.ips';pp=R/'patches/combo-charge-all'/pn;pp.parent.mkdir(parents=True,exist_ok=True);pp.write_bytes(patch);cp(pp,O/pn)
# Reaplicar el IPS sobre R10 y verificar cada byte del resultado.
applied=bytearray(base);pos=5
while patch[pos:pos+3]!=b'EOF':
 at=int.from_bytes(patch[pos:pos+3],'big');n=int.from_bytes(patch[pos+3:pos+5],'big');pos+=5;assert n;applied[at:at+n]=patch[pos:pos+n];pos+=n
assert applied==rom
manifest=dict(version='1.0',buildId=bid,experimental=True,userApprovalPending=True,source=dict(name='Namek R10 build 20261110-094744',sha256=sha(base)),target=dict(filename=name,sha256=sha(rom),bytes=len(rom)),patch=dict(path=pp.relative_to(R).as_posix(),sha256=sha(patch),scope='Delta against exact Namek R10 parent; not against the original retail ROM.'),validation=summary)
write(R/'patches/combo-charge-all/manifest.json',json.dumps(manifest,indent=2)+'\n');write(O/'version.json',json.dumps(manifest,indent=2)+'\n')
write(O/'LEEME.txt',f'PRUEBA v1.0 build {bid}\nPreparacion minima de tecnicas KI enlazadas en combo y Meteor de Cell. Once personajes comprobados con un especial representativo en ambos mandos y sentidos. Catalogo general de 110 tablas; no todas las variantes han sido probadas individualmente.\nAbrir la ROM BIN desde cero, sin estados de otra version. Conservar el build anterior. Velocidad normal; pendiente de valoracion con mando, Turbo y consola real.\nEl IPS incluido se aplica exclusivamente a Namek R10 build 20261110-094744, no a la ROM comercial original.\nVideo: Cargas-en-combo-antes-despues-v1.0.mp4, 35.86 segundos, sonido nativo de la nueva ROM y velocidad normal.\n')
E=R/'evidence/combo-charge-all'
for n in ['build.json','catalog.json','validation.json','comparison.json','before-cases.json','after-cases.json','roster-before-p1.json','roster-before-p2.json','roster-after-p1.json','roster-after-p2.json','repeat.json','video.json']:cp(P/n,E/n)
for v in ['before','after']:cp(P/'captures'/v/'manifest.json',E/f'video-{v}.json')
for n in ['charge.asm','charge.labels.txt','charge.listing.txt','assemble.ps1','build.py','runtime.py','probe.py','roster.py','repeat.py','analyze.py','record.py','edit.py','package.py','prepare-roster.py','prepare-p2.py']:cp(P/n,R/'research/combo-charge-all'/n)
write(R/'research/combo-charge-all/charge.hex',(P/'charge.bin').read_bytes().hex()+'\n');cp(Path('work/scripts/AssembleComboChargeAll.java'),R/'research/combo-charge-all/AssembleComboChargeAll.java')
cp(O/'comparacion-cell.png',R/'assets/media/combo-charge-all/comparacion-cell.png')
print('VALIDATED/PACKAGED',bid,sha(rom),len(allcases),'roster cases + 24 focused + 11 repeat')

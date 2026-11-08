from pathlib import Path
import json,hashlib,gzip,shutil,zipfile
P=Path('work/basic-chains');R=Path('repository');O=Path('outputs/Combos-Goku-y-Short');sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf8',newline='\n')
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
m=json.loads((P/'build.json').read_text());rom=(P/'candidate.bin').read_bytes();base=Path('work/throw-links/candidate.bin').read_bytes();assert sha(rom)==m['targetSha256'];matrix={}
for port in ['port1','port2']:
 for side in ['before','after']:
  d=json.loads((P/port/f'validation-{side}.json').read_text());assert d['passed'] and len(d['cases'])==48
  if side=='after':assert d['romSha256']==sha(rom)
  matrix[port+'-'+side]=d
limits={side:json.loads((P/f'{side}-limits.json').read_text()) for side in ['before','after']};assert all(x['passed'] for x in limits.values()) and limits['after']['romSha256']==sha(rom)
other=[]
for cid in range(1,11):
 a=json.loads((P/f'other-before-{cid}.json').read_text());b=json.loads((P/f'other-after-{cid}.json').read_text());signature=lambda r:dict(damage=r[0]['e']['hp']-r[-1]['e']['hp'],maxHits=max(t['p']['hits'] for t in r),programs=list(dict.fromkeys(t['p']['program'] for t in r if t['p']['program']>=0x400)),poses=sorted(set(t['pose'] for t in r if t['p']['program']>=0x400)));assert signature(a)==signature(b);other.append(dict(cid=cid,fullTraceIdentical=a==b,attackDamageProgramsPosesIdentical=True))
for a,z in [(0x1f8ba,0x2025c),(0x21b4e,0x21b54),(0x3da200,0x3db400),(0x3dc000,0x3dc100),(0x1f39f,0x1f3d8),(0x1f4b3,0x1f4d7)]:assert rom[a:z]==base[a:z]
patch=bytearray(next((R/'patches/throw-links').glob('*.ips')).read_bytes());assert patch[-6:-3]==b'EOF';patch=patch[:-6];i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 start=i
 while i<len(rom) and rom[i]!=base[i] and i-start<65535:i+=1
 patch+=start.to_bytes(3,'big')+(i-start).to_bytes(2,'big')+rom[start:i]
patch+=b'EOF'+len(rom).to_bytes(3,'big');bid=m['buildId'];filename=f'DBZ_Enhanced_v1.0_Goku_cadenas_build_{bid}.bin';patchname=f'Goku-cadenas-build-{bid}.ips';pp=R/'patches/basic-chains'/patchname;pp.parent.mkdir(parents=True,exist_ok=True);pp.write_bytes(patch)
manifest=dict(version='1.0',variant='Goku confirmed basic-chain variants; approved graphics K4 barrages and corrected throws retained',buildId=bid,headerTitle=m['headerTitle'],source=dict(sha256='217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557',bytes=2097152),target=dict(filename=filename,sha256=sha(rom),bytes=len(rom)),patch=dict(path=pp.relative_to(R).as_posix(),sha256=sha(patch)),experimental=True,userApprovalPending=True)
write(R/'patches/basic-chains/manifest.json',json.dumps(manifest,indent=2)+'\n');summary=dict(passed=True,romSha256=sha(rom),matrix=matrix,limits=limits,otherCharacters=other,beforeProbe=json.loads((P/'before-summary.json').read_text()),afterProbe=json.loads((P/'after-summary.json').read_text()),finishersBefore=json.loads((P/'before-finishers.json').read_text()),finishersAfter=json.loads((P/'after-finishers.json').read_text()),finisherDefense=json.loads((P/'after-guard-finishers.json').read_text()),tablesDamageK4BarrageThrowFixPreserved=True,newRamAllocated=False,limitsOfValidation=['Normal-speed human Goku only; prototype awaiting user validation.','The assist remains capped at3basics+1finisher; bounded tests do not prove absence of all native infinites.','Gohan/Cell have trace phase differences, but matching attack programs/poses/damage/HITS.','Finishers against a neutral rival are not guaranteed combos; guard-after-third blocks the sampled remates.','No all-matchup/corner/escape/CPU/turbo/hardware certification.']);write(R/'evidence/basic-chains/validation.json',json.dumps(summary,indent=2)+'\n');cp(P/'build.json',R/'evidence/basic-chains/build.json')
for port in ['port1','port2']:
 for f in (P/port).glob('trace-after-*.json'):(R/'evidence/basic-chains'/(port+'-'+f.stem+'.json.gz')).write_bytes(gzip.compress(f.read_bytes(),mtime=0))
for n in ['chain.asm','chain.labels.txt','chain.listing.txt','build.py','probe.py','singles.py','finishers.py','defense-finishers.py','matrix.py','limits.py','record.py','record-gohan.py','short.py','edit.py','package.py','assemble.ps1']:cp(P/n,R/'research/basic-chains'/n)
write(R/'research/basic-chains/chain.hex',(P/'chain.bin').read_bytes().hex()+'\n');cp(Path('work/scripts/AssembleBasicChains.java'),R/'research/basic-chains/AssembleBasicChains.java');cp(O/'Goku-cadenas-variadas-antes-despues.mp4',R/'assets/media/basic-chains/comparacion.mp4');cp(O/'comparacion.png',R/'assets/media/basic-chains/comparacion.png');cp(O/'Short-Combos-y-remates.mp4',R/'assets/media/basic-chains/short.mp4');cp(O/'Short-Combos-y-remates.png',R/'assets/media/basic-chains/short.png');cp(O/'combos-montaje.json',R/'evidence/basic-chains/short-montage.json')
text='''Título: DBZ Buyuu Retsuden Enhanced: ¡combos y remates! #Shorts

Descripción:
Probando nuevas cadenas de puños y patadas con Goku, junto a Meteor, ráfagas y especiales de varios personajes.

Juego real, sin acelerar. Mod de Mega Drive / Genesis en desarrollo con ayuda de IA.

#DragonBallZ #MegaDrive #Genesis #Romhack #Shorts
''';write(O/'Titulo-y-descripcion-Short.txt',text);write(R/'docs/basic-chains-short-texto.txt',text)
cp(P/'candidate.bin',O/filename);cp(pp,O/patchname);write(O/'version.json',json.dumps(manifest,indent=2)+'\n');write(O/'LEEME.txt',f'v1.0 build {bid}. Prueba de variantes de cadenas, solo Goku humano a velocidad normal.\nA-A-B: punetazo corto, recto y patada de mayor alcance.\nSe conservan3basicos+1remate del asistente; no se garantiza cada enlace ni ausencia total de infinitos.\nIncluye K4,6rafagas y correccion de dano de lanzamiento. No incluye ensayo de dos saltos.\nArrancar desde cero, sin estados de otras versiones.\n')
with zipfile.ZipFile(O/'ROM-prueba-Goku-cadenas-variadas.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in [O/filename,O/patchname,O/'version.json',O/'LEEME.txt']:z.write(f,f.name)
with zipfile.ZipFile(O/'Short-Combos-remates-con-portada-y-texto.zip','w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
 for f in [O/'Short-Combos-y-remates.mp4',O/'Short-Combos-y-remates.png',O/'Titulo-y-descripcion-Short.txt',O/'combos-montaje.json']:z.write(f,f.name)
print('Packaged',bid,sha(rom))

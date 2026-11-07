from pathlib import Path
import json,hashlib,gzip,shutil,zipfile,subprocess
P=Path('work/knockdown-k1');R=Path('repository');O=Path('outputs/derribos-K1');sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf8',newline='\n')
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
meta=json.loads((P/'build.json').read_text());rom=(P/'candidate.bin').read_bytes();base=Path('work/meteor-hits/candidate.bin').read_bytes();assert sha(rom)==meta['targetSha256'];internal=bytearray(rom)
for a in [0x120,0x150]:internal[a:a+48]=b'DBZ BUYUU V1.0 K1 KNOCKDOWN TRIAL'.ljust(48,b' ')
internalHash=sha(internal);assert internal[0x200:]==rom[0x200:];cases=[]
for prefix,port in [('',2),('port1/',1)]:
 for p in (P/prefix).glob('report-*.json'):
  d=json.loads(p.read_text());assert d['romSha256'] in [sha(rom),internalHash]
  for t in d['runs']:
   rows=json.loads((P/prefix/f'trace-{d["cid"]}-{t["delay"]}.json').read_text());wake=t['wakeStart'];idle=t['idle'];poses=sorted(set(x['e']['pose'] for x in rows[wake:idle]));assert rows[wake-1]['e']['y']==448 and rows[wake]['e']['y']==448;assert all(x in poses for x in [68,69,70]),(port,d['cid'],poses)
   cases.append(dict(port=port,cid=d['cid'],measurementSha256=d['romSha256'],**t,secondsToMovement=(t['firstMovement']-t['hit'])/t['fps'],getupPoses=poses))
assert len(cases)==42
old=R/'patches/release-v1-0-build-20261106-174207/DBZ-Enhanced-v1.0-build-20261106-174207.ips';patch=bytearray(old.read_bytes());assert patch[-6:-3]==b'EOF';patch=patch[:-6];i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 start=i
 while i<len(rom) and rom[i]!=base[i] and i-start<65535:i+=1
 patch+=start.to_bytes(3,'big')+(i-start).to_bytes(2,'big')+rom[start:i]
patch+=b'EOF'+len(rom).to_bytes(3,'big');patchname='DBZ-Enhanced-v1.0-K1-build-20261107-094832.ips';patchpath=R/'patches/knockdown-k1'/patchname;patchpath.parent.mkdir(parents=True,exist_ok=True);patchpath.write_bytes(patch)
filename='DBZ_Buyuu_Retsuden_Enhanced_v1.0_K1_build_20261107-094832.bin';manifest=dict(version='1.0',variant='K1 knockdown trial',buildId=meta['buildId'],headerTitle=meta['headerTitle'],source=dict(sha256='217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557',bytes=2097152),target=dict(filename=filename,sha256=sha(rom),bytes=len(rom)),patch=dict(path=patchpath.relative_to(R).as_posix(),sha256=sha(patch)),experimental=True,mainRomUnchanged=True)
write(R/'patches/knockdown-k1/manifest.json',json.dumps(manifest,indent=2)+'\n');movie=O/'Derribos-recuperacion-antes-despues-K1.mp4';cp(movie,R/'assets/media/knockdown-k1/comparacion.mp4');cp(O/'comparacion.png',R/'assets/media/knockdown-k1/captura.png');videoCases=json.loads((P/'video-cases.json').read_text());assert len(videoCases)==5 and all(c['comparison'][1]['seconds']<c['comparison'][0]['seconds'] and c['comparison'][0]['damage']==c['comparison'][1]['damage'] for c in videoCases)
validation=dict(passed=True,romSha256=sha(rom),sourceSha256=sha(base),cases=cases,measurementHeaderOnlyVariantSha256=internalHash,headerOnlyVariantPayloadMatches=True,videoCases=videoCases,mainRomUnchanged=True,normalSpeed=True,gameplayVideoTimeScaling=False,getupAlwaysGrounded=True,allThreeGetupPosesPreserved=True,video=dict(path='assets/media/knockdown-k1/comparacion.mp4',sha256=sha(movie.read_bytes()),seconds=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(movie)]).decode().strip())),limits=['One sweep with Goku; other knockdown causes, air reactions, KO and extended wake pressure not audited.','Normal-speed emulator, not turbo or hardware.','Earlier control also ends the existing state-based protection earlier; no new invulnerability frames.','33 timings use an otherwise identical internal header;9 first-port checks and all video captures use the delivered versioned ROM.','Main v1.0 build174207 unchanged; K1 pending user visual validation.'])
write(R/'evidence/knockdown-k1/validation.json',json.dumps(validation,indent=2)+'\n');cp(P/'build.json',R/'evidence/knockdown-k1/build.json');cp('outputs/medicion-derribos-20261107.json',R/'evidence/knockdown-k1/baseline-timing.json')
for prefix,tag in [('', 'p2-'),('port1/','p1-')]:
 for f in (P/prefix).glob('trace-*.json'):(R/'evidence/knockdown-k1'/(tag+f.stem+'.json.gz')).write_bytes(gzip.compress(f.read_bytes(),mtime=0))
for name in ['build.py','measure.py','measure-port1.py','record.py','edit.py','package.py']:cp(P/name,R/'research/knockdown-k1'/name)
cp(P/'candidate.bin',O/filename);cp(patchpath,O/patchname);write(O/'version.json',json.dumps(manifest,indent=2)+'\n');write(O/'LEEME.txt','Prueba K1 v1.0 build20261107-094832.\nDerribos normales y levantarse mas breves. Comparacion con build174207.\nLa ROM principal no cambia; K1 pendiente de elegir. Sin sacudidas nuevas.\nArrancar desde cero, velocidad normal, sin estados de otras versiones.\n')
with zipfile.ZipFile(O/'ROM-prueba-derribos-K1.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in [O/filename,O/patchname,O/'version.json',O/'LEEME.txt']:z.write(f,f.name)
print('PACKAGED',len(cases),sha(rom),validation['video']['seconds'])

from pathlib import Path
import json,hashlib,struct,gzip,shutil,zipfile,subprocess
P=Path('work/knockdown-k2');R=Path('repository');O=Path('outputs/derribos-K2');sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf8',newline='\n')
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
m=json.loads((P/'build.json').read_text());rom=(P/'candidate.bin').read_bytes();base=Path('work/knockdown-k1/candidate.bin').read_bytes();assert sha(rom)==m['targetSha256'];cases=[]
for p in P.glob('report-*.json'):
 d=json.loads(p.read_text());assert d['romSha256']==sha(rom)
 for t in d['runs']:
  r=json.loads((P/f'trace-{d["cid"]}-{t["delay"]}.json').read_text());poses=sorted(set(x['e']['pose'] for x in r[t['wakeStart']:t['idle']]));assert all(x in poses for x in [68,69,70]);assert r[t['wakeStart']-1]['e']['y']==r[t['wakeStart']]['e']['y']==448;cases.append(dict(cid=d['cid'],**t))
assert len(cases)==11
movie=O/'Incorporacion-K1-rapida-vs-K2-intermedia.mp4';videoCases=json.loads((P/'video-cases.json').read_text());assert len(videoCases)==5 and all(x['identicalThroughWakeStart'] and x['comparison'][1]['getupSeconds']>x['comparison'][0]['getupSeconds'] for x in videoCases)
patch=bytearray((R/'patches/knockdown-k1/DBZ-Enhanced-v1.0-K1-build-20261107-094832.ips').read_bytes());assert patch[-6:-3]==b'EOF';patch=patch[:-6];i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 start=i
 while i<len(rom) and rom[i]!=base[i] and i-start<65535:i+=1
 patch+=start.to_bytes(3,'big')+(i-start).to_bytes(2,'big')+rom[start:i]
patch+=b'EOF'+len(rom).to_bytes(3,'big');patchname='DBZ-Enhanced-v1.0-K2-build-20261107-100046.ips';pp=R/'patches/knockdown-k2'/patchname;pp.parent.mkdir(parents=True,exist_ok=True);pp.write_bytes(patch);filename='DBZ_Buyuu_Retsuden_Enhanced_v1.0_K2_build_20261107-100046.bin'
manifest=dict(version='1.0',variant='K2 intermediate getup trial',buildId=m['buildId'],headerTitle=m['headerTitle'],source=dict(sha256='217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557',bytes=2097152),target=dict(filename=filename,sha256=sha(rom),bytes=len(rom)),patch=dict(path=pp.relative_to(R).as_posix(),sha256=sha(patch)),experimental=True,mainRomUnchanged=True)
write(R/'patches/knockdown-k2/manifest.json',json.dumps(manifest,indent=2)+'\n');cp(movie,R/'assets/media/knockdown-k2/comparacion.mp4');cp(O/'comparacion.png',R/'assets/media/knockdown-k2/captura.png');validation=dict(passed=True,romSha256=sha(rom),sourceSha256=sha(base),cases=cases,videoCases=videoCases,groundReactionDataUnchanged=True,mainRomUnchanged=True,gameplayVideoTimeScaling=False,video=dict(path='assets/media/knockdown-k2/comparacion.mp4',sha256=sha(movie.read_bytes()),seconds=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(movie)]).decode().strip())),limits=['Normal-speed ground sweep; turbo, hardware, other knockdowns and extended wake pressure pending.','Matched-state native recordings show same trajectory and ground wait through wake start.','K2 pending visual feedback; principal174207 unchanged.'])
write(R/'evidence/knockdown-k2/validation.json',json.dumps(validation,indent=2)+'\n');cp(P/'build.json',R/'evidence/knockdown-k2/build.json')
for f in P.glob('trace-*.json'):(R/'evidence/knockdown-k2'/(f.stem+'.json.gz')).write_bytes(gzip.compress(f.read_bytes(),mtime=0))
for side in ['before','after']:
 for f in (P/f'comparison/{side}').glob('*.json'):(R/'evidence/knockdown-k2'/(side+'-'+f.stem+'.json.gz')).write_bytes(gzip.compress(f.read_bytes(),mtime=0))
for n in ['build.py','measure.py','record.py','edit.py','package.py']:cp(P/n,R/'research/knockdown-k2'/n)
cp(P/'candidate.bin',O/filename);cp(pp,O/patchname);write(O/'version.json',json.dumps(manifest,indent=2)+'\n');write(O/'LEEME.txt','Prueba K2 v1.0 build20261107-100046.\nMantiene caida, rebote y espera de K1. Incorporacion algo mas pausada.\nROM principal174207 sin cambios. Arrancar desde cero, velocidad normal, sin estados anteriores.\n')
with zipfile.ZipFile(O/'ROM-prueba-derribos-K2.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in [O/filename,O/patchname,O/'version.json',O/'LEEME.txt']:z.write(f,f.name)
print('PACKAGED K2',sha(rom),len(cases))

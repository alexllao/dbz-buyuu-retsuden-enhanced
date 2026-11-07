from pathlib import Path
import json,hashlib,struct,shutil,gzip,zipfile
P=Path('work/knockdown-k4');R=Path('repository');O=Path('outputs/derribos-K4');sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf8',newline='\n')
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
m=json.loads((P/'build.json').read_text());rom=(P/'candidate.bin').read_bytes();base=Path('work/knockdown-k3/candidate.bin').read_bytes();cases=[]
assert sha(rom)==m['targetSha256']
for p in sorted(P.glob('report-*.json')):
 d=json.loads(p.read_text());assert d['romSha256']==sha(rom);old=json.loads(Path(f'work/knockdown-k3/report-{d["cid"]}.json').read_text())['runs'][0];t=d['runs'][0]
 # Arranques independientes: tolerar la fase nativa de 1-2 frames.
 # Las tomas de video, en cambio, parten del mismo estado y se comparan exactas.
 assert all(abs(t[k]-old[k])<=2 for k in ['settledOnGround','firstGroundTouch','hit'])
 assert 16<=t['lyingFrames']-old['lyingFrames']<=22
 rows=json.loads((P/f'trace-{d["cid"]}-0.json').read_text());assert {68,69,70}.issubset({x['e']['pose'] for x in rows[t['wakeStart']:t['idle']]})
 cases.append(dict(cid=d['cid'],before=old,after=t,extraLyingFrames=t['lyingFrames']-old['lyingFrames']))
assert len(cases)==11
# BF/C0/C1/C2 permanecen byte por byte iguales a K3.
for program in [0xbf,0xc0,0xc1,0xc2]:
 a=0x1eb26+program*2;t=a+struct.unpack_from('>h',base,a)[0];assert rom[t:t+9]==base[t:t+9]
patch=bytearray(next((R/'patches/knockdown-k3').glob('*.ips')).read_bytes());assert patch[-6:-3]==b'EOF';patch=patch[:-6];i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 start=i
 while i<len(rom) and rom[i]!=base[i] and i-start<65535:i+=1
 patch+=start.to_bytes(3,'big')+(i-start).to_bytes(2,'big')+rom[start:i]
patch+=b'EOF'+len(rom).to_bytes(3,'big');bid=m['buildId'];patchname=f'DBZ-Enhanced-v1.0-K4-build-{bid}.ips';filename=f'DBZ_Buyuu_Retsuden_Enhanced_v1.0_K4_build_{bid}.bin';pp=R/'patches/knockdown-k4'/patchname;pp.parent.mkdir(parents=True,exist_ok=True);pp.write_bytes(patch)
manifest=dict(version='1.0',variant='K4 longer lying wait trial',buildId=bid,headerTitle=m['headerTitle'],source=dict(sha256='217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557',bytes=2097152),target=dict(filename=filename,sha256=sha(rom),bytes=len(rom)),patch=dict(path=pp.relative_to(R).as_posix(),sha256=sha(patch)),experimental=True,mainRomUnchanged=True)
write(R/'patches/knockdown-k4/manifest.json',json.dumps(manifest,indent=2)+'\n');video=O/'Derribos-K3-vs-K4-espera-tumbado.mp4';cp(video,R/'assets/media/knockdown-k4/comparacion.mp4');cp(O/'comparacion.png',R/'assets/media/knockdown-k4/captura.png')
validation=dict(passed=True,romSha256=sha(rom),cases=cases,videoCases=json.loads((P/'video-cases.json').read_text()),getupDataUnchanged=True,mainRomUnchanged=True,gameplayVideoTimeScaling=False,limits=['Normal-speed ground sweep only; A4 not triggered by this sweep.','State-based reaction protection lasts longer with longer floor wait.','Turbo, hardware and extended wake pressure not validated.','Pending user visual validation.'])
write(R/'evidence/knockdown-k4/validation.json',json.dumps(validation,indent=2)+'\n');cp(P/'build.json',R/'evidence/knockdown-k4/build.json')
for f in P.glob('trace-*.json'):(R/'evidence/knockdown-k4'/(f.stem+'.json.gz')).write_bytes(gzip.compress(f.read_bytes(),mtime=0))
for f in (P/'comparison/after').glob('*.json'):(R/'evidence/knockdown-k4'/('video-'+f.stem+'.json.gz')).write_bytes(gzip.compress(f.read_bytes(),mtime=0))
for name in ['build.py','record.py','measure.py','edit.py','package.py']:cp(P/name,R/'research/knockdown-k4'/name)
cp(P/'candidate.bin',O/filename);cp(pp,O/patchname);write(O/'version.json',json.dumps(manifest,indent=2)+'\n');write(O/'LEEME.txt',f'Prueba K4 v1.0 build {bid}.\nMas espera tumbado; gesto de levantarse igual a K3.\nPrincipal 174207 sin cambios. Arrancar desde cero, velocidad normal, sin estados anteriores.\n')
with zipfile.ZipFile(O/'ROM-prueba-derribos-K4.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in [O/filename,O/patchname,O/'version.json',O/'LEEME.txt']:z.write(f,f.name)
print('Packaged',sha(rom),'extra wait frames',[x['extraLyingFrames'] for x in cases])

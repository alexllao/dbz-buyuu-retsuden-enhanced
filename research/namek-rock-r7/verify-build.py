from pathlib import Path
import json,hashlib,subprocess,sys
T=Path('work/namek-native-r7');OLD=Path('work/namek-native-r6')
paths=[T/slug/name for slug in ['normal','aldea','porunga'] for name in ['tiles.bin','gfx.lz','map.bin','map-header.bin','palette.bin']]
before={p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
subprocess.run([sys.executable,str(T/'build.py')],check=True)
after={p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths};assert before==after
rom=(T/'integrated.bin').read_bytes();build=json.loads((T/'integrated-build.json').read_text());assert hashlib.sha256(rom).hexdigest()==build['sha256']
for resource in build['resources']:
 data=(T/resource['variant']/resource['path']).read_bytes();at=resource['address'];assert rom[at:at+len(data)]==data
for slug in ['normal','aldea','porunga']:
 report=json.loads((T/slug/'build.json').read_text());assert report['tiles']<=736 and report['outsideEditedRegionsChangedPixels']==0
 assert (T/slug/'palette.bin').read_bytes()==(OLD/slug/'palette.bin').read_bytes()
(T/'reproducibility.json').write_text(json.dumps(dict(resources=after,all15ResourcesByteIdentical=True,all9EmbeddedRomResourcesExact=True,all3PalettesR6Exact=True,editedRegionsOnly=True,romSha256=build['sha256']),indent=2))
print('VERIFIED: 15 reproducible resources, 9 embedded resources, 3 unchanged palettes',flush=True)

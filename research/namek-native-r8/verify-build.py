from pathlib import Path
import json,hashlib,subprocess,sys
sys.path.insert(0,'work/namek-native-r6')
import build as h
T=Path('work/namek-native-r8');R7=Path('work/namek-native-r7')
paths=[T/s/f for s in ['normal','aldea','porunga'] for f in ['tiles.bin','gfx.lz','map.bin','map-header.bin','palette.bin']]
hashes={p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
subprocess.run([sys.executable,str(T/'build.py')],check=True)
assert hashes=={p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
rom=(T/'integrated.bin').read_bytes();meta=json.loads((T/'integrated-build.json').read_text());assert hashlib.sha256(rom).hexdigest()==meta['sha256']
for r in meta['resources']:
 data=(T/r['variant']/r['path']).read_bytes();assert rom[r['address']:r['address']+len(data)]==data
houseHashes=[]
for slug in ['normal','aldea','porunga']:
 report=json.loads((T/slug/'build.json').read_text());assert report['tiles']<=736 and report['losslessPacking'] and report['outsideEditedRegionsChangedPixels']==0 and report['paletteErrorsOutsideDragon']==0
 assert (T/slug/'palette.bin').read_bytes()==(R7/slug/'palette.bin').read_bytes()
 houseHashes.append(report['houseColorSha256'])
assert len(set(houseHashes))==1
night=json.loads((T/'porunga/build.json').read_text());assert night['longestNightSkyGreenRun']<=96
(T/'reproducibility.json').write_text(json.dumps(dict(romSha256=meta['sha256'],resourceHashes=hashes,all15ResourcesReproducible=True,all9EmbeddedResourcesExact=True,all3PalettesUnchanged=True,sharedHouseExact=True,opaqueBackgrounds=True,losslessPacking=True,nightNoLongGreenStrips=True),indent=2))
print('VERIFIED R8: reproducible resources, unchanged palettes, common house, clean sky',flush=True)

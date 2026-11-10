from pathlib import Path
import sys,json,hashlib,subprocess,struct
sys.path.insert(0,'work/simulation-deps')
import numpy as np
from PIL import Image
from numpy.lib.stride_tricks import sliding_window_view
T=Path('work/namek-native-r10');OLD=Path('work/namek-native-r9')
paths=[T/s/f for s in ['normal','aldea','porunga'] for f in ['tiles.bin','gfx.lz','map.bin','map-header.bin','palette.bin']]
hashes={p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
subprocess.run([sys.executable,str(T/'build.py')],check=True)
assert hashes=={p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
rom=(T/'integrated.bin').read_bytes();meta=json.loads((T/'integrated-build.json').read_text());assert hashlib.sha256(rom).hexdigest()==meta['sha256']
for r in meta['resources']:assert rom[r['address']:r['address']+r['bytes']]==(T/r['variant']/r['path']).read_bytes()
bad=np.asarray(Image.open(OLD/'porunga/compiled-map.png'))[403:408,80:96]
Image.fromarray(bad).save(T/'reported-stamp-R9-1x.png')
def occurrences(rgb):
 w=sliding_window_view(rgb[392:],(5,16),axis=(0,1));return int((w==bad.transpose(2,0,1)).all((2,3,4)).sum())
oldCount=occurrences(np.asarray(Image.open(OLD/'porunga/compiled-map.png')));assert oldCount>0
reports=[]
for slug in ['normal','aldea','porunga']:
 rgb=np.asarray(Image.open(T/slug/'compiled-map.png'));report=json.loads((T/slug/'build.json').read_text())
 assert occurrences(rgb)==0,(slug,'reported repeated stamp still present')
 assert report['tiles']<=736 and report['cloudMaxY']<304 and report['opaqueNativeGlassPixels']>0
 assert (T/slug/'palette.bin').read_bytes()==(OLD/slug/'palette.bin').read_bytes()
 center=rgb[299,354];assert int(center[2])>int(center[0])*1.5 and int(center[2])>int(center[1]),(slug,'large window not blue',center)
 reports.append(dict(variant=slug,reportedStampOccurrences=0,windowCenterRGB=center.tolist(),tiles=report['tiles'],opaqueGlassPixels=report['opaqueNativeGlassPixels'],cloudMaxY=report['cloudMaxY']))
assert len({json.loads((T/s/'build.json').read_text())['houseColorSha256'] for s in ['normal','aldea','porunga']})==1
(T/'reproducibility.json').write_text(json.dumps(dict(romSha256=meta['sha256'],all15ResourcesReproducible=True,all9EmbeddedResourcesExact=True,all3PalettesUnchanged=True,sharedHouseExact=True,reportedOldStampCount=oldCount,fixes=reports,resourceHashes=hashes),indent=2))
print('VERIFIED R10. Old stamp occurrences:',oldCount,'new: zero in all three maps. Blue glass, clouds, palettes, resources pass.')

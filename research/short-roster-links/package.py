from pathlib import Path
import json,hashlib,shutil,gzip,zipfile
P=Path('work/short-roster-links');O=Path('outputs/Short-once-personajes-y-Cell');R=Path('repository');sha=lambda b:hashlib.sha256(b).hexdigest()
def cp(a,b):b.parent.mkdir(exist_ok=True,parents=True);shutil.copyfile(a,b)
def write(p,s):p.parent.mkdir(exist_ok=True,parents=True);p.write_text(s,encoding='utf-8')
h='7e60aa9b967f9c647bfd77992afbcca2e8261f5e2f63a6534838872aa02c7cc4';assert sha(Path('work/input-links/candidate.bin').read_bytes())==h
takes=json.loads((P/'takes.json').read_text());assert len(takes)==11 and all(t['romSha256']==h for t in takes)
for t in takes:assert len(t['contactFrames'])==len(t['pattern'])+1
long={k:json.loads(Path(f'work/long-chain/video/{k}/report.json').read_text()) for k in ['after','guard','jump']};assert all(t['romSha256']==h for t in long.values());assert long['after']['maxHits']==16 and long['after']['damage']==105 and long['guard']['maxHits']==16 and long['jump']['maxHits']==3 and long['jump']['damage']==27
manifest=json.loads((O/'roster-montaje.json').read_text(encoding='utf-8'));assert manifest['buildId']=='20261108-175044' and 44<manifest['seconds']<46 and manifest['gameplaySpeedScaling']==False
baseline={k:json.loads(Path('work/input-roster',k,'before-summary.json').read_text()) for k in ['.','port2-left']};assert all(d['romSha256']==h and len(d['cases'])==240 for d in baseline.values())
text='''Título: ¡16 HITS con Cell! | DBZ Buyuu Retsuden Enhanced #Shorts

Descripción:
Once personajes, golpes enlazados y especiales. Cell cierra con básicos, cambio de lado y Meteor: 16 impactos en esta prueba.

Mod de Mega Drive en desarrollo con ayuda de IA. Juego real, sin acelerar.

#DragonBallZ #MegaDrive #Romhack #Shorts
'''
write(O/'Titulo-y-descripcion.txt',text);write(R/'docs/short-once-personajes-texto.txt',text)
for n,dest in [('Short-Once-personajes-y-Cell-16.mp4','short.mp4'),('Short-Once-personajes-y-Cell-16.png','portada-goku.png'),('Portada-Cell-16.png','portada-cell.png'),('Cell-16-impactos-toma-completa.mp4','cell-toma-completa.mp4')]:cp(O/n,R/'assets/media/short-roster-links'/dest)
E=R/'evidence/short-roster-links';E.mkdir(exist_ok=True)
cp(P/'takes.json',E/'takes.json');cp(O/'roster-montaje.json',E/'montage.json')
for k,d in baseline.items():write(E/('native-inputs-p1.json' if k=='.' else 'native-inputs-p2-left.json'),json.dumps(d,indent=2)+'\n')
for k,d in long.items():write(E/f'cell-{k}.json',json.dumps(d,indent=2)+'\n');(E/f'cell-{k}-trace.json.gz').write_bytes(gzip.compress(Path(f'work/long-chain/video/{k}/Cell-16-impactos.json').read_bytes(),mtime=0))
write(E/'validation.json',json.dumps(dict(buildId='20261108-175044',romSha256=h,romChanged=False,characters=11,seconds=manifest['seconds'],nativeInputCasesP1=240,nativeStartsP1=223,nativeInputCasesP2Left=240,nativeStartsP2Left=224,cellSequence=long,unavoidableCombo=False,experimentIntegrated=False,note='Other native parsers already retain recognized commands in demonstrated routes. Extension experiment failed usefulness/regression review and is not used. Video sources all use the valid 175044 build.'),indent=2)+'\n')
for n in ['record.py','render.py','long-video.py','package.py']:cp(P/n,R/'research/short-roster-links'/n)
cp(Path('work/long-chain/record.py'),R/'research/short-roster-links/cell-record.py')
write(Path('work/input-roster/NOT-INTEGRATED.txt'),'No integrado en ROM, parches ni videos.\nLa extension inicial no mejora los arranques de la bateria: el parser nativo ya conserva B9.\nLa instrumentacion siguiente no pasa regresion por interceptar una zona con entrada interior en9376.\nSe detiene el experimento; no promover sus candidate.bin ni sus resultados after.\nShort y tomas finales usan exclusivamente work/input-links/candidate.bin, build20261108-175044.\n')
with zipfile.ZipFile(O/'Short-once-personajes-Cell-portadas-y-texto.zip','w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
 for n in ['Short-Once-personajes-y-Cell-16.mp4','Short-Once-personajes-y-Cell-16.png','Portada-Cell-16.png','Cell-16-impactos-toma-completa.mp4','Titulo-y-descripcion.txt','roster-montaje.json']:z.write(O/n,n)
print('Packaged Short',manifest['seconds'],'seconds; valid ROM unchanged',h)

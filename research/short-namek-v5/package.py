from pathlib import Path
import json,shutil,hashlib,gzip
P=Path('work/namek-v5-short');O=Path('outputs/YouTube-Short-Namek-V5');R=Path('repository');M=R/'assets/media/short-namek-v5';E=R/'evidence/short-namek-v5';S=R/'research/short-namek-v5'
for d in [M,E,S]:d.mkdir(parents=True,exist_ok=True)
manifest=json.loads((O/'manifest.json').read_text());assert manifest['onlyV5'] and manifest['noBeforeAfterComparisons']
assert hashlib.sha256(Path('work/namek-native-v5/integrated.bin').read_bytes()).hexdigest()==manifest['romSha256']
video=O/manifest['file']['name'];assert hashlib.sha256(video.read_bytes()).hexdigest()==manifest['file']['sha256']
shutil.copy2(video,M/'short.mp4');shutil.copy2(video.with_suffix('.png'),M/'portada.png');shutil.copy2(O/'manifest.json',M/'manifest.json');shutil.copy2(O/'texto-youtube.txt',R/'docs/short-namek-v5-texto.txt')
for i,scene in enumerate(manifest['scenes']):
 source=Path(scene['source']);assert hashlib.sha256(source.read_bytes()).hexdigest()==scene['sourceSha256']
 rows=json.loads(source.with_suffix('.json').read_text())[scene['startFrame']:scene['endFrame']]
 with gzip.open(E/f'{i:02d}-selected-frames.json.gz','wb') as z:z.write(json.dumps(rows).encode())
finding=dict(romSha256=manifest['romSha256'],scope='Preparation-only input probe, normal speed, P1 right-facing, normal Namek, spacing180',characters=['Goku','Vegeta'],firstTapFrames=[1,2,3,4,6,8,12],releaseFrames=[1,2,3,4,6,8,12,16],secondHoldFrames=24,cases=112,observedRunActions7or8=0,successfulTimings=json.loads((P/'run-timing.json').read_text()),status='Manual double-tap route needs investigation; ROM not modified for this Short',shortRunSource=manifest['groundRun'])
(E/'manual-run-probe.json').write_text(json.dumps(finding,indent=2));(E/'validation.json').write_text(json.dumps(dict(romUnchanged=True,onlyV5=True,allSourcesVerified=True,vertical=[1080,1920],fullGameRect=manifest['gameRect'],gameSpeedScaling=False,nativeSplitScreen=True,seconds=manifest['seconds'],nativeCPUForVegeta=True),indent=2))
for name in ['record.py','render.py','prepare-extra.py','probe-run.py','probe-cpu.py','package.py']:shutil.copy2(P/name,S/name)
S.joinpath('README.txt').write_text('SHORT SOLO NAMEK V5\n\nROM V5 20261109-093419 sin modificaciones. No se incluyen ROM, core ni estados.\nrecord.py reutiliza las herramientas locales de work/namek-native y input-v2.\nLa carrera y Final Flash de Vegeta los ejecuta la CPU original; Goku usa entradas de mando.\nrender.py recorta encabezados de captura, conserva el juego completo y crea1080x1920.\nNo usa comparaciones ni imagen de otros builds. FPS y tiempos del juego conservados.\nprobe-run.py registra la incidencia de doble toque manual detectada al preparar las tomas.\npackage.py comprueba hashes y guarda evidencia de los fragmentos empleados.\n',encoding='utf-8')
print('PACKAGED',manifest['seconds'],'seconds, V5 only; ROM unchanged')

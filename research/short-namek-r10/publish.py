from pathlib import Path
import json,shutil,hashlib
R=Path('repository');P=Path('work/namek-r10-short');O=Path('outputs/YouTube-Short-Namek-R10')
M=R/'assets/media/short-namek-r10';E=R/'evidence/short-namek-r10';S=R/'research/short-namek-r10'
for p in [M,E,S]:p.mkdir(parents=True,exist_ok=True)
manifest=json.loads((O/'manifest.json').read_text());video=Path(manifest['file']['path']);assert hashlib.sha256(video.read_bytes()).hexdigest()==manifest['file']['sha256']
assert manifest['romUnchanged'] and not manifest['gameSpeedChanged'] and len(manifest['scenes'])==5
shutil.copy2(O/'Portada-Short-Namek-R10.png',M/'portada.png')
for filename in ['Cruces.png','Final-Flash.png','Meteor-Vegeta.png','Meteor-Cell.png','Super-Kamehameha.png']:shutil.copy2(O/filename,M/filename)
shutil.copy2(O/'manifest.json',E/'manifest.json');shutil.copy2(P/'states/selection-proof.json',E/'selection-proof.json');shutil.copy2(P/'timeline-analysis.json',E/'timeline-analysis.json')
shutil.copy2(O/'Texto-YouTube.txt',R/'docs/short-namek-r10-texto.txt')
for filename in ['prepare.py','record.py','analyze.py','render.py','publish.py']:
 (S/filename).write_text((P/filename).read_text(encoding='utf-8-sig').rstrip()+'\n',encoding='utf-8',newline='\n')
(S/'README.txt').write_text('Short Namek R10, 30 seconds. Requires existing local work/namek-native-r10 and its emulator helpers.\nUses unchanged ROM85d70908, build20261110-094744. No ROM, emulator core, states or videos are included.\nprepare.py selects original native menus for Goku/Freezer normal, Vegeta/Goku devastated and Cell/Vegeta Porunga. Critical HP comes from native P2 punches before capture, KI from native charging.\nrecord.py uses real inputs and initial staging only; scripts two human ports. Sources are coordinated demos, not spontaneous CPU matches or proof of unavoidable combos.\nrender.py selects five uninterrupted excerpts, preserves native FPS and full game, integer3x geometry centered in1080x1920. No speed ramps or substituted backgrounds. Native audio only.\nFinal MP4 stays under outputs/YouTube-Short-Namek-R10, ready for user upload. Not automatically published anywhere.\n',encoding='utf-8')
doc='''# Short: Namek renace, R10

10 de noviembre de2026. El usuario acepta R10 («perfecto») y pide un vídeo vistoso de unos30 s para YouTube Shorts, con ataques, cambios de lado, Meteor y superataques. Se prepara un archivo local listo para subir; no se publica automáticamente en YouTube ni se añade el MP4 al repositorio.

[Portada](../assets/media/short-namek-r10/portada.png) · [Texto de YouTube](short-namek-r10-texto.txt).

## Montaje

Duración30,093 s,1080×1920. Juego completo y HUD visibles en un rectángulo960×672, escalado entero3× desde320×224, centrado en60,560. Cinco fragmentos continuos con cortes entre tomas, sin acelerar las animaciones, sin comparaciones y sin reemplazar fondos en posproducción. Sonido nativo; solo fundidos de12/18 ms en los cortes, sin música añadida.

| Tiempo aproximado | Toma real de R10 |
| --- | --- |
| 0:00–0:05 | Goku/Freezer, tres cambios de lado alternados P1/P2/P1 y remate Meteor, Namek normal. |
| 0:05–0:09 | Vegeta/Goku, básicos enlazados a Final Flash, devastado. |
| 0:09–0:14 | Vegeta/Goku, combo y Meteor, devastado. |
| 0:14–0:25 | Cell/Vegeta, básicos, cambio de lado y Meteor, Porunga. |
| 0:25–0:30 | Goku/Freezer, básicos y Super Kamehameha, normal. |

No se corta dentro de la cadena de Cell: el fragmento comienza en el primer básico y alcanza el último impacto del Meteor. La edición termina algunas tomas antes de que acabe la recuperación; no altera su duración interna ni fabrica una cadena entre tomas diferentes.

Archivo local: `outputs/YouTube-Short-Namek-R10/DBZ-Namek-R10-Short-30s.mp4`. También se entrega una portada y Texto-YouTube.txt. ROM v1.0 build20261110-094744, SHA-25685d7090885e83cba884ecaf161c1913feb80a118d0aa3c86f58f7945de2483cf, sin cambios.

## Grabación y comprobaciones

Se seleccionan los tres fondos y personajes desde el menú nativo, con estados nuevos de R10. HP crítico para los Meteor de Vegeta/Cell obtenido mediante golpes reales antes de grabar; energía por carga nativa. Después solo se preparan distancia, orientación y control humano antes de cada toma. Durante la captura se usan dos puertos de mando coordinados: no se escriben posiciones, acciones, vida, energía ni temporizadores. No se presenta como CPU reactiva ni como prueba de que las cadenas sean inevitables.

Se verifica el SHA de la ROM y de cada fuente, el escenario físico6 y la variante en todos los fotogramas seleccionados. Los programas esperados de Super Kamehameha, Final Flash y Meteor aparecen en las trazas. Se comprueban tres cruces alternados en Goku y uno en Cell, cambio de orden de los jugadores y recursos de VRAM/paleta al empezar cada toma. FFmpeg decodifica el Short entero; se revisan portada y capturas de los cinco fragmentos. El archivo final no cambia la velocidad de juego.

[Manifiesto, intervalos y hashes](../evidence/short-namek-r10/manifest.json) · [Selección desde menú](../evidence/short-namek-r10/selection-proof.json) · [Impactos y programas de las tomas](../evidence/short-namek-r10/timeline-analysis.json) · [Código y límites](../research/short-namek-r10/README.txt).
'''
(R/'docs/short-namek-r10.md').write_text(doc,encoding='utf-8',newline='\n')
p=R/'README.md';text=p.read_text(encoding='utf-8');head,rest=text.split('\n\n',1)
note='**Short nuevo · Namek R10 aceptado.** Vídeo vertical de30 s con Goku, Vegeta y Cell: cruces, combos, Meteor, Final Flash y Super Kamehameha en los tres Namek corregidos. Juego/HUD completos y velocidad normal. [Portada](assets/media/short-namek-r10/portada.png) · [Contenido, archivo local y comprobaciones](docs/short-namek-r10.md) · [Título y descripción](docs/short-namek-r10-texto.txt). MP4 preparado para que lo suba el usuario; no publicado automáticamente.'
text=head+'\n\n'+note+'\n\n'+rest;text=text.replace('Pendiente de valoración visual. [Cambios y comprobaciones](docs/namek-native-r10.md).','El usuario acepta esta revisión y solicita el Short. [Cambios y comprobaciones](docs/namek-native-r10.md).');p.write_text(text,encoding='utf-8',newline='\n')
p=R/'docs/decisions.md';text=p.read_text(encoding='utf-8');head,rest=text.split('\n',1);p.write_text(head+'\n\n**10/11/2026 — R10 aceptada; Short de30 s:** el usuario responde «perfecto» a las correcciones y pide una pieza vistosa para Shorts. Se entrega montaje vertical de30,1 s desde la misma ROM, sin aceleración, con Goku, Vegeta y Cell en los tres Namek. Vídeo local listo para subir, título/descripcion preparados; sin publicación automática. [Short](short-namek-r10.md).\n'+rest,encoding='utf-8',newline='\n')
p=R/'docs/namek-native-r10.md';text=p.read_text(encoding='utf-8');head,rest=text.split('\n',1);p.write_text(head+'\n\n**Valoración posterior:** el usuario responde «perfecto» y pide un [Short](short-namek-r10.md) con esta revisión. Se conserva el build sin modificaciones para la grabación.\n'+rest,encoding='utf-8',newline='\n')
print('Short documentation saved; MP4 kept local.')

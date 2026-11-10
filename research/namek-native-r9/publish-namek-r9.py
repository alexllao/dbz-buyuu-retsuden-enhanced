from pathlib import Path
import json,shutil,hashlib
T=Path('work/namek-native-r9');R=Path('repository');O=Path('outputs/Namek-R9-revision')
E=R/'evidence/namek-native-r9';S=R/'research/namek-native-r9';M=R/'assets/media/namek-native-r9'
for p in [E,S,M]:p.mkdir(parents=True,exist_ok=True)
for name in ['integrated-build.json','runtime-validation.json','reproducibility.json','delivery-manifest.json','live-vram-audit.json']:
 shutil.copy2(T/name,E/name)
shutil.copy2(T/'states-final-r9b/selection-proof.json',E/'selection-proof.json')
for slug in ['normal','aldea','porunga']:
 shutil.copy2(T/slug/'build.json',E/(slug+'-build.json'))
 shutil.copy2(T/'states-final-r9b'/slug/'capture-manifest.json',E/(slug+'-capture-manifest.json'))
 for name in [slug+'-ROM.png',slug+'-01-vuelo.png',slug+'-06-pantalla-partida.png']:
  shutil.copy2(O/name,M/name)
 shutil.copy2(T/slug/'compiled-map.png',M/(slug+'-mapa.png'))
for name in ['R9-tres-variantes-ROM.png','Comparacion-R8-R9-1x.png','Casa-y-roca-R8-R9.png','Cielo-Porunga-R8-R9.png']:shutil.copy2(O/name,M/name)
shutil.copy2(T/'normal/house-native.png',M/'house-native.png');shutil.copy2(T/'porunga/porunga-native.png',M/'porunga-native.png')
for name in ['build.py','integrate.py','prepare-scenes.py','record.py','resource_check.py','verify-runtime.py','verify-build.py','package.py']:
 (S/name).write_text((T/name).read_text(encoding='utf-8-sig').rstrip()+'\n',encoding='utf-8',newline='\n')
for name in ['prepare-namek-r9-assets.py','audit-namek-r9-live.py','publish-namek-r9.py']:shutil.copy2(Path('work')/name,S/name)
(S/'README.txt').write_text('R9 native pipeline, 10 November 2026.\nRun from the project root; working dependencies and R6/R7 pipeline resources are required.\nApproved parent ROM: work/combo-startup/candidate.bin. ROM is not included.\nBuild/import resources with prepare-namek-r9-assets.py and build.py, then integrate.py.\nAfter every changed ROM, use a fresh state directory consistently in preparation/recording/verification.\nprepare-scenes.py refuses to reuse an existing seed silently.\nrecord.py captures real ROM output; package.py only scales by integer2x and concatenates.\nNo video or ROM is published. See docs/namek-native-r9.md for scope and pending ground report.\n',encoding='utf-8')
A=R/'assets/concepts/namek-native-r9'
hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in A.iterdir() if p.is_file() and p.name!='manifest.json'}
(A/'manifest.json').write_text(json.dumps(dict(date='2026-11-10',sources={'house':'../namek-house-soft-outline/prueba-borde-suave.png','porunga':'../namek-likeness-study/porunga-anime-study.png','cloud':'../namek-native-r8/cloud-guide.png'},hashes=hashes,nativeApprovalPending=True),indent=2)+'\n',encoding='utf-8')
build=json.loads((T/'integrated-build.json').read_text())
doc=f'''# Namek R9: casa con borde suave y Porunga del anime en la ROM

10 de noviembre de 2026. El usuario acepta la dirección de Porunga del nuevo estudio y el acabado de la casa sin el contorno negro grueso. Pide que ambos se vean bien en la ROM. Se integran los recursos en un build experimental separado: **v1.0 `{build['buildId']}`**, SHA-256 `{build['sha256']}`. El acabado nativo queda pendiente de su valoración.

[Tres capturas reales a tamaño nativo](../assets/media/namek-native-r9/R9-tres-variantes-ROM.png) · [Casa R8/R9, misma escala](../assets/media/namek-native-r9/Casa-y-roca-R8-R9.png) · [Porunga R8/R9, misma escala](../assets/media/namek-native-r9/Cielo-Porunga-R8-R9.png).

## Qué llega al juego

- Casa de58×32: se importa el dibujo de borde suave aceptado, se obtiene un alfa retirando cielo/césped y se conservan puertas y ventanas. No se fuerza el borde oscuro de un píxel que usaba R8. Misma posición345,282 y mismo recurso de color en las tres variantes.
- Porunga de57×80: se importa la nueva postura del anime conservando proporciones, sin ensancharla a72×60 como R8. Se coloca en240,286. Se descarta un borrador en el que la cabeza quedaba bajo el HUD; las capturas finales muestran la figura completa en suelo. El desplazamiento de cámara puede ocultar partes del paisaje al volar o durante las cinematografías del juego.
- Se conservan la roca fina y el cielo nocturno de nubes completas. Las paletas propias son idénticas a R7/R6 y no cambian los10 colores comunes. Un píxel rojo del ojo usa un color ya existente;7 píxeles dentro de la figura se aproximan al banco necesario. Fuera de la figura no hay error de conversión entre bancos.
- Empaquetado exacto, sin otra aproximación de patrones: normal733, devastado732 y Porunga584, con máximo736. La casa tiene el mismo hash en los tres fondos. No se cambia la jugabilidad ni el Namek original.

Porunga, humo, lava y nubes siguen estáticos en el fondo. No se ha añadido un sprite VDP independiente ni flotación. No se aumenta la resolución de la consola ni se promete que el estudio grande conserve todos sus detalles al reducirse.

## Vídeo privado y PNG

Vídeo local de78 s, guardado en `outputs/Namek-R9-revision/DBZ-v1.0-Namek-R9-{build['buildId']}.mp4`: normal0:00, devastado0:26 y Porunga0:52. Incluye vuelo/aterrizaje, básicos y Kamehameha normal/con pantalla partida. Sale del framebuffer y audio de esta ROM, con velocidad normal. El juego320×224 se muestra a escala entera2×, con rótulos externos. No se reemplazan fondos en posproducción. El vídeo no se publica ni se incluye en GitHub. La ROM tampoco se publica.

Capturas completas: [normal](../assets/media/namek-native-r9/normal-ROM.png), [devastado](../assets/media/namek-native-r9/aldea-ROM.png), [Porunga](../assets/media/namek-native-r9/porunga-ROM.png). Mapas completos: [normal](../assets/media/namek-native-r9/normal-mapa.png), [devastado](../assets/media/namek-native-r9/aldea-mapa.png), [Porunga](../assets/media/namek-native-r9/porunga-mapa.png). Recortes finales: [casa](../assets/media/namek-native-r9/house-native.png), [Porunga](../assets/media/namek-native-r9/porunga-native.png).

## Comprobaciones y pendiente del suelo

Se reconstruyen los15 recursos byte a byte y se comprueban los9 embebidos en la ROM. Se seleccionan los tres escenarios desde su menú con estados nuevos del build final. En33 comprobaciones de vuelo, aterrizaje, carga y especiales coinciden los patrones de VRAM y las32 palabras de color. Las nueve tomas mantienen escenario físico6 y variante correcta. FFmpeg decodifica el vídeo completo sin errores. Emulador Genesis Plus GX; consola física pendiente.

**El usuario señala después un recorte con marcas rectangulares repetidas en el suelo. No se consideran corregidas.** La forma exacta no se ha localizado en el mapa actual comparando distintas escalas. Se ha solicitado identificar la imagen o el segundo del vídeo para reproducirla. Una auditoría adicional de1584 fotogramas de la secuencia normal no encuentra sobrescrituras de los gráficos del fondo; esto no descarta un defecto de dibujo, de otro momento o de otra versión. El suelo no se ha repintado a ciegas. R9 sigue para revisión, no es una aprobación final del apartado gráfico.

[Build y cambios permitidos](../evidence/namek-native-r9/integrated-build.json) · [Reproducción de recursos](../evidence/namek-native-r9/reproducibility.json) · [VRAM/paletas](../evidence/namek-native-r9/runtime-validation.json) · [Auditoría continua de gráficos](../evidence/namek-native-r9/live-vram-audit.json) · [Grabación y capítulos](../evidence/namek-native-r9/delivery-manifest.json) · [Fuentes y scripts](../research/namek-native-r9/README.txt).

Procedencia: [casa de borde suave](../assets/concepts/namek-house-soft-outline/prompt.json), [Porunga del anime](../assets/concepts/namek-likeness-study/prompt.json), ambos con image_gen.imagegen. R9 no genera otro dibujo: importa los dos aceptados y los convierte a recursos nativos. [Importación](../assets/concepts/namek-native-r9/import.json) · [Hashes](../assets/concepts/namek-native-r9/manifest.json). Los estudios originales y R6/R7/R8 se conservan.
'''
(R/'docs/namek-native-r9.md').write_text(doc,encoding='utf-8',newline='\n')
p=R/'README.md';s=p.read_text(encoding='utf-8');parts=s.split('\n\n');parts=[p for p in parts if not p.startswith(('**10/11 · Casa:','**Última valoración:'))]
lead='**Revisión actual: Namek R9 en la ROM.** Casa con borde suave y nuevo Porunga basado en el anime, manteniendo su proporción. [**Tres capturas reales**](assets/media/namek-native-r9/R9-tres-variantes-ROM.png) · [**Casa R8/R9**](assets/media/namek-native-r9/Casa-y-roca-R8-R9.png) · [**Porunga R8/R9**](assets/media/namek-native-r9/Cielo-Porunga-R8-R9.png). Vídeo privado de78 s en local, suelo/vuelo/especiales a velocidad normal. Build v1.0 `'+build['buildId']+'`. **Pendiente de valoración y de localizar el recorte de marcas rectangulares señalado en el suelo; no se da por corregido.** [Cambios, PNG completos y comprobaciones](docs/namek-native-r9.md).'
parts.insert(2,lead);p.write_text('\n\n'.join(parts),encoding='utf-8',newline='\n')
p=R/'docs/decisions.md';s=p.read_text(encoding='utf-8');heading,rest=s.split('\n',1);entry='\n\n**10/11/2026 — R9 integrada; revisión del suelo abierta:** se aceptan la dirección de Porunga del anime y la casa de borde suave. Se integran en una ROM experimental y se graban los tres Namek, suelo, vuelo y especiales. Se corrige la posición para mostrar la cabeza de Porunga bajo el HUD. El usuario señala marcas repetidas del suelo: no se ha identificado el recorte exacto ni se da por corregido. Vídeo privado local; aprobación nativa pendiente. [R9 y límites](namek-native-r9.md).\n'
p.write_text(heading+entry+rest,encoding='utf-8',newline='\n')
p=R/'docs/namek-likeness-study.md';s=p.read_text(encoding='utf-8');heading,rest=s.split('\n',1);p.write_text(heading+'\n\n**Estado posterior:** los dos dibujos se han integrado en [R9](namek-native-r9.md) para revisar su resultado real en la ROM. Los estudios siguientes se conservan como procedencia. El resultado nativo sigue pendiente de valoración.\n'+rest,encoding='utf-8',newline='\n')
print('R9 records saved; private video stays outside repository')

"""Publicar documentación, fuentes y PNG; los vídeos y ROM siguen locales."""
from pathlib import Path
import json,hashlib,shutil
T=Path('work/namek-native-r8');O=Path('outputs/Namek-R8-revision');R=Path('repository')
M=R/'assets/media/namek-native-r8';E=R/'evidence/namek-native-r8';S=R/'research/namek-native-r8';A=R/'assets/concepts/namek-native-r8'
for p in [M,E,S]:p.mkdir(parents=True,exist_ok=True)
for name in ['R8-tres-variantes-ROM.png','Comparacion-R6-R8-1x.png','Casa-y-roca-R6-R8.png','Cielo-Porunga-R6-R8.png']:shutil.copy2(O/name,M/name)
rows=[]
for slug in ['normal','aldea','porunga']:
 for src,dst in [(O/(slug+'-ROM.png'),M/(slug+'-ROM.png')),(O/(slug+'-mapa-512.png'),M/(slug+'-mapa.png')),(T/slug/'build.json',E/(slug+'-build.json'))]:shutil.copy2(src,dst)
 for label in ['01-vuelo','06-pantalla-partida']:shutil.copy2(O/(slug+'-'+label+'.png'),M/(slug+'-'+label+'.png'))
 report=json.loads((T/slug/'build.json').read_text());rows.append(f"| {slug} | {report['tiles']} | {report['outsideEditedRegionsChangedPixels']} | {report['paletteErrorsOutsideDragon']} |")
for name in ['integrated-build.json','runtime-validation.json','reproducibility.json','delivery-manifest.json']:shutil.copy2(T/name,E/name)
shutil.copy2(T/'states-final-r8/selection-proof.json',E/'selection-proof.json')
for slug in ['normal','aldea','porunga']:shutil.copy2(T/'states-final-r8'/slug/'capture-manifest.json',E/(slug+'-capture-manifest.json'))
for name in ['house-native.png','porunga-native.png']:
 src=T/('normal' if name.startswith('house') else 'porunga')/name
 shutil.copy2(src,M/name)
for name in ['build.py','integrate.py','prepare-scenes.py','record.py','resource_check.py','verify-runtime.py','verify-build.py','package.py','publish-records.py']:
 (S/name).write_text((T/name).read_text(encoding='utf-8-sig').rstrip()+'\n',encoding='utf-8',newline='\n')
sources={name:hashlib.sha256((A/name).read_bytes()).hexdigest() for name in ['house-source.png','porunga-guide.png','cloud-guide.png','prompts.json']}
(A/'manifest.json').write_text(json.dumps(dict(date='2026-11-09',mode='built-in image_gen.imagegen for dragon and cloud guides; existing transparent house source',dragonSource='exec-3e6dda14-0702-4208-bff4-2e2eed0b904b.png',cloudSource='exec-1c5325a0-e37d-4a3e-8dbd-f81505531946.png',houseSource='namek-native-v1/house.png',hashes=sources,nativeApprovalPending=True),indent=2)+'\n',encoding='utf-8')
build=json.loads((T/'integrated-build.json').read_text())
doc='''# Namek R8: casa definida y cielo de Porunga reconstruido

9 de noviembre de 2026. El usuario vuelve a señalar falta de definición en R6 y franjas/cortes en el cielo de Porunga. La preferencia anterior por R6 no se interpreta como aprobación final: se reabre la revisión. **R8 es una nueva entrega para valorar; R6, R7 y los maestros de arte se conservan.**

[**Los tres fondos R8, capturas reales**](../assets/media/namek-native-r8/R8-tres-variantes-ROM.png) · [R6/R8 a tamaño nativo](../assets/media/namek-native-r8/Comparacion-R6-R8-1x.png) · [Casa y roca, igual escala](../assets/media/namek-native-r8/Casa-y-roca-R6-R8.png) · [Cielo de Porunga, igual escala](../assets/media/namek-native-r8/Cielo-Porunga-R6-R8.png).

El vídeo local dura unos78 s: normal0:00, devastado0:26 y Porunga0:52. Incluye suelo, vuelo de uno y ambos jugadores, aterrizaje, básicos/Kamehameha y ataque grande con pantalla partida. Se graban directamente framebuffer y sonido de la ROM final. La imagen del juego320×224 se muestra a escala entera2× dentro de un archivo640×512 con rótulos externos. No se sustituyen fondos en posproducción ni se acelera el movimiento. El vídeo queda local y no se publica ni se incluye en el repositorio.

## Cambios de esta revisión

- **Casa:** la importación anterior perdía contornos oscuros y comprimía demasiado su altura. Se recupera el alfa del recurso separado, se conservan las líneas oscuras al cuantizar y se reconstruye un contorno nativo de un píxel. Mantiene58 píxeles de ancho y el apoyo enY314; su altura pasa de23 a32 para respetar mejor las proporciones de la fuente. Puerta, ventanas, cúpulas y cuernos se distinguen. El mismo recurso y los mismos colores se usan en los tres escenarios. Se limpia toda la zona ocupada por la casa anterior antes de colocar las nuevas nubes y arquitectura: la oclusión corresponde al alfa de la casa, no a un recorte rectangular del cielo.
- **Roca:** se conservan las vetas finas probadas en R7, en lugar de las grandes manchas planas de R6. No se vuelve a suavizar ese detalle ni a sustituirlo por representantes de otros tiles.
- **Cielo de Porunga:** se eliminan las bandas de verdes y los restos de las nubes anteriores. Se conserva el paisaje conectado al suelo y se limpia el aire, incluidos pequeños bordes grises aislados que la clasificación por colores no eliminaba. Se colocan nubes completas con alfa limpio, dos tonos verdes y márgenes transparentes. Los colores de cielo coinciden exactamente entre bancos; no dependen de la cobertura de cada tile. El cielo vacío queda en azul nocturno uniforme.
- **Porunga:** nueva figura de72×60, con cabeza, cuernos, brazos y cola legibles; se coloca en176,284 para dar más margen respecto al HUD. Usa el verde y marfil existentes. Dos píxeles de ojos rojos usan un color común ya presente: no se modifica la paleta compartida. Se aproxima el color de45 píxeles de la figura cuando su tile utiliza el banco con el rojo; fuera de la figura no hay error de conversión entre bancos.

Las paletas son idénticas byte a byte a R7/R6. El suelo y la jugabilidad se conservan fuera de las regiones documentadas. Humo, lava, nubes y Porunga permanecen estáticos dentro del fondo; no se ha añadido un sprite VDP independiente ni flotación. La revisión mejora el dibujo dentro de la rejilla nativa, no aumenta la resolución de la consola.

## Recursos nativos y límites

| Variante | Patrones, máximo736 | Píxeles cambiados fuera de las zonas editadas | Error de paleta fuera de Porunga |
| --- | ---: | ---: | ---: |
'''+ '\n'.join(rows)+'''

R8 se empaqueta sin pérdida adicional: todos los patrones finales se reproducen exactamente. No usa aproximación global de tiles. Los recursos de partida conservan sus decisiones anteriores de adaptación. En el cielo nocturno se verifica que no quedan píxeles ajenos en el aire vacío y que ninguna franja verde continua supera el ancho de una nube. Los límites no sustituyen la valoración visual.

Mapas completos512×512 decodificados del recurso final: [normal](../assets/media/namek-native-r8/normal-mapa.png), [devastado](../assets/media/namek-native-r8/aldea-mapa.png), [Porunga](../assets/media/namek-native-r8/porunga-mapa.png). Capturas completas: [normal](../assets/media/namek-native-r8/normal-ROM.png), [devastado](../assets/media/namek-native-r8/aldea-ROM.png), [Porunga](../assets/media/namek-native-r8/porunga-ROM.png). Los PNG conservan los colores calibrados de la salida del emulador.

## Comprobaciones y procedencia

'''+f"Build experimental **v1.0 `{build['buildId']}`**, SHA-256 `{build['sha256']}`. Padre general aprobado200852. Se conservan el Namek original y el código de combate. No se entrega ROM.\n\n"+'''
- Los quince archivos de gráficos/mapa/paleta se reproducen byte a byte; nueve recursos embebidos se comprueban contra la ROM final. La casa tiene el mismo hash de color en las tres variantes.
- Tres selecciones reales desde menú, con arranque nuevo de la ROM final. No se reutiliza la VRAM de los borradores anteriores.
- Quince comprobaciones en suelo, vuelo de uno y ambos jugadores, aterrizaje y carga de energía; dieciocho más al iniciar y terminar las tomas, incluido el final de los especiales. Coinciden VRAM,22 colores propios y10 comunes en los33 casos.
- Nueve tomas registran escenario físico6 y variante correcta en todos los fotogramas. En las muestras, básicos/Kamehameha mantienen88 de daño y el ataque grande58. Los clips son coordinados para revisar los fondos, no partidas espontáneas ni pruebas de balance.
- Vídeo decodificado completo con FFmpeg. Se inspeccionan capturas de suelo, vuelo y cinematografía de los tres escenarios. Probado en Genesis Plus GX; consola física pendiente.

[Build y escrituras permitidas](../evidence/namek-native-r8/integrated-build.json) · [Reproducción de recursos](../evidence/namek-native-r8/reproducibility.json) · [VRAM y paleta completa](../evidence/namek-native-r8/runtime-validation.json) · [Tomas y vídeo local](../evidence/namek-native-r8/delivery-manifest.json) · [Fuentes](../research/namek-native-r8/README.txt).

Guías creadas con la herramienta integrada **image_gen.imagegen**: [Porunga](../assets/concepts/namek-native-r8/porunga-guide.png) y [nube](../assets/concepts/namek-native-r8/cloud-guide.png). La [casa transparente](../assets/concepts/namek-native-r8/house-source.png) es el recurso existente de namek-native-v1, con la importación corregida. [Prompts completos](../assets/concepts/namek-native-r8/prompts.json) · [Hashes y procedencia](../assets/concepts/namek-native-r8/manifest.json). Estas imágenes fuente no son capturas del juego. Los recortes nativos [casa58×32](../assets/media/namek-native-r8/house-native.png) y [Porunga72×60](../assets/media/namek-native-r8/porunga-native.png) permiten revisar qué detalle llega a la ROM.
'''
(R/'docs/namek-native-r8.md').write_text(doc,encoding='utf-8')
(S/'README.txt').write_text('NAMEK R8 - REVISION DE DEFINICION\n\nFuentes de la adaptacion, importacion de alfa/contorno, reconstruccion del\ncielo, integracion, captura directa y comprobaciones de la ROM. Requieren\nel entorno privado, ROM base, recursos R7, helpers anteriores, Genesis Plus\nGX, Python, Pillow, NumPy y FFmpeg. No son una distribucion autonoma del juego.\nNo se incluyen ROM, estados, DLL ni los videos de revision privados.\nR8 conserva versiones anteriores y queda pendiente de valoracion visual.\n',encoding='utf-8')
print('R8 records saved; videos remain local',flush=True)

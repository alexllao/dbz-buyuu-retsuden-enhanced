"""Guardar fuentes, PNG y evidencias; mantener los vídeos de revisión locales."""
from pathlib import Path
import json,hashlib,shutil
T=Path('work/namek-native-r7');O=Path('outputs/Namek-roca-R7');R=Path('repository')
M=R/'assets/media/namek-rock-r7';E=R/'evidence/namek-rock-r7';S=R/'research/namek-rock-r7'
for p in [M,E,S]:p.mkdir(parents=True,exist_ok=True)
for name in ['Comparacion-ROM-1x.png','Comparacion-ROM-2x.png','Detalle-roca-misma-escala.png','Referencia-original-R6-R7-1x.png']:
 shutil.copy2(O/name,M/name)
for slug in ['normal','aldea','porunga']:
 shutil.copy2(O/(slug+'-ROM.png'),M/(slug+'-ROM.png'));shutil.copy2(O/(slug+'-mapa.png'),M/(slug+'-mapa.png'));shutil.copy2(T/slug/'build.json',E/(slug+'-build.json'))
for name in ['integrated-build.json','runtime-validation.json','delivery-manifest.json','comparison-validation.json','reproducibility.json']:shutil.copy2(T/name,E/name)
shutil.copy2(T/'states-final/selection-proof.json',E/'selection-proof.json')
for name in ['build.py','integrate.py','prepare-scenes.py','record.py','verify-runtime.py','package.py','verify-build.py','publish-records.py']:
 text=(T/name).read_text(encoding='utf-8-sig').rstrip()+'\n';(S/name).write_text(text,encoding='utf-8',newline='\n')
guide=R/'assets/concepts/namek-rock-r7/guia-textura.png'
source=dict(date='2026-11-09',mode='built-in image_gen.imagegen',guideSha256=hashlib.sha256(guide.read_bytes()).hexdigest(),sourceOutput='exec-0269863c-8fc5-46d5-ab9e-87e126d88a03.png',prompt='prompt.json',nativeApprovalPending=True)
(guide.parent/'manifest.json').write_text(json.dumps(source,indent=2)+'\n',encoding='utf-8')
build=json.loads((T/'integrated-build.json').read_text());rows=[]
for slug in ['normal','aldea','porunga']:
 b=json.loads((T/slug/'build.json').read_text());rows.append(f"| {slug} | {b['tiles']} | {b['rockChangedPixels']} | {b['treeChangedPixels']} | {b['budgetAdjustmentPixels']} |")
doc='''# Namek R7: prueba de textura fina en la ROM

9 de noviembre de 2026. El usuario señala que R6 se ve muy pixelado y aporta una captura. Cumplir las restricciones de Mega Drive no resolvía el acabado: las grandes manchas planas de las mesetas perdían detalle frente a las vetas del fondo original. **R7 es una prueba pendiente de valoración; los maestros aprobados y R6 se conservan.**

[**Comparación de la roca a la misma escala**](../assets/media/namek-rock-r7/Detalle-roca-misma-escala.png) · [Pantallas completas a1x](../assets/media/namek-rock-r7/Comparacion-ROM-1x.png) · [A2x](../assets/media/namek-rock-r7/Comparacion-ROM-2x.png) · [Fondo del juego, R6 y R7 a1x](../assets/media/namek-rock-r7/Referencia-original-R6-R7-1x.png).

Vídeos locales, sin publicar ni copiar al repositorio: `Comparacion-ROM-R6-R7.mp4` (unos20 s, ambas ROM a la misma escala entera2x) y `Namek-R7-ROM-tres-escenarios.mp4` (unos78 s, los tres fondos con vuelo, básicos/Kamehameha y pantalla partida). Carpeta de entrega: `outputs/Namek-roca-R7`. Se captura el framebuffer y sonido reales del emulador; la comparación solo recorta los rótulos anteriores y coloca las dos capturas juntas. No reemplaza fondos ni acelera animaciones.

## Qué cambia

Se genera una [guía de vetas finas](../assets/concepts/namek-rock-r7/guia-textura.png) con la herramienta integrada image_gen.imagegen, usando el mapa R6 y la roca nativa original como referencias. [Prompt completo](../assets/concepts/namek-rock-r7/prompt.json) · [Procedencia y hash](../assets/concepts/namek-rock-r7/manifest.json). La guía generada no se presenta como una captura de juego: se importa a la rejilla nativa, se cuantiza y se comprueba después dentro de la ROM.

Solo se importan índices dentro de las rocas y algunas copas ya existentes. La intersección con la geometría del normal protege también a Porunga y el humo cuando ocupan las mismas cajas. La paleta es idéntica byte a byte a R6; los píxeles de cielo, suelo, casa y cualquier región exterior a esas máscaras quedan intactos. La silueta se conserva. El cambio en las copas es pequeño; la mejora principal es el sombreado y las vetas de la roca.

No se aplica el filtrado de consolidación de ruido de R6 sobre las nuevas vetas, para conservar sus detalles a un píxel. Se deduplican patrones idénticos y sus reflejos. Normal y devastado caben sin aproximación adicional. Porunga requiere reducir cinco patrones: se sustituyen detalles próximos dentro de tiles totalmente interiores a la roca, ponderando más sus bordes. El informe registra111 cambios de píxel en ese ajuste respecto a la importación inicial.

| Variante | Patrones finales, máximo736 | Píxeles de roca cambiados frente aR6 | Píxeles de copa cambiados | Ajuste por presupuesto |
| --- | ---: | ---: | ---: | ---: |
'''+ '\n'.join(rows)+'''

La resolución del juego continúa siendo320×224 y el mapa512×512. No se elimina la cuadrícula propia del pixel art; se prueba un dibujo con más detalle dentro de la misma cuadrícula. Lava, humo y Porunga continúan estáticos.

## Comprobaciones

'''+f"ROM experimental v1.0 build `{build['buildId']}`, SHA-256 `{build['sha256']}`. Padre general aprobado200852, sin cambios de jugabilidad. No se entrega ROM.\n\n"+'''
- Quince archivos de recursos reproducidos byte a byte y nueve recursos embebidos comprobados contra la ROM final. Las tres paletas siguen idénticas aR6 y no cambia ningún píxel fuera de las máscaras editadas.
- Quince comprobaciones en el emulador de los gráficos y22 colores propios cargados: suelo, vuelo de uno y de ambos jugadores, aterrizaje y aura. Los escenarios se seleccionan con mandos desde un arranque nuevo, sin reutilizar VRAM antigua.
- Nueve tomas de la ROM final, con escenario y variante correctos en todos los fotogramas. La comparación usa normal: vuelo437f y pantalla partida775f. Entradas y estado de ambos personajes coinciden exactamente con R6 en los1212 fotogramas de origen comparados.
- Ambos vídeos se decodifican completos con FFmpeg. Capturas a1x y2x sin suavizado; el vídeo mantiene la velocidad normal. Consola física pendiente.

[Build](../evidence/namek-rock-r7/integrated-build.json) · [Reproducción de recursos](../evidence/namek-rock-r7/reproducibility.json) · [VRAM y CRAM](../evidence/namek-rock-r7/runtime-validation.json) · [Comparación de estados](../evidence/namek-rock-r7/comparison-validation.json) · [Tomas y vídeo local](../evidence/namek-rock-r7/delivery-manifest.json) · [Fuentes de investigación](../research/namek-rock-r7/README.txt).
'''
(R/'docs/namek-rock-r7.md').write_text(doc,encoding='utf-8')
(S/'README.txt').write_text('NAMEK R7 - PRUEBA DE TEXTURA FINA\n\nFuentes locales para adaptar solo rocas y copas, integrar y grabar la ROM.\nRequieren el entorno privado, la ROM base, recursos R6, helpers de captura,\nGenesis Plus GX, Python, Pillow, NumPy y FFmpeg. No son una distribucion\nautonoma del juego. No se incluyen ROM, estados, DLL ni los videos privados.\n\nLa guia imagegen es una fuente de textura; la evidencia final es la ROM\ny sus capturas nativas. R7 queda pendiente de valoracion del usuario.\n',encoding='utf-8')
print('Saved R7 sources, screenshots and evidence; videos remain local',flush=True)

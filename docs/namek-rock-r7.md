# Namek R7: prueba de textura fina en la ROM

9 de noviembre de 2026. El usuario señala que R6 se ve muy pixelado y aporta una captura. Cumplir las restricciones de Mega Drive no resolvía el acabado: las grandes manchas planas de las mesetas perdían detalle frente a las vetas del fondo original. **R7 es una prueba pendiente de valoración; los maestros aprobados y R6 se conservan.**

[**Comparación de la roca a la misma escala**](../assets/media/namek-rock-r7/Detalle-roca-misma-escala.png) · [Pantallas completas a1x](../assets/media/namek-rock-r7/Comparacion-ROM-1x.png) · [A2x](../assets/media/namek-rock-r7/Comparacion-ROM-2x.png) · [Fondo del juego, R6 y R7 a1x](../assets/media/namek-rock-r7/Referencia-original-R6-R7-1x.png).

Vídeos locales, sin publicar ni copiar al repositorio: `Comparacion-ROM-R6-R7.mp4` (unos20 s, ambas ROM a la misma escala entera2x) y `Namek-R7-ROM-tres-escenarios.mp4` (unos78 s, los tres fondos con vuelo, básicos/Kamehameha y pantalla partida). Carpeta de entrega: `outputs/Namek-roca-R7`. Se captura el framebuffer y sonido reales del emulador; la comparación solo recorta los rótulos anteriores y coloca las dos capturas juntas. No reemplaza fondos ni acelera animaciones.

## Qué cambia

Se genera una [guía de vetas finas](../assets/concepts/namek-rock-r7/guia-textura.png) con la herramienta integrada image_gen.imagegen, usando el mapa R6 y la roca nativa original como referencias. [Prompt completo](../assets/concepts/namek-rock-r7/prompt.json) · [Procedencia y hash](../assets/concepts/namek-rock-r7/manifest.json). La guía generada no se presenta como una captura de juego: se importa a la rejilla nativa, se cuantiza y se comprueba después dentro de la ROM.

Solo se importan índices dentro de las rocas y algunas copas ya existentes. La intersección con la geometría del normal protege también a Porunga y el humo cuando ocupan las mismas cajas. La paleta es idéntica byte a byte a R6; los píxeles de cielo, suelo, casa y cualquier región exterior a esas máscaras quedan intactos. La silueta se conserva. El cambio en las copas es pequeño; la mejora principal es el sombreado y las vetas de la roca.

No se aplica el filtrado de consolidación de ruido de R6 sobre las nuevas vetas, para conservar sus detalles a un píxel. Se deduplican patrones idénticos y sus reflejos. Normal y devastado caben sin aproximación adicional. Porunga requiere reducir cinco patrones: se sustituyen detalles próximos dentro de tiles totalmente interiores a la roca, ponderando más sus bordes. El informe registra111 cambios de píxel en ese ajuste respecto a la importación inicial.

| Variante | Patrones finales, máximo736 | Píxeles de roca cambiados frente aR6 | Píxeles de copa cambiados | Ajuste por presupuesto |
| --- | ---: | ---: | ---: | ---: |
| normal | 732 | 5226 | 49 | 0 |
| aldea | 734 | 4877 | 108 | 0 |
| porunga | 736 | 4960 | 294 | 111 |

La resolución del juego continúa siendo320×224 y el mapa512×512. No se elimina la cuadrícula propia del pixel art; se prueba un dibujo con más detalle dentro de la misma cuadrícula. Lava, humo y Porunga continúan estáticos.

## Comprobaciones

ROM experimental v1.0 build `20261109-173255`, SHA-256 `1e12cd036f5c0bb9ef464f6e428d9ee2df32a17e5b80ac67fbfb2330c06373b4`. Padre general aprobado200852, sin cambios de jugabilidad. No se entrega ROM.


- Quince archivos de recursos reproducidos byte a byte y nueve recursos embebidos comprobados contra la ROM final. Las tres paletas siguen idénticas aR6 y no cambia ningún píxel fuera de las máscaras editadas.
- Quince comprobaciones en el emulador de los gráficos y22 colores propios cargados: suelo, vuelo de uno y de ambos jugadores, aterrizaje y aura. Los escenarios se seleccionan con mandos desde un arranque nuevo, sin reutilizar VRAM antigua.
- Nueve tomas de la ROM final, con escenario y variante correctos en todos los fotogramas. La comparación usa normal: vuelo437f y pantalla partida775f. Entradas y estado de ambos personajes coinciden exactamente con R6 en los1212 fotogramas de origen comparados.
- Ambos vídeos se decodifican completos con FFmpeg. Capturas a1x y2x sin suavizado; el vídeo mantiene la velocidad normal. Consola física pendiente.

[Build](../evidence/namek-rock-r7/integrated-build.json) · [Reproducción de recursos](../evidence/namek-rock-r7/reproducibility.json) · [VRAM y CRAM](../evidence/namek-rock-r7/runtime-validation.json) · [Comparación de estados](../evidence/namek-rock-r7/comparison-validation.json) · [Tomas y vídeo local](../evidence/namek-rock-r7/delivery-manifest.json) · [Fuentes de investigación](../research/namek-rock-r7/README.txt).

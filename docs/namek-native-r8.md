# Namek R8: casa definida y cielo de Porunga reconstruido

**Valoración posterior: casa y Porunga rechazados por falta de parecido.** R8 queda archivada como prueba; los controles técnicos no validan el dibujo. [Estudio posterior y pendientes](namek-likeness-study.md).

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
| normal | 736 | 0 | 0 |
| aldea | 736 | 0 | 0 |
| porunga | 592 | 0 | 0 |

R8 se empaqueta sin pérdida adicional: todos los patrones finales se reproducen exactamente. No usa aproximación global de tiles. Los recursos de partida conservan sus decisiones anteriores de adaptación. En el cielo nocturno se verifica que no quedan píxeles ajenos en el aire vacío y que ninguna franja verde continua supera el ancho de una nube. Los límites no sustituyen la valoración visual.

Mapas completos512×512 decodificados del recurso final: [normal](../assets/media/namek-native-r8/normal-mapa.png), [devastado](../assets/media/namek-native-r8/aldea-mapa.png), [Porunga](../assets/media/namek-native-r8/porunga-mapa.png). Capturas completas: [normal](../assets/media/namek-native-r8/normal-ROM.png), [devastado](../assets/media/namek-native-r8/aldea-ROM.png), [Porunga](../assets/media/namek-native-r8/porunga-ROM.png). Los PNG conservan los colores calibrados de la salida del emulador.

## Comprobaciones y procedencia

Build experimental **v1.0 `20261109-182600`**, SHA-256 `d32e0d412ffc3f977bc25767fd2cd7258a4e69a089bce58717f92c047d23dc06`. Padre general aprobado200852. Se conservan el Namek original y el código de combate. No se entrega ROM.


- Los quince archivos de gráficos/mapa/paleta se reproducen byte a byte; nueve recursos embebidos se comprueban contra la ROM final. La casa tiene el mismo hash de color en las tres variantes.
- Tres selecciones reales desde menú, con arranque nuevo de la ROM final. No se reutiliza la VRAM de los borradores anteriores.
- Quince comprobaciones en suelo, vuelo de uno y ambos jugadores, aterrizaje y carga de energía; dieciocho más al iniciar y terminar las tomas, incluido el final de los especiales. Coinciden VRAM,22 colores propios y10 comunes en los33 casos.
- Nueve tomas registran escenario físico6 y variante correcta en todos los fotogramas. En las muestras, básicos/Kamehameha mantienen88 de daño y el ataque grande58. Los clips son coordinados para revisar los fondos, no partidas espontáneas ni pruebas de balance.
- Vídeo decodificado completo con FFmpeg. Se inspeccionan capturas de suelo, vuelo y cinematografía de los tres escenarios. Probado en Genesis Plus GX; consola física pendiente.

[Build y escrituras permitidas](../evidence/namek-native-r8/integrated-build.json) · [Reproducción de recursos](../evidence/namek-native-r8/reproducibility.json) · [VRAM y paleta completa](../evidence/namek-native-r8/runtime-validation.json) · [Tomas y vídeo local](../evidence/namek-native-r8/delivery-manifest.json) · [Fuentes](../research/namek-native-r8/README.txt).

Guías creadas con la herramienta integrada **image_gen.imagegen**: [Porunga](../assets/concepts/namek-native-r8/porunga-guide.png) y [nube](../assets/concepts/namek-native-r8/cloud-guide.png). La [casa transparente](../assets/concepts/namek-native-r8/house-source.png) es el recurso existente de namek-native-v1, con la importación corregida. [Prompts completos](../assets/concepts/namek-native-r8/prompts.json) · [Hashes y procedencia](../assets/concepts/namek-native-r8/manifest.json). Estas imágenes fuente no son capturas del juego. Los recortes nativos [casa58×32](../assets/media/namek-native-r8/house-native.png) y [Porunga72×60](../assets/media/namek-native-r8/porunga-native.png) permiten revisar qué detalle llega a la ROM.

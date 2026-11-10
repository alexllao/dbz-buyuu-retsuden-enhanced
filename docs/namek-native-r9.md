# Namek R9: casa con borde suave y Porunga del anime en la ROM

10 de noviembre de 2026. El usuario acepta la dirección de Porunga del nuevo estudio y el acabado de la casa sin el contorno negro grueso. Pide que ambos se vean bien en la ROM. Se integran los recursos en un build experimental separado: **v1.0 `20261110-082044`**, SHA-256 `40e7d04b2e725938322070d3d0f02a95caa870248ccba76f8386cf3524dc5d21`. El acabado nativo queda pendiente de su valoración.

[Tres capturas reales a tamaño nativo](../assets/media/namek-native-r9/R9-tres-variantes-ROM.png) · [Casa R8/R9, misma escala](../assets/media/namek-native-r9/Casa-y-roca-R8-R9.png) · [Porunga R8/R9, misma escala](../assets/media/namek-native-r9/Cielo-Porunga-R8-R9.png).

## Qué llega al juego

- Casa de58×32: se importa el dibujo de borde suave aceptado, se obtiene un alfa retirando cielo/césped y se conservan puertas y ventanas. No se fuerza el borde oscuro de un píxel que usaba R8. Misma posición345,282 y mismo recurso de color en las tres variantes.
- Porunga de57×80: se importa la nueva postura del anime conservando proporciones, sin ensancharla a72×60 como R8. Se coloca en240,286. Se descarta un borrador en el que la cabeza quedaba bajo el HUD; las capturas finales muestran la figura completa en suelo. El desplazamiento de cámara puede ocultar partes del paisaje al volar o durante las cinematografías del juego.
- Se conservan la roca fina y el cielo nocturno de nubes completas. Las paletas propias son idénticas a R7/R6 y no cambian los10 colores comunes. Un píxel rojo del ojo usa un color ya existente;7 píxeles dentro de la figura se aproximan al banco necesario. Fuera de la figura no hay error de conversión entre bancos.
- Empaquetado exacto, sin otra aproximación de patrones: normal733, devastado732 y Porunga584, con máximo736. La casa tiene el mismo hash en los tres fondos. No se cambia la jugabilidad ni el Namek original.

Porunga, humo, lava y nubes siguen estáticos en el fondo. No se ha añadido un sprite VDP independiente ni flotación. No se aumenta la resolución de la consola ni se promete que el estudio grande conserve todos sus detalles al reducirse.

## Vídeo privado y PNG

Vídeo local de78 s, guardado en `outputs/Namek-R9-revision/DBZ-v1.0-Namek-R9-20261110-082044.mp4`: normal0:00, devastado0:26 y Porunga0:52. Incluye vuelo/aterrizaje, básicos y Kamehameha normal/con pantalla partida. Sale del framebuffer y audio de esta ROM, con velocidad normal. El juego320×224 se muestra a escala entera2×, con rótulos externos. No se reemplazan fondos en posproducción. El vídeo no se publica ni se incluye en GitHub. La ROM tampoco se publica.

Capturas completas: [normal](../assets/media/namek-native-r9/normal-ROM.png), [devastado](../assets/media/namek-native-r9/aldea-ROM.png), [Porunga](../assets/media/namek-native-r9/porunga-ROM.png). Mapas completos: [normal](../assets/media/namek-native-r9/normal-mapa.png), [devastado](../assets/media/namek-native-r9/aldea-mapa.png), [Porunga](../assets/media/namek-native-r9/porunga-mapa.png). Recortes finales: [casa](../assets/media/namek-native-r9/house-native.png), [Porunga](../assets/media/namek-native-r9/porunga-native.png).

## Comprobaciones y pendiente del suelo

Se reconstruyen los15 recursos byte a byte y se comprueban los9 embebidos en la ROM. Se seleccionan los tres escenarios desde su menú con estados nuevos del build final. En33 comprobaciones de vuelo, aterrizaje, carga y especiales coinciden los patrones de VRAM y las32 palabras de color. Las nueve tomas mantienen escenario físico6 y variante correcta. FFmpeg decodifica el vídeo completo sin errores. Emulador Genesis Plus GX; consola física pendiente.

**El usuario señala después un recorte con marcas rectangulares repetidas en el suelo. No se consideran corregidas.** La forma exacta no se ha localizado en el mapa actual comparando distintas escalas. Se ha solicitado identificar la imagen o el segundo del vídeo para reproducirla. Una auditoría adicional de1584 fotogramas de la secuencia normal no encuentra sobrescrituras de los gráficos del fondo; esto no descarta un defecto de dibujo, de otro momento o de otra versión. El suelo no se ha repintado a ciegas. R9 sigue para revisión, no es una aprobación final del apartado gráfico.

[Build y cambios permitidos](../evidence/namek-native-r9/integrated-build.json) · [Reproducción de recursos](../evidence/namek-native-r9/reproducibility.json) · [VRAM/paletas](../evidence/namek-native-r9/runtime-validation.json) · [Auditoría continua de gráficos](../evidence/namek-native-r9/live-vram-audit.json) · [Grabación y capítulos](../evidence/namek-native-r9/delivery-manifest.json) · [Fuentes y scripts](../research/namek-native-r9/README.txt).

Procedencia: [casa de borde suave](../assets/concepts/namek-house-soft-outline/prompt.json), [Porunga del anime](../assets/concepts/namek-likeness-study/prompt.json), ambos con image_gen.imagegen. R9 no genera otro dibujo: importa los dos aceptados y los convierte a recursos nativos. [Importación](../assets/concepts/namek-native-r9/import.json) · [Hashes](../assets/concepts/namek-native-r9/manifest.json). Los estudios originales y R6/R7/R8 se conservan.

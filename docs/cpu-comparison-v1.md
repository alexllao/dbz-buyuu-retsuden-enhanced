# CPU contra CPU: original frente a la ROM preparada

Se compara la **ROM japonesa original sin parches**, SHA-256 `217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557`, con **Jugabilidad v1 + Colores v1 + Ki individual v4**, SHA-256 `100b546f0555b014ac8cd01ddd7d12af97b8acf8011a006e2933afcc3a42983b`.

[Ver la comparación completa, lado a lado](../assets/media/cpu-comparison-v1/Comparacion-CPU-original-vs-mod.mp4).

## Método y duración

Seis enfrentamientos de 35 segundos por versión: **209,97 segundos formales por ROM**, unos 3 minutos y medio, con los once personajes. Incluyendo los sondeos previos de activación de IA: **260,99 segundos en el original y 254,98 en la nueva**, ambos por debajo del máximo de cinco minutos.

Cada caso arranca su propia ROM desde el menú nativo y conserva la dificultad, velocidad normal y escenario del torneo. Se activan los dos indicadores nativos de CPU en RAM; no se pulsan botones durante el combate. No se fuerzan vida, posiciones, azar, animaciones ni escenas. El BIN entregado conserva los controles normales para jugar: las marcas de CPU del ensayo no se guardan en la ROM.

La navegación y las selecciones son iguales, pero no se afirma un estado interno idéntico: los tiempos y las decisiones de IA pueden divergir. Las diferencias de vida final no prueban por sí solas mejora, regresión o equilibrio. Los vídeos están sin audio.

| Enfrentamiento | Vida final original P1/P2 | Vida final nueva P1/P2 | Vídeo |
| --- | --- | --- | --- |
| Goku SSJ vs Gohan SSJ2 | 165/157 | 160/163 | [Comparar](../assets/media/cpu-comparison-v1/Combates/01-Goku-SSJ-vs-Gohan-SSJ2.mp4) |
| Recoome vs A18 | 181/160 | 170/168 | [Comparar](../assets/media/cpu-comparison-v1/Combates/02-Recoome-vs-A18.mp4) |
| Ginyu vs Freezer | 168/166 | 190/156 | [Comparar](../assets/media/cpu-comparison-v1/Combates/03-Ginyu-vs-Freezer.mp4) |
| Piccolo vs Cell | 189/135 | 154/157 | [Comparar](../assets/media/cpu-comparison-v1/Combates/04-Piccolo-vs-Cell.mp4) |
| Vegeta SSJ vs Trunks SSJ | 155/155 | 165/181 | [Comparar](../assets/media/cpu-comparison-v1/Combates/05-Vegeta-SSJ-vs-Trunks-SSJ.mp4) |
| Krilin vs Cell | 179/176 | 174/172 | [Comparar](../assets/media/cpu-comparison-v1/Combates/06-Krilin-vs-Cell.mp4) |

## Resultado observado

- Los doce ensayos mantienen la IA nativa activa en ambos jugadores, con acciones y daño. No se observó KO en estos intervalos.
- Cero sospechas de bloqueo según el detector de imagen y contador inmóviles durante cinco segundos fuera de escenas de efectos. Los máximos inmóviles observados fueron sólo unos pocos fotogramas.
- En la nueva ROM, las 20 muestras juzgadas con ki visible de Krilin/Cell conservaron los recursos previstos. Las 2136 muestras de residencia normales coinciden, pero no equivalen a 2136 muestras de ki visible.
- Pico observado de 77/80 sprites y 16/20 por línea en la nueva. La suma conservadora de anchos llegó a 344 en el original y 328 en la nueva en Piccolo/Cell; incluye regiones transparentes o parcialmente fuera de pantalla. Los fotogramas inspeccionados no muestran un fallo visual nuevo evidente. No es una garantía exhaustiva por fotograma.
- Estas partidas no activaron las escenas cinemáticas de especiales: **su restauración natural no queda validada por este ensayo**.

La respuesta del mando, los comandos y la sensación de juego quedan para la prueba manual del usuario. CPU contra CPU sirve aquí como comprobación acotada de estabilidad y comportamiento, no como aprobación de jugabilidad humana.

## ROM reproducible

`pnpm build:auras:v4 --rom ruta/a/original.bin`

La salida de 4 MiB coincide exactamente con la ROM probada. El [IPS y manifiesto](../patches/auras-c2-v4/manifest.json) siguen siendo los mismos; esta prueba no cambió código ni paletas. El BIN se entrega localmente, sin subir la ROM completa al repositorio.

La ROM incluye jugabilidad v1, paletas v1 y ki v4 aceptado visualmente. Presentación G, crédito, retratos de selección, HUD H4 y escenario nevado siguen pendientes de integración.

[Resumen y hashes](../evidence/cpu-comparison-v1/summary.json) · [Auditoría detallada](../evidence/cpu-comparison-v1/comparison-audit.json) · [Activación de CPU](../evidence/cpu-comparison-v1/menu-ai-setup.json) · [Límites y direcciones](../evidence/cpu-comparison-v1/native-ai-findings.json).

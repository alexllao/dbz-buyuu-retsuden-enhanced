# Short de Namek: solo V5

9/11/2026. El usuario pide ver únicamente V5 en movimiento, con carrera, ondas y pantalla partida, en formato YouTube Short. Se entrega un vídeo vertical de **41 s,1080×1920**, conservando el juego y su HUD completos al máximo ancho. No aparecen paneles editoriales de antes/después ni imágenes de otras versiones.

[**Ver Short listo para subir**](../assets/media/short-namek-v5/short.mp4) · [Portada](../assets/media/short-namek-v5/portada.png) · [Título y descripción](short-namek-v5-texto.txt).

El montaje muestra Namek normal con Final Flash y carrera de Vegeta, vuelo en la aldea devastada, Kamehameha grande con pantalla partida, básicos y onda cercana de Goku, vuelo en Porunga y otro Kamehameha a distancia. La pantalla partida es la del propio juego. El rectángulo completo del juego ocupa1080×756 desdeY500 dentro del lienzo vertical; no se recortan personajes, escenario o HUD en edición. Los rótulos quedan fuera de ese rectángulo.

Se mantiene la velocidad nativa de59,9227fps. Solo se recortan las tomas y se añaden fundidos de audio de18/25ms en los cortes. Sonido original, sin música añadida. El fondo del lienzo vertical es sólido, sin otra copia del combate ni panel de comparación.

## Procedencia

Toda la imagen procede del build V5 **`20261109-093419`**, SHA256 `ed28bb56d207f0d0fd12f1cd1e6eff5597c0f8344e6a7bcf39c8b4017c89f2a8`. **La ROM no se modifica para grabar este Short.** Se conservan los colores V4 aprobados y la limpieza del terreno de V5. Porunga continúa estático.

La toma de Vegeta es juego de la **CPU nativa**, con el rival controlado en reposo; incluye un Final Flash y una carrera real por el suelo. En la secuencia de carrera hay79 fotogramas con acción7 yY448, recorriendo deX135 aX599. Goku y las rutas de vuelo se graban con entradas de mando coordinadas. La preparación entre tomas fija distancia/orientación y tipos de control; no se escriben acciones, daño, velocidad o posición durante la grabación.

Se verifican los hashes de los seis vídeos fuente y sus informes de ROM, el escenario/variante por fotograma, las dimensiones del archivo final y su decodificación íntegra con FFmpeg. No se publica automáticamente en YouTube ni se entrega ROM o parche.

## Incidencia de entrada observada

Al preparar la toma,112 pruebas de doble toque manual con Goku/Vegeta en P1, orientados a la derecha, distancia180 y velocidad normal, no activaron las acciones7/8. Se probaron pulsaciones iniciales de1–12f y liberaciones de1–16f. Es un problema de esa ruta pendiente de investigar; no se presenta como una certificación de todos los personajes, puertos o situaciones. **El Short muestra la carrera auténtica de la CPU y no simula ni acelera una carrera manual.** Esta incidencia se registra separada de la aprobación del color y del acabado de Namek.

[Manifiesto y cortes exactos](../assets/media/short-namek-v5/manifest.json) · [Validación](../evidence/short-namek-v5/validation.json) · [Prueba de entrada y alcance](../evidence/short-namek-v5/manual-run-probe.json) · [Fuentes](../research/short-namek-v5/README.txt).

# Auras C2: prototipo real para revisión

**Versión histórica.** La revisión actual es [C2 v2](auras-c2-v2.md), con más tamaño, rayos blancos largos y polvo. Esta primera prueba se conserva íntegra para comparar.

C2 ya tiene una primera implementación en la ROM. Es una **prueba experimental**, pendiente de aprobación visual del usuario; no una versión gráfica final.

[Vídeo de los once personajes, original frente a C2](../assets/media/auras-c2-v1/Todas-las-auras-antes-despues.mp4) · [Salida de Goku a cámara lenta](../assets/media/auras-c2-v1/Salida-Goku-lenta.mp4).

## Adaptación a Mega Drive

El recurso utiliza **64 × 112 píxeles y 45 tiles**. Se conserva la paleta compartida nativa. El boceto C2 sirve como dirección artística: no debe confundirse con una captura ni esperarse una reproducción idéntica de sus detalles y colores.

- Goku y los demás personajes: aura sin rayos.
- Gohan SSJ2 (ID 1) y Cell (ID 5): aura con rayos.
- Retirada al soltar la carga: doce ticks de transición visual.

La revisión debe comprobar el inicio, la carga sostenida, el cierre al soltar, la interrupción por un golpe y el regreso a movimiento/ataques. La evidencia de pruebas está en [validation.json](../evidence/auras-c2-v1/validation.json). Las pruebas del prototipo no sustituyen la revisión visual ni la validación en consola física.

Se han comprobado seis golpes naturales, carga del jugador 2, dos cargas consecutivas y carga simultánea; no quedan sprites residuales en los casos probados. El motor conserva su alternancia de dibujo de las auras, que produce parpadeo. Los doce ticks de salida pueden ocupar más fotogramas si el juego se ralentiza. El polvo del boceto C2 aún no está integrado.

La ilustración de partida se creó con `image_gen`; [su prompt y adaptación](../assets/source/auras-c2-v1/provenance.json) están guardados. Los vídeos son capturas del recurso ya integrado en la ROM.

## Vídeos individuales

Las comparaciones son grabaciones reales del juego, no animaciones generadas del concepto.

| Personaje | Comparación |
| --- | --- |
| Goku | [Antes y después](../assets/media/auras-c2-v1/00-Goku.mp4) |
| Gohan SSJ2 | [Antes y después](../assets/media/auras-c2-v1/01-Gohan-SSJ2.mp4) |
| Piccolo | [Antes y después](../assets/media/auras-c2-v1/02-Piccolo.mp4) |
| Vegeta | [Antes y después](../assets/media/auras-c2-v1/03-Vegeta.mp4) |
| Trunks | [Antes y después](../assets/media/auras-c2-v1/04-Trunks.mp4) |
| Cell | [Antes y después](../assets/media/auras-c2-v1/05-Cell.mp4) |
| Androide 18 | [Antes y después](../assets/media/auras-c2-v1/06-Android-18.mp4) |
| Krilin | [Antes y después](../assets/media/auras-c2-v1/07-Krillin.mp4) |
| Freezer | [Antes y después](../assets/media/auras-c2-v1/08-Freezer.mp4) |
| Recoome | [Antes y después](../assets/media/auras-c2-v1/09-Recoome.mp4) |
| Ginyu | [Antes y después](../assets/media/auras-c2-v1/10-Ginyu.mp4) |

## Archivos versionados

- [Fuente del 68000](../src/auras/c2-v1/aura.asm) y [código hexadecimal](../src/auras/c2-v1/aura.hex).
- [Tiles](../src/auras/c2-v1/tiles.hex) y [mapas](../src/auras/c2-v1/maps.hex).
- [Parche IPS desde la base original](../patches/auras-c2-v1/auras-c2.ips) y [manifiesto](../patches/auras-c2-v1/manifest.json).

El parche de prueba combina Jugabilidad v1, Colores v1 y Auras C2. La ROM completa se genera localmente y no se versiona. La presentación G, el crédito **- 2026 ALEX LLAO**, los retratos de selección y el HUD H4 todavía no están integrados en esta prueba.

Para construirla con tu copia japonesa original:

```sh
pnpm build:auras --rom ruta/a/original.bin
```

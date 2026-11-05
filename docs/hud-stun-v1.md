# Barras de aturdimiento integradas, sin texto

Prueba opcional basada en la versión 5 con reacción original. **Dos barras pequeñas, sin etiquetas**, con borde claro, fondo oscuro y relleno sólido como las barras de vida/ki. Aparecen en las esquinas inferiores:32 × 4 píxeles nativos cada una, reflejadas para mantener la simetría. Se dibujan dentro de la ROM; el vídeo no añade el HUD por encima.

[Grabación real con sonido](../assets/media/hud-stun-v1/Barras-aturdimiento-juego-real.mp4) · [Acumulación](../assets/media/hud-stun-v1/Barras-acumulacion.png) · [Recuperación](../assets/media/hud-stun-v1/Barras-recuperacion.png).

## Lectura de las barras

- Verde: acumulación nativa respecto a la resistencia del personaje.
- Naranja: aviso al aproximarse a tres cuartos de la capacidad.
- Rojo: aturdimiento real activo; el relleno indica el tiempo restante y disminuye cuando se recupera.

La acumulación utiliza los campos originales de cada actor, sin sumar puntos nuevos. La recuperación roja lee su temporizador real, incluida la recuperación más rápida por direcciones y la reducción nativa al recibir golpes. Al terminar o cuando el juego limpia el acumulador, la barra se reinicia. No se inventa una caída gradual independiente de la jugabilidad. Las pausas y cargas nativas también pueden detener la actualización visual.

El cálculo y los umbrales de aturdimiento se conservan. La versión 5 base ya había retirado las ayudas que prolongaban o reiniciaban la reacción de daño. No se acelera la animación de los ataques para mantener cadenas. **El contador global HITS sigue pendiente y no forma parte de esta prueba.**

## Integración gráfica

Se utilizan dos sprites y sólo cuatro patrones en VRAM `AF20..AFA0`. Las mitades verticales de esos patrones contienen las dos barras: el sprite de P2 se refleja; la parte que no corresponde queda fuera de las 224 líneas activas del modo nativo. Esto permite mantener el HUD pequeño sin ocupar patrones de las auras, el desplazamiento, las tablas de planos o la ventana. La tabla de ventana también dibuja parte del escenario y debe conservarse.

Los sprites se insertan temporalmente al transferir la lista nativa. Se respeta la limpieza original de la cabecera y sus salidas de registros/estado. Los píxeles sólo se actualizan en la ruta de VBlank con renderizado preparado; la ruta `6EE8`, que puede interrumpir una carga de gráficos, se conserva intacta. No se reserva RAM persistente ni se escriben campos de los luchadores o colores de paleta.

La capacidad total de hardware es 80 sprites. Si la lista nativa ocupa más de 78, se omiten las barras en esa transferencia para no dañar personajes o efectos. No se observó ese límite en las pruebas de los once personajes: el máximo muestreado fue 72 entradas nativas. No se afirma cobertura de todos los efectos o hardware original.

## Comprobaciones

- 13.200 fotogramas de juego con los once personajes: auras simultáneas, liberación, saltos y comandos de ataque.1.100 muestras verifican los píxeles de las barras contra la acumulación/recuperación nativas, la cabecera de sprites y la ausencia de colisiones con sus patrones.
- 16 lecturas de las barras realmente visibles en capturas: ambos jugadores, acumulación y recuperación; el relleno coincide con los valores nativos, permitiendo un píxel por el momento de muestreo de pantalla.
- 2.157 fotogramas de comparación del HUD superior original: bordes, textos y zonas fijas idénticos. Se excluyen únicamente los interiores variables de vida/ki y los indicadores inferiores a esa zona. Los gráficos del escenario y los gráficos comunes del HUD conservan sus hashes en las muestras de ambos combates.
- 374 casos del cambio de lado y 22 comparaciones de programas, poses y cursores de ataques con el original. Los tiempos de pantalla incluyen pausas y sondeos de entrada; no se afirma equivalencia ciclo a ciclo.

Las pruebas de ejecución corresponden al escenario 0 y al núcleo local Genesis Plus GX. El reparto de memoria y los colores comunes no dependen de la paleta del escenario, pero falta una prueba exhaustiva en todos los escenarios, especiales y consola original. Las capturas son con mandos automatizados y no sustituyen una prueba humana de jugabilidad.

## Construcción y fuentes

`pnpm build:review --rom ruta/a/original.bin --version hud-stun-v1`

v6.6 sigue siendo la construcción predeterminada. **Arrancar desde cero, sin cargar estados guardados de pruebas anteriores.** Esos estados pueden conservar patrones y mapas de una integración anterior.

[ASM](../src/hud/stun-v1/bars.asm) · [Recursos](../src/hud/stun-v1/resources.json) · [Manifiesto](../patches/hud-stun-v1/manifest.json) · [Pruebas de ejecución](../evidence/hud-stun-v1/runtime-validation.json) · [Barras visibles](../evidence/hud-stun-v1/visible-bars-validation.json) · [Comparación gráfica](../evidence/hud-stun-v1/graphics-validation.json) · [Comprobación estática](../evidence/hud-stun-v1/static-validation.json) · [Medios](../evidence/hud-stun-v1/media-validation.json) · [Mecanismo nativo y contador pendiente](hud-hits-stun.md).


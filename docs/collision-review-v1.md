# Revisión de colisiones v1

Se conservan las diferencias naturales de tamaño: Gohan es pequeño y una patada alta puede pasarle por encima. Esto es correcto; no se ampliarán sus cajas para que todos los golpes conecten. **Esta revisión no modifica geometría ni equilibrio.**

## Ver los golpes paso a paso

Abre [visor-colisiones.html](../assets/tools/collision-viewer/visor-colisiones.html) en un navegador. Funciona sin conexión. Elige un ensayo, reproduce despacio o avanza con las flechas. Verde: recibe daño; rojo: ataque activo; amarillo: separación; azul: geometría de guardia.

Hay 13 ensayos y 913 muestras con gráficos nativos y cajas extraídas de la memoria del juego. Es una reconstrucción de poses lógicas sincronizadas con las cajas registradas, no una grabación ni un emulador ejecutando la ROM. Los cuadros de guardia no implican por sí solos que estén activas todas las condiciones de bloqueo.

## Qué hemos comprobado

- Las tablas de colisión, las rutinas examinadas y el selector de golpe cercano/lejos conservan sus bytes originales tanto en Jugabilidad v1 + Colores v1 como en la prueba de Auras C2 v3. Los cambios de tiempos en otras rutinas quedan fuera de esta comparación de bytes.
- 66 comparaciones emparejadas de alcance y otras 96 alrededor del cambio entre golpe cercano y lejano mantienen los mismos resultados observados de contacto, daño y primer impacto entre original y Jugabilidad v1 + Colores v1.
- Las pruebas adicionales con distintos defensores confirman diferencias por tamaño y pose. Se conservan.
- Goku tiene una pequeña franja donde el golpe cercano no alcanza antes de que el juego seleccione el lejano. Se observa también en el original. Es un punto para valorar jugando, no un fallo confirmado ni una modificación aplicada.

La revisión cubre golpes básicos de pie, velocidad normal y un conjunto limitado de enfrentamientos. No permite concluir que estén revisados todos los personajes, guardias, saltos, vuelo, proyectiles, especiales o turbo.

## Ver las cajas en un emulador

[buyuu-hitboxes.lua](../tools/collision/buyuu-hitboxes.lua) es un visor de solo lectura para Gens-rr. Sigue `buyuu-hitboxes-README.txt`. Su API y las direcciones se han contrastado, pero **no se ha ejecutado el script en Gens-rr**. La animación del juego y la carga de gráficos no siempre llegan al mismo tiempo: el retraso visual configurable no garantiza alineación universal. Para valorar las pruebas registradas, usa el HTML.

La fuente es la ROM japonesa con SHA-256 `217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557`. No se incluye la ROM completa.

[Datos y trazas de la revisión](../evidence/collision-v1).

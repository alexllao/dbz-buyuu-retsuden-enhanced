# Cambio de lado sin golpe: revisión v6

**Adelante, atrás, adelante + C**, cerca del rival. Está disponible para los once personajes y para ambos mandos. Las direcciones se invierten al mirar hacia la izquierda. C es el botón de vuelo por defecto; si cambias la asignación de botones, se usa la función asignada al vuelo.

La última dirección y C pueden pulsarse juntos. Haz la secuencia con rapidez. Al mantener C después del cruce no se activa el vuelo; soltarlo devuelve su funcionamiento habitual. Las entradas de A y B conservan las técnicas del original. No pulses A o B junto al comando nuevo.

Sólo se acepta en estados de movimiento, a una separación horizontal máxima de 96 píxeles, en el mismo plano y con una diferencia de altura máxima de 32. No cancela golpes propios, daño, derribos, cargas ni cinemáticas. Los bordes del escenario conservan la limitación del movimiento nativo: puede abortar si no hay espacio al otro lado. La CPU mantiene su repertorio original; esta incorporación se activa con los mandos humanos.

## Corrección sobre el movimiento de Gohan

El usuario señaló que el movimiento original no daba ningún golpe. La comprobación en juego lo confirma: el High Speed Move de Goku, Gohan y Cell **no activa la detección de ataque ni hace daño**. La descripción anterior como técnica ofensiva era incorrecta. Se conservan sus comandos originales → ← → + B; la nueva entrada con C ofrece ese comportamiento al resto del reparto.

Se reutiliza el programa nativo `0x0843`, su animación y las poses existentes. No se han creado sprites nuevos ni cambiado las cajas de colisión. Se conserva la presentación G, Bandai y ALEX LLAO en la misma línea, el reposo terrestre de 12 ticks y el ki v4 sin rayos.

## Grabaciones reales

[Ver los once personajes](../assets/media/side-switch/Todos-cambio-de-lado.mp4). Orden: Goku, Gohan, Piccolo, Vegeta, Trunks, Cell, A18, Krilin, Freezer, Recoome y Ginyu. Cada toma dura aproximadamente dos segundos. Las posiciones iniciales se fijan para repetir el ensayo; la secuencia se introduce con botones reales del emulador, sin forzar el programa, el daño o la animación. Vídeos sin audio.

## Pruebas y límites

- 374 casos del comando real: once personajes con P1 en normal y P2 en turbo, ambos sentidos, salto, C mantenido, ataque posterior y entradas que deben quedar fuera del movimiento nuevo.
- 122 ensayos previos distinguen la entrada original de Gohan y la reutilización del programa en otros personajes. Parte de esos ensayos iniciales activa el programa de forma sintética y está etiquetada como tal; no sustituye a las pruebas del comando real.
- Las tablas de técnicas, el parser original de A/B, el movimiento nativo y las cajas conservan sus bytes de v5.2. Se han probado muestras de las combinaciones A/B, no todas las técnicas, enfrentamientos y situaciones posibles.

[Matriz del comando](../evidence/side-switch/matrix.json) · [Comprobación del movimiento nativo](../evidence/side-switch/native-summary.json) · [Auditoría de la combinación libre](../evidence/side-switch/input-audit.json) · [Cambios permitidos y bytes conservados](../evidence/side-switch/static-verification.json).

Las pruebas se hacen en Genesis Plus GX. La sensación de juego, el equilibrio al dar esta maniobra a todos y el funcionamiento en consola física quedan para revisión del usuario. Arranca la nueva ROM desde cero; no cargues estados de otra versión.

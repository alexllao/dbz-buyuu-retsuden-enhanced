# Combos v4: ritmo natural

Esta prueba responde a la petición de no acelerar los movimientos. Cada ataque termina su animación antes de ejecutar el siguiente. Una orden introducida tras un impacto se guarda en la cola, sin reiniciar el programa, la acción o el cursor del movimiento actual. Se retira el paso instantáneo de ocho píxeles y se desactiva el recorte heredado de dos unidades al final de los básicos.

[**Vídeo largo nuevo: 4 minutos y45 segundos, con sonido**](../assets/media/combos-v4-natural/Combos-v4-ritmo-natural-4min.mp4). Ocho combates o fragmentos con los once personajes, usando dos mandos automatizados. Se conservan los FPS y el audio nativos; no se acelera la reproducción. No es una partida humana ni la IA nativa, y no lleva contador superpuesto. No se fuerzan posición inicial, vida, energía, acciones ni temporizadores; sólo se fija control humano para ambos mandos.

## Patadas rápidas y lanzamiento de Goku

En el vídeo largo, hacia15,32s, el mando automatizado introduce expresamente el comando del Meteor de Goku después de los básicos. Ese especial nativo contiene una ráfaga rápida y lanza al rival. Se ha comparado con la ROM original: coinciden las fases de ataque y la altura máxima del lanzamiento; la duración observada del Meteor varía tres fotogramas. Ninguno activa el modo de vuelo. La otra ráfaga nativa de patadas conserva también sus fases y pequeño salto final originales.

[Comparar Meteor original/mod](../assets/media/combos-v4-natural/Meteor-original-frente-a-mod.mp4) · [A-B-A sin ordenar Meteor](../assets/media/combos-v4-natural/Goku-A-B-A-sin-Meteor.mp4). La prueba A-B-A muestra tres impactos y ambos luchadores permanecen en tierra. Se separan las tomas para distinguir la cadena básica de una técnica nativa ordenada por el controlador. [Comprobaciones](../evidence/combos-v4-natural/goku-meteor-review.json). Esta revisión no modifica la ROM ni elimina los remates nativos.

## Qué cambia al jugar

Se mantienen hasta tres básicos A/B y una técnica propia, con su combinación y requisitos originales. La ampliación sigue siendo para humanos, suelo y velocidad normal. Tras confirmar un impacto, suelta y pulsa el botón siguiente; la orden espera al final natural del ataque actual. La animación del remate también conserva sus datos nativos. Los límites de enlaces y cierre del remate siguen activos.

**Algunas rutas de tres impactos de v3 dejan de conectar** al conservar el final del ataque y quitar el desplazamiento de seguimiento. Los golpes pueden fallar por distancia, retroceso, pose o derribo; no se cambian cajas para impedirlo. La cola funciona para los once personajes y ambos mandos, pero no se afirma que cada orden A-B-A produzca tres impactos. Los once conectan un A y su técnica B nativa de muestra (adelante, abajo+B mirando a la derecha). Las rutas más largas necesitan ajuste por personaje y prueba con mando, sin acelerar animaciones.

Se conserva la ayuda de reacción de daño de pie del rival durante enlaces confirmados: prolonga esa reacción para permitir el enlace y no acelera al atacante. Se mantienen los ajustes previamente acordados de carrera, inercia y levantarse antes tras una caída; no se ha vuelto toda la jugabilidad al estado original. Gráficos, paletas, auras y créditos se conservan.

## Comprobaciones

Se comparan A/B independientes de los once personajes con la ROM original:22 casos conservan programa, orden de poses del ataque y secuencia de unidades del cursor de animación. La primera pose de reposo puede ser1 o2 y se compara aparte. Los tiempos de pantalla incluyen entrada y pausas: quedan registrados, con diferencias de hasta cuatro fotogramas en estas muestras. No se afirma equivalencia ciclo a ciclo ni que todo el combate dure exactamente lo mismo que el original.

Pasan396 casos de cola y límites: ambos mandos en normal, once personajes, orientaciones, mezclas, pulsación mantenida/repetida, fallo, guardia y puerta de turbo. Se registra por separado si se observan tres impactos; esa observación no se convierte en una garantía cuando el alcance original interrumpe la ruta. Pasan374 casos del cambio de lado. Se añaden22 sondeos de técnicas nativas tras un básico: los once conectan la técnica B de muestra, mientras otras órdenes conservan rechazos o fallos nativos.

La verificación estática limita los cambios a los enlaces, sus comprobaciones de contacto/reacción, el código nuevo y la desactivación del recorte de recuperación. Conserva datos nativos de animación, daño, paletas, auras, créditos y cambio de lado. El código de la cola no reinicia el ataque ni desplaza instantáneamente al luchador. No se asegura ausencia universal de infinitos: siguen pendientes defensa real, esquinas, todos los emparejamientos, hardware y equilibrio humano.

## Construcción

`pnpm build:review --rom ruta/a/original.bin --version combos-v4-natural`

La construcción predeterminada permanece en v6.6. Se conservan las pruebas anteriores v1/v2/v3; sus vídeos muestran un comportamiento anterior y no representan esta corrección. Arrancar sin estados guardados de otra versión.

[ASM](../src/gameplay/combos-v4-natural/combos.asm) · [Manifiesto](../patches/combos-v4-natural/manifest.json) · [Tiempos frente al original](../evidence/combos-v4-natural/timing-validation.json) · [Cola y límites](../evidence/combos-v4-natural/matrix.json) · [Técnicas](../evidence/combos-v4-natural/finisher-validation.json) · [Cambio de lado](../evidence/combos-v4-natural/side-regression.json) · [Límites del parche](../evidence/combos-v4-natural/static.json) · [Vídeo](../evidence/combos-v4-natural/video-validation.json).

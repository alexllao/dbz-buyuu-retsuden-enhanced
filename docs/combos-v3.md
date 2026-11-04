# Combos v3: sistema común para los once personajes

Prototipo opcional, pendiente de valoración jugando. Se pueden mezclar hasta **tres básicos A/B de pie** al acertar y rematar con **una técnica propia o Meteor**, introduciendo su comando original. El juego consulta el repertorio del personaje; no asigna el mismo movimiento de Goku a todos. Sólo humanos, suelo y velocidad normal. La construcción por defecto permanece en v6.6.

## Capturas reales

[**Vídeo largo con sonido: 4 min 41 s**](../assets/media/combos-v3/Combos-v3-combates-largos-con-sonido.mp4). Ocho combates o fragmentos de hasta36 segundos, con los once personajes y distintos escenarios. Se usan posiciones iniciales y recursos nativos, sin forzar vida, energía, acciones ni temporizadores. Dos mandos automatizados introducen los movimientos según la situación; no es la IA nativa ni una partida humana. Los combates que llegan a KO muestran hasta tres segundos posteriores, dentro del límite de cada fragmento. El archivo incluye capítulos por enfrentamiento. [Validación](../evidence/combos-v3/long-video-validation.json).

[Los once personajes: A-B-A y una técnica nativa](../assets/media/combos-v3/Combos-v3-once-personajes.mp4) · [Goku: A-B-A → Meteor](../assets/media/combos-v3/Goku-ABA-Meteor.mp4) · [Goku: A-B-A → ráfaga](../assets/media/combos-v3/Goku-ABA-rafaga.mp4).

Son grabaciones reales del emulador, sin audio y sin contador añadido. **El contador todavía no está en la ROM.** Se arranca por los menús y se introducen botones reales; únicamente se fijan posición/orientación iniciales y ambos mandos humanos. No se fuerzan vida, energía, acciones ni temporizadores. Las trazas de vida de los vídeos coinciden con las de los sondeos y se conserva el final y regreso al control.

## Cómo probarlo

Pulsa A cerca del rival, suelta, pulsa B al acertar y después A al conectar la patada. Tras el tercer básico introduce una técnica propia. Mirando a la derecha, **adelante, abajo+B** activa la técnica B nativa que sirve de muestra en los once personajes. Goku también permite rematar con su Meteor: adelante, diagonal abajo-adelante, abajo, diagonal abajo-atrás, atrás, adelante+B. Se mantiene el comando completo; no hay un botón nuevo que regale Meteor a todo el reparto.

También se admiten AAA, BAB o ABB: se limita el número de básicos, no se impone una receta. Esto permite cancelar, pero **no garantiza que todo orden impacte**. El alcance y las poses de daño originales siguen contando: por ejemplo, BAB de A18 falla en esta distancia y una orientación de su ABA puede perder el último puño. AAA o ABB sí enlazan en esas muestras. No se han ampliado cajas ni movido directamente al defensor para fabricar impactos. Hay un paso de seguimiento de hasta ocho píxeles al cancelar un básico cuando existe separación suficiente.

Requiere energía en estado normal (al menos125), sin fatiga. Los especiales conservan sus condiciones propias de energía, distancia, plano, rival y escena; algunas técnicas no admiten iniciarse contra ese estado del rival, y otras arrancan pero fallan por alcance. Una orden no válida no consume un remate ni se sustituye por una técnica ajena. Ginyu conserva su repertorio propio; no se inventa un Meteor equivalente al de Goku.

La ventana tras un básico confirmado es de36 actualizaciones elegibles, suficiente para introducir movimientos largos. Una pulsación durante la pausa de impacto puede aprovechar la cola existente de seis actualizaciones, pero conviene soltar y volver a pulsar claramente; los tiempos de cada animación varían. Las pulsaciones de sólo dos fotogramas no se reconocen de forma uniforme en todos los sondeos; se usan pulsaciones de6/4 fotogramas en la matriz principal. Pendiente de validar sensación con mando.

## Reglas para reducir bucles

- Máximo tres básicos: dos transiciones después del primer impacto confirmado. Fallar o golpear guardia no habilita una cadena.
- Un único remate asistido por cadena. Tras comprometerlo no se cancela hacia básicos ni hacia otro especial.
- Cuando termina el programa nativo del remate se cierran sus excepciones de colisión y prolongación de reacción; otra técnica desde reposo no hereda esas ayudas.
- El presupuesto se reinicia sólo después de seis actualizaciones consecutivas con **ambos luchadores libres**, no por una transición fugaz a reposo del atacante. Recibir daño, abandonar suelo o perder la reacción de pie del rival bloquea la cadena actual.
- Se prolonga/refresca únicamente la reacción de daño de pie necesaria para enlazar. No se alarga la espera en el suelo ni se crea un levantamiento forzado.

Un remate nativo puede tener varios impactos. Por eso tres básicos y una ráfaga pueden superar cuatro impactos reales. **El daño del remate sigue siendo el original**: esta versión no hereda la reducción a un cuarto de las patadas de v2 ni cambia los cálculos del Meteor. El equilibrio de daño necesita una prueba manual. Las reglas acotan las ayudas nuevas; no reescriben todos los enlaces que el juego ya permitía ni demuestran ausencia de cualquier infinito. Las pruebas de repetición muestran presión nativa tras derribo/fatiga, por ejemplo con Gohan: no se ha eliminado globalmente la posibilidad de repetir técnicas una vez acabada su animación. Falta comprobar esas situaciones con defensa real.

## Comprobaciones y alcance

La matriz principal comprende396 casos: once atacantes, ambos mandos en normal, un mando en turbo, ambas orientaciones, distintas mezclas, guardia, fallo, pulsación mantenida y repetida. Se verifica un enlace de tres básicos para cada personaje en ambos mandos/orientaciones, además del máximo de dos transiciones y tres básicos por reacción continua. No se exige que todos los órdenes conecten donde el alcance original no lo permite.

Se sondean176 combinaciones de comandos y energía, con entrada real de la carga A+B. Los once conectan A-B-A y su técnica B nativa de muestra: cuatro descensos reales de vida por toma. La rama cargada sólo llega aproximadamente a148 de energía; no valida por sí sola todos los Meteor que requieren más de205. Las condiciones originales se consultan antes de cancelar y de nuevo en el despacho nativo. El inicio de un movimiento no equivale a demostrar que impacta como combo.

Quince pruebas de repetición mantienen órdenes de especial durante720 fotogramas después de la cadena en cinco atacantes. Se comprueba que no se rearme el presupuesto sin recuperación neutral ni persista la excepción de remate después de acabar su programa. Pasan además374 casos del cambio de lado y ocho comparaciones de técnicas fuera del combo: programas, impactos, daño final, mínimo de energía y acción final. Los instantes de impacto pueden variar un fotograma; no se afirma equivalencia ciclo a ciclo.

Las pruebas usan Goku como defensor. Faltan los121 emparejamientos, esquinas, todas las alturas y estados, hardware original y equilibrio humano. CPU, turbo y combos aéreos no reciben esta ampliación. Paletas, gráficos, auras, créditos, cambio de lado y los demás ajustes de v6.6 se conservan. La ROM experimental se entrega por separado.

## Construcción y fuentes

`pnpm build:review --rom ruta/a/original.bin --version combos-v3`

Arrancar sin estados guardados de otra versión. Se conservan `--version combos-v1`, `--version combos-v2` y v6.6 por defecto. El ASM de estudio completo entregado anteriormente corresponde a v6.2; este parche tiene su propia fuente comentada y bytes verificables.

[ASM](../src/gameplay/combos-v3/combos.asm) · [Manifiesto](../patches/combos-v3/manifest.json) · [Matriz](../evidence/combos-v3/matrix.json) · [Remates](../evidence/combos-v3/finisher-validation.json) · [Repetición](../evidence/combos-v3/repeat-validation.json) · [Cambio de lado](../evidence/combos-v3/side-regression.json) · [Técnicas normales](../evidence/combos-v3/native-regression.json) · [Vídeos](../evidence/combos-v3/video-validation.json) · [Límites del parche](../evidence/combos-v3/static.json).

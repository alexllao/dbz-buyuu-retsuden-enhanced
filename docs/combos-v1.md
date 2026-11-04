# Prueba opcional de combos v1

Goku y Vegeta pueden enlazar dos puños cercanos de pie y cancelar hacia el Energy Blast nativo. **Sólo funciona a velocidad normal y con mandos humanos.** Es un prototipo separado, pendiente de valoración con mando. La ROM predeterminada sigue siendo v6.6; no se da por aprobado el equilibrio de esta prueba.

## Cómo probarlo

Acércate al rival, pulsa A y suéltalo. Cuando conecte el primer puño, pulsa A de nuevo. Tras acertar el segundo, introduce atrás, adelante y pulsa A al final para intentar la salida a Energy Blast. Invierte las direcciones mirando a la izquierda. Se usan las funciones de puño y patada asignadas al mando; el comando descrito corresponde a los botones por defecto.

Requiere energía en estado normal, sin agotamiento. No se habilita al fallar ni al pegar en la guardia. No cancela desde saltos, vuelo, golpes recibidos o derribos. El primer enlace añade un paso de seguimiento de hasta ocho píxeles si el empuje del golpe deja suficiente separación; no mueve al rival ni cambia sus cajas.

Los dos puños sí enlazan antes de que el rival recupere el control en los casos registrados. **El proyectil conserva su salida y alcance nativos: no se garantiza que sea un tercer impacto ininterrumpido ni que acierte siempre.** No se han cambiado sus tablas de daño ni se ha forzado ki o daño desde el parche. La CPU mantiene su repertorio, turbo conserva el combate de v6.6 y los otros nueve personajes no reciben estos enlaces.

## Comparación real

[Goku y Vegeta, v6.6 a la izquierda y prototipo a la derecha](../assets/media/combos-v1/Comparacion-combos-Goku-Vegeta.mp4). También: [Goku](../assets/media/combos-v1/Goku-antes-despues.mp4) y [Vegeta](../assets/media/combos-v1/Vegeta-antes-despues.mp4).

Son grabaciones sin audio de Genesis Plus GX. En cada pareja se reproducen exactamente las mismas pulsaciones. Se fijan posición y orientación iniciales para repetir el ensayo; no se fuerzan HP, ki, programa, acción ni temporizadores. En estas grabaciones el prototipo registra dos daños con Goku y tres con Vegeta; el proyectil de Goku no añade daño en esa toma. Esto ilustra por qué la salida a proyectil no equivale a prometer tres impactos garantizados.

## Vídeo del contador propuesto

[Ver la demostración del contador](../assets/concepts/combo-counter-v1/Contador-combos-demostracion.mp4). **Es una previsualización superpuesta en edición sobre grabaciones reales; el contador todavía no está en la ROM.** La propia imagen del vídeo lo indica durante toda la reproducción.

Se muestran Goku, Vegeta, un bloqueo real y un golpe al aire. El contador aparece desde el segundo impacto observado de una misma cadena, se conserva 36 fotogramas tras la recuperación del rival y se apaga en doce. En la toma de Vegeta, el daño posterior del proyectil ocurre después de la recuperación: abre otra cadena de un golpe y no suma3. Guardia y fallo mantienen el contador oculto. Todas las tomas acaban con el contador oculto.

La lectura usa HP y acciones de daño11/12 de estas tomas de pie; no es un detector general ya validado para todo el juego. El estilo, tamaño y posición son una propuesta pendiente de valorar y de adaptar después a las paletas, tiles y sprites reales de Mega Drive.

[Datos de eventos y validación](../evidence/combo-counter-preview-v1/validation.json).

## Implementación y comprobaciones

El código de prueba se coloca en `0x3D0000`. Se ejecuta tras el reconocimiento nativo de combinaciones y antes de la llamada al cambio de lado. Sólo se habilita para Goku/Vegeta humanos a velocidad normal. Reserva cuatro bytes por actor, `104..107`, separados de los controles `108..10F` y las auras `110..117`.

La ventana de continuación dura doce actualizaciones de entrada tras detectar daño real del puño cercano. Una pulsación conservada durante la pausa nativa de impacto se consume al arrancar el siguiente movimiento. Cuatro comprobaciones de contacto reciben una excepción limitada al segundo puño confirmado: el permiso se retira cuando éste conecta. Se conserva el daño nativo, la geometría, los comandos de especiales y la protección fuera de ese caso.

La exploración inicial detectó una colisión con los campos de las auras al probar una ubicación de estado; se corrigió antes de empaquetar. El prototipo entregado usa `104..107`. El análisis estático de referencias es acotado y no prueba por sí solo que toda la lógica original esté recuperada.

Han pasado 200 casos de la prueba: ambos personajes y mandos, dos orientaciones, pulsaciones mantenidas, presión repetida, guardia, fallo y bloqueo de la función en turbo. Las continuaciones se introducen a partir de los impactos reales en varios tiempos; no se impone un único ritmo fijo a ambos personajes. Se agrupan los impactos en cadenas separadas por recuperación del rival, para no confundir un segundo combo posterior con un tercer golpe infinito del anterior. También pasan los 374 casos de regresión del cambio de lado de los once personajes.

Esto no demuestra ausencia de infinitos en todos los enfrentamientos. Faltan todos los rivales, especiales y situaciones posibles, hardware original y la valoración de sensación y equilibrio con mando. Turbo queda pendiente de una adaptación posterior; los intentos iniciales no dieron márgenes consistentes con Vegeta, por lo que se excluye de esta versión.

## Construir

`pnpm build:review --rom ruta/a/original.bin --version combos-v1`

Sin `--version combos-v1` se sigue generando v6.6. Arrancar sin estados guardados de otras ROM. El mapa ASM modificado de estudio entregado para v6.2 sigue correspondiendo a aquella versión histórica.

[Fuente ASM](../src/gameplay/combos-v1/combos.asm) · [Manifiesto](../patches/combos-v1/manifest.json) · [Matriz de combos](../evidence/combos-v1/matrix.json) · [Regresión del cambio de lado](../evidence/combos-v1/side-regression.json) · [Límites de cambios y bytes conservados](../evidence/combos-v1/static.json) · [Registro de vídeo](../evidence/combos-v1/video.json).

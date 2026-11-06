# Piccolo: contactos del Meteor y cruces ejecutados más seguidos

**Build conservado. La entrega actual añade la corrección de Gohan: [124607](gohan-hits-v1.md).**

**v1.0 · build 20261106-105411 · 6 de noviembre de 2026, 10:54:11 de Madrid.** Se conserva la compilación anterior y se identifica la nueva en el archivo, las dos cabeceras internas de título y el manifiesto.

[**Cruces rápidos P1/P2/P1 y Meteor, juego real**](../assets/media/release-v1-0-build-20261106-105411/Cruces-rapidos-y-Meteor-v1.0-build-20261106-105411.mp4) · [**Piccolo: HITS antes/después simultáneos**](../assets/media/release-v1-0-build-20261106-105411/Piccolo-Meteor-HITS-antes-despues-v1.0-build-20261106-105411.mp4) · [**Anuncio completo actualizado**](../assets/media/release-v1-0-build-20261106-105411/DBZ-Enhanced-v1.0-build-20261106-105411-Anuncio.mp4).

## Cruces más rápidos: ejecución de los mandos

Se ejecutan adelante, atrás y adelante+C durante dos fotogramas por tramo, y el siguiente jugador responde en cuanto termina el cruce anterior y recupera la acción. Se eliminan las esperas largas de la coreografía anterior. La prueba registra tres cruces P1/P2/P1 con intervalos de unos 15–18 fotogramas entre sus inicios, frente a los 40 anteriores, y un Meteor de Goku de tres impactos como remate.

**Esto cambia la ejecución coordinada de los mandos, no la velocidad ni la animación del movimiento en la ROM.** La edición tampoco acelera el vídeo. Se respeta cuándo permite actuar el juego; la demostración no garantiza que el adversario deba aceptar el remate.

## Fallo confirmado del Meteor de Piccolo

El contador omitía siete contactos intermedios de la secuencia capturada. Sólo registraba la entrada inicial y el daño final al caer al suelo, por lo que mostraba 2 HITS.

La rutina nativa de la secuencia `845` emite un sonido de impacto una vez al entrar en los golpes `24`, `30` y `28`, protegida por su propio indicador `CB.0`. Las poses se repiten formando **siete contactos**. La víctima permanece en la reacción nativa `886`; el descuento de vida se aplica agrupado al terminar, no una vez por cada golpe intermedio.

El nuevo enlace cuenta cada uno de esos eventos nativos una vez y sólo si se confirma la víctima en `886`. No se cuenta por cada fotograma que dura una pose, ni se escribe directamente un total de nueve. La entrada y la caída final continúan pasando por los enlaces existentes.

Resultado de la toma: **1 entrada + 7 contactos intermedios + 1 impacto final = 9 HITS**, frente a 2 antes. **43 de daño en ambos casos**, con la misma secuencia de mando y sin modificar movimientos, reacciones, colisiones o fórmulas de daño/mareo. La rutina de contador existente conserva su actualización de la ventana de combo e inactividad al registrar contactos.

## Comprobaciones

Doce casos: ambos mandos, ambos sentidos, acierto, guardia y fallo. Los cuatro aciertos registran siete eventos intermedios, terminan en 9 HITS y causan 43 de daño. Guardia y fallo no añaden contactos. La comparación grabada reproduce el ataque completo en ambos builds a velocidad normal.

El anuncio vuelve a comprobar los ejemplos de Goku, Vegeta y Cell; conserva los ajustes de preparación de Kamehameha y Masenko del [build anterior](ki-startup-v1.md). La revisión se centra en el error reproducido de Piccolo; no certifica que todos los especiales del plantel estén auditados.

La sensación y el equilibrio con mando siguen pendientes de revisión humana. No se ha modificado la velocidad de ningún movimiento para ejecutar los cruces más seguidos.

## ROM

Archivo: `DBZ_Buyuu_Retsuden_Enhanced_v1.0_build_20261106-105411.bin`.

`pnpm build:review --rom ruta/a/original.bin --version v1.0-build-20261106-105411` genera este build. [Manifiesto](../patches/release-v1-0-build-20261106-105411/manifest.json) · [Validación](../evidence/release-v1-0-build-20261106-105411/validation.json).

Arranca desde cero, a velocidad normal y sin estados de la compilación anterior. Los builds `20261106-100534` y `20261106-103002` se conservan como historial.

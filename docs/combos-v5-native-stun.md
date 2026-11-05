# Reacción de daño original: corrección experimental v5

Esta corrección retira las dos ayudas de v4 que podían prolongar el bloqueo del rival: duplicar la duración de su reacción de daño de pie y reiniciar el cursor de esa reacción al conectar otro impacto. Se restaura la llamada de animación nativa, sin modificar las tablas originales de daño o aturdimiento. Se conserva la finalización completa del ataque, sin paso instantáneo de seguimiento.

[Combate real de36 segundos con sonido](../assets/media/combos-v5-native-stun/Goku-Vegeta-reaccion-original.mp4). Son dos mandos automatizados; no es una prueba humana. No se fuerzan vida, energía, temporizadores o acciones. Conservar los tiempos originales rompe algunas rutas de combos anteriores: hay que ajustarlas sin alargar artificialmente el bloqueo.

## Qué se ha comprobado sobre Vegeta

El primer combate del último vídeo v4 se ha reproducido y su vida coincide con la traza guardada. En ese combate concreto no se registra activación del temporizador de aturdimiento de Vegeta, aunque sí hay reacciones de daño y derribos repetidos. Esto no identifica qué otro vídeo anterior vio el usuario ni invalida su observación sobre una sensación de bloqueo excesivo.

En la muestra nueva v5 se observan dos activaciones reales separadas, aproximadamente a10,15s y31,16s. Durante la primera, Vegeta vuelve tres veces a la animación de aturdido tras ser golpeado, con el temporizador restante360,164 y1: **son retornos a un mismo episodio, no tres aturdimientos nuevos**. El juego original permite esa secuencia y reduce el tiempo restante al recibir daño. La barra solicitada debe mostrar ese episodio continuo y sólo marcar una nueva activación cuando realmente vuelva a dispararse el temporizador.

Los dos combates usan la misma estrategia automatizada, pero los botones posteriores cambian al responder a la situación: no son una reproducción idéntica de entradas. Esta muestra no demuestra ausencia universal de presión abusiva ni sustituye una prueba con defensa humana. [Auditoría de ambos combates](../evidence/combos-v5-native-stun/vegeta-review.json).

## Estado y pruebas

Pasan22 comparaciones de ataques independientes con el original,396 casos de cola/límites y374 del cambio de lado. La verificación estática comprueba que la llamada nativa de animación vuelve a estar activa, que no quedan escrituras de reinicio del cursor del rival en el parche y que se conserva el cálculo nativo de aturdimiento/daño y recuperación. Los ataques y su duración no se aceleran para forzar enlaces.

Esta ROMv5no incluye HUD nuevo. Las dos barras sin texto ya están integradas en la prueba posterior [HUD v1](hud-stun-v1.md); el contador global de impactos sigue pendiente. Quedan registrados en [los requisitos del HUD y la explicación del aturdimiento](hud-hits-stun.md). Los vídeos anteriores de contadores superpuestos no equivalen a esa implementación.

Construcción opcional: `pnpm build:review --rom ruta/a/original.bin --version combos-v5-native-stun`. v6.6 permanece como construcción predeterminada. Las versiones anteriores se conservan para comparar; sus vídeos no representan esta corrección. Arrancar sin estados guardados de otra versión.

[ASM](../src/gameplay/combos-v5-native-stun/combos.asm) · [Manifiesto](../patches/combos-v5-native-stun/manifest.json) · [Límites del parche](../evidence/combos-v5-native-stun/static.json) · [Cola/límites](../evidence/combos-v5-native-stun/matrix.json) · [Ataques](../evidence/combos-v5-native-stun/timing-validation.json) · [Cambio de lado](../evidence/combos-v5-native-stun/side-regression.json).

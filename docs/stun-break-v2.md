# Salir del aturdimiento al primer golpe

El usuario eligió que **el primer impacto conectado quite el aturdimiento activo y reinicie su acumulación**. La víctima pasa a la reacción normal de daño; un combo puede continuar según las reglas normales. Esperar o fallar un golpe no libera al rival. Fuera del mareo, los impactos siguen acumulando los puntos originales. No se añade inmunidad temporal: los impactos posteriores pueden volver a acumular aturdimiento.

Esta prueba parte de HUD v1: mantiene las dos barras pequeñas sin texto y sus correcciones gráficas. No acelera ataques ni cambia su daño. El contador global HITS sigue pendiente. Las [propuestas de Namek](namek-anime-v1.md) están guardadas aparte y no incluidas en esta ROM.

[Vídeo real en Namek, 24 segundos y sonido nativo](../assets/media/stun-break-v2/Namek-stun-primer-golpe.mp4).

## Integración

El enlace de seis bytes en `21A0E` se ejecuta después de descartar impactos no aceptados y separar bloqueos. La rutina de 32 bytes en `3B01DE` comprueba el temporizador nativo `actor+36`. Si está activo, llama a la limpieza original `20914`, que borra acumulación `+51` y temporizadores `+32/+34/+36`. Continúa en `21A64` antes de elegir la reacción normal, evitando reactivar el mareo por la acumulación antigua. No se toca `+38`, que no es el temporizador de mareo mostrado por estas barras.

Sin mareo activo, reproduce la comparación original de energía y vuelve a `21A14` con sus banderas. No se fuerzan poses, cursores ni tiempos de reacción. Sólo cambian checksum, enlace y 32 bytes antes vacíos; el HUD, gráficos, paletas, controles, auras y código de combos se conservan.

[ASM de la rutina](../src/gameplay/stun-break-v2/on-hit.asm) · [Hexadecimal](../src/gameplay/stun-break-v2/on-hit.hex) · [ASM completo, base 3B0000](../research/stun-break-v2/hud.asm). Para reensamblar el ASM completo se utiliza el ensamblador conservado en [HUD v1](../research/hud-stun-v1/assemble.ps1).

## Comprobaciones

- 110 ensayos: once víctimas diferentes, P2 normal y P1 turbo; primer puñetazo, primera patada, espera, golpe fallado y acumulación ordinaria. La preparación fija distancia y acumulación a un punto del umbral; un golpe nativo activa el mareo. Los ensayos del primer impacto no fuerzan vida, pose ni temporizador.
- Los 44 primeros impactos conectados limpian temporizador y acumulación en la misma muestra del daño. Después de la reacción no reaparece el mareo sin otro golpe.
- Un proyectil a distancia de Goku contra Vegeta también limpia el mareo al conectar. No se afirma cobertura de todos los especiales o cinemáticas.
- La versión anterior conserva el temporizador después de los mismos puñetazos y patadas en el ensayo de control con Vegeta.
- En el combate grabado sin preparar acumulación, el fotograma 884 muestra vida de Vegeta de 128 a 114, mareo de 235 a 0 y acumulación a 0; continúa la reacción normal `0C`.

[Pruebas](../evidence/stun-break-v2/runtime-validation.json) · [Proyectil](../evidence/stun-break-v2/projectile-validation.json) · [Versión anterior](../evidence/stun-break-v2/previous-version.json) · [Verificación estática](../evidence/stun-break-v2/static-validation.json) · [Evento del vídeo](../evidence/stun-break-v2/demo-events.json).

Construcción: `pnpm build:review --rom ruta/a/original.bin --version stun-break-v2`. La opción predeterminada sigue siendo v6.6. Arrancar desde cero, sin estados anteriores. Las pruebas utilizan Genesis Plus GX; falta validación manual y en consola original.

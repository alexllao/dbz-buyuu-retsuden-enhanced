# K4: más espera tumbado antes de levantarse

El usuario aclara que quiere alargar **la espera tumbado**, no el gesto de incorporarse. K2/K3 estaban ajustando la fase equivocada para esa sensación. K4 parte de K3 y añade tiempo exclusivamente a la última pose de suelo de A1/A4/A5, manteniendo sus segmentos anteriores y los datos de incorporación BF/C0/C1/C2.

[Comparación simultánea K3/K4](../assets/media/knockdown-k4/comparacion.mp4) · [Manifiesto](../patches/knockdown-k4/manifest.json) · [Mediciones](../evidence/knockdown-k4/validation.json)

![Antes empieza a levantarse; propuesta sigue tumbado](../assets/media/knockdown-k4/captura.png)

| Espera desde quedar definitivamente en el suelo hasta empezar a levantarse | Antes K3 | Propuesta K4 |
|---|---:|---:|
| Goku |0,22 s|0,53 s|
| Cell |0,20 s|0,52 s|

Tomas reales a velocidad normal, mismo estado inicial y mandos. Caída, rebote y posición coinciden hasta el momento en que K3 empieza a levantarse. Cada toma se repite dos veces. No se ralentiza el vídeo. La imagen compara el mismo instante: Goku de K3 ya se está incorporando y el de K4 sigue tumbado.

En once personajes con el barrido de Goku a velocidad normal, la espera aumenta 18–19 fotogramas del emulador (aproximadamente 0,30–0,32 s). Los arranques independientes pueden diferir en 1–2 fotogramas de fase; las dos comparaciones de vídeo usan estados idénticos. Los datos del gesto de levantarse son idénticos a K3, aunque su duración medida puede variar unos fotogramas por el motor. No se atribuye esa variación a un cambio deliberado del gesto.

Cambio de datos: último peso de A1/A4/A5 +4; cabecera de duración +16 para conservar la unidad nativa de 4. Marcador aéreo, pesos anteriores y poses sin cambios. Cabecera identificada como **v1.0 K4 build 20261107-102624**. El código de daño, hitstop y filtros de colisión permanece igual. Como la protección nativa depende del estado de reacción, alargar la espera también prolonga ese estado: no se garantiza una protección independiente idéntica.

**Aprobada visualmente por el usuario el 7/11/2026: «k4 perfecto». Se conserva en el paquete K4; la ROM principal 20261106-174207 sigue igual.** Se conserva K3 como historial. No se ha probado turbo, consola real, presión prolongada ni otros derribos; A4 se modifica por la estructura de sus datos pero el barrido usado no activa esa rama.

Construcción: `pnpm build:review --rom ruta/a/original.bin --version knockdown-k4`. El repositorio distribuye el parche IPS y evidencia, sin ROM completa.

## Comparación con la ROM original japonesa

[Vídeo original frente a K4](../assets/media/knockdown-k4/original-vs-K4.mp4). Dos casos, cada uno repetido dos veces. Original a la izquierda; K4 a la derecha. Ambos ejecutan DOWN durante 20 frames, DOWN+B durante 2 y LEFT del defensor desde el frame 20. Posiciones y sentido iniciales iguales. Arranque nativo independiente en original y estado nativo compatible en K4; no se carga un estado modificado en la ROM original. Solo se recortan 1–3 frames iniciales para sincronizar el primer impacto; no se cambia la velocidad. Audio de K4.

| Del golpe a caminar | Original japonesa | K4 |
|---|---:|---:|
| Goku |3,00 s|2,27 s|
| Cell |3,00 s|2,25 s|

La espera definitiva tumbado es 1,05/1,08 s en original y 0,53/0,52 s en K4 (Goku/Cell). La original japonesa es distinta del build modificado 174207 usado en mediciones anteriores. Estos tiempos no deben mezclarse con los de esa base. K4 incluye también los demás cambios del mod, visibles en las paletas y el HUD. [Trazas y condiciones](../evidence/knockdown-k4/original-video-cases.json).

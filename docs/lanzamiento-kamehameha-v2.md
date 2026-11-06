# Lanzar al rival y preparar Kamehameha — prueba de Respuesta v2

6 de noviembre de 2026. Prueba de la ROM existente, **sin modificarla**. SHA-256: `17c1d2789c095cba7d3e66ec7c16af24503899f195b3ca4e9be4fc26889aff74`.

[Vídeo real con sonido, unos 25 segundos](../assets/media/throw-kame-v2/Lanzamiento-y-Kamehameha-en-juego-v2.mp4).

**Sí: Goku puede empezar a preparar Kamehameha antes de que el rival toque el suelo.** Eso no significa que el rayo conecte en el aire o que sea un combo garantizado. En la muestra, preparar pronto falla; esperando al descenso conecta después del primer aterrizaje, y el defensor puede cubrirse para reducir el daño.

| Toma | Preparación del Kamehameha | Resultado |
| --- | --- | --- |
| 1. Temprana | Fotograma 78; el rival está en Y=298 y aterriza por primera vez en el 128. | El rayo no conecta. El rival pierde sólo los 12 HP del lanzamiento. |
| 2. Durante el descenso | Fotograma 119; el rival está en Y=403 y aterriza por primera vez en el 130. | Los 12 HP del lanzamiento se aplican al aterrizar. El Kamehameha añade 60 HP de daño en el fotograma 217. |
| 3. Rival cubriéndose | Misma secuencia y comienzo de preparación en el 119. | Manteniendo atrás, el rival reduce el daño del Kamehameha a 30 HP, además de los 12 del lanzamiento. |

El suelo está en Y=448; los fotogramas se cuentan desde el comienzo de cada toma a unos 59,92 fps. El lanzamiento tiene rebote, por lo que «primer aterrizaje» no implica que toda su reacción haya terminado. El daño de 12 HP del lanzamiento no se atribuye al Kamehameha aunque Goku ya esté preparándolo cuando se descuenta.

Se usa Goku contra Vegeta con ambos puertos humanos. El ki se carga mediante A+B antes de grabar. Se fija la separación y orientación inicial para reproducir el agarre; no se fuerzan HP, reacciones, impactos ni temporizadores. En las dos primeras tomas el rival no pulsa botones; en la tercera mantiene atrás desde el comienzo del comando de Kamehameha.

## Incidencia pendiente de entradas después del lanzamiento

Además del vídeo se probaron diez demoras entre terminar la recuperación de Goku e introducir el comando. En cuatro de esas diez entradas concretas no llegó a arrancar el Kamehameha; en las otras seis sí. No se ha aislado la causa con este ensayo.

Esto amplía la revisión pendiente del buffer: las 200 variantes anteriores, ejecutadas desde sus estados preparados, no garantizan el reconocimiento en todas las transiciones del combate. Hace falta comprobar específicamente la salida del agarre y el estado del rival lanzado. Esta prueba registra el problema; **no incluye una corrección ni una ROM nueva**.

[Resultados de las tres tomas](../evidence/throw-kame-v2/recording.json) · [Diez pruebas de demora](../evidence/throw-kame-v2/probe.json) · [Guía de la ROM utilizada](respuesta-v2.md).

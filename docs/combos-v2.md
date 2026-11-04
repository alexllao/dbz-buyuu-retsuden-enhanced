# Combos v2: dos puños y remate de patadas

**A, soltar A, A al conectar, B después del segundo impacto.** Prueba opcional para Goku y Vegeta humanos, en suelo y a velocidad normal. Se conserva v6.6 como construcción por defecto y Combos v1 como versión anterior. La valoración visual, de sensación y de equilibrio sigue pendiente del usuario.

## Vídeo real

[Ver ambos remates](../assets/media/combos-v2/Combos-v2-punetazos-y-patadas.mp4). El combate sí es la ROM ejecutada: **el contador es superpuesto y todavía no está en la ROM**. También están las tomas [limpia de Goku](../assets/media/combos-v2/Goku-combo-real-sin-contador.mp4) y [limpia de Vegeta](../assets/media/combos-v2/Vegeta-combo-real-sin-contador.mp4).

| Personaje | Secuencia observada | Daño de la toma |
| --- | --- | --- |
| Goku | Dos puños + tres impactos de su ráfaga nativa; **5 impactos enlazados** | 41 de 200 HP |
| Vegeta | Dos puños + dos impactos de su remate nativo; **4 impactos enlazados** | 23 de 200 HP |

Entre el primer y el último impacto de cada toma no se observa recuperación del rival. Ambos actores vuelven al reposo al final. El último impacto de Vegeta provoca el derribo nativo. La toma conserva ese final y el regreso posterior al control. Las grabaciones son sin audio, arrancan por menús nativos y usan entradas reales; sólo se fijan posición y orientación iniciales, sin imponer vida, energía, programas, acciones ni temporizadores.

## Comportamiento de la prueba

Los dos puños cercanos se enlazan al acertar. B se acepta tras confirmar el segundo y puede aprovechar la cola de seis actualizaciones existente si se pulsa durante la pausa del impacto. No sirve pulsar A+B juntos ni mantener vuelo. Fallar o golpear la guardia no habilita la cadena. Requiere energía en estado normal, sin agotamiento.

El remate reutiliza Flurry Kick de Goku, programa nativo `0803`, y el programa `0815` de Vegeta. No se fuerza la animación de Goku sobre Vegeta. Se aceleran sus fases sólo cuando se usan como remate de esta cadena. Al enlazar se aplica un paso corto de seguimiento, ocho píxeles en el primer enlace y hasta dieciséis al rematar cuando hay separación suficiente; no se reposiciona directamente al rival.

Para hacer un combo real, el segundo impacto refresca la reacción de daño de pie. Durante el remate confirmado se refresca esa reacción al recibir un impacto y se amplía su tiempo de animación mientras queda presupuesto de patadas. Sólo se aplica a acciones de daño de pie `0B/0C`; no amplía derribos ni añade una espera en el suelo. Al acabar el remate deja de aplicarse.

El remate admite como máximo tres daños de patada. Una vez consumidos, se impiden nuevos contactos de daño durante las fases restantes del movimiento. Los daños positivos del remate se reducen a un cuarto, con mínimo uno, antes del descuento normal de vida. No se añaden daños sólo por reproducir una animación. La fuente y las trazas permiten revisar estas reglas; no se afirma que todos los movimientos de todo el juego hayan sido revisados.

Turbo y la CPU no reciben el atajo. Los otros nueve personajes conservan su combate anterior. Las paletas, los gráficos, los datos nativos de animación, la intro, el título, ambos créditos y las auras se conservan.

## Comprobaciones y límites

Pasan 200 casos del prototipo: ambos mandos y orientaciones, tiempos de continuación, guardia, fallo, pulsación mantenida y presión repetida. Se comprueba la cadena completa en normal, su límite de impactos y vuelta a reposo. En turbo se comprueba que el atajo queda desactivado. Pasan además los 374 casos del cambio de lado de los once personajes.

Ocho sondeos comparan patadas y combinaciones B introducidas normalmente, fuera de A-A-B: conservan programas observados, cantidad de impactos, daño final, mínimo de ki y estado final. No son equivalentes ciclo a ciclo: hay impactos con un fotograma de diferencia y una toma de Goku acaba con dos unidades menos de ki; los valores están registrados. El parche no añade escrituras de ki. La energía final incluye recuperación pasiva y no se afirma idéntica.

Las pruebas no cubren todos los rivales, alturas, esquinas y especiales, ni demuestran ausencia universal de infinitos. Se ha probado contra el defensor predeterminado Goku. Faltan pruebas humanas de equilibrio y hardware original. El contador continúa siendo una propuesta de vídeo; su detector y sus fuentes aún deben implementarse para Mega Drive.

## Construcción

`pnpm build:review --rom ruta/a/original.bin --version combos-v2`

Sin esta opción se sigue generando v6.6. La prueba anterior se conserva con `--version combos-v1`. Arrancar sin estados guardados de otra versión. El mapa ASM modificado completo de estudio entregado anteriormente corresponde a v6.2; este prototipo conserva su propio ASM comentado y bytes revisables.

[Fuente](../src/gameplay/combos-v2/combos.asm) · [Manifiesto](../patches/combos-v2/manifest.json) · [Matriz](../evidence/combos-v2/matrix.json) · [Regresión del cambio de lado](../evidence/combos-v2/side-regression.json) · [Ataques fuera del combo](../evidence/combos-v2/native-regression.json) · [Validación del vídeo](../evidence/combos-v2/video-validation.json) · [Límites de modificación](../evidence/combos-v2/static.json).

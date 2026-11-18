# Recuperación del rival al finalizar el combo aéreo

18 de noviembre de 2026. **v1.0 build `20261118-150132`**, SHA-256 `87c5802b4ba677b2b5c3443e08d105a0a9fe7cdf758f45f6bfdd3c9415569cc0`. Alex señala que el rival se levanta demasiado rápido tras recibir el remate. Se confirma un fallo de la caída nueva: al llegar al suelo se borraban programa y reloj y se forzaba el estado neutro, saltándose rebote, espera tumbado e incorporación.

Se devuelve el control al motor conservando programa, reloj y reacción en las acciones nativas13..16. Esto incluye el derribo A1 del Kamehameha y la caída fuerte C6 de Final Flash/Super Kamehameha. Las tablas de K4 y de incorporación permanecen idénticas byte a byte. No se añade un temporizador arbitrario ni se ralentiza el vídeo. El sonido de aterrizaje corregido en145200 se conserva.

| Ejemplo | Espera desde el último apoyo definitivo hasta empezar a incorporarse |
| --- | --- |
| Goku: Kamehameha sobre Freezer |32 fotogramas /0,53 s. Ruta normal con K4. |
| Vegeta: Final Flash sobre Goku |41 fotogramas /0,68 s. Reacción fuerte nativa C6. |
| Goku: Super Kamehameha sobre Freezer |45 fotogramas /0,75 s. Reacción fuerte nativa C6. |

La reacción fuerte conserva sus propios tiempos: no se afirma que C6 tenga exactamente la espera K4 de A1. Antes, el rival pasaba directamente a reposo al primer contacto con el suelo; ahora conserva también el rebote y el gesto de levantarse. En las tomas fuertes el motor puede pasar después a mareo si su estado ya lo requiere; la corrección deja de borrar esa reacción, sin cambiar su fórmula ni declarar resuelta la auditoría de stun/HITS.

**Comparación real antes/después de tres casos**, misma velocidad, audio de la nueva ROM: `outputs/Recuperacion-K4-Combos-Aereos/Antes-despues-recuperacion-K4.mp4`. [Kamehameha](../assets/media/air-pursuit-knockdown/comparacion-1.png) · [Final Flash](../assets/media/air-pursuit-knockdown/comparacion-2.png). La comparación llega al final del gesto de incorporación, aunque después quede un estado nativo de mareo; ese punto no significa siempre recuperar el control.

**Short v4:27,655 s**, con fragmentos más largos para mostrar la recuperación: `outputs/YouTube-Short-Persecuciones-Aereas-v4/DBZ-Combos-Aereos-Short.mp4`. Pantalla/HUD completos, audio nativo y velocidad normal. [Texto para YouTube](short-air-pursuit-v4-texto.txt), sin preguntas ni menciones a IA en el texto público. Los vídeos anteriores se conservan como histórico.

Se repiten28 casos de enlace, ambos mandos/sentidos, con verificación de sonido al aterrizar y retorno de fases, más10 negativos. Los daños de las cinco capturas siguen89/92/114. La comparación comprueba que el rival conserva su reacción al tocar suelo y mide espera/incorporación; se decodifican los vídeos completos y se revisan fotogramas de las tres rutas. Se conservan los límites del prototipo: mando, hardware, equilibrio, interrupciones/KO de la cola, lectura extrema y auditoría general de HITS/stun pendientes.

[Matriz](../evidence/air-pursuit-knockdown/matrix.json) · [Mediciones de recuperación](../evidence/air-pursuit-knockdown/recovery-validation.json) · [Negativos](../evidence/air-pursuit-knockdown/negative.json) · [Short v4](../evidence/air-pursuit-knockdown/short-manifest.json) · [ASM comentado](../research/air-pursuit-knockdown/pursuit.asm).

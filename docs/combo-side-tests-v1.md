# Combos, cambio de lado y remates: prueba real

Se prueban las combinaciones pedidas sobre **Ventaja v1, sin modificar de nuevo la ROM**. La grabación dura **1 min 37 s**, con diez tomas independientes, sonido nativo y velocidad normal. Incluye la recuperación y vuelta al control; no se recortan las animaciones para encadenar.

[Ver vídeo completo](../assets/media/combo-side-tests-v1/Combos-cambio-de-lado-y-remates.mp4).

## Secuencias grabadas

| Tiempo aproximado | Personaje y secuencia |
| --- | --- |
| 00:00 | GOKU | BASICOS - CAMBIO DE LADO - METEOR |
| 00:10 | GOKU | BASICOS - CAMBIO DE LADO - ESPECIAL |
| 00:18 | GOKU | CAMBIO DE LADO - RAFAGA NATIVA |
| 00:24 | GOKU | CAMBIO DE LADO - METEOR CONTRA GUARDIA |
| 00:29 | VEGETA | BASICOS - CAMBIO DE LADO - METEOR |
| 00:39 | VEGETA | P1 COMBO Y CRUCE - P2 CONTRA Y METEOR |
| 00:51 | PICCOLO | BASICOS - CAMBIO DE LADO - ESPECIAL |
| 00:58 | PICCOLO | BASICOS - CRUCE - ACERCAMIENTO - REMATE |
| 01:11 | CELL | BASICOS - CAMBIO DE LADO - ESPECIAL |
| 01:19 | CELL | BASICOS - CRUCE - ACERCAMIENTO - REMATE |

Los básicos AAA conectan tres descuentos de vida con Goku, Piccolo y Cell en estas muestras; Vegeta conecta dos. Los remates activan sus programas nativos propios: Goku `83E`, Vegeta `846`, Piccolo `844` y Cell `84A`. Se incluyen la ráfaga de Goku, Meteor contra guardia y una respuesta de P2: Goku devuelve el cambio de lado de Vegeta y conecta su Meteor por 35 de daño.

## Qué funciona y qué no significa

**Hay huecos de defensa entre los básicos, el cruce y el remate.** El vídeo muestra cadenas de presión y reposicionamiento; no demuestra un combo cerrado desde el primer puño hasta el final. Que una técnica empiece tampoco basta: se registran por separado su programa, daño y recuperación. El Meteor de Goku contra guardia queda bloqueado y hace sólo 3 de daño residual.

El cambio de lado actual sigue exigiendo que termine el ataque propio: no se ha añadido una cancelación de ataques en curso. Mantiene su ventana de seis actualizaciones para dos mandos humanos, con defensa y respuesta C disponibles. Los comandos completos de los remates tardan más que esa ventaja y no obtienen un golpe garantizado.

AAA, ABA, ABB y BAB no se comportan igual: las animaciones completas, alcance y retroceso rompen algunas rutas. De los 52 sondeos se conservan también los fallidos o incompletos. Las tomas elegidas no convierten esos fallos en éxitos ni prueban equilibrio frente a un jugador que se defiende activamente.

## Condiciones nativas de los remates

Vegeta y Cell exigen **ki por encima de 205 y vida estrictamente inferior a un cuarto del máximo**, además de sus otras condiciones originales. Las tomas parten respectivamente de 42 y 38 de vida, con 232 de ki. Esa preparación se obtiene recibiendo puñetazos reales del segundo mando y cargando con A+B; no se asigna vida o energía directamente.

Para Cell se verificó el comando **↓ ↘ → ← + B**, invertido al mirar a la izquierda, que entra en el token `1A` y programa `84A` de Needle Rush. La secuencia larga anterior no lo activaba en estos ensayos; se corrige la tabla del README con el comando comprobado. En las ramas iniciales con vida alta no se debe confundir una patada ordinaria con ese remate.

Goku y Piccolo pueden usar sus remates sin esa condición de vida baja. Piccolo necesita acercarse después del cruce para conectar en estas tomas; el acercamiento se hace caminando con el mando, no moviendo al personaje desde fuera.

[Filas y condiciones nativas auditadas](../evidence/combo-side-tests-v1/native-requirements.json).

## Procedencia y límites

Dos mandos coordinados, con un defensor pasivo salvo las pruebas de guardia o contra. Se restaura una preparación por toma y se fija sólo la separación/orientación inicial; durante la grabación no se escriben posiciones, vida, ki, acciones o temporizadores. Los rótulos externos identifican la secuencia; no hay contador HITS falso ni impactos añadidos en edición. Los descuentos de vida registrados no equivalen a un contador universal de impactos de todas las cinemáticas.

Se verifica la vuelta al control en las diez tomas. Faltan valoración humana, defensa activa general, todos los emparejamientos, esquinas y cobertura de hardware. No se declara ausencia de infinitos. No se ha cambiado la ROM ni se han aplicado las propuestas pendientes de Namek.

[Resumen verificable](../evidence/combo-side-tests-v1/validation.json) · [52 sondeos](../evidence/combo-side-tests-v1/probes.json) · [Tiempos de capítulos](../evidence/combo-side-tests-v1/chapters.json) · [Reglas de ventaja vigentes](side-advantage-v1.md).

Las muestras completas de entrada y estado están comprimidas como JSON gzip junto a los resúmenes `clip-00` a `clip-09` en `evidence/combo-side-tests-v1`, con sus hashes. Las fuentes de los generadores se conservan en `research/combo-side-tests-v1`.

# HUD global: impactos y dos barras de aturdimiento

Cambio posterior elegido por el usuario: [Stun v2](stun-break-v2.md) termina el mareo al primer impacto aceptado y reinicia su acumulación. El análisis nativo de este documento describe el original y las versiones anteriores a ese cambio.

Estado: las dos barras sin texto están integradas en la prueba opcional [HUD v1](hud-stun-v1.md). El contador global ya está integrado en [HUD HITS v2](hud-hits-v2.md), visible desde2; esta página conserva los requisitos y el estudio nativo previo. No presentar una superposición de vídeo como HUD implementado. El Meteor comparado entre el original y v4 conserva el mismo movimiento; aquella comparación era una comprobación de conservación, no una mejora del ataque.

## Contador de impactos

Un contador por atacante, independiente del prototipo de combos. Debe registrar cualquier impacto confirmado: puños, patadas, técnicas de varios golpes, cada proyectil de una ráfaga de Cell que conecte, patadas múltiples de Goku y los impactos de un Meteor aunque se inicie solo. Debe funcionar para ambos jugadores y no depender de haber iniciado A-A-B o A-B-A.

Contar el primer impacto internamente; por la indicación posterior del usuario, mostrar sólo a partir de2 impactos. Sumar por contacto aceptado o por un evento de impacto verificado de una técnica cinematográfica que ya ha conectado; no por cada fotograma de animación, partícula o rayo dibujado. Un rayo que falla no suma. La guardia no suma como golpe recibido; si se desea un contador de bloqueo será otra función. Evitar contar dos veces un contacto que atraviesa varias rutinas.

No usar sólo la reducción de vida: algunos ataques cinematográficos aplican el daño conjunto al final y eso no representa el número de golpes. Falta auditar sus eventos internos y comprobar todos los especiales; no inventar cantidades a partir de la apariencia. Una animación de aturdido que reaparece no constituye por sí sola un nuevo impacto ni debe mantener indefinidamente abierto un combo.

## Dos barras inferiores

Una en la esquina inferior izquierda y otra en la derecha, asociadas inequívocamente al jugador de ese lado. Leer la acumulación real de cada actor y su resistencia propia: fracción visible igual a acumulado dividido entre umbral, limitada entre0y100%. No modificar el cálculo de jugabilidad para que la barra resulte más vistosa.

Al activarse el aturdimiento real, distinguir ese estado visualmente del simple peligro de llegar al límite. El indicador activo debe leer el temporizador nativo; al recuperarse y reiniciarse el valor nativo, la barra debe reflejarlo. Una misma fase de aturdimiento puede reanudar su animación tras otros golpes sin iniciar un episodio nuevo. El HUD no debe anunciar una nueva activación por cada regreso de esa animación.

La [corrección posterior de acumulación](hud-hits-v1.md) reinicia el temporizador nativo32 en cada impacto aceptado: la limpieza600 pasa a corresponder a inactividad. El texto siguiente describe el comportamiento original.

## Cómo lo calcula el original

Hay dos mecanismos distintos:

- **Reacción de daño:** el breve intervalo tras un impacto en que el rival no puede actuar. Depende del programa de reacción y sus tiempos de animación; dos reacciones de pie tienen12y30 unidades nominales a velocidad normal. No equivalen siempre a ese número exacto de fotogramas de vídeo, porque existen pausas y otras puertas de actualización. v3/v4 añadían prolongación y reinicio para sostener cadenas; v5 retira ambas ayudas.
- **Aturdimiento acumulado:** los golpes elegibles suman la carga definida para ese ataque. Se compara con la resistencia del defensor. Goku tiene umbral22 y Vegeta21; un puñetazo cercano de Goku tiene carga4. Hay condiciones de energía, estado y excepciones de ciertas técnicas: una barra llena indica peligro, pero no garantiza que cualquier técnica active inmediatamente el aturdimiento.

El temporizador base del aturdimiento es360 actualizaciones, escalado por la velocidad nativa. El jugador puede recuperarse antes pulsando direcciones. En la prueba automatizada del original, recuperar sin pulsaciones tomó393 fotogramas; alternar direcciones cada dos fotogramas tomó53. Son mediciones de esa situación, no tiempos universales garantizados. Recibir daño durante el aturdimiento reduce el temporizador activo en60, con mínimo1, en la ruta examinada: no lo reinicia a360.

El acumulador se borra al recuperarse y existe además una limpieza periódica nativa con contador600 escalado mientras no está activo el temporizador de aturdimiento. No se ha observado una barra que decaiga suavemente por sí sola; el HUD debe reflejar el valor real. No se debe presentar esa limpieza como un temporizador de inactividad reiniciado en cada golpe, porque esa regla no está establecida en el código examinado.

### Referencias para implementación

Actor P1 en RAM`E75E`, P2 en`E886`. Acumulador: byte`+51`; resistencia: byte`+54`; temporizador de aturdimiento: word`+36`; contador periódico: word`+32`. La carga del ataque se consulta por personaje atacante y tipo de golpe en la tabla dirigida por`2277E`, byte2del registro de cuatro bytes. La suma está en`21A32`, comparación/activación en`2174E..2176E`, recuperación en`1A52C..1A576`, limpieza en`20914`y`12FBA..12FDC`. Los campos sólo son lecturas para el HUD.

[Auditoría y umbrales de los once personajes](../evidence/stun-native/audit.json) · [Revisión de Vegeta](../evidence/combos-v5-native-stun/vegeta-review.json) · [Corrección de reacción original](combos-v5-native-stun.md).

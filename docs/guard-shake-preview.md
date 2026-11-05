# Impacto y vibración: pruebas visuales

## Prueba variada: contactos suaves y remates tipo B

[Ver 1:06 alternando actual y propuesta](../assets/media/shake-varied-preview/Impactos-variados-actual-y-propuesta.mp4).

El usuario propone la intensidad B en los Meteor para dar dinamismo. Esta prueba distribuye el efecto: contactos normales, bloqueos e impactos intermedios suaves; remates de multigolpe y último contacto del Meteor con intensidad B. El HUD queda quieto. El cambio de lado no produce sacudida por sí mismo.

| Situación | Actual | Propuesta |
| --- | --- | --- |
| Tres bloqueos |0:00|0:08|
| Ataque multigolpe |0:15|0:21|
| Meteor de Goku solo |0:27|0:36|
| Tres golpes →cruce →Meteor |0:44|0:55|

Se usan las mismas grabaciones para cada pareja, sin acelerar ni cortar las animaciones y con sonido nativo. 1 píxel nativo adicional para contactos suaves, 2 para el remate B. El encuadre común evita bordes vacíos y se aplica por igual a ambas variantes.

**Es una previsualización sobre las grabaciones; aún no modifica la ROM.** Pendiente de validación de la sensación general antes de integrar. Conservados 3984 cuadros, 66,49 segundos y 15 contactos distintos; las dos versiones de cada toma tienen el mismo número de cuadros. [Registro y eventos](../evidence/shake-varied-preview/manifest.json).

## Prueba anterior de bloqueos: A/B/C

[Ver 23 segundos con tres intensidades](../assets/media/guard-shake-preview/Bloqueos-vibracion-A-B-C.mp4).

- **A:** movimiento actual, con el mismo encuadre de comparación.
- **B:** sacudida adicional horizontal suave, equivalente a 2 píxeles nativos.
- **C:** algo más marcada, equivalente a 3 píxeles nativos.

Cada pasada usa los mismos tres bloqueos reales, sonido y velocidad natural. La sacudida dura pocos cuadros y el HUD permanece quieto. **B y C son una previsualización aplicada sobre la grabación; no están integradas en la ROM.** Pendiente de elección del usuario antes de implementar la intensidad elegida. La versión HUD HITS v3 conserva la reacción original del bloqueo.

[Registro del montaje y eventos](../evidence/guard-shake-preview/manifest.json).

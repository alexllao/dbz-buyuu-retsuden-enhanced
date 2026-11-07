# Decisiones vigentes

**7/11/2026 — prueba K4:** alargar la espera tumbado, no el gesto de levantarse. Goku 0,22 → 0,53 s; Cell 0,20 → 0,52 s. [Comparación y estado pendiente](knockdown-k4.md).

**7/11/2026 — prueba K3:** K2 no resultó perceptible al usuario. Recuperar duraciones originales de incorporación; mantener caída/espera de K1. Mostrar K1/K2/K3 ampliadas a velocidad normal. [Vídeo y estado pendiente](knockdown-k3.md).

**7/11/2026 — prueba K2:** el usuario nota que K1 se incorpora demasiado rápido. Mantener su espera corta y probar una incorporación intermedia. [Comparación K1/K2](knockdown-k2.md). K2 pendiente de validar, principal 174207 sin cambios.

**7/11/2026 — prueba K1:** el usuario pide acortar bastante los derribos y ver antes/después. Recuperación breve en una variante separada, pendiente de validar. [Vídeo, tiempos y alcance](knockdown-k1.md). La ROM principal 174207 se conserva.

**6/11/2026 — build174207:** revisión de HITS de los diez Meteor; correcciones en Krilin, Freezer, A18 y Trunks. Cell validado a13 contactos y a11 con KO previo. Sacudidas añadidas retiradas por petición explícita. G1/G2 de gravedad no aceptadas; modelo pendiente. [Estado, vídeo y120 pruebas](meteor-hits-v2.md).

**Actualización 5/11/2026:** la prueba actual es [Respuesta v2: entradas, frenada, saltos y tercera bola](respuesta-v2.md). Incluye los comandos de Goku elegidos y la separación de la memoria del parche; esta sección anterior se conserva como historial.

**5/11/2026 — Respuesta v1:** carga/salida/buffer, cancels sólo de básicos confirmados, control tras lanzamiento y comandos SF para Goku. [Reglas, comandos, vídeo y límites](respuesta-v1.md). HITS y stun: discrepancias del usuario pendientes, sin cambios en esta revisión.

Actualizado el 5 de noviembre de 2026. [Registro estructurado](../project/decisions.json). Las pruebas anteriores se conservan; una elección posterior sustituye a la anterior.

| Apartado | Elección vigente | Estado |
| --- | --- | --- |
| Personajes | Los once recolores elegidos; Goku G2 HDBZ. | Integrados en combate. |
| Intro y título | Goku grande cálido con contraste anime; personajes pequeños originales. BANDAI 1994 y - 2026 ALEX LLAO juntos, misma tipografía. | Integrados y conservados. |
| Retratos / HUD | Retratos elegidos; H4 y cara de P2 reflejada. | Diseño elegido; integración combinada pendiente. Las barras inferiores son una incorporación distinta, ya implementada. |
| Auras | C2 con contorno corregido, ki v4 individual, polvo en suelo y salida animada. **Todos sin rayos.** | Once paletas aceptadas e implementadas; sustituye las elecciones anteriores de rayos para Cell y Gohan. |
| Carrera y caída | Doble toque y mantener, frenado con inercia; reposo terrestre de 12 ticks en las rutas ajustadas. | Implementados. |
| Cambio de lado | → ← → + C para todos, cerca del rival, sin golpe ni ki. | Implementado. [Demostración de respuestas P1/P2 grabada](teleport-exchange-v1.md) con el movimiento existente. [Ventaja adicional v1](side-advantage-v1.md) implementada para dos mandos humanos: seis actualizaciones que limitan nuevos A/B, con defensa y contra C disponibles. Equilibrio manual pendiente. |
| Combos | A/B combinables con técnicas propias y Meteor, sin acelerar movimientos. | Experimental; se retiró la prolongación artificial de reacción y los reinicios de animación del rival. |
| Aturdimiento | Dos barras pequeñas sin texto; el primer impacto conectado termina el mareo y reinicia la acumulación. | Stun v2 implementado y probado. |
| HITS | Contar impactos reales; ocultar 1 y mostrar desde 2. Pausar el plazo durante ataques/cruce y mareo; Goku Meteor suma 3. Conservar el total al enlazar; plazo de 30 separado de lectura de 90. Los golpes aislados no forman cadena. | [HUD HITS v3](hud-hits-v3.md) integrado, con pruebas de guardia, fallo, multigolpe y P2; auditoría exhaustiva pendiente. |
| Impacto y vibración | Suave en golpes normales, bloqueos e impactos intermedios; tipo B en remates; HUD quieto y velocidad natural. | **Aprobado visualmente el 5/11/2026** tras la [prueba variada](guard-shake-preview.md). Integración en la ROM y grabación real pendientes. |
| Namek | Primera propuesta rosada y primera destrucción descartadas. Nueva propuesta normal azul/ocre/verde. | Comparación v2 preparada, pendiente de elegir; no aplicada a la ROM entregada. |
| Escenario 10 | Montañas nevadas, suelo y vuelo. | Bocetos, no integrado. |
| Colisiones | Respetar tamaños, incluido Gohan. | Visor/auditoría disponibles; cajas sin cambios. |

Última ROM de prueba: [v1.0, build 20261106-124607](gohan-hits-v1.md), con ventaja, salida del mareo y corrección del borrado periódico de acumulación. El comando sin versión conserva v6.6; no confundir esa opción con la prueba más reciente.

[Namek antes y después](namek-anime-v2.md) · [Intro elegida](intro-original-lineup-v6-6.md) · [Ki aceptado](ki-colores-v4.md) · [Historial gráfico](graphics.md) · [Hoja de ruta](roadmap.md).


## Versión 1.0 · 6 de noviembre de 2026

Versión y build en nombre de ROM, cabeceras y manifiesto. Corregidas la reducción de lecturas después de golpes y la pérdida de historial tras agarres; 120 técnicas tras lanzar reconocidas en las muestras. El contador pausa durante ki ofensivo; tres bolas de Goku, Meteor y trece impactos de Cell comprobados. Sin cambios de daño, colisiones ni fórmula de mareo respecto a Respuesta v2. Se mantienen los ajustes de carga, buffer, cancels, movimiento y gráficos. [Guía, anuncio real de 1:25 y límites de las pruebas](version-1-0.md).


## Build 20261106-103002 · 6 de noviembre de 2026

[Preparación de Kamehameha/Masenko más breve y tres cruces alternados con Meteor](ki-startup-v1.md), integrados en la nueva prueba v1.0. La velocidad del proyectil, daño, débito de ki, Super y rutas de pantalla partida se conservan. Nuevo anuncio de 1:27 y comparación simultánea antes/después. Falta probar la sensación y equilibrio con mando.


## Build 20261106-105411 · Piccolo y cruces rápidos

[Corrección del Meteor de Piccolo: 2 a 9 HITS, con 43 de daño conservado; doce casos. Cruces ejecutados con los mandos en intervalos de 15–18 fotogramas, sin acelerar la ROM](piccolo-hits-v1.md). Nuevo anuncio y comparación real; builds anteriores conservados.


## Presentación completa · 6 de noviembre de 2026

[Vídeo de 2:14, 26 tomas y once personajes](presentacion-completa-v1.md), con copia ligera para correo, lista de mejoras y borrador para un canal retro. Misma ROM/build; las tomas se coordinan sin acelerar el juego y los diseños pendientes no se incorporan en edición.


## Gohan HITS y YouTube Short · 6 de noviembre de 2026

[Build 124607: Gohan de dos a cinco HITS, mismo daño, doce casos y doce de regresión de Piccolo](gohan-hits-v1.md). [Short vertical de 28 segundos](youtube-short-v1.md), sin acelerar y sin ese Meteor; mantiene su procedencia 105411. La presentación larga anterior permanece archivada.

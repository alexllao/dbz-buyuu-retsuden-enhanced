# Decisiones vigentes

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

Última ROM de prueba: [HUD HITS v3](hud-hits-v3.md), con ventaja, salida del mareo y corrección del borrado periódico de acumulación. El comando sin versión conserva v6.6; no confundir esa opción con la prueba más reciente.

[Namek antes y después](namek-anime-v2.md) · [Intro elegida](intro-original-lineup-v6-6.md) · [Ki aceptado](ki-colores-v4.md) · [Historial gráfico](graphics.md) · [Hoja de ruta](roadmap.md).

# Hoja de ruta

Actualizada el 5 de noviembre de 2026. Última ROM de prueba: [HUD HITS v3](hud-hits-v3.md), sobre Ventaja v1.

## Implementado

- [x] Once paletas de combate elegidas y nueve escenarios recoloreados.
- [x] Goku grande cálido con personajes pequeños originales en la intro.
- [x] BANDAI conservado y ALEX LLAO al lado con la misma tipografía.
- [x] Carrera de doble toque y frenado con inercia nativa.
- [x] Reposo terrestre reducido en las rutas ajustadas.
- [x] Cambio de lado sin golpe ni ki para los once: → ← → + C.
- [x] Contorno de aura corregido y once paletas de ki v4 aceptadas; todos sin rayos.
- [x] Combos experimentales con animaciones completas; retiradas las ayudas que prolongaban/reiniciaban la reacción del rival.
- [x] Dos barras de aturdimiento pequeñas sin texto y corrección de las interferencias gráficas detectadas.
- [x] Salida del mareo y reinicio de acumulación al primer impacto conectado.
- [x] Visor y auditoría de cajas, conservando tamaños y geometría originales.
- [x] Comparación real antes/después de la nueva propuesta de Namek; anteriores descartadas guardadas.

- [x] [Diez tomas de básicos, cambio de lado y remates](combo-side-tests-v1.md), 52 sondeos; huecos y defensa documentados.

## En revisión y próximos trabajos

- [x] [Vídeo de respuestas alternadas P1/P2](teleport-exchange-v1.md) con dos mandos coordinados y el movimiento existente.
- [x] [Ventaja breve v1](side-advantage-v1.md) implementada para dos jugadores humanos; defensa y respuesta C conservadas.
- [x] Validación visual del impacto: contactos suaves y remates tipo B, HUD quieto y velocidad natural.
- [ ] Integrar esa vibración en la ROM y grabar la prueba real; el vídeo aprobado es una previsualización.
- [ ] Valorar con mando las seis actualizaciones, el descarte de A/B durante la ventana y las contras.
- [ ] Extender y comprobar la ventaja frente a CPU; no incluida en esta prueba.
- [ ] Validación con mando de jugabilidad, combos y equilibrio, sin acelerar movimientos ni garantizar infinitos.
- [x] Contador HITS integrado desde 2 impactos; multigolpes, Meteor solo, guardia/fallo y P2 comprobados.
- [x] Corrección del borrado periódico de acumulación: limpieza tras inactividad desde el último impacto no bloqueado.
- [ ] Auditoría exhaustiva de todos los remates/cinemáticas y revisión humana de la lectura del HUD.
- [ ] Integrar los retratos elegidos y HUD H4, con P2 reflejado.
- [ ] Elegir la nueva paleta de Namek normal; revisar de nuevo Namek en destrucción. No aplicar las propuestas descartadas.
- [ ] Revisión completa de especiales, efectos simultáneos y colores.
- [ ] Ampliar cobertura de escenarios, situaciones y consola original.
- [ ] Integrar, si se decide continuar, el décimo escenario nevado; sólo hay bocetos de suelo y vuelo.

Las versiones anteriores, fuentes, paletas y vídeos se conservan. Una prueba en emulador no equivale a aprobación visual o de jugabilidad del usuario. [Decisiones vigentes](decisions.md).

- [x] [HITS v3](hud-hits-v3.md): pausa durante ataques/cruce y mareo; Meteor de Goku con tres contactos, enlace corto separado de lectura; los golpes aislados no se suman.

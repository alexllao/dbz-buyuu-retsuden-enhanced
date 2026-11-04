# Trabajar en el proyecto

La rama de trabajo actual es `development`.

1. Mantén separadas las mejoras de control, velocidad y gráficos para poder compararlas.
2. Conserva las versiones visuales anteriores; registra cada elección en `project/decisions.json`.
3. Distingue propuesta, elección, implementación y prueba real. No presentes un boceto de aura/HUD como captura del mod.
4. Ejecuta `pnpm check` y `pnpm test`. Si hay ROM local, reconstruye ambas variantes y comprueba los hashes.
5. Para cambios de 68000, ensambla la fuente, verifica los hooks y repite las pruebas relevantes en emulador. Documenta el alcance real.
6. Versiona IPS y manifiestos. Las ROMs completas, herramientas, estados, cachés y salidas locales están excluidos de Git.

No cambies la regla de rayos: sólo Gohan y Cell, como máximo. La presentación vigente es B; Goku usa como referencia de aura C2 sin rayos. HUD con retratos originales y jugador 2 reflejado hacia dentro.

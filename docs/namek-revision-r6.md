# Namek R6: revisión del dibujo antes de la ROM

9 de noviembre de 2026. El usuario pide corregir primero los PNG completos y validarlos antes de otra adaptación al juego. La paleta anterior le parece correcta; señala curvas de terreno sin sentido y una ruina aparentemente pegada sobre una roca.

## Estado de la revisión

| Fondo | PNG completo | Estado |
| --- | --- | --- |
| Namek normal | [Abrir PNG](../assets/concepts/namek-revision-r6/normal-aprobado.png) | **Aprobado**: «este primerp perfecto». Archivo conservado sin modificación posterior. |
| Aldea devastada con lava | [Abrir PNG](../assets/concepts/namek-revision-r6/aldea-lava-aprobado.png) | **Aprobado**: «si, mucho mejor». Volcán distante, casa rota más cercana y más humo. |
| Invocación de Porunga | [Abrir PNG](../assets/concepts/namek-revision-r6/porunga-propuesta.png) | **Aprobado** junto a los otros dos fondos. |

Se redibujan las uniones de las mesetas con el suelo, eliminando los arcos de roca repetidos y separados que persistían en V5. Las dos variantes se generan usando el normal aprobado como referencia de composición, casa, montañas y terreno. En la aldea se colocan pequeñas ruinas sobre suelo plano con una base visible; en Porunga se conserva la invocación distante y el cielo oscuro. La casa del Patriarca mantiene el emplazamiento y la escala visual de la base.

**Son maestros de arte de 1254×1254 para revisión visual. No son mapas nativos de 512×512, ni se ha verificado su ajuste a CRAM, tiles o VRAM.** La generación de cada variante puede introducir diferencias de dibujo; compartir referencia no garantiza identidad de píxeles entre escenarios. El normal aprobado se conserva byte a byte, sin cuantizar, reducir ni repintar después de la aprobación.

El usuario aprueba después los tres maestros: «perfctos los tres, kedan muy bien, almenso como yo lo veo». La [aldea inicial sin lava](../assets/concepts/namek-revision-r6/aldea-propuesta.png) se conserva como alternativa archivada. [Prompt de la variante con lava](../assets/concepts/namek-revision-r6/lava-prompt.json), también editada con la herramienta integrada image_gen.imagegen.

La fase de revisión del arte no cambiaba la ROM. Después de aprobar los tres PNG, el usuario pide explícitamente integrarlos y ver un vídeo real de la ROM, para revisión propia y sin publicarlo. Se prepara una [adaptación nativa R6 separada](namek-native-r6.md); su acabado todavía necesita valoración. El build general aprobado sigue siendo `20261108-200852` y V5 se conserva por separado. Porunga, humo y lava son estáticos en esta prueba; su animación sigue pendiente.

## Procedencia

Ediciones con la herramienta integrada **image_gen.imagegen**, sin CLI. [Prompts completos y modo](../assets/concepts/namek-revision-r6/prompts.json) · [Dimensiones, SHA-256, estado y originales](../assets/concepts/namek-revision-r6/manifest.json). Los archivos del repositorio son copias idénticas de las salidas generadas. V5 se conserva como evidencia histórica, no como acabado final aprobado.

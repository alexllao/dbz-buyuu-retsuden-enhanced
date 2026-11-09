# Namek R6: revisión del dibujo antes de la ROM

9 de noviembre de 2026. El usuario pide corregir primero los PNG completos y validarlos antes de otra adaptación al juego. La paleta anterior le parece correcta; señala curvas de terreno sin sentido y una ruina aparentemente pegada sobre una roca.

## Estado de la revisión

| Fondo | PNG completo | Estado |
| --- | --- | --- |
| Namek normal | [Abrir PNG](../assets/concepts/namek-revision-r6/normal-aprobado.png) | **Aprobado**: «este primerp perfecto». Archivo conservado sin modificación posterior. |
| Aldea devastada | [Abrir PNG](../assets/concepts/namek-revision-r6/aldea-propuesta.png) | Propuesta pendiente de validación. |
| Invocación de Porunga | [Abrir PNG](../assets/concepts/namek-revision-r6/porunga-propuesta.png) | Propuesta pendiente de validación. |

Se redibujan las uniones de las mesetas con el suelo, eliminando los arcos de roca repetidos y separados que persistían en V5. Las dos variantes se generan usando el normal aprobado como referencia de composición, casa, montañas y terreno. En la aldea se colocan pequeñas ruinas sobre suelo plano con una base visible; en Porunga se conserva la invocación distante y el cielo oscuro. La casa del Patriarca mantiene el emplazamiento y la escala visual de la base.

**Son maestros de arte de 1254×1254 para revisión visual. No son mapas nativos de 512×512, ni se ha verificado su ajuste a CRAM, tiles o VRAM.** La generación de cada variante puede introducir diferencias de dibujo; compartir referencia no garantiza identidad de píxeles entre escenarios. El normal aprobado se conserva byte a byte, sin cuantizar, reducir ni repintar después de la aprobación.

No se modifica ninguna ROM, menú, jugabilidad ni vídeo para esta revisión. El build general aprobado sigue siendo `20261108-200852` y el experimento nativo V5 se conserva por separado. La integración de R6 y sus vídeos quedan para después de validar los PNG. Porunga sigue siendo una imagen estática; su flotación como sprite continúa pendiente.

## Procedencia

Ediciones con la herramienta integrada **image_gen.imagegen**, sin CLI. [Prompts completos y modo](../assets/concepts/namek-revision-r6/prompts.json) · [Dimensiones, SHA-256, estado y originales](../assets/concepts/namek-revision-r6/manifest.json). Los archivos del repositorio son copias idénticas de las salidas generadas. V5 se conserva como evidencia histórica, no como acabado final aprobado.

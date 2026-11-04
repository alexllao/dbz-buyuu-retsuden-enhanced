# Investigación de la apertura v6.2

Estas son copias de los scripts usados en la investigación local, no una segunda interfaz de construcción pública. Conservan rutas del espacio de trabajo y requieren las ROM y extracciones locales indicadas en cada script. No incluyen esos archivos privados.

La construcción reproducible del resultado final es `pnpm build:review --rom ruta/a/original.bin`: verifica los hashes de la ROM original, el IPS y el resultado. Las operaciones de cada recurso se conservan en `src/intro/characters-v2` y `src/title/credit-v2`; la validación está en `evidence/intro-v2`.

`extract.py` identifica propietarios y paletas de los píxeles nativos; `recompose.py` agrupa colores y recompone tiles, fondo y sprites. `lz.py` comprime en el formato nativo. `build_font.py` amplía el crédito con las medidas de la tipografía nativa. `combine_final.py` comprueba que las operaciones no se solapan y actualiza el checksum.

La fuente de la ROM y los glifos originales no se han recuperado como un proyecto de desarrollo original. Los listados de estudio se explican en la documentación de ASM.

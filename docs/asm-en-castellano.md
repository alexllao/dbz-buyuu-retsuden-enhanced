# ASM de estudio en castellano

No tenemos el código fuente original del juego. Tenemos la ROM japonesa aportada por el usuario, el desensamblado que se puede obtener de ella y las fuentes de los parches del proyecto.

Se ha preparado un paquete local de estudio con:

- Un mapa de direcciones de la ROM original con las instrucciones clasificadas y las zonas no clasificadas como `INCBIN`.
- Un segundo mapa de la revisión v6.2, que conserva instrucciones originales con los mismos bytes y añade los bloques ASM documentados de nuestros parches.
- Un índice de funciones y nombres didácticos de las rutinas que se han identificado.
- Copias comentadas en castellano de los controles, cambio de lado, auras y ayuda de créditos.

## Qué significan los comentarios

Los comentarios tienen tres alcances diferentes. Las descripciones de entrada, historial de combinaciones, reinicio de estado y cambio de lado se apoyan en la investigación y las pruebas registradas del proyecto. Los comentarios repetidos junto a instrucciones describen mecánicamente la operación del 68000; no son una interpretación manual de todo el juego. Las regiones o funciones desconocidas se marcan como pendientes.

El análisis ampliado parte de los vectores, programas referenciados por las tablas de técnicas y tablas de fase con el patrón de salto reconocido. No hace un barrido lineal que convierta los gráficos comprimidos en instrucciones.

## Límites

La cobertura completa es de **direcciones**, no una prueba de que se haya identificado todo el código. Las zonas `INCBIN` pueden contener gráficos, mapas, tablas, relleno o código aún no descubierto. Su porcentaje del tamaño de la ROM no equivale al porcentaje de lógica recuperada.

No se han recuperado los nombres de variables ni comentarios originales. No se ha validado recompilar todo el listado para reproducir la ROM. Los dialectos de impresión y los datos intercalados exigen trabajo adicional para convertirlo en un proyecto reconstruible.

El paquete completo se genera localmente. El repositorio conserva herramientas, el índice de regiones conocidas y [extractos auditados](../research/disassembly-es/rutinas_nativas_comentadas.asm); no incluye la ROM ni una codificación íntegra de sus gráficos/datos.

## Regenerar

Es una herramienta opcional de análisis: requiere Ghidra 12.1.4, un JDK compatible y Python. La construcción normal del parche sigue funcionando sin esas herramientas.

Desde PowerShell, ajustando las rutas a tus instalaciones:

```powershell
pwsh -File tools/disassembly/export-study.ps1 `
  -GhidraHome 'ruta/a/ghidra_12.1.4_PUBLIC' `
  -JavaHome 'ruta/a/jdk-21' `
  -Rom 'ruta/a/original.bin' `
  -Output 'ruta/de/salida' `
  -PatchRepo '.'
```

`-CapstoneDir` es opcional si se dispone de Capstone 5.0.6 en una carpeta local. Permite añadir los tramos auditados con límites explícitos. Las scripts crean siempre un proyecto privado nuevo; no modifican la base de análisis de trabajo ni la ROM.

El mapa modificado se produce con [overlay-modified-study-es.py](../tools/disassembly/overlay-modified-study-es.py), indicando los listados de ensamblado de esa revisión. No se debe aplicar el mapa de una revisión a otra ROM con distinto hash.

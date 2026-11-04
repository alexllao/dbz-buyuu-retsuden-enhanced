# Investigación de combos v1

Estas son copias de los scripts usados en el espacio de investigación local. Conservan rutas de ese espacio y reutilizan su emulador, ROM privada, proyecto Ghidra y utilidades; no constituyen una segunda interfaz pública de construcción ni incluyen esas dependencias.

La reproducción pública del resultado es `pnpm build:review --rom ruta/a/original.bin --version combos-v1`. El comando verifica los hashes de la ROM japonesa, el parche y la ROM generada. La construcción por defecto conserva v6.6.

`test_combo.py` usa entradas reales tras arrancar por los menús nativos. `run_matrix.py` comprueba las cadenas y sus límites, y admite `--summarize-only` para volver a evaluar trazas del mismo hash sin repetir la ejecución. `run_side_regression.py` reutiliza las pruebas del cambio de lado. `record_demo.py` graba las entradas del prototipo y luego las reproduce en la base para comparar.

`AssembleCombo.java` y `assemble.ps1` conservan el procedimiento local usado para ensamblar. Los bytes revisables del resultado están en `src/gameplay/combos-v1`; los informes finales están en `evidence/combos-v1`.

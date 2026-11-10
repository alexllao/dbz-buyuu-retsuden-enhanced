Preparacion minima de tecnicas enlazadas: v1.0 build 20261110-120502.

charge.asm: codigo 68000 nuevo, comentado en castellano. 692 bytes.
charge.hex/listing/labels: ensamblado de ese codigo, sin ROM comercial.
build.py: aplica los hooks y genera el catalogo desde el padre Namek R10 exacto.
AssembleComboChargeAll.java / assemble.ps1: ensamblador local Ghidra.
runtime/probe/roster/repeat: pruebas mediante entradas de mando y lecturas de RAM.
record/edit: captura de framebuffer/audio nativos y comparacion simultanea.
package: comprueba matrices y vuelve a aplicar el IPS para verificar cada byte.

Los scripts conservan rutas work/ del espacio de trabajo y reutilizan los
auxiliares de las revisiones anteriores. No son un SDK independiente. Requieren
la ROM privada R10 exacta, el emulador y estados locales, no incluidos aqui.
El resto de fuentes auxiliares esta documentado en research/ de cada revision.

Hooks:
20A7A: recuperar selector nativo de las animaciones de rafaga.
20A8A: lectura de cabecera y adelanto de preparacion por fase.
11C1E: cargar/cachar cajas receptoras nativas, restauracion de B/C solo para KI enlazado.
11EF4 / 120D4: aceptar contacto del proyectil enlazado durante reaccion B/C.
73F4: borrar caches por ronda y continuar al reset anterior.
Codigo nuevo 3E1000; catalogo 3E3000.
RAM F7B0..B7 y F7D0..EF; no invade F7C0 (variante Namek).

Analisis y emulacion locales. No se envio la ROM al conector externo.
Limites, hashes y resultados en docs/combo-charge-all.md y evidence/combo-charge-all/.

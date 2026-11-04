# Auras C2: contorno aceptado, sin rayos

El usuario acepta el aspecto del nuevo contorno y pide retirar los rayos de Cell y Gohan SSJ2. **Ahora ningún personaje lleva rayos de aura.** La aprobación anterior de los rayos queda en el historial.

[Gohan sin rayos](../assets/media/auras-c2-v3-no-rays/Gohan-SSJ2.mp4) · [Cell sin rayos](../assets/media/auras-c2-v3-no-rays/Cell.mp4).

Son grabaciones reales de la ROM de prueba. La llama, su tamaño, el polvo, la salida y los colores actuales se conservan. La nueva tabla remite los 384 estados posibles a mapas sin rayos; no hay referencias alcanzables a sus seis tiles. Los únicos cambios frente a C2 v3 son 114 bytes de punteros y checksum. Se han repetido carga, salida y movimiento con Gohan y Cell en el emulador.

## Colores: siguiente revisión

La misma forma y animación se adaptarán por tipo de personaje, manteniendo la estética del juego original. Los Super Saiyan conservarán el dorado. Para los demás no se deducirá el aura del color de piel, traje o proyectiles. El original usa una paleta compartida dorada incluso para Piccolo: sirve de referencia de estilo, pero no demuestra un color de anime distinto para cada luchador.

Esta variante intermedia todavía conserva la paleta común. No debe presentarse como la adaptación de colores terminada. Tampoco implica aprobación de una paleta verde para Piccolo o violeta para Ginyu. Las versiones con rayos siguen guardadas como historial.

## Construcción

`pnpm build:auras:no-rays --rom ruta/a/original.bin`

[Manifiesto](../patches/auras-c2-v3-no-rays/manifest.json) · [Punteros](../src/auras/c2-v3-no-rays/map-pointers.hex) · [Evidencia](../evidence/auras-c2-v3-no-rays/validation.json) · [Base C2 v3](auras-c2-v3.md).

[Registro de referencias y confianza de los colores](../research/auras-colors/reference-ledger.json). El primer pase se conserva como historial. La [revisión con fotogramas del anime](aura-color-references.md) aporta referencias para cinco personajes; A18 y Ginyu siguen abiertos. Cell queda elegido en dorado como los SSJ.

**Estado posterior:** los colores individuales ya están [implementados y grabados en v4](ki-colores-v4.md), pendientes de validación visual.

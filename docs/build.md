# Construcción

## Generar las dos variantes verificadas

El flujo habitual aplica los IPS versionados. No necesita Java, Ghidra ni un emulador.

```sh
pnpm install --frozen-lockfile
pnpm check
pnpm test
pnpm build --rom "ruta/a/original.bin"
pnpm build:colors --rom "ruta/a/original.bin"
```

La base se valida por tamaño y SHA-256. El constructor comprueba los parches, recalcula el checksum de Mega Drive y exige que el resultado coincida con el hash del [manifiesto](../patches/gameplay-v1/manifest.json). Nunca sobrescribe la entrada. Las salidas y su registro aparecen en `dist/`.

La variante `colors` aplica primero Colores v1 y después Jugabilidad v1; por último recalcula el checksum. No incluye aún la presentación G, el HUD ni el aura C2.

El [prototipo C2](auras-c2-v1.md) se conserva como un parche experimental separado en [patches/auras-c2-v1](../patches/auras-c2-v1), con su propio manifiesto. Combina Jugabilidad v1, Colores v1 y Auras C2 desde la base original. Los comandos de arriba siguen generando las dos variantes v1 anteriores; no incorporan automáticamente ese prototipo. La presentación G, el crédito y el HUD tampoco están incluidos en la prueba C2.

## Prueba actual de auras: C2 v2

La [segunda revisión C2](auras-c2-v2.md) amplía el aura a 80 × 128 píxeles y añade rayos blancos largos y polvo. Se genera por separado, conservando las variantes anteriores:

```sh
pnpm build:auras:v2 --rom "ruta/a/original.bin"
```

El [parche C2 v2](../patches/auras-c2-v2/auras-c2.ips) y su [manifiesto](../patches/auras-c2-v2/manifest.json) corresponden a Jugabilidad v1 + Colores v1 + Auras C2 v2 desde la misma base japonesa original. El usuario ha aceptado su tamaño, polvo y rayos; una revisión posterior detectó cortes rectos y huecos del contorno, pendientes de corregir. Este comando sigue generando C2 v2, anterior a esa reparación. La presentación G, el crédito, la selección recoloreada y el HUD siguen pendientes de integración.

## Ensamblar la fuente del 68000

La fuente vigente es [controls.asm](../src/gameplay/v1/controls.asm). El código verificado está en [controls.hex](../src/gameplay/v1/controls.hex); son 796 bytes alojados en el relleno original desde `0x7B000`.

En Windows, con PowerShell 7, Ghidra 12.1.4 y Java 21 instalados:

```powershell
pnpm assemble -GhidraHome "ruta/a/ghidra_12.1.4_PUBLIC" -JavaHome "ruta/al/jdk-21" -Rom "ruta/a/original.bin"
```

También se admiten `GHIDRA_HOME` y `JAVA_HOME`. El ensamblado crea un proyecto temporal bajo `build-local/`, usa `68000:BE:32:default` y compara los bytes con la versión revisada. **No actualiza automáticamente un parche publicado**: al cambiar instrucciones hay que revisar los hooks, generar un nuevo IPS y repetir las pruebas en emulador antes de cambiar el manifiesto.

## Investigación histórica

Los scripts previos están en [research/legacy](../research/legacy). Conservan convenciones del espacio de trabajo original y no son la entrada de construcción soportada de este repositorio. Las pruebas automáticas de CI verifican herramientas, catálogos y evidencia; no ejecutan la ROM ni descargan una ROM o un emulador.

## Corrección de contorno C2 v3

pnpm build:auras:v3 --rom ruta/a/original.bin genera la prueba de contorno corregido. Conserva las variantes anteriores. Véase [C2 v3](auras-c2-v3.md). El escenario nevado sólo tiene bocetos de suelo y vuelo, sin integración en ROM.

## Revisión combinada v5

`pnpm build:review --rom ruta/a/original.bin` aplica el IPS completo sobre la base japonesa y verifica el hash de salida. Incluye controles v2, derribos terrestres ajustados, paletas de combate, ki v4 y presentación G con Bandai y ALEX LLAO. [Alcance y pruebas](gameplay-v2.md).

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

La variante `colors` aplica primero Colores v1 y después Jugabilidad v1; por último recalcula el checksum. No incluye aún la presentación B, el HUD ni el aura C2.

## Ensamblar la fuente del 68000

La fuente vigente es [controls.asm](../src/gameplay/v1/controls.asm). El código verificado está en [controls.hex](../src/gameplay/v1/controls.hex); son 796 bytes alojados en el relleno original desde `0x7B000`.

En Windows, con PowerShell 7, Ghidra 12.1.4 y Java 21 instalados:

```powershell
pnpm assemble -GhidraHome "ruta/a/ghidra_12.1.4_PUBLIC" -JavaHome "ruta/al/jdk-21" -Rom "ruta/a/original.bin"
```

También se admiten `GHIDRA_HOME` y `JAVA_HOME`. El ensamblado crea un proyecto temporal bajo `build-local/`, usa `68000:BE:32:default` y compara los bytes con la versión revisada. **No actualiza automáticamente un parche publicado**: al cambiar instrucciones hay que revisar los hooks, generar un nuevo IPS y repetir las pruebas en emulador antes de cambiar el manifiesto.

## Investigación histórica

Los scripts previos están en [research/legacy](../research/legacy). Conservan convenciones del espacio de trabajo original y no son la entrada de construcción soportada de este repositorio. Las pruebas automáticas de CI verifican herramientas, catálogos y evidencia; no ejecutan la ROM ni descargan una ROM o un emulador.

# Investigación de Combos v2

Scripts conservados de la investigación local; contienen rutas de ese espacio y dependen de la ROM propia, el emulador local y el ensamblador Ghidra previamente preparado. No incluyen esas dependencias ni son la interfaz pública de construcción.

El resultado se reproduce con `pnpm build:review --rom ruta/a/original.bin --version combos-v2`, con verificación de los hashes de origen, parche y ROM generada. El ASM canónico está en `src/gameplay/combos-v2/combos.asm`; el script preparatorio conserva un paso de exploración anterior y no sustituye a ese ASM revisado.

Las pruebas usan pulsaciones reales y posiciones/orientación iniciales fijadas. `render_video.py` añade un contador calculado desde las trazas a las grabaciones limpias; ese contador no se ha integrado en la ROM.

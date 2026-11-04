# Mapa técnico del parche

La ROM original es un artefacto 68000, no un proyecto de C recompilable. El trabajo actual aplica cambios localizados y conserva su tamaño de 2 MB.

| Elemento | Ubicación |
| --- | --- |
| Código nuevo | Relleno FF desde `0x7B000`, 796 bytes |
| Hook de entrada | `0x8F58` |
| Hook previo de animación | `0x209DC` |
| Hook de salida visual | `0x20A46` |
| Estado nuevo por jugador | Hueco `0x108..0x10F` en la estructura de `0x128` bytes |
| Resolución de secuencias | `0x20A4C` |
| Reinicio de estado nativo | `0x20BA0` |
| Historial de direcciones | `0x9170` / `0x917C` |

**No reutilizar `0x118..0x11F`: contiene temporizadores nativos.** Ese conflicto se detectó durante el desarrollo y se corrigió antes de la v1 entregada.

La entrada pendiente dura cinco actualizaciones posteriores, se consume una vez y se limpia al salir de los estados admitidos o cambiar el tipo de control. Las pulsaciones tempranas caducan. Las recuperaciones sólo se recortan cuando una secuencia simple ha llegado a su última pose; las fases complejas y el movimiento aéreo conservan sus reglas.

La transición visual de Jugabilidad v1 usa poses existentes y cede inmediatamente a una nueva acción. Ese parche no añade sprites dibujados ni incluye el HUD o las auras. El [prototipo C2](auras-c2-v1.md) se versiona por separado, con sus propios gráficos y código.

El turbo usa los valores nativos `E756/E758`: `0x100/0x100` normal y `0x140/0xCC` turbo. El cálculo inverso está en `0x207E6`. El juego ya conserva un historial de direcciones; no asumir que carece de toda memoria de entrada.

Offsets de paleta históricos: normales `0x80064`, alternativas `0x801E4`, fondos `0x19E51E`, con diez colores comunes desde `0x9102`. Ver [research/palettes](../research/palettes) y los scripts de extracción históricos antes de modificar estos bloques.

## Auras C2 experimentales

La primera adaptación C2 usa un recurso de 64 × 112 píxeles y 45 tiles y conserva la paleta compartida nativa. El código distingue Gohan SSJ2 (ID 1) y Cell (ID 5) para los rayos; el resto utiliza la variante sin rayos. La salida visual al soltar dura doce ticks. Fuente, código y recursos están en [src/auras/c2-v1](../src/auras/c2-v1). La validación y la aprobación visual se registran separadas de las pruebas históricas de Jugabilidad v1.

La [revisión actual C2 v2](auras-c2-v2.md) amplía el mapa completo a 80 × 128 píxeles. Reutiliza el atlas de llamas sin cambiar sus píxeles y reduce su almacenamiento a 38 tiles eliminando extremos vacíos; deja sitio para los arcos blancos de 32 píxeles y el polvo. Las dos nubes de polvo se animan con ocho fotogramas y tres tamaños, sólo cuando la coordenada Y del actor coincide con el suelo (`0x1C0`). La fase de retirada mantiene doce ticks y reduce piezas en sus últimos mapas para respetar los límites del VDP. La paleta compartida nativa se conserva. Fuente y recursos nuevos: [src/auras/c2-v2](../src/auras/c2-v2). C2 v1 no se sobrescribe.

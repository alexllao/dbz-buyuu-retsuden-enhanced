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

La transición visual usa poses existentes y cede inmediatamente a una nueva acción. No añade sprites dibujados ni incluye el HUD o aura conceptual.

El turbo usa los valores nativos `E756/E758`: `0x100/0x100` normal y `0x140/0xCC` turbo. El cálculo inverso está en `0x207E6`. El juego ya conserva un historial de direcciones; no asumir que carece de toda memoria de entrada.

Offsets de paleta históricos: normales `0x80064`, alternativas `0x801E4`, fondos `0x19E51E`, con diez colores comunes desde `0x9102`. Ver [research/palettes](../research/palettes) y los scripts de extracción históricos antes de modificar estos bloques.

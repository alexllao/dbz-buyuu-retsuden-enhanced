# Auras C2 v2: más tamaño, rayos largos y polvo

Esta segunda revisión amplía las auras y añade los detalles que faltaban en la primera prueba. Es un **prototipo real para revisión visual**, todavía pendiente de aprobación del usuario.

[Vídeo de los once personajes, antes y después](../assets/media/auras-c2-v2/Todas-las-auras-antes-despues.mp4) · [Tres tamaños con Goku](../assets/media/auras-c2-v2/Comparacion-tres-tamanos-Goku.mp4) · [Salida a cámara lenta](../assets/media/auras-c2-v2/Salida-Goku-lenta.mp4).

## Qué cambia

| Versión | Tamaño completo del aura |
| --- | --- |
| Original | 80 × 112 píxeles |
| Primera prueba C2 v1 | 64 × 112 píxeles |
| **C2 v2 actual** | **80 × 128 píxeles** |

C2 v2 es un 25 % más ancha y aproximadamente un 14 % más alta que la primera prueba. Recupera el ancho original y supera su altura. El vídeo de tres tamaños permite comparar esa diferencia en la misma escena.

**Goku y el resto del reparto siguen sin rayos. Cell y Gohan SSJ2 llevan arcos blancos largos e intermitentes**, de 32 píxeles frente a los ocho del recurso anterior. También aparecen dos nubes de polvo junto a los pies, animadas con ocho fotogramas y tres tamaños. El polvo sólo se dibuja en el suelo; no acompaña a un personaje que carga en el aire.

Al soltar la carga, la retirada dura doce ticks del juego. Sus últimas fases usan menos piezas para evitar sobrecargar el dibujo. El tiempo visible puede alargarse si el motor se ralentiza; el vídeo lento permite revisar el cierre. La paleta compartida nativa se conserva. El dibujo es una adaptación del concepto C2 a Mega Drive y no una reproducción idéntica del boceto generado.

## Vídeos individuales

Son grabaciones reales del juego, no animaciones generadas del concepto.

| Personaje | Comparación |
| --- | --- |
| Goku | [Antes y después](../assets/media/auras-c2-v2/00-Goku.mp4) |
| Gohan SSJ2 | [Antes y después](../assets/media/auras-c2-v2/01-Gohan-SSJ2.mp4) |
| Piccolo | [Antes y después](../assets/media/auras-c2-v2/02-Piccolo.mp4) |
| Vegeta | [Antes y después](../assets/media/auras-c2-v2/03-Vegeta.mp4) |
| Trunks | [Antes y después](../assets/media/auras-c2-v2/04-Trunks.mp4) |
| Cell | [Antes y después](../assets/media/auras-c2-v2/05-Cell.mp4) |
| Androide 18 | [Antes y después](../assets/media/auras-c2-v2/06-Android-18.mp4) |
| Krilin | [Antes y después](../assets/media/auras-c2-v2/07-Krillin.mp4) |
| Freezer | [Antes y después](../assets/media/auras-c2-v2/08-Freezer.mp4) |
| Recoome | [Antes y después](../assets/media/auras-c2-v2/09-Recoome.mp4) |
| Ginyu | [Antes y después](../assets/media/auras-c2-v2/10-Ginyu.mp4) |

La [primera versión C2 v1](auras-c2-v1.md), sus fuentes, parches y vídeos se conservan para comparar o volver atrás.

## Qué se ha comprobado

La [validación de esta revisión](../evidence/auras-c2-v2/validation.json) y el [informe de ejecución](../evidence/auras-c2-v2/runtime-qa.json) registran las pruebas en Genesis Plus GX:

- Seis golpes naturales interrumpen el aura sin dejar sprites residuales.
- Carga del jugador 2, dos cargas consecutivas y cargas simultáneas.
- Cincuenta y cinco muestras de carga aérea sin polvo.
- Máximos observados de 76 sprites de 80 disponibles; en una línea, 18 de 20 sprites y 232 de 320 píxeles.

Estos resultados corresponden a los casos probados. Quedan fuera otros efectos simultáneos y la consola física. La revisión visual del tamaño, los rayos, el polvo y la suavidad del cierre sigue pendiente.

Las pruebas de colisión fijan posiciones y orientación para reproducir los golpes. La comprobación aérea fuerza la altura y el plano después de iniciar la carga; demuestra que se elige el mapa sin polvo, no una secuencia natural de vuelo.

## Construcción y fuentes

```sh
pnpm build:auras:v2 --rom "ruta/a/original.bin"
```

- [Fuente del 68000](../src/auras/c2-v2/aura.asm) y [código hexadecimal](../src/auras/c2-v2/aura.hex).
- [Tiles](../src/auras/c2-v2/tiles.hex) y [mapas](../src/auras/c2-v2/maps.hex).
- [Parche IPS desde la base original](../patches/auras-c2-v2/auras-c2.ips) y [manifiesto](../patches/auras-c2-v2/manifest.json).
- [Origen de los diseños de rayos y polvo, prompts y conversión a sprites](../assets/source/auras-c2-v2/provenance.json).

La prueba combina Jugabilidad v1, Colores v1 y Auras C2 v2. La ROM completa se genera localmente y no se versiona. La presentación G, el crédito **- 2026 ALEX LLAO**, los retratos de selección y el HUD H4 aún no están integrados.

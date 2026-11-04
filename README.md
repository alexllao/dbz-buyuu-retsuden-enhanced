# Dragon Ball Z: Buyuu Retsuden Enhanced

Un mod de **Mega Drive / Genesis** para mejorar la respuesta de los controles y revisar los colores de *Dragon Ball Z: Buyuu Retsuden (Japan)*, tomando el anime y Hyper Dragon Ball Z como referencias visuales.

**Estado: revisión v6.6 de prueba · intro y título con contraste anime cálido · cambio de lado sin golpe para los once personajes · carrera nativa e inercia recuperadas · derribos terrestres más breves · presentación C cálida y créditos integrados · ki v4 aceptado**

![Comparación real de jugabilidad: original y mod](assets/media/gameplay-v1-preview.gif)

**[Ver la comparación completa en vídeo](assets/media/gameplay-v1-comparison.mp4)** · [Galería de variantes](docs/graphics.md) · [Decisiones guardadas](docs/decisions.md) · [Hoja de ruta](docs/roadmap.md)

**[Auras C2 v2: vídeo real con los once personajes, antes y después](assets/media/auras-c2-v2/Todas-las-auras-antes-despues.mp4)** · [Comparar los tres tamaños con Goku](assets/media/auras-c2-v2/Comparacion-tres-tamanos-Goku.mp4) · [Final del aura a cámara lenta](assets/media/auras-c2-v2/Salida-Goku-lenta.mp4)

La [primera prueba C2 v1](docs/auras-c2-v1.md) y [sus vídeos](assets/media/auras-c2-v1/Todas-las-auras-antes-despues.mp4) se conservan como historial.

## Qué hay ahora

| Apartado | Estado |
| --- | --- |
| Controles v3 | Conserva carrera e inercia, reposo terrestre breve y añade **adelante, atrás, adelante + C** para cambiar de lado sin golpe con los once personajes. [Pruebas y vídeo](docs/side-switch.md). |
| Personajes | **Propuesta elegida para los 11; Goku G2 HDBZ**. Disponible en Colores v1. |
| Escenarios | **Propuesta elegida para los 9**. Disponible en Colores v1. |
| Retratos de selección | **Propuesta v1 elegida para los 11**; pendiente de integrar en el próximo BIN combinado. |
| Presentación | **C cálida adaptada a apertura y título**, pendiente de revisión visual; **© BANDAI 1994** y **- 2026 ALEX LLAO** juntos. [Capturas actuales](docs/intro-original-lineup-v6-6.md). |
| HUD | **H4**, coherente con los retratos de selección elegidos; conserva el diseño H3 y el jugador 2 reflejado. Pendiente implementar. |
| Auras | **Ki v4 con colores individuales implementado y grabado para los once personajes.** Todos sin rayos; paletas aceptadas visualmente. |
| Ataques especiales | Revisión pendiente. |

Las capturas comparativas de paletas, los bocetos de HUD y los conceptos de aura están identificados por separado. **El vídeo superior sí es una grabación real del juego original frente a la ROM de jugabilidad v1.**

## Prueba opcional actual: Combos v4 con ritmo natural

**Cada ataque termina su animación antes del siguiente.** Se guardan las órdenes durante el contacto y se ejecutan al acabar el movimiento: se elimina el corte anticipado de v3, se restaura la recuperación final completa y se retira el paso instantáneo de seguimiento. No se acelera el vídeo ni el reloj de animación. La ampliación sigue siendo para humanos, en suelo y velocidad normal.

[**Ver vídeo largo nuevo con sonido (4 min 45 s)**](assets/media/combos-v4-natural/Combos-v4-ritmo-natural-4min.mp4) · [Reglas, comparación con el original y límites](docs/combos-v4-natural.md). Son ocho combates o fragmentos reales con dos mandos automatizados, sin contador superpuesto.

Al conservar duración, alcance y retroceso, algunas rutas de tres golpes de v3 dejan de conectar; se registran y quedan pendientes de ajustar jugando. Hay un máximo de tres básicos y una técnica asistida, sin asegurar que todo orden impacte. Se conservan v1/v2/v3 y la ROM principal v6.6. Construcción opcional: `pnpm build:review --rom ruta/a/original.bin --version combos-v4-natural`.

## Prueba opcional de combos v3: los once personajes

Mezcla hasta **tres básicos A/B** al acertar y remata con una técnica propia o Meteor, introduciendo su comando original. Primera prueba común para los once personajes humanos en suelo y velocidad normal. El remate cierra las ayudas de la cadena; sólo se recupera el presupuesto tras seis actualizaciones con ambos luchadores libres. Pendiente de probar con mando.

[**Ver combates largos con sonido (4 min 41 s)**](assets/media/combos-v3/Combos-v3-combates-largos-con-sonido.mp4) · [Vídeo real de los once personajes](assets/media/combos-v3/Combos-v3-once-personajes.mp4) · [Goku A-B-A → Meteor](assets/media/combos-v3/Goku-ABA-Meteor.mp4) · [Goku A-B-A → ráfaga](assets/media/combos-v3/Goku-ABA-rafaga.mp4) · [Reglas, resultados y límites](docs/combos-v3.md). Los vídeos no llevan contador: todavía no está en la ROM.

Construcción: `pnpm build:review --rom ruta/a/original.bin --version combos-v3`. **La opción por defecto sigue siendo v6.6** y se conservan v1/v2. Se mantienen alcance, cajas, condiciones y daño nativos del remate; algunas rutas fallan por distancia o pose. Las pruebas reducen riesgos de bucles, sin demostrar que todo infinito sea imposible.

## Prueba opcional de combos v2: puños y patadas

**A, A, B al conectar: dos puñetazos y remate de patadas.** En las tomas reales, Goku enlaza cinco impactos y Vegeta cuatro. Sólo velocidad normal y mandos humanos; se usa una ráfaga nativa distinta para cada personaje y se modera el daño de las patadas. Pendiente de valorar jugando.

[Ver el vídeo real de los remates](assets/media/combos-v2/Combos-v2-punetazos-y-patadas.mp4) · [Condiciones, pruebas y límites](docs/combos-v2.md). El contador del vídeo está superpuesto; no está en la ROM. Hay [toma limpia de Goku](assets/media/combos-v2/Goku-combo-real-sin-contador.mp4) y [de Vegeta](assets/media/combos-v2/Vegeta-combo-real-sin-contador.mp4).

Construir esta prueba: `pnpm build:review --rom ruta/a/original.bin --version combos-v2`. **La construcción predeterminada sigue siendo v6.6.** Se conserva la [prueba v1 de dos puños y proyectil](docs/combos-v1.md) y la [primera propuesta visual de contador](assets/concepts/combo-counter-v1/Contador-combos-demostracion.mp4).

## Revisión actual: ROM v6.6

**Los personajes pequeños de la intro vuelven exactamente al original**, por petición del usuario. Se conserva el Goku grande cálido de C y la pantalla de BANDAI y ALEX LLAO de v6.4/v6.5. [Capturas reales y comprobaciones](docs/intro-original-lineup-v6-6.md).

Los colores de combate, escenarios, auras y jugabilidad se conservan. Las propuestas de recolor del reparto se guardan únicamente como historial.

También está disponible el [ASM de estudio comentado en castellano](docs/asm-en-castellano.md): incluye rutinas identificadas y fuentes de nuestros parches. No es el código fuente original; las zonas desconocidas quedan marcadas y no se ha validado recompilar el juego completo.

**Cambio de lado sin golpe para todos: adelante, atrás, adelante + C**, cerca del rival. La última dirección y C pueden pulsarse juntos. Se conserva la función normal de C al soltarlo; las técnicas originales de A y B no se sustituyen. [Ver los once dentro del juego](assets/media/side-switch/Todos-cambio-de-lado.mp4) · [Controles, condiciones y pruebas](docs/side-switch.md).

El movimiento original de Gohan tampoco golpea: se corrigió la descripción anterior tras comprobarlo en juego. Se reutiliza ese comportamiento y se añade una combinación propia.

**Ajuste tras la prueba del usuario:** el reposo tumbado baja de 30 a **12 ticks** (unos 0,22–0,25 s en estos ensayos). Se conserva la caída y el levantamiento. Bandai y ALEX LLAO comparten ahora la misma línea. [Comparación Gohan: v5 izquierda / v5.2 derecha](assets/media/gameplay-v2/Gohan-v5-izquierda-v5-2-derecha.mp4).

Corrige la carrera que fallaba en v1: doble toque hacia delante o atrás y mantener; al soltar, salida con inercia original. Acorta la espera tumbado tras los derribos terrestres largos e integra la presentación G con los créditos originales y el del mod. **La valoración con mando sigue abierta.**

[Ver la revisión anterior de movimiento y derribos](docs/gameplay-v2.md) y [el cambio de lado actual](docs/side-switch.md). Genera esta versión con `pnpm build:review --rom "ruta/a/original.bin"`. Las versiones anteriores y sus comparaciones se conservan.

## Prueba CPU anterior: original frente a v4

**Seis enfrentamientos con los once personajes, unos 3 min 30 s por versión**, sin botones humanos durante el combate. Original japonés sin parches a la izquierda; Jugabilidad v1 + Colores v1 + Ki v4 a la derecha. No se detectaron bloqueos en estos ensayos. La jugabilidad con mando sigue pendiente de valoración del usuario.

[Ver la comparación completa](assets/media/cpu-comparison-v1/Comparacion-CPU-original-vs-mod.mp4) · [Vídeos por pareja, resultados y límites](docs/cpu-comparison-v1.md)

Contando los sondeos previos, la IA se ejecutó 260,99 s en el original y 254,98 s en la nueva, dentro del máximo de cinco minutos por ROM. No se activaron escenas cinemáticas de especiales en esta tanda, por lo que su restauración natural sigue pendiente de revisar.

## Ki actual: colores por personaje v4

**Ya están implementadas y grabadas las once paletas para revisión. Todos los personajes van sin rayos.** Cell comparte dorado con los Super Saiyan; Ginyu usa lila, Recoome blanco/violeta, Piccolo/A18/Freezer blanco azulado y Krilin blanco. El contorno aprobado se mantiene.

![Ginyu: ki lila dentro del juego](assets/media/ki-colores-v4/Capturas/10-Ginyu.png)

[Ver los once, antes y después](assets/media/ki-colores-v4/Ki-todos-antes-despues.mp4) · [Revisar las salidas a cámara lenta](assets/media/ki-colores-v4/Salida-ki-todos-lenta.mp4) · [Vídeos individuales, pruebas y límites](docs/ki-colores-v4.md)

La comparación muestra el ki nativo con Colores v1 a la izquierda y la nueva aura a la derecha. Son grabaciones reales. La ROM de prueba es de 4 MiB y las once paletas están aceptadas visualmente. La revisión de especiales completos y hardware sigue pendiente.

La [variante anterior sin rayos y paleta común](docs/auras-c2-v3-no-rays.md) se conserva. Los vídeos con rayos de versiones antiguas que aparecen más abajo forman parte del historial.

## Colores de aura: referencias

[Imágenes del anime y decisiones de color](docs/aura-color-references.md). Cell dorado, Ginyu lila y A18 blanca como Freezer son elecciones expresas del usuario; ya están aplicadas en esta prueba v4.

## Corrección del contorno: C2 v3

Tras elegir el tamaño de C2 v2, el usuario señaló puntas cortadas y huecos. **C2 v3 ya corrige esas uniones dentro del juego**, con un contorno de 80 × 128 basado en la referencia SNES aportada. Mantiene el dorado para los superguerreros y el polvo; Cell y Gohan SSJ2 alternan tres formas de rayos blancos. El contorno fue aceptado posteriormente; los rayos de este vídeo se retiraron en la [revisión actual](docs/auras-c2-v3-no-rays.md).

![Ginyu: contorno anterior y corregido, grabación real](assets/media/auras-c2-v3/Ginyu-contorno-antes-despues.gif)

[Ver los once personajes](assets/media/auras-c2-v3/Todas-las-auras-antes-despues.mp4) · [Ver Cell y sus rayos](assets/media/auras-c2-v3/05-Cell.mp4) · [Revisar la salida a cámara lenta](assets/media/auras-c2-v3/Salida-Goku-lenta.mp4) · [Fuentes y pruebas de C2 v3](docs/auras-c2-v3.md)

La salida conserva el contorno entero y lo apaga durante doce ticks; ya no contrae tiras por separado. La ROM de prueba combina Jugabilidad v1, Colores v1 y esta revisión del aura. Las versiones anteriores siguen disponibles.

## Auras C2 v2: dirección elegida e historial

**C2 v2 elegida el 4 de noviembre de 2026:** tamaño, aspecto del aura y polvo aceptados. También quedan aprobados los rayos blancos largos de Cell y Gohan SSJ2.

La revisión posterior detectó extremos de llama rectos y huecos en el contorno, visibles en la captura de Ginyu. **La corrección de esas uniones está en curso**: se mantienen los 80 × 128 píxeles, el polvo y los rayos elegidos. El apartado visual sigue abierto hasta revisar el contorno corregido.

![Comparación real: original, C2 v1 y C2 v2](assets/media/auras-c2-v2/Tres-tamanos-preview.gif)

**Rayos de Cell y Gohan SSJ2, dentro del juego:**

![Rayos blancos y polvo de Cell y Gohan SSJ2](assets/media/auras-c2-v2/Rayos-Cell-Gohan-preview.gif)

[Ver Cell en vídeo](assets/media/auras-c2-v2/05-Cell.mp4) · [Ver Gohan SSJ2 en vídeo](assets/media/auras-c2-v2/01-Gohan-SSJ2.mp4)

La segunda prueba responde a la revisión de tamaño: el aura ocupa **80 × 128 píxeles**, frente a los 64 × 112 de C2 v1 y los 80 × 112 del original. Es un **25 % más ancha y un 14 % más alta que la primera prueba**. Conserva la paleta compartida nativa; el dibujo sigue siendo una adaptación para Mega Drive del concepto elegido.

**Goku y el resto del reparto no llevan rayos; Gohan SSJ2 y Cell, sí.** Sus arcos blancos son intermitentes y alcanzan 32 píxeles, frente a los ocho del recurso anterior. Se añaden dos nubes de polvo animadas junto a los pies, sólo al cargar desde el suelo. Al soltar, la retirada visual sigue durando doce ticks del juego y reduce sus piezas para respetar los límites de dibujo de la consola.

Los vídeos son grabaciones reales de los once personajes. Las pruebas cubren golpes, cargas consecutivas, ambos jugadores y ausencia de polvo en el aire. **La dirección C2 v2 y sus rayos están aceptados; falta corregir y revisar el contorno.** [Detalles, vídeos y evidencia C2 v2](docs/auras-c2-v2.md).

La ROM de prueba combina **Jugabilidad v1 + Colores v1 + Auras C2 v2**. La presentación G, el crédito **- 2026 ALEX LLAO**, los retratos de selección y el HUD H4 todavía están pendientes de integración.

## Propuesta de décimo escenario: montañas nevadas

El usuario ha elegido montañas nevadas para una primera propuesta visual, con vistas de suelo y vuelo. **Son bocetos; el décimo escenario todavía no está integrado en la ROM.**

| En el suelo | Durante el vuelo |
| --- | --- |
| ![Boceto del escenario nevado en el suelo](assets/concepts/stage10-snow/Nieve-propuesta-v1.png) | ![Boceto de la vista aérea del escenario nevado](assets/concepts/stage10-snow/Nieve-vuelo-propuesta-v1.png) |

[Ver ambas vistas y sus referencias](docs/stage10-snow.md). Las imágenes del escenario se han generado como conceptos visuales; los vídeos y GIF de las auras sí son grabaciones del mod en el emulador.

Referencias aportadas: [Super Butōden 2 en The Spriters Resource](https://www.spriters-resource.com/snes/dragonballzsuperbutoden2/) y [archivos conservados con sus créditos](assets/references/super-butoden-2/references.json).

## Revisión de colisiones

**Se conservan las diferencias de tamaño entre personajes.** Que una patada alta no alcance a Gohan puede ser correcto. No hemos cambiado las cajas.

![Visor de cajas nativas](assets/tools/collision-viewer/Visor-colisiones-vista.jpg)

[Descargar y abrir el visor paso a paso](assets/tools/collision-viewer/visor-colisiones.html) · [Resultados y límites](docs/collision-review-v1.md) · [Visor Lua de solo lectura](tools/collision)

El HTML funciona sin conexión y reconstruye 13 ensayos con gráficos nativos y cajas registradas del juego. No es una grabación. Las comparaciones de alcance no detectan cambios en los casos probados; las tablas y rutinas de colisión examinadas conservan sus bytes originales.

## Controles y movimientos

**Mando por defecto:** A = puño, B = patada, C = cambiar entre suelo y vuelo; A+B = cargar ki. Si reasignas los botones, usa su función equivalente.

| Acción | Entrada |
| --- | --- |
| Caminar | Mantener adelante o atrás. |
| Correr hacia delante | Adelante, soltar brevemente, adelante y mantener. |
| Correr hacia atrás | Atrás, soltar brevemente, atrás y mantener. |
| Frenar | Soltar la dirección; conservar una breve inercia como en el original es la conducta elegida para la revisión v2. |
| Saltar / agacharse | Arriba / abajo. |
| Defender | Mantener atrás frente al ataque. |
| Cargar ki | Mantener A+B. |
| Cambiar de lado sin golpear, v6 | Adelante, atrás, adelante + C; cerca del rival, sin A/B simultáneos. |

Las flechas de las tablas suponen que miras a la **derecha**: → = hacia el rival, ← = alejarse. Invierte las direcciones cuando mires a la izquierda. Haz las direcciones en secuencia y pulsa el botón junto a la última. «Mantener ↓» indica carga previa; «en el aire» exige estar saltando o volando. La distancia, el ki y el estado de ambos luchadores también pueden condicionar una técnica.

**Guía del juego original:** combinaciones adaptadas de [StrategyWiki: Moves](https://strategywiki.org/wiki/Dragon_Ball_Z:_Buyuu_Retsuden/Moves), revisión [1096353](https://strategywiki.org/w/index.php?title=Dragon_Ball_Z:_Buyuu_Retsuden/Moves&oldid=1096353), aportada por el usuario. Se conservan sus nombres para facilitar la consulta. Las tablas conservan los comandos originales y añaden, identificado como **nuevo del mod**, el cambio de lado de cada personaje. No equivalen a una validación completa de todos los especiales en el parche.

El **High Speed Move** original de Goku, Gohan y Cell usa → ← → + B y **no golpea**. En la revisión v6, los once personajes pueden cambiar de lado cerca del rival con **→ ← → + C**, sin sustituir sus comandos A/B. Invierte las flechas cuando mires a la izquierda. [Grabaciones y límites](docs/side-switch.md).

**Cambio de lado nuevo:** realiza las direcciones rápidamente y pulsa C con la última. C corresponde a vuelo con el mando por defecto; si reasignas botones, usa esa función. No pulses A ni B a la vez. Funciona cerca del rival, en el mismo plano y desde un estado de movimiento; no cancela ataques, daño ni derribos y puede abortar si no hay espacio al otro lado. La combinación es la misma para los once personajes y ambos jugadores humanos.

<details>
<summary>Goku: movimientos</summary>

| Técnica | Combinación |
| --- | --- |
| **Cadena común (prueba opcional Combos v3, normal)** | Hasta tres básicos de pie A/B al acertar → comando nativo de una técnica propia. [Reglas y ejemplos](docs/combos-v3.md) |
| **Dos puños + patadas (prueba opcional Combos v2, sólo normal)** | A, soltar, A al conectar, B tras el segundo impacto. [Condiciones](docs/combos-v2.md) |
| **Dos puños + proyectil (prueba opcional Combos v1, sólo normal)** | A, soltar, A al conectar; después ← → + A. [Condiciones](docs/combos-v1.md) |
| **Cambio de lado sin golpe (nuevo del mod)** | → ← → + C, cerca del rival y en el mismo plano |
| Energy Blast | ← → + A |
| Consecutive Energy Blast | mantener ↓ ↓ ↙ ← + A |
| Kiai Cannon | mantener ↓ ↓ ↘ → + A |
| Solar Flare | → ← → + A |
| Dash Elbow | ↓ ↙ ← + A |
| Jump Knee Lift | ↙ ↗ + B |
| Flurry Kick | ← ↙ ↓ ↘ → + B |
| Kamehameha | → ↘ ↓ ↙ ← + A |
| Super Kamehameha | ↓ ↙ ← → + A |
| Sliding Kick | → ↘ ↓ + B |
| Slashdown Kick | en el aire: → ↘ ↓ + B |
| High Speed Move | → ← → + B |
| Super Meteor Smash | → ↘ ↓ ↙ ← → + B |

</details>

<details>
<summary>Gohan: movimientos</summary>

| Técnica | Combinación |
| --- | --- |
| **Cadena común (prueba opcional Combos v3, normal)** | Hasta tres básicos de pie A/B al acertar → comando nativo de una técnica propia. [Reglas y ejemplos](docs/combos-v3.md) |
| **Cambio de lado sin golpe (nuevo del mod)** | → ← → + C, cerca del rival y en el mismo plano |
| Energy Blast | ← → + A |
| Kiai Cannon | mantener ↓ ↓ ↘ → + A |
| Shock Wave | → ← → + A |
| Bakuretsu Punch | ← ↙ ↓ ↘ → + A |
| Super Straight Punch | ↓ ↘ → + A |
| Bakuretsu Kick | ← ↙ ↓ ↘ → + B |
| Flying Kick | en el aire: → ↘ ↓ + B |
| Masenko | ← ↙ ↓ ↘ → ← + A |
| Kamehameha | ↓ ↙ ← → + A |
| Sliding Kick | → ↘ ↓ + B |
| High Speed Move | → ← → + B |
| Chou Bakuretsu Rush | → ↘ ↓ ↙ ← → + B |

</details>

<details>
<summary>Piccolo: movimientos</summary>

| Técnica | Combinación |
| --- | --- |
| **Cadena común (prueba opcional Combos v3, normal)** | Hasta tres básicos de pie A/B al acertar → comando nativo de una técnica propia. [Reglas y ejemplos](docs/combos-v3.md) |
| **Cambio de lado sin golpe (nuevo del mod)** | → ← → + C, cerca del rival y en el mismo plano |
| Energy Shot | ← → + A |
| Energy Shock | ← ↙ ↓ + A |
| Shock Wave | → ← → + A |
| Dash Elbow | ↓ ↙ ← + A |
| Knee Upper | ← ↙ ↓ + B |
| Sonic Kick | → ← → + B |
| Flying Kick | en el aire: → ↘ ↓ + B |
| Special Beam Cannon | ↓ ↙ ← → + A |
| Light Grenade | → ↘ ↓ ↙ ← + A |
| Sliding Kick | → ↘ ↓ + B |
| Namekian Style: Moukou Retsuken | ← ↙ ↓ ↘ → ← + B |

</details>

<details>
<summary>Vegeta: movimientos</summary>

| Técnica | Combinación |
| --- | --- |
| **Cadena común (prueba opcional Combos v3, normal)** | Hasta tres básicos de pie A/B al acertar → comando nativo de una técnica propia. [Reglas y ejemplos](docs/combos-v3.md) |
| **Dos puños + patadas (prueba opcional Combos v2, sólo normal)** | A, soltar, A al conectar, B tras el segundo impacto. [Condiciones](docs/combos-v2.md) |
| **Dos puños + proyectil (prueba opcional Combos v1, sólo normal)** | A, soltar, A al conectar; después ← → + A. [Condiciones](docs/combos-v1.md) |
| **Cambio de lado sin golpe (nuevo del mod)** | → ← → + C, cerca del rival y en el mismo plano |
| Energy Blast | ← → + A |
| Consecutive Energy Blast | mantener ↓ ↓ ↙ ← + A |
| Destructo Disc | mantener ↓ ↓ ↘ → + A |
| Ground Flare | ↓ ↘ → + A |
| Slash Arrow Kick | ↓ ↘ → + B |
| Driving Elbow Attack | ↓ ↙ ← + A |
| Super Crush | ← ↙ ↓ + A |
| Big Bang Attack | ← ↙ ↓ ↘ → ← + A |
| Final Flash | ↓ ↙ ← → + A |
| Sliding Kick | → ↘ ↓ + B |
| Final Brid Attack | → ↘ ↓ ↙ ← → + B |

</details>

<details>
<summary>Trunks: movimientos</summary>

| Técnica | Combinación |
| --- | --- |
| **Cadena común (prueba opcional Combos v3, normal)** | Hasta tres básicos de pie A/B al acertar → comando nativo de una técnica propia. [Reglas y ejemplos](docs/combos-v3.md) |
| **Cambio de lado sin golpe (nuevo del mod)** | → ← → + C, cerca del rival y en el mismo plano |
| Energy Cannon | ← → + A |
| Energy Slash | mantener ↓ ↓ ↙ ← + A |
| Double Energy Blast | → ← → + A |
| Ground Flare | ↓ ↘ → + A |
| Slashdown Kick | en el aire: → ↘ ↓ + B |
| Consecutive Kick | → ← → + B |
| Bakuretsu Punch | ← ↙ ↓ ↘ → + A |
| Burning Attack | ↓ ↙ ← → + A |
| Finish Blaster | ← ↙ ↓ ↘ → ← + A |
| Sliding Kick | → ↘ ↓ + B |
| Tornado Breaker | → ↘ ↓ ↙ ← → + B |

</details>

<details>
<summary>Cell: movimientos</summary>

| Técnica | Combinación |
| --- | --- |
| **Cadena común (prueba opcional Combos v3, normal)** | Hasta tres básicos de pie A/B al acertar → comando nativo de una técnica propia. [Reglas y ejemplos](docs/combos-v3.md) |
| **Cambio de lado sin golpe (nuevo del mod)** | → ← → + C, cerca del rival y en el mismo plano |
| Energy Shot | ← → + A |
| Consecutive Energy Blast | mantener ↓ ↓ ↙ ← + A |
| Kiai Cannon | mantener ↓ ↓ ↘ → + A |
| Wave Shock | ← ↙ ↓ + A |
| Ground Slider | ← ↙ ↓ + B |
| Dash Headbutt | ↓ ↙ ← + A |
| Ground Flare | en el aire: ← ↙ ↓ + A |
| Special Beam Cannon | ↓ ↙ ← → + A |
| Kamehameha | → ↘ ↓ ↙ ← + A |
| Sliding Kick | → ↘ ↓ + B |
| High Speed Move | → ← → + B |
| Needle Rush | ← ↙ ↓ ↘ → ← + B |

</details>

<details>
<summary>A18: movimientos</summary>

| Técnica | Combinación |
| --- | --- |
| **Cadena común (prueba opcional Combos v3, normal)** | Hasta tres básicos de pie A/B al acertar → comando nativo de una técnica propia. [Reglas y ejemplos](docs/combos-v3.md) |
| **Cambio de lado sin golpe (nuevo del mod)** | → ← → + C, cerca del rival y en el mismo plano |
| Flash Beam | ← → + A |
| Consecutive Energy Blast | mantener ↓ ↓ ↙ ← + A |
| Energy Slash | → ← → + A |
| Critical Attack | ↓ ↘ → + A |
| Slash Dance | en el aire: → ↘ ↓ + B |
| Dash Elbow | ↓ ↙ ← + A |
| Dash Attack | ← ↙ ↓ + A |
| Super Energy Wave | ← ↙ ↓ ↘ → + A |
| Energy Flame | ↓ ↙ ← → + A |
| Sliding Kick | → ↘ ↓ + B |
| Bloody Drive | ← ↙ ↓ ↘ → ← + B |

</details>

<details>
<summary>Krilin: movimientos</summary>

| Técnica | Combinación |
| --- | --- |
| **Cadena común (prueba opcional Combos v3, normal)** | Hasta tres básicos de pie A/B al acertar → comando nativo de una técnica propia. [Reglas y ejemplos](docs/combos-v3.md) |
| **Cambio de lado sin golpe (nuevo del mod)** | → ← → + C, cerca del rival y en el mismo plano |
| Energy Blast | ← → + A |
| Consecutive Energy Blast | mantener ↓ ↓ ↙ ← + A |
| Destructo Disc | mantener ↓ ↓ ↘ → + A |
| Solar Flare | → ← → + A |
| Bakuretsu Kick | ← ↙ ↓ ↘ → + B |
| Kamehame Attack | ↓ ↙ ← + A |
| Kamehame Down Attack | en el aire: → ↘ ↓ + A |
| Super Kiai Cannon | → ↘ ↓ ↙ ← + A |
| Kamehameha | ↓ ↙ ← → + A |
| Sliding Kick | → ↘ ↓ + B |
| Turtle School Style: Gekishuu Ranbu | → ↘ ↓ ↙ ← → + B |

</details>

<details>
<summary>Freezer: movimientos</summary>

| Técnica | Combinación |
| --- | --- |
| **Cadena común (prueba opcional Combos v3, normal)** | Hasta tres básicos de pie A/B al acertar → comando nativo de una técnica propia. [Reglas y ejemplos](docs/combos-v3.md) |
| **Cambio de lado sin golpe (nuevo del mod)** | → ← → + C, cerca del rival y en el mismo plano |
| Frieza Beam | ← → + A |
| Destructo Disc | mantener ↓ ↓ ↘ → + A |
| Frieza Cutter | → ← → + A |
| Ground Flare | ↓ ↘ → + A |
| Tail Cut | → ← → + B |
| Head Attack | ← ↙ ↓ + A |
| Dash Elbow | ↓ ↙ ← + A |
| Mega Buster | ↓ ↙ ← → + A |
| Death Ball | ← ↙ ↓ ↘ → ← + A |
| Sliding Kick | → ↘ ↓ + B |
| Frieza Tail Buster | ← ↙ ↓ ↘ → ← + B |
| Frieza Psychokinesis | → ↘ ↓ ↙ ← → + B |

</details>

<details>
<summary>Recoome: movimientos</summary>

| Técnica | Combinación |
| --- | --- |
| **Cadena común (prueba opcional Combos v3, normal)** | Hasta tres básicos de pie A/B al acertar → comando nativo de una técnica propia. [Reglas y ejemplos](docs/combos-v3.md) |
| **Cambio de lado sin golpe (nuevo del mod)** | → ← → + C, cerca del rival y en el mismo plano |
| Energy Blast | ← → + A |
| Consecutive Energy Blast | mantener ↓ ↓ ↙ ← + A |
| Energy Defense | → ← → + A |
| Mach Attack | ↓ ↘ → + A |
| Power Bomb | ← ↙ ↓ + A |
| Crush Down | ↓ ↘ → + B |
| Recoome Kick | ← ↙ ↓ + B |
| Fighting Bomber | → ↘ ↓ ↙ ← + A |
| Eraser Gun | ↓ ↙ ← → + A |
| Sliding Kick | → ↘ ↓ + B |
| Ultra Fighting Dance | → ← → + B |
| Recoome Death Driver | → ↘ ↓ ↙ ← → + B |

</details>

<details>
<summary>Ginyu: movimientos</summary>

| Técnica | Combinación |
| --- | --- |
| **Cadena común (prueba opcional Combos v3, normal)** | Hasta tres básicos de pie A/B al acertar → comando nativo de una técnica propia. [Reglas y ejemplos](docs/combos-v3.md) |
| **Cambio de lado sin golpe (nuevo del mod)** | → ← → + C, cerca del rival y en el mismo plano |
| Energy Blast | ← → + A |
| Energy Cannon | mantener ↓ ↓ ↘ → + A |
| Ground Explosion | → ← → + A |
| Ground Flare | ↓ ↘ → + A |
| Straight Kick | → ← → + B |
| Dash Elbow | ↓ ↙ ← + A |
| Dynamite Punch | ← ↙ ↓ ↘ → + A |
| Terra Smash | ↓ ↙ ← → + A |
| Sliding Kick | → ↘ ↓ + B |
| Body Change | ← ↙ ↓ ↘ → ← + B |

</details>

Atribución: colaboradores de StrategyWiki, enlace y revisión indicados arriba. Esta adaptación de sus tablas se ofrece bajo [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/); se han convertido los iconos a texto, añadido la correspondencia A/B y notas del proyecto. Esa licencia se aplica a esta adaptación documental, no declara una licencia para la ROM ni para todo el repositorio.

## Historial: las cuatro mejoras de jugabilidad v1

1. **Parada más rápida (retirada en v2):** la cancelación añadida rompía el doble toque para correr. La revisión actual recupera el movimiento y la inercia nativos a petición del usuario.
2. **Pulsación pendiente:** una nueva pulsación de puño o patada se conserva durante cinco actualizaciones posteriores de entrada. Si termina la recuperación a tiempo, se ejecuta; una entrada demasiado temprana caduca.
3. **Recuperaciones ajustadas:** se recortan hasta dos ticks del tramo final de secuencias simples de golpes básicos, al llegar a su pose final.
4. **Vuelta a guardia más suave:** se enlazan unas pocas poses existentes; empezar otra acción cancela la transición visual inmediatamente.

Estos ajustes se centran en **movimiento terrestre y golpes básicos**. Se conserva la velocidad general y el turbo nativo; salto, vuelo y especiales mantienen sus reglas originales. Mantener A no debe producir ataques repetidos automáticamente.

### Qué se ha comprobado

- 11 personajes × 2 velocidades: **22 combinaciones** de pruebas.
- **32 situaciones** de alcance, golpes y defensa con el mismo daño que el original.
- **15 interrupciones por daño** sin que salga un ataque pendiente después del golpe recibido.
- Segundo mando y una secuencia prolongada contra CPU.
- Checksum de Mega Drive, aplicación del IPS e integridad de los archivos.

La evidencia histórica está en [evidence/gameplay-v1](evidence/gameplay-v1). Las pruebas se hicieron en **Genesis Plus GX v1.7.4 f27655b**; falta la prueba del usuario con mando y no se ha validado en consola física. No es una validación completa de todos los combos y enfrentamientos.

## Generar tu ROM

Necesitas **Node.js 22.13 o posterior**, **pnpm 11.18.0** y tu copia de la ROM japonesa original de 2 MB. Las herramientas de construcción usan sólo módulos incluidos en Node.

```sh
pnpm install --frozen-lockfile
pnpm check
pnpm test

# Revisión actual v6.1: incluye cambio de lado y paleta de apertura corregida
pnpm build:review --rom "ruta/a/original.bin"

# Historial: controles v1 y colores originales
pnpm build --rom "ruta/a/original.bin"

# Los mismos controles y las paletas Colores v1
pnpm build:colors --rom "ruta/a/original.bin"

# Historial: controles v1, colores y auras C2 v2
pnpm build:auras:v2 --rom "ruta/a/original.bin"
```

También puedes colocar la base en `roms/original.bin` y ejecutar `pnpm build`. El resultado aparece en `dist/`, con un registro de hashes. El archivo de entrada nunca se sobrescribe.

**SHA-256 de la base admitida:**

```text
217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557
```

Abre el BIN generado en tu emulador **desde el arranque**, sin estados guardados de otra ROM. El repositorio contiene fuentes, parches y comparaciones; las ROMs completas se generan localmente. [Construcción y ensamblado](docs/build.md).

## Dirección gráfica

### Presentación elegida: G — C con contraste marcado

![Presentación G, captura real de la paleta elegida](assets/comparisons/title/G.png)

La piel de G parte de C con sombras más marcadas y menos amarillo. El crédito solicitado es **- 2026 ALEX LLAO**, con el nombre real; su cambio gráfico está pendiente. Esta elección todavía no forma parte de la ROM de jugabilidad v1. **Las demás variantes se conservan** para poder volver atrás o retocar el tono de piel.

### Comparar el resto

| Personajes | Escenarios |
| --- | --- |
| [![Personajes](assets/comparisons/overview/01-Personajes-todas.png)](docs/graphics.md#personajes) | [![Escenarios](assets/comparisons/overview/03-Escenarios.png)](docs/graphics.md#escenarios) |

[Las 71 imágenes y todas las variantes →](docs/graphics.md)

Reglas guardadas: retratos originales de selección para el HUD; jugador 2 mirando hacia el centro; **Goku C2 con llamas y polvo, sin rayos**. **Cell y Gohan SSJ2 deben llevar rayos; los demás, sin rayos**. Los conceptos anteriores con rayos se conservan como historial.

## Estructura

```text
assets/          Comparaciones y vídeo de jugabilidad
docs/            Construcción, estado, decisiones, pruebas y hoja de ruta
evidence/        Resultados históricos de las comprobaciones en emulador
patches/         IPS y manifiesto de hashes
project/         Catálogo de imágenes y elecciones en formato legible
research/        Datos de paletas y fuentes históricas de investigación
src/gameplay/    Ensamblador 68000 del parche y código verificado en hexadecimal
src/auras/       Fuente, tiles y mapas del prototipo C2
tests/           Pruebas de las herramientas de parcheo
tools/           Construcción, verificación y ensamblado local
roms/            Base local, excluida de Git
```

La rama de trabajo es **`development`**. Cada cambio debe conservar las variantes anteriores, actualizar su estado y distinguir entre **propuesto**, **elegido**, **implementado** y **probado**. Ver [CONTRIBUTING.md](CONTRIBUTING.md).

## Próximo paso

Corregir las uniones, los cortes rectos y los huecos del contorno del aura, manteniendo el tamaño, el polvo y los rayos aceptados; volver a grabarlo y revisarlo. Después, integrar la presentación G, el crédito, los retratos elegidos y el HUD H4. La prueba con mando, los ataques especiales y la validación en consola siguen pendientes; las localizaciones nuevas permanecen en espera.

Proyecto de modificación no oficial. Los personajes, el juego original y Hyper Dragon Ball Z se mencionan como obras y referencias de sus respectivos autores. [Créditos y procedencia](docs/credits.md).

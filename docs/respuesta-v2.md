# Respuesta v2: entradas, frenada, saltos y tercera bola

Prueba de jugabilidad del 5 de noviembre de 2026, sobre Respuesta v1. Arrancar desde cero a velocidad normal, **sin estados guardados de versiones anteriores**: el estado del parche se ha trasladado a otra zona de RAM.

[Vídeo real con sonido, 1:18: antes/después y prueba de combate](../assets/media/responsive-v2/Respuesta-v2-controles-saltos-y-tres-bolas.mp4). Las tomas de cada prueba parten de estados preparados; el último tramo mezcla movimiento y ataques con dos mandos automatizados. No es una sesión humana continua.

## Cambios para probar con mando

- **Entradas de Goku:** reconocedor propio más tolerante. Conserva el gesto si el primer intento falla, admite componentes de diagonales y un pequeño margen de botón anticipado o retrasado. Comprueba los movimientos largos antes de los cortos. En el gesto doble deja un margen breve para reunir A+B, evitando elegir Super Kamehameha si A llega ligeramente antes que B. Al completar un especial con el botón algo anticipado, puede reconducir el arranque de un básico aún inactivo; no interrumpe técnicas ni golpes activos por esta vía.
- **Caminar:** al soltar la dirección termina el paso pendiente y deja una frenada corta de cuatro actualizaciones. En la muestra de Goku, un toque de dos fotogramas pasa de 33 píxeles de avance extra a 2. La velocidad al mantener la dirección no cambia. Esta corrección apunta a caminar; la carrera por doble toque conserva su comportamiento anterior.
- **Salto normal:** primera propuesta con aproximadamente tres cuartas partes de altura y menor tiempo en el aire. En Goku, el salto vertical y los dos diagonales pasan de 116 a 87 píxeles y de 48 a 35 fotogramas en el aire. Se modifican los parámetros y el tiempo del salto voluntario, no la velocidad general del juego. El vuelo con C y las trayectorias de las técnicas no reciben esos cambios.
- **Tercera bola:** se separa la memoria del parche de los datos nativos de los proyectiles. La ráfaga produce tres impactos reales en las cuatro distancias comprobadas. No se añade daño ficticio ni se modifican colisiones para fabricar el tercer impacto.
- Se conservan la salida rápida de carga, la parada a ki máximo, el buffer de carga, los cancels de básicos que aciertan y el control del lanzador antes de que el rival aterrice.

La fluidez y el equilibrio siguen sujetos a prueba con mando. Superar las secuencias automáticas no garantiza que toda combinación de mando, dirección y momento vaya a sentirse perfecta.

## Comandos de Goku en esta ROM

Mirando hacia la derecha. Invierte izquierda y derecha al mirar hacia la izquierda. Pulsa el botón con el final del gesto; las flechas representan el movimiento que se pretende realizar, aunque el reconocedor tolere algunas diagonales no muestreadas por separado.

| Técnica | Comando |
| --- | --- |
| Energy Blast / proyectil básico | ← → + A |
| Consecutive Energy Blast / ráfaga de tres bolas | ↓ ↘ → + A |
| Kiai Cannon | → ↓ ↘ + A |
| Solar Flare | ↓, soltar, ↓ + A |
| Dash Elbow / codazo | ↓ ↙ ← + A |
| Jump Knee Lift / rodillazo | → ↓ ↘ + B |
| Flurry Kick / patadas múltiples | ↓ ↙ ← + B |
| **Kamehameha** | **← ↙ ↓ ↘ → + A** |
| **Super Kamehameha** | **← ↙ ↓ ↘ →, ← ↙ ↓ ↘ → + A** |
| Sliding Kick / deslizante | ↓ ↘ → + B |
| Slashdown Kick / descendente | En el aire: ↓ ↘ → + B |
| High Speed Move / desplazamiento original | → ← → + B |
| **Super Meteor Smash** | **← ↙ ↓ ↘ →, ← ↙ ↓ ↘ → + A+B** |
| Cambio de lado del mod, sin golpe | → ← → + C, cerca del rival |

**A+B sin el gesto completo sigue cargando ki.** Al cambiar Kamehameha al medio círculo, la ráfaga ocupa el cuarto de círculo para evitar comandos duplicados. El nuevo reconocedor se limita a Goku humano; los otros personajes y la CPU conservan sus comandos. Se mantienen las condiciones de ki, distancia, suelo/aire y estado de cada técnica.

Para probar el buffer: mantén A+B, introduce el medio círculo del Kamehameha, suelta A+B y pulsa A enseguida. El comando reconocido tiene un plazo corto y caduca; no queda guardado para un ataque mucho después. Si preparas los dos medios círculos durante la carga, suelta A+B y vuelve a pulsar A para Super Kamehameha o A+B para Meteor. El gesto se conserva hasta conocer el botón final, para no confundir esas dos técnicas. Una entrada de gesto incompleto no debe convertirse en un Super o Meteor.

## Qué se ha probado

- **200 variantes** de entrada de Goku, con ambas orientaciones: gestos completos o cardinales, distintos ritmos, botón anticipado/retrasado y movimientos incorrectos. Pasan las 200, incluidos los casos negativos que deben rechazarse.
- **10 pruebas del Meteor** entre ambos mandos, con A y B simultáneos o separados hasta dos fotogramas en cualquier orden.
- Segundo mando y gesto invertido durante carga; caducidad del buffer; comprobación de que fallar un básico o golpear la guardia no activa la asistencia de cancels por contacto.
- Carga, barra llena y enlaces en los **once personajes**. Las rutas no se fuerzan a conectar cuando el alcance o la reacción nativa no lo permiten.
- **88 200 fotogramas**, unos **24,5 minutos acumulados**, con dos puertos automatizados: once personajes y nueve escenarios. Se restauran estados iniciales cargados al acabar una vida o cada 1800 fotogramas. Se comprueba, entre otras cosas, que las coordenadas del tercer proyectil no vuelvan a adquirir los valores corruptos del parche anterior. No equivale a 24 minutos de combate humano continuo ni valida todo el equilibrio.
- Tres impactos de la ráfaga a distancias iniciales de 32, 64, 120 y 180 píxeles; cinco pruebas de frenada por toques de distinta duración; salto vertical y diagonales de Goku.

El vídeo presenta antes/después de caminar, saltar y disparar la ráfaga; Kamehameha, Super y Meteor nuevos; buffer durante carga; puño enlazado a Kamehameha; orientación izquierda y un tramo de movilidad y ataques variados. Son imágenes del emulador, sin contador añadido en edición. Las posiciones se fijan al comienzo de las pruebas cercanas y el ki se carga con A+B; no se fuerzan impactos, HP ni reacciones para grabar las demostraciones.

## Corrección de memoria y asuntos pendientes

La tercera ranura nativa de proyectil usa campos del actor desde `0x104` en adelante, entre ellos X en `0x108`, Y en `0x10C` y tipo en `0x11E`. Las versiones anteriores habían usado parte de esa zona para controles, auras, combos y HUD. Esa suposición era incorrecta: la tercera bola y el parche se sobrescribían mutuamente.

Se trasladan **168 referencias** a un estado separado: los campos del parche `0x104..0x117` y `0x120..0x125` pasan a un desplazamiento adicional de `0xC00`. P1 queda en `0xFFFFF462..F483` y P2 en `0xFFFFF58A..F5AB`. Los estados adicionales de entradas usan `0xFFFFF700..F73F`. La rutina de nueva ronda limpia estas zonas. Los datos nativos del proyectil recuperan su espacio original.

El traslado incluye el estado del HUD para eliminar la colisión de memoria, pero **no cambia las reglas de conteo HITS ni las fórmulas de stun**. Las discrepancias señaladas por el usuario siguen pendientes de valoración. Tampoco se han cambiado el daño, las cajas de colisión o la reacción nativa al golpe. No se afirma haber resuelto todas las rarezas del HUD por haber corregido esta causa de corrupción.

Pendiente: valorar con mando la altura del salto, la pequeña inercia y las tolerancias; revisar turbo y hardware original; seguir buscando entradas perdidas, acciones accidentales, rutas abusivas y problemas de HITS/stun. Las propuestas de árbol, nave y nuevas sacudidas continúan fuera de esta ROM.

Construcción:

```sh
pnpm build:review --rom ruta/a/original.bin --version responsive-v2
```

[Manifiesto](../patches/responsive-v2/manifest.json) · [Validación resumida](../evidence/responsive-v2/validation.json) · [Matriz de entradas](../evidence/responsive-v2/input-matrix.json) · [Traslado exacto de referencias](../evidence/responsive-v2/relocations.json) · [ASM del reconocedor y frenada](../src/gameplay/responsive-v2/inputs.asm).

# Namek R6: revisión real desde la ROM

**Revisión reabierta:** después de volver a ver las tres variantes, el usuario señala falta de definición y cortes en el cielo de Porunga. La preferencia anterior por R6 no se considera una aprobación final del acabado. Se prepara [R8 con la casa corregida, roca fina, Porunga redibujado y cielo reconstruido](namek-native-r8.md). R6 se conserva como referencia histórica.

9 de noviembre de 2026. [Los tres maestros de arte están aprobados](namek-revision-r6.md), incluido el devastado con volcán distante, humo y una casa rota más cercana. El usuario pide explícitamente integrarlos y que el vídeo salga de la ROM, para revisión personal y sin subirlo. **La aprobación del dibujo no se extiende automáticamente a esta adaptación nativa.**

Vídeo local: `Namek-R6-ROM-tres-escenarios.mp4`, carpeta de entrega `outputs/Namek-R6-ROM-revision`, aproximadamente **2:34**. No se publica en YouTube ni se copia el MP4 al repositorio. Es una captura directa del framebuffer y sonido de Genesis Plus GX, a velocidad normal. No se sustituye el fondo en posproducción. Solo se añaden rótulos y se concatenan las tomas.

| Parte | Inicio aproximado | Captura real de la ROM | Mapa nativo completo |
| --- | --- | --- | --- |
| Namek normal | 0:00 | [PNG](../assets/media/namek-native-r6/normal-ROM.png) | [512×512](../assets/media/namek-native-r6/normal-mapa.png) |
| Devastado con lava | 0:51 | [PNG](../assets/media/namek-native-r6/aldea-ROM.png) | [512×512](../assets/media/namek-native-r6/aldea-mapa.png) |
| Invocación de Porunga | 1:43 | [PNG](../assets/media/namek-native-r6/porunga-ROM.png) | [512×512](../assets/media/namek-native-r6/porunga-mapa.png) |

En cada escenario: vuelo y aterrizaje, Goku con básicos/Kamehameha, Gohan con Masenko, Vegeta con Meteor, Cell con cruce/Meteor y ataque grande con pantalla partida. Se preparan las posiciones iniciales y se coordinan entradas; son tomas de demostración, no partidas espontáneas ni una certificación de combos inevitables.

## Patrones y adaptación

Los maestros de1254×1254 se conservan intactos. El juego recibe mapas de512×512 con paletas de Mega Drive. **La imagen nativa no es una copia exacta del maestro.** El cambio de paleta y el presupuesto de patrones requieren una adaptación separada.

- El suelo recupera un módulo completo de128 píxeles de ancho del terreno original, con reflejo y repetición a escala1:1. Solo se usa desdeY392: no se reutilizan los arcos sueltos y fragmentos de acantilado que causaban los errores de V5. La casa destruida cercana y sus grietas se conservan por encima de ese módulo. DesdeY432 el módulo nativo queda exacto, sin aproximación de textura.
- Las mesetas usan el normal como referencia compartida. El ruido de color aislado se consolida dentro de la roca. Durante el empaquetado se preservan los límites de **cada tono de roca**, además del contorno de los materiales: no se permite intercambiar una luz de la ladera por una sombra al elegir un tile.
- Para reservar más patrones a las laderas se reutilizan nubes completas, alineadas a tiles, en el devastado y Porunga. Esto modifica parte de las nubes respecto al maestro. No se reducen a una miniatura para ampliarlas después.
- Los colores de tierra siguen la dirección neutral de V4. El devastado reserva tonos para lava y grises de humo; Porunga usa verdes y azul oscuro. Los diez colores comunes del juego no cambian. La casa del Patriarca tiene exactamente los mismos colores y píxeles protegidos en las tres variantes.

El horizonte del devastado usa un solo banco y un gris compartido con el cielo. Se elimina la selección de banco según la cobertura de cada tile: producía rectángulos visibles en la niebla. Algunas nubes bajas y gradaciones del maestro se simplifican al fijar ese gris; la composición superior usa la nube reutilizable.

Una primera prueba R6 se descartó durante la revisión del vídeo porque la aproximación de tonos generaba bloques visibles en las rocas. La entrega usa la revisión corregida: compartir patrones no altera las fronteras de sus luces y sombras. El resto del detalle puede aproximarse dentro de contornos equivalentes; el acabado sigue pendiente de valoración.

**Lava, humo y Porunga permanecen estáticos.** Se ve movimiento de personajes, efectos nativos, cámara y scroll. No se ha implementado todavía flotación de Porunga ni animación volcánica.

## Build y comprobaciones

ROM experimental **v1.0 build `20261109-115335`**, SHA-256 `7e2bd26e6b801c823a1be61ba79bfbdb1719c0b51eba62b971ceeffa7c92c084`. Se conserva el padre aprobado `20261108-200852`, SHA-256 `68f838f7ce1fcf0f237d56c09826a359d26931d331cc1ec9716b9d321654ffab`. Esta revisión no modifica la jugabilidad.

Los tres recursos usan **736 patrones**, dentro del área anterior a VRAM0x5C00, y22 entradas propias de CRAM. La deduplicación acepta reflejos de tile; no desplaza el contorno para encajar.

| Variante | Grupos de contorno protegidos | Cambios de frontera de roca al compartir patrones | Cambios de textura tras cuantizar |
| --- | ---: | ---: | ---: |
| Normal | 646 | 0 | 266 píxeles |
| Devastado | 653 | 0 | 418 píxeles |
| Porunga | 732 | 0 | 8225 píxeles |

Las cifras parten de la imagen ya cuantizada y adaptada, no del maestro de1254×1254. No incluyen la cuantización inicial, limpieza de ruido, reutilización de nubes ni sustitución del primer plano por textura nativa.

- Selección con mandos desde el menú nativo, en un arranque nuevo de la ROM final: tres variantes por cuatro emparejamientos para preparar las tomas. Los estados anteriores no se reutilizan porque contendrían la VRAM de otra prueba.
- Quince comprobaciones de recursos: gráficos cargados en VRAM y22 palabras de CRAM idénticos a los compilados, en suelo, vuelo de uno y de ambos personajes, aterrizaje y carga de energía.
- Dieciocho tomas con escenario físico6 y variante correcta en todos los fotogramas registrados. En las muestras se conservan88 de daño con Goku,71 con Gohan,74 con Vegeta y105 con Cell; no se cambia la lógica de impactos.
- La ROM solo cambia recursos de los escenarios extra, enganches del selector ya existentes, cabecera y checksum. El Namek original y los recursos comunes quedan intactos. El vídeo se decodifica completo con FFmpeg, con audio y velocidad normal.

[Build y límites de escritura](../evidence/namek-native-r6/integrated-build.json) · [Selección desde menú](../evidence/namek-native-r6/selection-proof.json) · [VRAM y CRAM](../evidence/namek-native-r6/runtime-validation.json) · [Tomas y procedencia del vídeo local](../evidence/namek-native-r6/delivery-manifest.json) · [Fuentes del compilador y captura](../research/namek-native-r6/README.txt).

Entrega solo del vídeo local y capturas; no se entrega ROM. Probado en Genesis Plus GX; consola física pendiente. El selector conserva los extras NUEVO/RUINAS/DRAGON de la prueba anterior. No se crea aquí un modo práctica independiente ni se cambian comandos, combos o controles.

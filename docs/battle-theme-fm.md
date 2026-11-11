# Battle theme: primer boceto de audio FM

11 de noviembre de 2026. El usuario aporta un MP3 de92,24s y pide probar una adaptación para una futura BGM seleccionable. Se prepara una muestra local de los primeros25s. **Es un boceto de transcripción e instrumentación automática, no una versión musical terminada. No está integrada en Buyuu Retsuden ni se ha añadido BGM8 al menú.**

## Archivos de escucha

En `outputs/Battle-theme-prueba-FM/` del espacio de trabajo:

- `Battle-theme-boceto-FM-25s.mp3`: muestra FM/PSG,25,13s incluyendo el margen del MP3.
- `Referencia-original-25s.mp3`: mismo fragmento de la referencia, para comparar.
- `LEEME.txt` y `procedencia.json`.

Los audios quedan locales y se entregan en el chat; no se publican ni se suben al repositorio. La referencia original completa permanece en la ruta facilitada por el usuario. No se atribuye la composición a los metadatos del descargador.

## Cómo se ha generado

Estimación armónica de notas mediante FFT, separación aproximada de contenido sostenido y percusivo, ajuste no negativo a plantillas de armónicos y seguimiento temporal de melodía/bajo. Se asignan cinco partes afinadas a voces FM, un bombo FM y ruido PSG para percusión. El análisis es aproximado: melodía, acordes, inversiones, articulación y timbres requieren revisión musical. No se afirma una transcripción fiel nota por nota.

El sonido se genera mediante **un reproductor68000 independiente y original**, ejecutado en Genesis Plus GX v1.7.4 f27655b. Interpreta2883 escrituras de registros YM2612/PSG sincronizadas al VBlank. No contiene la ROM del juego ni reproduce muestras PCM del MP3. El código y los registros de la prueba se conservan; la secuencia musical derivada queda local en `work/battle-theme-fm/score.json`.

Una prueba de tono de440Hz devuelve440Hz medidos. La captura nativa del boceto tiene25,68s con cola de liberación, pico0,180FS y cero muestras saturadas; el reproductor alcanza todos los pasos previstos. Se prepara el MP3 de escucha con objetivo de−16LUFS y−1,5dBTP, un fundido final de250ms y192kbps. Estas comprobaciones verifican síntesis, afinación y ausencia de saturación, **no certifican la calidad musical**.

## Integración pendiente

El selector original tiene siete opciones de BGM. Se ha localizado el recorrido de esas entradas y su tabla en3B8E4. La inicialización del sonido del juego en1AF442 copia8008bytes desde1B5CF8 a la RAM del Z80. Eso no establece todavía el formato completo de las canciones ni garantiza que el reproductor de audición sea intercambiable con el del juego.

Faltan revisión musical, bucle de la canción, adaptación al formato/reproductor del juego, nueva entrada del selector y pruebas conjuntas con golpes, voces y combate. La ROM actual sigue siendo **v1.0 build20261110-173703**, SHA-256 `666135fff3069ecd06d25bab945b43970d929fea5d3493b88ff1fe6a54ca1f7f`, sin modificar.

[Procedencia y archivos](../evidence/battle-theme-fm/manifest.json) · [Calibración](../evidence/battle-theme-fm/tone-render.json) · [Captura nativa](../evidence/battle-theme-fm/draft-render.json) · [Reproductor comentado](../research/battle-theme-fm/player.asm).

Referencia técnica primaria consultada para el chip: [código del emulador Nuked OPN2](https://github.com/nukeykt/Nuked-OPN2/blob/master/ym3438.c). No se incorpora ese código a este reproductor; la captura utiliza el núcleo Genesis Plus GX local del proyecto.

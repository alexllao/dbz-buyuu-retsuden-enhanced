# Recuperación aérea defensiva: Goku y Vegeta

18 de noviembre de 2026. **Prototipo v1.0 build `20261118-152153`**, SHA-256 `d3a29d308473b966ed4edda70a0b9df154f1badb2371e92e0d7b23e7b2ccc3fb`. Prueba solicitada por Alex para responder a las nuevas persecuciones aéreas. No sustituye una versión validada con mando.

## Cómo se usa

**A + C después de recibir un básico durante la persecución aérea enemiga.** Solo Goku y Vegeta humanos, velocidad normal. Cuesta32 de ki, exige una pulsación nueva del acorde y se permite una vez por cadena. No basta con mantener A+C antes del golpe.

La ventana se abre tras un contacto real del básico durante12 actualizaciones nativas. Al aceptarse, el defensor sale de la reacción, recupera su pose de salto y retrocede48 píxeles en12 actualizaciones, con un pequeño impulso vertical y caída continua. Durante esa retirada se protege del filtro de básicos; no se implementa inmunidad global frente a proyectiles. No cura vida ni devuelve el daño anterior. El coste se descuenta una sola vez:225→193 en las tomas. El control ofensivo vuelve después de la retirada; los contraataques del Short se introducen manualmente tras aterrizar.

No se activa en suelo, en un derribo fuerte o cuando el atacante ya ejecuta ki/Meteor. No rompe un Meteor ya iniciado. Los mandos siguen sus acciones originales fuera de esa situación. La CPU no usa todavía la nueva defensa. Al quedar ambos en suelo y libres, con las cadenas cerradas, vuelve a habilitarse para el siguiente intercambio. Se limpia el estado al iniciar ronda.

Se conservan el daño, las poses del juego, los tres Namek, la recuperación nativa/K4 y el sonido de aterrizaje. La función usa los bytes libres +2A..2D de los slotsF800/F840 y fase6; no ocupa el estado de proyectiles ni cambia las tablas globales de stun/HITS.

## Pruebas realizadas

- **48 casos de defensa**: dos personajes, ambos puertos, ambos sentidos, seis situaciones. Ocho recuperaciones válidas con contraataque; controles sin acorde, acorde mantenido antes del golpe, ki0, entrada tarde y crédito ya consumido. Ki0 y crédito usado son fixtures explícitos para aislar esas puertas, nunca usados en vídeos.
- **10 comprobaciones aisladas**: suelo, HP0, reacción fuerte, acción de Meteor, acción de ki, turbo, A solo, C solo, ki31 y ki32. Parten de un contacto real y fijan la condición antes de unos fotogramas. Son pruebas sintéticas de las puertas, no reproducciones completas de cada Meteor/KO.
- **28 rutas anteriores** de persecución/ki/Meteor, ambos mandos/sentidos, conservan contactos, daño, limpieza de fases y solicitud del sonido de aterrizaje. Se repiten los10 negativos anteriores de persecución.
- Cuatro tomas nuevas con recursos VRAM/paleta verificados al empezar y durante la recuperación. Los estados provienen del menú del prototipo151610, compatible con la distribución nativa y slots del build final152153. La grabación final usa la ROM con el hash indicado arriba. Durante las tomas solo se envían botones; distancia/orientación se preparan antes.

En la ruta control de Vegeta defensor recibe37 de daño sin escapar y25 con recuperación: evita la segunda patada. En la ruta concreta de Goku la patada de seguimiento ya falla por separación en el control, de modo que recibe18 con o sin recuperación; la retirada y el contraataque funcionan, pero esa toma **no demuestra daño evitado**. No se certifica que todo seguimiento conecte ni que los contraataques sean inevitables. Los adversarios son dos puertos humanos programados; no es una CPU reactiva.

## Short entregado

**24,915 s,1080×1920**, archivo local `outputs/YouTube-Short-Defensa-Aerea/DBZ-Defensa-Aerea-Short.mp4`. Cuatro secuencias: Goku recupera y responde con Kamehameha, Vegeta con Final Flash; luego se alternan puerto y sentido. Se muestran todos los contactos del contraataque y la recuperación del defensor. Algunos cortes suceden mientras el rival sigue derribado por el contraataque.

Pantalla/HUD completos a escala entera3×, audio nativo, velocidad normal y rótulos temporizados fuera del juego. Sin preguntas al público ni menciones a IA en los textos públicos. Se verifican resolución/duración, hashes, escenario/variante de cada fotograma seleccionado, programas de contraataque y decodificación completa del vídeo; se revisan capturas de recuperación y remate. El MP4 permanece local, sin publicación automática.

[Vista del Short](../assets/media/air-recovery/short.png) · [Goku recuperado](../assets/media/air-recovery/goku-recupera.png) · [Vegeta recuperado](../assets/media/air-recovery/vegeta-recupera.png) · [Título y descripción](short-air-recovery-texto.txt).

Pendientes: comodidad con mando, equilibrio del coste/ventana, otros personajes y ataques, persecución cerca de los límites del escenario, pruebas completas de interrupción/KO en la retirada, CPU, turbo y consola real. Las puertas aisladas no certifican esas rutas completas. La lectura extrema de comandos y la auditoría general de HITS/stun continúan pendientes.

[48 casos](../evidence/air-recovery/defense-matrix.json) · [Puertas](../evidence/air-recovery/guard-tests.json) · [Enlaces anteriores](../evidence/air-recovery/matrix.json) · [Short](../evidence/air-recovery/short-manifest.json) · [Capturas](../evidence/air-recovery/captures.json) · [ASM comentado](../research/air-recovery/pursuit.asm).

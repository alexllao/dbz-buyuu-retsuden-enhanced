# Persecución + Meteor y recuperación de caída

18 de noviembre de 2026. ROM experimental **v1.0 build `20261118-143144`**, SHA-256 `bd352394b7b091863b57c8aa53b84b702e1234565b9af11bb670267247f591d4`. Conserva la base con selector japonés, los tres Namek R10 y las cargas de ki en combo. El prototipo anterior140820 permanece como histórico; no se publica todavía una ROM de lanzamiento.

## Meteor corregido

Se enlazan lanzamiento, ↑ + C, A, B y Meteor con Goku o Vegeta. El lector ya reconocía la técnica, pero el asistente de cancelación reemplazaba el buffer de48 actualizaciones por el de6 reservado para acciones aéreas inmediatas. El comando desaparecía antes de tocar suelo. Se conserva el buffer largo de Meteor, se espera a que ambos actores aterricen y se inicia la técnica nativa, respetando sus requisitos de vida/ki. No se inventan animaciones de Meteor en el aire ni se mueve de golpe a los actores al suelo.

Vídeo local **32,438 s**: `outputs/Persecucion-Aerea-Meteor/DBZ-Persecucion-Aerea-Combos-Meteor.mp4`. Cuatro tomas, Goku y Vegeta, ambas orientaciones y tres Namek. Cada toma alcanza el último golpe del Meteor y la recuperación del atacante. Pantalla/HUD completos, audio real y velocidad normal, sin vibración añadida.

## Caída tras las ondas

Alex señala los brazos extendidos durante todo el descenso en el primer Short. En esta revisión Kamehameha, Super Kamehameha y Final Flash, usados como remate de la persecución, conservan una breve pose de disparo después de crear la onda y vuelven al salto/descenso. Se recuperan las poses originales11/8 según altura y la pose de suelo al aterrizar. Se conserva la trayectoria continua y la gravedad propia del prototipo aéreo: **no se afirma que sea la rutina física original de salto**. Tampoco se adelanta la generación de la onda ni se interrumpe la carga antes del disparo. Los especiales fuera de la persecución no reciben esta salida anticipada.

Short actualizado **22,895 s**: `outputs/YouTube-Short-Persecuciones-Aereas-v2/DBZ-Combos-Aereos-Short.mp4`. El archivo anterior no se sobrescribe.

[Comandos para jugar](comandos-persecucion-aerea.md) · [Meteor de Vegeta](../assets/media/air-pursuit-meteor/meteor-vegeta.png) · [Goku recupera la caída](../assets/media/air-pursuit-meteor/goku-caida.png) · [Vista del Short v2](../assets/media/air-pursuit-meteor/short-v2.png).

## Pruebas y límites

- **28 casos de persecución**: siete rutas, dos mandos, dos orientaciones; retorno al suelo y limpieza de fases. Los ejemplos de Goku terminan en6HITS y64 de daño con Meteor; Vegeta en11HITS y78. Son las lecturas de estas secuencias, no una certificación general del contador.
- **10 negativos**: ↑+C sin lanzamiento, lanzamiento sin persecución y daño único original, intento sin ki, A mantenido sin repetir básicos y ↑+C posterior al aterrizaje sin una segunda persecución; Goku y Vegeta. Solo el test de ki usa un ajuste explícito de ki=0 antes del intento; no se usa en vídeos.
- **88 pares de regresión** frente al prototipo140820: una técnica representativa de ki por personaje, suelta/en combo, ambos mandos y sentidos. Mismos tiempos de aceptación/preparación, daño, contactos, HITS, bandera de carga rápida y estado final en estos casos. No equivale a probar todos los ataques del juego.
- Se revisan recursos gráficos/paletas en las capturas, programas de remate, hashes, decodificación completa de vídeos y fotogramas de caída y Meteor. Durante las tomas solo hay entradas de mando; distancia/orientación se preparan antes. Vegeta usa estados de vida crítica obtenida con golpes reales, conservando requisitos nativos.
- Final Flash con dos fotogramas por dirección falló en una ruta P2. Con tres pasa la matriz final. La tolerancia de entrada, interrupciones durante la cola de Meteor, KO, juego libre, equilibrio, mando y consola real siguen pendientes. HITS y stun generales no se dan por corregidos. No se afirma que estas cadenas sean inevitables.

[Matriz](../evidence/air-pursuit-meteor/matrix.json) · [Negativos](../evidence/air-pursuit-meteor/negative.json) · [Regresión](../evidence/air-pursuit-meteor/validation.json) · [Vídeo Meteor](../evidence/air-pursuit-meteor/video-manifest.json) · [Short v2](../evidence/air-pursuit-meteor/short-manifest.json) · [ASM comentado](../research/air-pursuit-meteor/pursuit.asm).


## Short de Meteor con textos

A petición de Alex se adapta el vídeo de los cuatro Meteor a **YouTube Shorts:1080×1920,32,438 s**. Archivo local `outputs/YouTube-Short-Meteor-Aereo/DBZ-Combos-Aereos-Meteor-Short.mp4`. Se usan las mismas tomas nativas del build143144; no cambia la ROM. Juego/HUD completos a escala entera3×, audio nativo y velocidad normal. Cada toma incluye el lanzamiento, persecución, dos básicos, Meteor completo y recuperación.

Rótulos exteriores al juego: «¡REMATE METEOR!», nombre del personaje, y pasos temporizados «Lanza al rival», «Persigue y enlaza dos golpes», «¡Remata con el Meteor!». Crédito ALEX LLAO y versión/build visibles. Se comprueban resolución/duración, hash de las fuentes, escenario/variante en todos los fotogramas seleccionados, remate completo y decodificación del MP4; se revisan capturas del lanzamiento, enlace y Meteor. No se publica automáticamente ni se guarda el MP4 en Git.

[Vista del Short](../assets/media/air-pursuit-meteor/short-meteor.png) · [Título y descripción](short-meteor-aereo-texto.txt) · [Manifiesto](../evidence/air-pursuit-meteor/short-meteor-manifest.json) · [Montaje reproducible](../research/air-pursuit-meteor/render-short-meteor.py).

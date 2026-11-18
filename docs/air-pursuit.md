# Persecución aérea: primer prototipo140820 y Short

**Histórico.** [Revisión actual: Meteor y caída corregidos, build143144](air-pursuit-meteor.md) · [Comandos](comandos-persecucion-aerea.md).

18 de noviembre de 2026. Prueba real de ROM v1.0 build `20261118-140820`, derivada del selector japonés `20261110-173703`. No sustituye la candidata anterior ni se presenta como versión final validada con mando.

Después del lanzamiento propio, **↑ + C** permite perseguir al rival en el aire con Goku o Vegeta, a velocidad normal. Consume 16 de ki. Dos golpes simples A/B pueden enlazarse con Kamehameha, Super Kamehameha o Final Flash. Una persecución y dos básicos por cadena; no se certifica todavía la ausencia de infinitos o el equilibrio en juego libre.

La trayectoria del lanzamiento original se conserva durante la aproximación. El perseguidor se mueve hacia la posición real del rival; los contactos usan sus cajas nativas. Al alcanzarlo se liquida una sola vez el daño pendiente del agarre y se aplica caída propia acotada durante los golpes aéreos. No se modifican las tablas de daño ni se añade vibración a los Meteor.

## Vídeo entregado

Archivo local `outputs/YouTube-Short-Persecuciones-Aereas/DBZ-Combos-Aereos-Short.mp4`, **22,895 s, 1080×1920**, cinco secuencias completas hasta el remate. Goku/Freezer y Vegeta/Goku en los tres Namek R10; ambas orientaciones. Pantalla y HUD completos a escala entera 3×, audio de la ROM, sin acelerar ni reemplazar fondos. Preparación de distancia/orientación antes de grabar; durante las tomas solo entradas de mando. No se muestra una CPU reactiva ni se afirma que el defensor no pueda responder.

[Vista del Short](../assets/media/air-pursuit/short-preview.png) · [Goku en el aire](../assets/media/air-pursuit/goku-air.png) · [Vegeta en el aire](../assets/media/air-pursuit/vegeta-air.png) · [Título y descripción](short-air-pursuit-texto.txt).

Se verificaron **20 casos**: ambos puertos, ambas orientaciones, Goku/Vegeta con dos básicos, Goku con Kame/Super y Vegeta con Final Flash. Se comprueban contactos, programas de remate y retorno al suelo con limpieza del estado nuevo. Las cinco capturas comprueban los bancos gráficos y paletas de Namek al comenzar y durante la persecución. El vídeo final se decodifica completo y se revisan fotogramas de los cinco fragmentos.

## Límites pendientes

El enlace con **Meteor no pasa** en esta revisión y queda excluido del Short. El código de su cola experimental se conserva para depurarlo, sin anunciarlo como terminado. Faltan pruebas negativas de bajo ki, interrupción, KO, repetición del comando y regresión amplia del plantel, además de validación con mando y consola real. El contador HITS y el mareo general siguen pendientes de auditoría; los 20 casos no certifican todo el juego. La ROM experimental permanece local y no se entrega como release.

[Resultados de 20 casos](../evidence/air-pursuit/matrix.json) · [Capturas y recursos](../evidence/air-pursuit/captures.json) · [Montaje y hash](../evidence/air-pursuit/short-manifest.json) · [ASM experimental](../research/air-pursuit/pursuit.asm).

# v1.0 · build 20261106-103002 · preparación de ki y cruces con Meteor

**Build conservado. La entrega actual corrige Piccolo e incluye cruces ejecutados más seguidos: [20261106-105411](piccolo-hits-v1.md).**

Build del **6 de noviembre de 2026, 10:30:02 de Madrid**. Sustituye para las pruebas al build 20261106-100534, que se conserva. Sigue siendo versión **1.0**, con un identificador de compilación nuevo en el archivo, las dos cabeceras internas de título y el manifiesto.

[**Anuncio actualizado, 1:27**](../assets/media/release-v1-0-build-20261106-103002/DBZ-Enhanced-v1.0-build-20261106-103002-Anuncio.mp4) · [**Tres cruces y Meteor, toma completa**](../assets/media/release-v1-0-build-20261106-103002/Tres-cruces-y-Meteor-v1.0-build-20261106-103002.mp4) · [**Kamehameha y Masenko antes/después, simultáneos**](../assets/media/release-v1-0-build-20261106-103002/Kamehameha-Masenko-antes-despues-v1.0-build-20261106-103002.mp4).

## La secuencia solicitada

P1 cruza, P2 responde cruzando y P1 vuelve a cruzar; Goku termina con su Meteor nativo de tres impactos y 35 de daño en la toma. Todo se ejecuta mediante comandos de los dos mandos, a velocidad normal, sin mover personajes ni escribir golpes durante la grabación. El cruce no suma impactos. La secuencia está incluida al final del anuncio, antes del cierre con BANDAI y ALEX LLAO.

La demostración muestra una coreografía reproducible; no afirma que el rival esté obligado a aceptar el Meteor ni que los cruces formen un combo inevitable.

## Preparación más breve sin pantalla partida

Se recorta la espera en la pose de preparación del **Kamehameha normal de Goku** y del **Masenko de Gohan**. Se mantiene la fase de lanzamiento, su unidad de animación y los datos de desplazamiento del proyectil. No se acelera el juego entero.

| Técnica | Antes, muestra cercana | Nuevo build, muestra cercana |
| --- | --- | --- |
| Kamehameha | 74 fotogramas, unos 1,24 s | 26 fotogramas, unos 0,43 s |
| Masenko | 93 fotogramas, unos 1,55 s | 41 fotogramas, unos 0,68 s |

Se cuenta desde que se acepta el programa de la técnica hasta que aparece su primer proyectil. Las muestras a otra distancia oscilan unos fotogramas por las actualizaciones nativas. Los comandos de entrada son idénticos antes y después y el vídeo compara ambos a la vez, sin cambiar sus tiempos; se oye el sonido de la derecha.

Sólo cambian cuatro bytes de datos de animación del cuerpo de la ROM: duración total y peso de preparación de las dos tablas normales. La cabecera de versión/fecha y el checksum también se actualizan. El peso de lanzamiento y la unidad de animación se conservan. **Super Kamehameha y las rutas con pantalla partida no se retocan**, tampoco las preparaciones de las otras técnicas. No se cambia ninguna instrucción del motor respecto al build anterior.

## Validación y límites

Se comparan **16 casos antes y 16 después**: dos personajes, ambos sentidos, dos distancias, con y sin guardia. El daño y el débito real de ki coinciden en los pares; los bloqueos siguen reduciendo el daño. El saldo de ki observado puede diferir por la recuperación pasiva durante una preparación ahora más corta; no debe confundirse ese saldo con el coste de la técnica.

Las dos rutas lejanas de pantalla partida conservan exactamente el registro observado en la prueba de 400 píxeles. Se repiten **200 variantes de comandos**, diez acordes de Meteor, siete casos negativos y **30 técnicas tras lanzamiento**: Goku/Gohan en P1 y Goku en P2, diez momentos por caso.

Un montaje original de Masenko a distancia 280 falla también antes del cambio; no se ha fabricado un impacto ni se ha alterado su alcance para ocultarlo. La auditoría completa de especiales y el equilibrio con mando siguen pendientes. El recorrido acumulado de 24,5 minutos pertenece al build anterior; esta revisión tiene comprobaciones diferenciales centradas en las dos técnicas y el vídeo nuevo.

Se conservan todas las decisiones gráficas y los cambios de controles de la [primera compilación v1.0](version-1-0.md). Árbol/nave de Namek, vibración aprobada, nuevo HUD de retratos y escenario nevado continúan sin integrar.

## Archivo y construcción

`DBZ_Buyuu_Retsuden_Enhanced_v1.0_build_20261106-103002.bin`

`pnpm build:review --rom ruta/a/original.bin --version v1.0-build-20261106-103002` genera este build. El anterior queda fijado mediante `--version v1.0-build-20261106-100534`. [Manifiesto actual](../patches/release-v1-0-build-20261106-103002/manifest.json) · [Evidencia](../evidence/release-v1-0-build-20261106-103002/validation.json).

Arranca desde cero, en velocidad normal, sin cargar estados de la compilación anterior. Es una primera propuesta de rapidez de salida para probar con mando, no una aprobación de equilibrio.

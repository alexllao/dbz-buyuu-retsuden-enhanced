# Versión 1.0 · build 20261106-100534

Build fechado el **6 de noviembre de 2026, 10:05:34, Europe/Madrid**. La fecha identifica esta compilación; la validación y el empaquetado se completan después. Archivo: `DBZ_Buyuu_Retsuden_Enhanced_v1.0_build_20261106-100534.bin`.

La versión y la fecha figuran también en los dos títulos internos de la cabecera de Mega Drive: `DBZ BUYUU ENHANCED V1.0 2026-11-06 09:05Z`. Esa hora es UTC, equivalente a las 10:05 de Madrid. El crédito gráfico conserva BANDAI y ALEX LLAO. La cabecera identifica la ROM en herramientas compatibles; no añade un rótulo nuevo a la pantalla de título del juego.

Esta entrega sustituye a Respuesta v2 para las pruebas de jugabilidad. El nombre técnico `responsive-v3` identifica el módulo de código, no otra versión pública.

## Vídeo y ROM

[**Anuncio: 1:25 de juego real con sonido**](../assets/media/release-v1-0/DBZ-Enhanced-v1.0-build-20261106-100534-Anuncio.mp4) · [Manifiesto y huella del build](../patches/release-v1-0/manifest.json) · [Validación](../evidence/release-v1-0/validation.json).

El anuncio abre con el título nativo y ambos créditos. Incluye tres básicos → cambio de lado → Meteor de Goku con 6 HITS, tres bolas con 3 impactos, Super Kamehameha, Meteor de Vegeta y Piccolo, lanzamiento → Masenko / Final Flash / Kamehameha, los trece impactos de Cell y cruces entre dos mandos. Termina de nuevo en el título.

Son tomas del emulador a velocidad normal con entradas coordinadas y sonido original. Se preparan posiciones antes de cada toma y ki mediante carga nativa; la vida baja requerida por algunos Meteor se obtiene recibiendo golpes antes de grabar. No se escriben vida, daño, temporizadores ni contadores durante las tomas. Los rótulos laterales son edición; el contador y las barras pertenecen a la ROM. No se acelera la acción.

Un lanzamiento seguido de una técnica puede ser defendible. Que el contador conserve la secuencia durante la técnica no certifica un combo inevitable. No se ha añadido una excepción para golpear artificialmente al rival en el aire.

## Lectura del mando corregida

Se localizaron dos problemas distintos. Durante el temporizador posterior a impactos, la ruta nativa reducía las lecturas del mando; además, determinadas comprobaciones frente a un rival lanzado borraban el historial de órdenes del atacante aunque su agarre ya hubiese terminado.

Ahora se usa la lectura nativa del mando en cada actualización de combate elegible y se conserva el historial tras acabar el agarre propio mientras el rival sigue cayendo. Esto sirve para los once personajes y ambos puertos. Se mantienen las pausas, menús, fin de ronda, cinematografías y restricciones de técnicas activas. No se acelera la animación ni se elimina la reacción al golpe.

La prueba específica reconoce **110/110 técnicas tras lanzar**, diez momentos distintos por cada personaje, más **10/10 con Goku en P2**. Incluye Masenko y Final Flash con sus comandos nativos. Ocho muestras de pulsaciones de un fotograma comprueban los dos puertos durante actualizaciones posteriores a un impacto; también se comprueba cargar y recuperar movimiento con el rival todavía cayendo. Las pausas nativas siguen existiendo: esto no equivale a almacenar cualquier pulsación realizada durante cualquier fotograma de una pausa.

Se repiten las 200 variantes del reconocedor de Goku, diez pruebas del acorde A+B, siete casos negativos y las pruebas de expiración del buffer, guardia, fallo y segundo puerto. El recorrido largo suma **88.200 fotogramas, unos 24,5 minutos acumulados**, con once personajes y nueve escenarios. Son entradas automatizadas y estados restaurados entre tandas, no una partida humana continua ni una certificación de mando físico o consola original.

## HITS y aturdimiento

El contador conservaba la ventana durante básicos y Meteor, pero no durante ciertas técnicas ofensivas de ki. Se amplía esa pausa a los programas de ki ofensivos, sin incluir la carga libre, guardia o recuperación. La ráfaga de Goku suma ahora sus tres contactos, y se comprueban 6 HITS en básico/cruce/Meteor, 8 en el Meteor de Vegeta y 13 en la ráfaga final de Cell. Un golpe aislado sigue sin mostrar el HUD hasta el segundo impacto.

La fórmula de daño, las colisiones y la fórmula de aturdimiento nativas no cambian respecto a Respuesta v2. Una prueba separada comprueba golpes espaciados, mareo, cruce sin golpe que no borra el mareo, primer impacto que libera del mareo, ausencia de mareo inmediato repetido y limpieza de acumulación tras inactividad. Esto cubre esos casos concretos; sigue pendiente una auditoría exhaustiva de todas las técnicas.

## Mejoras que conserva esta versión

| Área | Estado integrado |
| --- | --- |
| Personajes en combate | Once paletas elegidas; Goku G2 HDBZ. |
| Título e intro | Goku grande cálido con contraste anime y contornos negros; reparto pequeño con sus colores originales. BANDAI 1994 y - 2026 ALEX LLAO juntos, misma tipografía. |
| Fondos existentes | Paletas entregadas de los nueve escenarios. Las nuevas propuestas de Namek siguen sin aplicarse. |
| Auras | Forma C2 corregida, colores de ki individuales, polvo y salida animada; todos sin rayos, incluidos Cell y Gohan. |
| Movimiento | Carrera por doble toque y mantener; frenada con inercia breve. Caminando, un toque corto de Goku deja unos 2 píxeles frente a los 33 anteriores. |
| Salto normal | Propuesta más baja y breve: Goku 87 frente a 116 píxeles; 35–36 frente a 48 fotogramas en el aire. No cambia la velocidad general. |
| Carga y buffer | Aura empieza antes, salida rápida al soltar, parada al llenar ki y memoria breve de órdenes que caduca. |
| Cancels | Recuperación de básicos de pie que aciertan; especiales y Meteor completan su ejecución. Límite de tres básicos y un remate en la ruta ajustada; equilibrio por probar con mando. |
| Cambio de lado | Adelante, atrás, adelante + C, cerca del rival, sin golpe ni ki, con la ventaja breve y la respuesta del otro jugador ya integradas. |
| Derribos y agarres | Menor reposo terrestre en las rutas ajustadas y control del atacante antes de que termine la caída del rival. |
| HUD | Contador HITS desde dos contactos y una barra pequeña de mareo por jugador, sin texto STUN. |
| Proyectiles | Estado del mod separado de la memoria nativa del tercer proyectil; la ráfaga de Goku conserva sus tres bolas. |

Los nuevos retratos/HUD H4, la vibración aprobada, árbol y nave de Namek y décimo escenario nevado son diseños o pruebas pendientes de integración. No forman parte de esta ROM. [Decisiones gráficas](decisions.md).

## Comandos de Goku

Mirando a la derecha: Kamehameha **← ↙ ↓ ↘ → + A**; Super **← ↙ ↓ ↘ →, ← ↙ ↓ ↘ → + A**; Meteor **← ↙ ↓ ↘ →, ← ↙ ↓ ↘ → + A+B**; tres bolas **↓ ↘ → + A**. Se invierten al mirar a la izquierda. A+B sin el movimiento completo carga ki. [Tabla completa de los comandos conservados](respuesta-v2.md).

## Construcción y prueba

`pnpm build:review --rom ruta/a/original.bin --version v1.0` aplica el parche sobre la base japonesa verificada y comprueba el resultado. La construcción sin versión sigue siendo la histórica v6.6. La ROM completa se entrega localmente; el repositorio contiene el parche, código, evidencia y vídeo.

Arranca desde cero, a velocidad normal y sin cargar estados de versiones anteriores. Identifica cualquier incidencia con **v1.0 / build 20261106-100534**, personaje, rival, comando y situación. La revisión con mando del usuario y el equilibrio de jugabilidad siguen pendientes.

Para las próximas compilaciones, cambia el identificador del build, conserva versión/fecha en nombre, cabecera y manifiesto y registra la huella del archivo probado. No reutilices el mismo nombre para una ROM distinta.

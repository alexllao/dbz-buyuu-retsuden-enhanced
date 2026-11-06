# Mejoras respecto al juego original

Estado de la ROM **v1.0 · build 20261106-105411**. La presentación completa se ha grabado con esa compilación; crear el vídeo no modifica la ROM.

## Gráficos

- **Once paletas de combate revisadas**, con el anime y HDBZ como referencias. Goku utiliza la opción G2 elegida.
- **Paletas de los nueve escenarios existentes** revisadas. Las nuevas propuestas posteriores de Namek normal/destruido siguen pendientes y no sustituyen la paleta entregada.
- **Goku grande del título y la intro** con color cálido, contraste y contornos negros. El reparto pequeño de la intro conserva sus colores originales por decisión del usuario.
- **Crédito personal integrado junto a BANDAI**, conservando © BANDAI 1994 y añadiendo - 2026 ALEX LLAO en la misma línea y tipografía.
- **Auras C2 retocadas**: contorno continuo, puntas sin los cortes rectos detectados y tamaño elegido; colores de ki por personaje, polvo en suelo y salida animada. Todos los personajes quedan sin rayos, incluidos Cell y Gohan.

## Controles y movimiento

- **Lectura de los mandos durante las actualizaciones elegibles del combate**: se evita la reducción de lecturas posterior a impactos y la pérdida de historial tras terminar el agarre propio.
- **Comandos humanos nuevos para Goku**, con un reconocimiento más permisivo: medio círculo para Kamehameha; doble medio círculo para Super y para Meteor con A+B. Se conserva el esquema nativo de los otros personajes y de la CPU.
- **Margen breve para A+B**: pequeñas diferencias de tiempo entre los dos botones no eligen de inmediato el ataque de un solo botón.
- **Buffer de órdenes breve y con caducidad**, incluyendo la preparación de una técnica mientras se carga ki y su selección al soltar.
- **Carga de ki más ágil**: inicio ajustado, devolución rápida del control al soltar y parada al completar la energía.
- **Carrera por doble toque y mantener la dirección**; al soltar conserva una frenada con inercia.
- **Menor deslizamiento al caminar**. En la muestra corta de Goku, la inercia pasó de 33 a unos 2 píxeles, conservando una transición breve.
- **Salto normal más bajo y breve**. En Goku, 116 → 87 píxeles y 48 → 35–36 fotogramas en el aire. No se acelera globalmente el combate.
- **Menor reposo terrestre tras los derribos en las rutas ajustadas**, con una espera de 12 ticks en las fases modificadas.
- **Control del atacante recuperado tras su agarre**, antes de que la víctima termine de caer; permite moverse o preparar técnicas durante esa caída.

## Combate y HUD

- **Cancels de recuperación de básicos de pie que aciertan**: puñetazos y patadas pueden enlazarse con otro básico, un especial o Meteor. La ruta asistida limita la cadena a tres básicos y un remate; las técnicas activas completan su ejecución.
- **Reconducción de un básico todavía inactivo** si se termina de introducir un especial durante su arranque. No es un cancel libre de cualquier ataque.
- **Cambio de lado cercano para los once personajes**, mediante adelante, atrás, adelante+C, sin golpe ni gasto de ki. Conserva una ventaja breve y la posibilidad de responder entre jugadores humanos con otro cruce.
- **Preparación de Kamehameha normal y Masenko más breve sin pantalla partida**: muestras de aproximadamente 1,24 → 0,43 s y 1,55 → 0,68 s. Se mantienen el lanzamiento, daño, débito de ki y datos de velocidad del proyectil. Super y rutas con pantalla partida conservan sus tiempos.
- **Contador HITS integrado en la ROM**, visible desde dos contactos, para cadenas y ataques multigolpe. Se conserva durante las fases ofensivas, técnicas de ki, cruces y mareo según la ventana implementada. Un golpe aislado permanece oculto y los golpes separados no se unen automáticamente.
- **Contactos de Meteor contabilizados dentro de la secuencia**, además del daño agrupado al final: ejemplos comprobados de Goku, Vegeta y Piccolo; el Meteor de Piccolo suma nueve en la prueba corregida. Las ráfagas de Cell también incrementan el contador por contacto.
- **Dos barras pequeñas de mareo**, una por jugador, con el estilo de las barras originales y sin rótulo STUN.
- **Salida del mareo al primer impacto conectado**, reinicio de su acumulación en esa salida y limpieza por inactividad desde el último contacto, evitando el borrado periódico durante ataques recientes. Se mantienen las fórmulas nativas de daño y acumulación base.

## Seguimiento y correcciones durante el desarrollo

- Cada ROM entregada se identifica mediante **versión, fecha/hora del build y huella**, en el nombre, las cabeceras internas y el manifiesto.
- Se conservan las variantes gráficas, parches, fuentes de los módulos, pruebas y vídeos anteriores en el historial.
- Se ha separado la memoria del mod de la del tercer proyectil nativo de Goku. Esta corrección arregla una interferencia introducida durante el desarrollo y conserva la ráfaga original de tres bolas; no se presenta como una avería del juego original.
- Las correcciones del contador, incluido el Meteor de Piccolo, completan una función nueva del mod. El original no llevaba este HUD HITS.

## Alcance pendiente

El equilibrio, la sensación con mando y una auditoría exhaustiva de todas las técnicas siguen en pruebas. Los ensayos grabados son de emulador; no certifican funcionamiento en consola original. Una secuencia sumada por el contador no garantiza que el defensor no pueda escapar o bloquear según la situación.

El HUD H4 con retratos, la nueva vibración aprobada, árbol y nave de Namek y el décimo escenario nevado son propuestas o pruebas visuales pendientes de integrar. La presentación completa utiliza únicamente la ROM actual.

Los cruces más seguidos del vídeo se ejecutan con órdenes más rápidas de los dos mandos. Su animación y la velocidad de reproducción siguen siendo las del juego.

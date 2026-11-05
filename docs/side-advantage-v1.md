# Ventaja breve al terminar el cambio de lado

Prueba pedida por el usuario después de ver los intercambios P1/P2. Parte de Stun v2 y mantiene las decisiones de paleta, aura, control y aturdimiento. **La ventaja ya está implementada en esta ROM experimental; falta valorar su sensación y equilibrio con mando.**

[Vídeo real de la nueva ROM, unos 27 segundos con sonido](../assets/media/side-advantage-v1/Cambios-de-lado-con-ventaja.mp4).

## Regla elegida para esta primera prueba

Al finalizar correctamente **el comando nuevo → ← → + C**, cruzando al rival y quedando orientado hacia él, se abre una ventana de **seis actualizaciones elegibles de entrada** sobre el otro jugador. No son necesariamente seis fotogramas de pantalla: en las muestras se observaron pausas y actualizaciones que abarcan varios fotogramas.

Durante esa ventana, el otro jugador conserva direcciones, movimiento, defensa y el comando de cambio de lado con C. No puede iniciar nuevos puñetazos/patadas A/B. **Una respuesta C aceptada elimina su ventana recibida**; al completar su propio cruce puede obtener la ventaja en el sentido contrario. Esto permite encadenar respuestas P1/P2.

Las pulsaciones de A/B durante la ventana **se descartan**, no quedan en cola: hay que soltar y pulsar de nuevo al terminar. Los ataques ya iniciados continúan sin interrumpirse. La ventana no cancela daño, derribos o un ataque propio ni salta sus recuperaciones. No añade golpe automático, daño imbloqueable, invulnerabilidad, coste de ki o aceleración de animaciones.

**Alcance de esta prueba: ambos luchadores con mando humano.** La nueva ventaja no altera la CPU; extender y equilibrar esa conducta contra CPU queda pendiente. El comando mantiene los requisitos y límites de [cambio de lado](side-switch.md): proximidad, mismo plano, estado de movimiento y espacio al otro lado. Un intento abortado o interrumpido no obtiene ventaja. Las técnicas originales de B no activan esta regla nueva.

## Qué está anotado y probado

- Once personajes, P1 normal y P2 turbo: 22 arranques y **132 ramas de entrada**. Se comprueba que A/B nuevos no empiezan durante la ventana, que las direcciones siguen funcionando, que el contador termina y que una pulsación nueva de puño después vuelve a iniciar el ataque.
- **374 casos** del comando anterior siguen pasando, incluidos ambos sentidos, aire, C mantenido y variantes de entrada no aceptadas.
- Tres ensayos con respuesta preparada verifican que una contra se acepta y elimina una ventana todavía activa. Otros intentos coordinados no entraron con esa temporización: no se garantiza que cualquier secuencia arbitraria sea una contra válida.
- Vídeo con Goku/Vegeta y Piccolo/Freezer: veinte cruces sin daño durante el movimiento, ocho de ellos respondiendo dentro de una ventana activa. Son dos mandos coordinados, no una CPU reactiva.
- La comparación estática conserva gráficos, paletas, auras, colisiones, animaciones nativas, daño, combos y el parche Stun v2. En la muestra Goku/Vegeta aparecen los mismos dos patrones de píxeles fijos del HUD que en la ROM anterior; no se afirma cobertura exhaustiva de efectos o hardware.

[Entrada y ventana](../evidence/side-advantage-v1/runtime-validation.json) · [Regresión del comando](../evidence/side-advantage-v1/side-regression.json) · [Versión anterior](../evidence/side-advantage-v1/previous-version.json) · [Cambios permitidos](../evidence/side-advantage-v1/static-validation.json) · [Vídeo](../evidence/side-advantage-v1/video-validation.json).

## Implementación y construcción

La fuente de cambio de lado vive en `3E0000`; el enlace previo de controles se actualiza a su nueva dirección. Se reserva sólo el byte `actor+117`: bits de estado y orientación, y tres bits para el contador 0..6. **No se escribe `actor+116`**, utilizado por la recarga de auras v4. La restricción actúa antes del historial de A/B y después de reconocer C. Los registros se conservan en el envoltorio original.

[ASM](../src/gameplay/side-advantage-v1/side.asm) · [Código verificado](../src/gameplay/side-advantage-v1/side.hex) · [Manifiesto](../patches/side-advantage-v1/manifest.json).

`pnpm build:review --rom ruta/a/original.bin --version side-advantage-v1`

Arrancar desde cero, sin estados anteriores. La opción sin versión conserva v6.6. HITS y las propuestas de Namek siguen pendientes. Falta la prueba humana de prioridad, facilidad de contra, esquinas, todos los emparejamientos y ausencia de bucles abusivos; no se presenta como equilibrio definitivo ni como validación de consola original.

# Respuesta v1: carga, buffer, cancels y comandos de Goku

**Actualización 5/11/2026:** la prueba actual es [Respuesta v2: entradas, frenada, saltos y tercera bola](respuesta-v2.md). Incluye los comandos de Goku elegidos y la separación de la memoria del parche; esta sección anterior se conserva como historial.

ROM experimental de mando, 5 de noviembre de 2026. Parte de HUD HITS v3 y conserva sus gráficos. **HITS y stun tienen discrepancias comunicadas por el usuario y quedan pendientes: esta revisión no cambia sus rutinas.**

[Vídeo real con sonido: antes/después y todos los especiales de Goku](../assets/media/responsive-v1/Respuesta-v1-antes-despues-y-Goku.mp4). Duración aproximada: 1:28. Son mandos automatizados a velocidad normal; sin acelerar las animaciones. Cada técnica parte de un estado preparado y se deja terminar; no es un combate continuo.

## Cambios incluidos

- **Carga:** el aura aparece al comenzar la carga y se acorta su preparación. Soltar A+B devuelve el control sin esperar al final del aura. El desvanecimiento puede seguir mientras se camina. Al llegar al máximo se detiene la carga; mantener A+B no debe reiniciarla. Hay que soltarlos para cargar otra vez.
- **Buffer durante la carga:** las direcciones del especial se reconocen aunque se mantengan A+B. Tras soltarlos, un comando reconocido se conserva durante 12 actualizaciones de la lógica. Una pulsación nueva del botón correspondiente lo ejecuta, sujeto a las condiciones originales. Caduca; no queda almacenado indefinidamente y recibir un golpe lo descarta.
- **Cancels:** un básico de pie que acierta permite cortar su propia recuperación y enlazar otro básico A/B o una técnica propia. Se conserva el límite experimental de tres básicos y un remate. No se reinicia ni se prolonga la reacción del rival. Fallos y golpes bloqueados no reciben esta asistencia. Los especiales y Meteor terminan su ejecución. Esta regla sustituye la espera completa de los básicos de v5; no acelera sus fotogramas.
- **Lanzamientos:** una vez terminada la recuperación del lanzador, puede volver a moverse y ordenar ataques mientras el rival sigue cayendo. Se conserva la trayectoria y la reacción del lanzado. Se retira el veto a ordenar especiales desde ese estado libre; sus condiciones e impactos siguen siendo nativos.
- **Comandos de Goku:** sólo el jugador humano que usa Goku recibe el nuevo esquema. Los otros personajes y la CPU mantienen sus comandos. Se respetan las condiciones nativas de ki, distancia, suelo/aire y estado.

## Goku mirando hacia la derecha

Invierte izquierda y derecha cuando mire hacia la izquierda. Pulsa el botón con la última dirección. En «↓, soltar, ↓» deja una separación breve entre las dos pulsaciones.

| Técnica | Comando de esta prueba |
| --- | --- |
| Energy Blast / proyectil básico | ← → + A |
| Consecutive Energy Blast / ráfaga | ← ↙ ↓ ↘ → + A |
| Kiai Cannon | → ↓ ↘ + A |
| Solar Flare | ↓, soltar, ↓ + A |
| Dash Elbow / codazo | ↓ ↙ ← + A |
| Jump Knee Lift / rodillazo | → ↓ ↘ + B |
| Flurry Kick / patadas múltiples | ↓ ↙ ← + B |
| Kamehameha | ↓ ↘ → + A |
| Super Kamehameha | ↓ ↘ → ↓ ↘ → + A |
| Sliding Kick / deslizante | ↓ ↘ → + B |
| Slashdown Kick / descendente | En el aire: ↓ ↘ → + B |
| High Speed Move / desplazamiento original | → ← → + B |
| Super Meteor Smash | ↓ ↘ → ↓ ↘ → + B |
| Cambio de lado del mod, sin golpe | → ← → + C, cerca del rival |

Los comandos largos se comprueban antes que los cortos. El esquema propone el estilo solicitado; el ajuste fino de tolerancias y equilibrio requiere probar con mando.

## Prueba manual sugerida

1. Arranca la ROM desde cero, a velocidad normal; evita estados guardados de otras versiones.
2. Mantén A+B y suelta mientras pulsas una dirección: comprueba que el personaje vuelve a moverse. Prueba también una carga muy corta y llenar la barra.
3. Mientras cargas con Goku, introduce ↓ ↘ →. Suelta A+B y enseguida pulsa A. Debe salir el Kamehameha; si esperas demasiado, el comando debe caducar.
4. Cerca del rival, prueba A → B → A después de cada contacto. Prueba también puño que acierta → ↓ ↘ → + A. No todas las rutas conectan: se conserva la reacción original del defensor y no se han ajustado las cajas de colisión.
5. Lanza al rival con adelante + A de cerca. Mantén una dirección al terminar tu animación: debes poder moverte antes de que aterrice.
6. Prueba ambos lados de la pantalla y ambos mandos. No uses el contador HITS como único criterio para valorar los enlaces; su revisión continúa pendiente.

## Comprobaciones y límites

Se comprobaron carga, salida y barra llena en once personajes humanos a velocidad normal; el segundo mando y el comando invertido de Goku; caducidad del buffer; ausencia de nuevos cancels por fallo o bloqueo; los doce comandos de especiales de suelo y la patada descendente aérea. En las muestras nuevas, el aura aparece en 1–2 fotogramas y se acepta movimiento en 0–1 fotogramas tras soltar; el momento exacto depende de la fase de actualización del motor.

La grabación incluye antes/después de carga, lanzamiento y cadena A/B/A; buffer, barra llena, puño cancelado a Kamehameha, patada aérea y las doce ejecuciones de suelo. Las posiciones iniciales se fijan para las pruebas cercanas; el ki se carga con A+B. No se fuerzan HP, impactos, temporizadores de reacción ni animaciones.

Es una prueba de respuesta, no una validación exhaustiva de equilibrio, turbo o hardware original. Algunos enlaces se pierden por alcance o por la reacción nativa; no se garantiza que las tres entradas siempre formen un combo. No se integran en esta versión el árbol, la nave o las nuevas sacudidas de pantalla.

Construcción desde la base japonesa admitida:

```sh
pnpm build:review --rom ruta/a/original.bin --version responsive-v1
```

[Manifiesto y huellas](../patches/responsive-v1/manifest.json) · [Resultados de ejecución](../evidence/responsive-v1/validation.json) · [ASM de la revisión](../src/gameplay/responsive-v1/responsive.asm).

El código nuevo ocupa `0x3D2000`; los cuatro bytes de estado por jugador se separan en bloques de ocho en RAM `0xFFFFF700` y `0xFFFFF708`. No se usan los campos nativos del actor `0x118..0x11F`. Se conserva byte por byte el código de HITS/stun, el daño y la reacción original del defensor. La comprobación de RAM combina búsqueda de accesos directos y observación en once personajes; no constituye prueba de ausencia de todo acceso calculado o copia masiva.

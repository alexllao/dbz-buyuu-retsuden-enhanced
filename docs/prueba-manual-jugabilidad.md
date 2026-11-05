# ROM de pruebas de jugabilidad — HUD HITS v3

**Actualización 5/11/2026:** la prueba actual es [Respuesta v2: entradas, frenada, saltos y tercera bola](respuesta-v2.md). Incluye los comandos de Goku elegidos y la separación de la memoria del parche; esta sección anterior se conserva como historial.

Esta es la última ROM de jugabilidad implementada. Se entrega para la prueba manual del usuario; no es una versión nueva del motor respecto a HUD HITS v3.

## Cómo empezar

1. Abre `Buyuu_Retsuden_Enhanced_HUD_Hits_v3.bin` en tu emulador de Mega Drive y arranca desde cero, sin cargar estados guardados de otra versión.
2. Empieza con **velocidad normal**. La ampliación de combos no se aplica a turbo. Evita activar el truco de turbo al encender para esta primera prueba.
3. Para reproducir las demostraciones de ventaja y contras, usa **dos jugadores humanos**. Esa ventaja todavía no está extendida a CPU.
4. Una primera prueba sencilla: Goku contra Vegeta, cerca y en el suelo. Configura los botones del emulador como A, B y C.

## Controles por defecto

| Acción | Entrada |
| --- | --- |
| Puño / patada | A / B. Pulsaciones separadas, soltando entre ataques. |
| Defender | Mantener atrás frente al ataque. |
| Cargar ki | Mantener A+B. |
| Suelo / vuelo | C fuera de la combinación nueva. |
| Carrera | Doble toque delante o atrás y mantener la dirección. |
| Frenado | Soltar la dirección; queda la inercia elegida. |
| Cambio de lado | Adelante, atrás, adelante+C; cerca, mismo plano y sin A/B simultáneos. |
| Meteor de Goku, mirando a la derecha | → ↘ ↓ ↙ ← → + B. Invierte las direcciones mirando a la izquierda. |

## Pruebas recomendadas

- **Básicos:** empieza con A,A,A a corta distancia. Después mezcla puños y patadas, por ejemplo A,B,A. Confirma los impactos y pulsa durante la recuperación; no se trata de mantener los botones. El alcance y retroceso pueden romper una ruta.
- **Remate:** carga ki y prueba una técnica propia con su combinación nativa. Algunos remates conservan requisitos de vida y ki; que se introduzca el comando no garantiza que arranque o conecte.
- **Goku Meteor solo:** al conectar completo debe contar 3 HITS.
- **Tres básicos rápidos →cruce →Meteor de Goku:** la ruta registrada llega a 6 HITS. Hay huecos de defensa; no es un combo garantizado contra cualquier rival.
- **Golpes separados:** no deben sumarse sólo porque siga visible el número anterior. Un golpe suelto queda oculto.
- **Caducidad:** plazo de 30 actualizaciones elegibles para enlazar, 90 para leer el resultado. Ataques, cruce y mareo activo pausan el plazo. Las actualizaciones no equivalen siempre a fotogramas de vídeo.
- **Cambio de lado:** no pega ni gasta ki. En dos humanos, al completarse limita nuevos A/B del rival durante seis actualizaciones, conservando defensa, direcciones y respuesta C. Los A/B pulsados durante esa ventana se descartan; hay que pulsar de nuevo después.
- **Mareo:** las barras pequeñas no llevan texto STUN. El primer impacto conectado sobre un rival mareado termina el mareo y reinicia su acumulación. Conserva sólo la cadena de HITS vigente; no une los golpes aislados anteriores.
- **Acumulación:** no debería vaciarse por cambiar de lado ni por un temporizador periódico en medio de golpes recientes. Se limpia después de la inactividad nativa desde el último impacto aceptado.
- **Derribos:** comprobar que el reposo tumbado se siente más fluido sin cortar caída ni levantamiento. Sólo están ajustadas las rutas terrestres A1/A4/A5.

La asistencia de combos está limitada a humanos en suelo y velocidad normal, hasta tres básicos y un remate asistido. No se aceleran las animaciones ni se alarga artificialmente la reacción de daño para forzar enlaces. Las pruebas registradas no garantizan ausencia de todos los infinitos.

## Qué contiene

Controles y carrera corregidos, reposo terrestre reducido, cambio de lado para los once, ventaja experimental entre dos humanos, asistencia de combos, HITS v3, barras y salida del mareo al primer impacto, y corrección de limpieza de acumulación. Conserva las paletas de combate/auras elegidas y la presentación cálida con reparto pequeño original, BANDAI y ALEX LLAO.

## Qué sigue pendiente

**Las sacudidas suaves/B, el árbol y la nave de Namek todavía no están en esta ROM.** Sus vídeos eran previsualizaciones. Las propuestas nuevas de paleta de Namek, los retratos y HUD H4 combinados y el escenario nevado tampoco se han integrado.

## Para anotar un fallo

Personaje y rival, P1/P2, normal/turbo, suelo/vuelo, botones y qué esperabas que ocurriera. Si puedes grabarlo, una toma breve ayuda a repetir el caso.

## Versión comprobada

- Variante: `hud-hits-v3`.
- Archivo: `Buyuu_Retsuden_Enhanced_HUD_Hits_v3.bin`, 4 MiB.
- SHA-256: `2907df9f27139b6bfa8c646aca7a92f61ee2aa9f38b6924b6238b4f8548cf748`.
- Se reconstruye desde la base japonesa con `pnpm build:review --rom "ruta/a/original.bin" --version hud-hits-v3`.
- ROM y ZIP sólo locales; el repositorio conserva el parche y los registros.

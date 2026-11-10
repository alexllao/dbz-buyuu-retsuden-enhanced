# Short: Namek renace, R10

10 de noviembre de2026. El usuario acepta R10 («perfecto») y pide un vídeo vistoso de unos30 s para YouTube Shorts, con ataques, cambios de lado, Meteor y superataques. Se prepara un archivo local listo para subir; no se publica automáticamente en YouTube ni se añade el MP4 al repositorio.

[Portada](../assets/media/short-namek-r10/portada.png) · [Texto de YouTube](short-namek-r10-texto.txt).

## Montaje

Duración30,093 s,1080×1920. Juego completo y HUD visibles en un rectángulo960×672, escalado entero3× desde320×224, centrado en60,560. Cinco fragmentos continuos con cortes entre tomas, sin acelerar las animaciones, sin comparaciones y sin reemplazar fondos en posproducción. Sonido nativo; solo fundidos de12/18 ms en los cortes, sin música añadida.

| Tiempo aproximado | Toma real de R10 |
| --- | --- |
| 0:00–0:05 | Goku/Freezer, tres cambios de lado alternados P1/P2/P1 y remate Meteor, Namek normal. |
| 0:05–0:09 | Vegeta/Goku, básicos enlazados a Final Flash, devastado. |
| 0:09–0:14 | Vegeta/Goku, combo y Meteor, devastado. |
| 0:14–0:25 | Cell/Vegeta, básicos, cambio de lado y Meteor, Porunga. |
| 0:25–0:30 | Goku/Freezer, básicos y Super Kamehameha, normal. |

No se corta dentro de la cadena de Cell: el fragmento comienza en el primer básico y alcanza el último impacto del Meteor. La edición termina algunas tomas antes de que acabe la recuperación; no altera su duración interna ni fabrica una cadena entre tomas diferentes.

Archivo local: `outputs/YouTube-Short-Namek-R10/DBZ-Namek-R10-Short-30s.mp4`. También se entrega una portada y Texto-YouTube.txt. ROM v1.0 build20261110-094744, SHA-25685d7090885e83cba884ecaf161c1913feb80a118d0aa3c86f58f7945de2483cf, sin cambios.

## Grabación y comprobaciones

Se seleccionan los tres fondos y personajes desde el menú nativo, con estados nuevos de R10. HP crítico para los Meteor de Vegeta/Cell obtenido mediante golpes reales antes de grabar; energía por carga nativa. Después solo se preparan distancia, orientación y control humano antes de cada toma. Durante la captura se usan dos puertos de mando coordinados: no se escriben posiciones, acciones, vida, energía ni temporizadores. No se presenta como CPU reactiva ni como prueba de que las cadenas sean inevitables.

Se verifica el SHA de la ROM y de cada fuente, el escenario físico6 y la variante en todos los fotogramas seleccionados. Los programas esperados de Super Kamehameha, Final Flash y Meteor aparecen en las trazas. Se comprueban tres cruces alternados en Goku y uno en Cell, cambio de orden de los jugadores y recursos de VRAM/paleta al empezar cada toma. FFmpeg decodifica el Short entero; se revisan portada y capturas de los cinco fragmentos. El archivo final no cambia la velocidad de juego.

[Manifiesto, intervalos y hashes](../evidence/short-namek-r10/manifest.json) · [Selección desde menú](../evidence/short-namek-r10/selection-proof.json) · [Impactos y programas de las tomas](../evidence/short-namek-r10/timeline-analysis.json) · [Código y límites](../research/short-namek-r10/README.txt).

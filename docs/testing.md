# Pruebas y evidencia

## Comprobaciones del repositorio

`pnpm check` valida hashes, catálogo de 71 imágenes, decisión G, código hexadecimal, resultados históricos y enlaces locales de la documentación. `pnpm test` prueba el parser IPS, sus errores y el checksum de Mega Drive.

`pnpm build` verifica además una construcción real cuando se facilita la ROM base. La base no está disponible en CI.

## Pruebas históricas del juego

- Motor: Genesis Plus GX v1.7.4 f27655b, aproximadamente 59,923 fotogramas/s.
- Once personajes × normal/turbo: 22 combinaciones. Arranque nativo; turbo activado al encender con el truco original.
- Rival mantenido quieto mediante el tipo de control en RAM, sólo en la prueba. La ROM publicada conserva el control normal de la CPU.
- Instantánea neutral restaurada por secuencia para comparar entradas.
- Parada tras soltar, toques cortos, inversión de dirección, puño, patada, salto, carga, pulsación tardía y no repetición al mantener A.
- 32 pruebas de alcance/defensa con el mismo daño que el original.
- 15 interrupciones por daño con entrada pendiente y sin ataque retrasado posterior.
- Segundo mando y secuencia prolongada contra CPU.

Resultados: [resumen](../evidence/gameplay-v1/summary.json) y [matriz](../evidence/gameplay-v1/character-matrix.json). Vídeo: [original frente a v1](../assets/media/gameplay-v1-comparison.mp4).

Estas medidas son del motor emulado, no del retraso físico mando/pantalla. La rapidez al leer una dirección no equivale al tiempo de preparación de un golpe. Las pruebas no cubren todos los combos, colisiones, especiales y enfrentamientos, ni hardware real.

## Prototipo de auras C2

La evidencia del prototipo se conserva en [validation.json](../evidence/auras-c2-v1/validation.json). Las grabaciones reales de los once personajes y la retirada a cámara lenta están reunidas en [Auras C2](auras-c2-v1.md).

El alcance que debe revisarse incluye aparición, carga sostenida, retirada de doce ticks, corte por daño, regreso al control, cargas repetidas, segundo jugador y cargas simultáneas. La aprobación visual del usuario sigue pendiente, aunque una prueba automática pase. No se afirma validación en Mega Drive física.

## Revisión C2 v2

La [validación C2 v2](../evidence/auras-c2-v2/validation.json) y el [informe de ejecución](../evidence/auras-c2-v2/runtime-qa.json) corresponden a la revisión actual de 80 × 128 píxeles, rayos blancos largos y polvo animado. Hay [vídeos reales de todos los personajes y comparación de tamaños](auras-c2-v2.md).

Pasan los seis golpes naturales probados, el jugador 2, dos cargas consecutivas y cargas simultáneas. En 55 muestras de carga aérea no se dibujó polvo. Los máximos observados fueron 76/80 sprites, 18/20 sprites en una línea y 232/320 píxeles en una línea. La retirada sigue durando doce ticks del juego y reduce piezas en sus fases finales.

El resultado está limitado a esos escenarios en Genesis Plus GX. No se han validado todos los efectos simultáneos ni consola física, y sigue pendiente la aprobación visual del usuario. Las pruebas y vídeos C2 v1 se conservan como historial.

Los golpes usan colisiones reales con posiciones y orientación preparadas. La prueba aérea fuerza altura y plano tras iniciar la carga: comprueba la selección del mapa sin polvo, no una entrada de vuelo natural. Los vídeos de los once personajes se registran aparte de este pase centrado en Goku y Gohan.

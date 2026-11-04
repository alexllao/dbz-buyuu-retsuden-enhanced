# Alcance empírico: original frente a Jugabilidad v1 + Colores v1

No son cajas dibujadas ni una extracción de hitboxes. Se observa si baja la vida nativa del rival tras la misma entrada.

Resultado: **PASS for tested empirical reach/damage comparisons**. 96 comparaciones emparejadas, 192 ensayos de emulador.

| Atacante | Botón | Acción nativa | Distancias solicitadas que conectan | Que fallan | Daño | Primer impacto (frames) |
| --- | --- | --- | --- | --- | --- | --- |
| Goku | A | 32 | 49, 50, 51, 52, 53, 54 | 55, 56 | 8 | 9 |
| Goku | A | 33 | 57, 58, 59, 60, 61, 62, 63, 64 | — | 6 | 9 |
| Goku | B | 35 | 49, 50, 51, 52, 53, 54, 55 | 56 | 8 | 12 |
| Goku | B | 36 | 57, 58, 59, 60, 61, 62, 63, 64 | — | 5 | 12 |
| Piccolo | A | 32 | 49, 50, 51, 52, 53, 54, 55, 56 | — | 7 | 10 |
| Piccolo | A | 33 | 57, 58, 59, 60, 61, 62, 63, 64 | — | 5 | 10 |
| Piccolo | B | 35 | 49, 50, 51, 52, 53, 54, 55, 56 | — | 7 | 13 |
| Piccolo | B | 36 | — | 57, 58, 59, 60, 61, 62, 63, 64 | — | — |
| Recoome | A | 32 | 49, 50, 51, 52, 53, 54, 55, 56 | — | 7 | 10 |
| Recoome | A | 33 | 57, 58, 59, 60, 61, 62, 63, 64 | — | 8 | 10 |
| Recoome | B | 35 | 49, 50, 51, 52, 53, 54, 55, 56 | — | 8 | 14 |
| Recoome | B | 36 | — | 57, 58, 59, 60, 61, 62, 63, 64 | — | — |

## Interpretación

No observed change in hit/miss, damage, impact distance, active impact poses or first-hit display-frame latency in these 96 matched pairs. This supports unchanged reach for these fixtures; it is NOT proof of identical exact collision boxes.

- Native near/far basic attack selection switches at E71E57 decimal (0x39), established independently by static attack-selector analysis. Reach cannot be represented as a single monotonic threshold per button.
- Coarse pass: Goku at requested48 connects, at56 misses, at64 connects again for both A and B. Original and mod agree. At56 close action32/35 remains selected; at64 far action33/36 is selected.
- Requested24 is resolved by native push-apart during3 idle frames; use initialActualDistance and impact distance, not requested distance alone.
- Baselines are independently booted for each ROM. E6A8 counter and idle sequence cursor can differ by a tick; initial physical state is explicitly compared. No same-state cross-ROM loading.

## Límites

- No exact hitbox extraction or overlay
- No sprite bounds substituted for collision boxes
- No crouch, guard, flight, projectiles, turbo, reverse facing or full matchup coverage
- Defender is Gohan only
- No ROM or balance edits
- Display-frame latency is not physical controller/display input lag

Datos detallados: `range-fine-summary.json`. Cada carpeta conserva `range-results.json` con trazas de posición, pose, acción, vida e impacto.

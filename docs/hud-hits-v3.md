# HITS v3: los golpes separados no forman combo

Se corrige el tramo del 0:24 del vídeo anterior. Los seis puñetazos separados de Goku **ya no se suman**: cada uno comienza de nuevo como un golpe suelto y queda oculto.

[Antes y después, izquierda v2 y derecha v3](../assets/media/hud-hits-v3/Antes-y-despues-golpes-separados.mp4) · [Un minuto de pruebas actuales](../assets/media/hud-hits-v3/HITS-v3-enlaces-y-golpes-separados.mp4).

## Dos tiempos distintos

- **Enlace: 30 actualizaciones elegibles.** Si se agota, el siguiente impacto inicia otra cadena.
- **Lectura: 90 actualizaciones elegibles.** Permite leer el resultado, aunque la cadena ya se haya cerrado. Ver el número no permite sumar indefinidamente.
- Ambos se pausan durante la ejecución de ataques/cruce y el mareo activo, como se eligió. El cruce no añade impactos. El mareo conserva sólo la cuenta vigente, sin reunir puñetazos aislados anteriores.
- Se muestra desde 2 impactos. El primer golpe sigue terminando el mareo, sin cambiar su duración ni alargar reacciones. Un impacto del rival cierra la cadena anterior.

Se reutiliza `actor+124` como plazo de enlace; `+121` conserva el tiempo de lectura. `+125` queda reservado. No se añade memoria ni se modifica el contador nativo de acumulación de aturdimiento. El ajuste sigue siendo una ventana de enlace experimental; no demuestra que todos sus enlaces impidan defenderse.

## Resultados grabados

| Inicio | Prueba | Resultado |
| --- | --- | --- |
|0:00|Puñetazos separados|Cada uno vuelve a 1, oculto. No forman6 HITS.|
|0:11|Mareo provocado por esos golpes|Conserva sólo el último1; golpe posterior suma 2 y Meteor termina en 5.|
|0:23|Tres golpes rápidos →cruce →Meteor|6 HITS.|
|0:34|Meteor de Goku solo|3 contactos.|
|0:43|Caduca el enlace mientras el 3 sigue visible →Meteor|Nueva cadena de 3, no 6.|
|0:54|Meteor defendido|Sin HITS.|

Mismos controles, daño y velocidad natural que antes. 88 casos con once personajes y ambos lados, 374 pruebas del cruce y la recuperación/salida del mareo siguen pasando. Se conserva la corrección anterior de acumulación por inactividad. Falta valoración con mando y auditoría de todos los especiales y hardware original.

[Validación](../evidence/hud-hits-v3/validation.json) · [Comparación de bytes](../evidence/hud-hits-v3/static-validation.json) · [ASM](../src/hud/hits-v3/hud.asm) · [Manifiesto](../patches/hud-hits-v3/manifest.json).

## Movimiento al bloquear

Se observó movimiento horizontal breve del fondo tanto en la ROM original como en ésta durante la reacción/cámara de una guardia. La ruta nativa del bloqueo se conserva. Esa comprobación no identifica una sacudida independiente para todos los ataques. [Registro](../evidence/hud-hits-v3/guard-comparison.json).

La propuesta posterior de aumentarlo es una [previsualización separada](guard-shake-preview.md), todavía sin aplicar a esta ROM.

```sh
pnpm build:review --rom "ruta/a/original.bin" --version hud-hits-v3
```

La fuente y el ensamblador son los de las revisiones anteriores; la fuente de caracteres no cambia. Las herramientas de investigación usan rutas locales `work/`; la construcción habitual usa IPS y no necesita el emulador.

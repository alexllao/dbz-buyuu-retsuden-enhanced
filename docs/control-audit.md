# Afinar controles antes de añadir mecánicas

**Seguimiento:** [build175044: buffer para una orden perdida al terminar el básico](input-links.md). Esta auditoría se conserva como referencia del build171303.

8/11/2026. El usuario acepta priorizar controles fiables, cadenas naturales y recuperación coherente. Se revisa el build de prueba **20261108-171303**, sin cambiar su ROM ni dar por aprobadas las variantes pendientes.

## Comprobaciones sobre la ROM actual

Se ejecutan de nuevo en Genesis Plus GX a velocidad normal:

- 200 variantes de entradas de Goku: ambos sentidos, gestos completos/cardinales, distintos ritmos y botón anticipado/retrasado. Pasan las 200, incluidos gestos incorrectos que deben rechazarse.
- 7 casos de selección/rechazo para no confundir A+B de carga, Kamehameha, Super y Meteor.
- 10 Meteor en ambos mandos: A y B juntos o separados hasta dos fotogramas, en ambos órdenes. Los diez arrancan.
- 2 elecciones tras carga: doble medio círculo seguido de A inicia Super; seguido de A+B inicia Meteor.
- 5 comprobaciones adicionales: inicio/salida de carga de P2, buffer invertido de P2, caducidad del buffer, fallo y guardia que no abren el cancel por contacto.

[Resultados y hash de ROM](../evidence/control-audit/validation.json) · [Matriz de entradas](../evidence/control-audit/input-matrix.json) · [Buffer y casos negativos](../evidence/control-audit/extra-runtime.json).

## Prioridad que resulta de la revisión

El reconocedor desde reposo pasa estos casos. Eso no demuestra que toda entrada humana sea fiable ni que los enlaces tengan la misma tolerancia. La [matriz anterior de remates](basic-chains.md) ya registra intentos que no arrancan según el ritmo: Kamehameha a cuatro fotogramas por dirección y Meteor a dos, después de AAB. Hay que distinguir reconocimiento, condiciones de la técnica y ventana del enlace antes de alterar tolerancias.

Orden de trabajo: reproducir esas transiciones; ajustar solo la causa medida; comparar ambos mandos/sentidos, carga, guardia y fallo; revisar con mando. No ampliar hitstun para fabricar combos ni acelerar movimientos. Conservar K4 y las variantes ya elegidas.

Esta revisión no añade una versión de ROM: se conserva exactamente el build 171303. Tampoco declara arreglados HITS/stun, todo el equilibrio, turbo o consola original. No se han vuelto a cambiar saltos ni añadido movimientos.

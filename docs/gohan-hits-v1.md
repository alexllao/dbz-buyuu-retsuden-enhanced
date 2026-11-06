# Gohan: contactos del Meteor

**v1.0 · build 20261106-124607 · 6 de noviembre de 2026, 12:46:07 de Madrid.** El build anterior se conserva.

[**Meteor de Gohan: contador antes/después**](../assets/media/release-v1-0-build-20261106-124607/Gohan-Meteor-HITS-antes-despues-v1.0-build-20261106-124607.mp4) · [Manifiesto](../patches/release-v1-0-build-20261106-124607/manifest.json) · [Validación](../evidence/release-v1-0-build-20261106-124607/validation.json).

El contador sólo registraba la entrada de la captura y el remate con descuento de vida. Se omiten tres señales intermedias de contacto de la rutina nativa `842`, mientras la víctima permanece en la reacción `885`.

El enlace nuevo registra una vez cada señal nativa, protegida por el propio indicador CB.0. Un cuarto efecto sonoro llega después de que el remate ya haya descontado vida y la víctima haya salido de `885`: no se vuelve a contar. Se evita así tanto omitir los golpes intermedios como duplicar el remate.

Resultado comprobado: **1 entrada + 3 contactos intermedios + 1 remate = 5 HITS**, frente a 2 antes. El daño sigue siendo **34** contra Goku en la prueba comparada. No se retoca la animación, movimiento, reacción, daño, ki o fórmula base de aturdimiento.

Doce casos específicos: ambos mandos, ambos sentidos, acierto, guardia y fallo. Acierto suma cinco; guardia y fallo no añaden golpes. Se repiten además doce casos de Piccolo para conservar sus nueve contactos y 43 de daño. El módulo de contador mantiene sus actualizaciones existentes de ventana e inactividad al registrar un contacto.

La corrección sólo añade un enlace de ocho bytes y un ayudante propio de 52 bytes, además de identificación/checksum del build. El módulo de Piccolo y los ajustes anteriores permanecen intactos. Sigue pendiente la auditoría exhaustiva de todas las técnicas del plantel.

Archivo: `DBZ_Buyuu_Retsuden_Enhanced_v1.0_build_20261106-124607.bin`. `pnpm build:review --rom ruta/a/original.bin --version v1.0` genera este build. Arranca desde cero, sin estados guardados de versiones anteriores.

La presentación completa de 2:14 se conserva como grabación del build 105411 y muestra el contador anterior de Gohan. La comparación de esta página muestra la corrección. El Short no contiene ese Meteor y conserva su propia procedencia.

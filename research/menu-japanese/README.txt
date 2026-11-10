Nombres japoneses para los tres Namek extra; v1.0 build20261110-173703.

build.py: cambio minimo y verificado sobre cargas-en-combo build120502.
33015C: CLR.W D0; NOP; JSR 1FEE en vez de copiar el atlas latino por1780.
331000/331300/331600: palabras de glifos del cargador japones nativo.
332100..117: seis indices por nombre, con relleno vacio.
No cambia las tablas de los nueve escenarios originales ni las fuentes.
No modifica el codigo de combate o los recursos Namek R10.

capture.py: cuatro capturas reales, seleccionadas con botones.
validate.py: vuelta completa de doce entradas e inicio de tres combates.
validate-modes.py: entrada en P1-CPU, P1-P2 y CPU-CPU.
package.py: IPS delta, reaplicacion exacta y entrega local de ROM.

Los scripts usan los auxiliares y el emulador local de work/ y las rutas
de las revisiones anteriores; no constituyen un SDK independiente.
La ROM privada, el emulador y los estados guardados no se incluyen.

VISOR DE CAJAS NATIVAS — BUYUU RETSUDEN (JAPAN)

Archivo: buyuu-hitboxes.lua
Destino: Gens-rr con Lua. No se ha instalado un emulador adicional.

USO
1. Abre la ROM japonesa original o el parche de controles en Gens-rr.
2. Entra en un combate.
3. Tools > Lua Scripting > New Lua Script Window; selecciona buyuu-hitboxes.lua.
4. Pausa y avanza fotograma a fotograma para revisar cuándo se activa cada golpe.
   También puedes arrastrar el archivo .lua sobre Gens-rr.

COLORES
- Amarillo, push0/1: cajas usadas para separación/contacto entre personajes.
- Verde, hurt2/3: regiones que pueden recibir ataques.
- Rojo, hit4/5: ataque, visible sólo con el bit de actividad nativo activo.
- Azul, guard6/7: regiones de guardia que existen en la pose cargada. Mostrarlas
  no afirma por sí solo que todas las condiciones de bloqueo estén activas.

Las etiquetas muestran jugador, tipo y slot nativo. El texto superior muestra
la pose lógica de la muestra de cajas (boxpose), acción y estado de su bit de
ataque, todos tomados de la MISMA muestra. No se mezclan datos actuales con cajas
anteriores. Puedes desactivar grupos o etiquetas
en la tabla OPTIONS, al comienzo del script. Las coordenadas son 320x224; el
emulador se ocupa de ampliarlas al tamaño de la ventana.

ALINEACIÓN VISUAL: FRAME_DELAY
OPTIONS.FRAME_DELAY = 1 es el valor predeterminado. El visor guarda las muestras
de ambos actores y dibuja la anterior, para aproximar la alineación de las cajas
con el sprite que ya ha llegado a la pantalla. La leyenda muestra RAM display
delay1. Con 0 dibuja la RAM inmediata; puedes elegir más fotogramas si procede.
Durante el arranque o tras limpiar el historial usa la muestra actual y muestra
warmup hasta disponer del retraso configurado. Conserva tres muestras por defecto
y amplía el búfer si configuras más retraso. Limpia muestras antiguas al cambiar
los personajes, detectar una vuelta desde HP cero o un retroceso del contador.

El juego calcula contactos con el caché anterior, después actualiza animación y
cajas y prepara los gráficos; la subida de sprites pasa por VBlank. Por eso la
RAM leída al final puede adelantarse a la imagen. El campo actor+0x04 es la pose
lógica; actor+0x05 es la última pose preparada/solicitada para gráficos, NO una
prueba de qué pose está visible en VRAM.

El retraso de una muestra es una ayuda de alineación visual: coincide en las
secuencias observadas salvo alguna fase de recuperación con más demora. NO es
una garantía universal del pipeline. No permite declarar que una colisión sea
incorrecta por una diferencia de un fotograma entre caja e imagen. Los JSON de
pruebas conservan sus muestras de RAM originales, sin desplazar ni alterar.

QUÉ LEE
- P1: RAM 0xFFE75E. P2: RAM 0xFFE886.
- Ocho rectángulos de cuatro bytes con signo, en actor+0x5C..0x7B.
- Primer byte 0x80: slot desactivado.
- Slots 4/5 sólo se muestran con memory.readbyte(actor+0x1E) bit7 activo.
  Equivale a word+0x1E & 0x8000, NO a &0x0080.

COORDENADAS CONFIRMADAS EN EL CÓDIGO NATIVO
El cargador 0x11C1E..0x11C9A ya aplicó orientación y los desplazamientos de
actor+0x0E/+0x14 al caché. El script no los suma ni refleja de nuevo.

Cada extremo se obtiene como el juego:
  mundoX = max(0, suma de palabra con signo(worldX+0x0A, byteXdelcache))
  mundoY = max(0, suma de palabra con signo(worldY+0x10, byteYdelcache))
  pantallaX = mundoX - cámara(actor+0x16)
  pantallaY = mundoY - cámara(actor+0x18) + 32

El recorte a cero se observa en 0x12434..0x1246C. El +32 vertical procede del
renderizador de personajes 0x8972..0x89C8, no de una corrección visual inventada.
Ejemplo de la prueba Goku A a distancia48: worldX300, worldY448, cámara164/280.
El origen de pantalla es136/200. La caja verde [-21,-78,17,-3] queda en
[115,122,153,197]. Los límites de sprites dibujados no se usan como hitboxes.

ALCANCE Y ESTADO
El script sólo lee memoria y dibuja una superposición. No cambia ROM, RAM,
entradas, alcance ni daño. Se usa durante el combate: fuera de él, los mismos
campos de RAM pueden contener datos antiguos. No hay lógica de proyectiles ni
otros efectos. El rojo puede desaparecer después de un contacto aunque la pose
del golpe siga dibujada, porque el juego limpia su bit de ataque.
La superposición no sustituye las demás comprobaciones del juego: plano de
combate, estados especiales, prioridades y condiciones completas de bloqueo.
Puede verse un fotograma transitorio del caché si la muestra cae durante su
actualización; no se corrige inventando otro reflejo de la caja.

La fórmula y el bit se han contrastado con el código y capturas de RAM nativa.
El visor aún no se ha ejecutado en una instalación de Gens-rr; no se presenta
como verificación visual final de su alineación en ese emulador.

API CONSULTADA EN LA DOCUMENTACIÓN OFICIAL DEL PROYECTO
https://github.com/TASEmulators/gens-rerecording/blob/master/Gens-rr/Output/LuaSamples/gens-lua.html
Se usan memory.readbyte/readword, gens.registerafter, gui.register, gui.box y
gui.text. El callback de GUI evita el retraso adicional de dibujar desde un
bucle de frameadvance; el FRAME_DELAY descrito arriba es un retraso intencional
e independiente para la alineación visual con el juego.

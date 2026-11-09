NAMEK R6 - FUENTES DE INVESTIGACION

build.py adapta los maestros aprobados, recupera patrones del suelo original,
protege contornos y sombras de roca y codifica mapas/paletas/patrones nativos.
integrate.py coloca los recursos en una copia privada del build aprobado.
prepare-scenes.py selecciona los escenarios con el menu y prepara las tomas.
record-promo.py captura directamente framebuffer RGB565 y sonido del core.
verify-runtime.py comprueba recursos cargados en VRAM/CRAM durante el juego.
package.py monta el video local de revision, sin publicarlo.
update-records.py actualiza aprobaciones, fuentes y evidencias; no copia MP4.

Requieren el entorno privado de trabajo, la ROM base, el core Genesis Plus GX,
Python, Pillow, NumPy y FFmpeg, y los helpers de captura de versiones anteriores.
No constituyen una distribucion autonoma del juego ni incluyen ROM o estados.

Los tres PNG maestros se conservan byte a byte en assets/concepts/namek-revision-r6.
La adaptacion nativa es una version separada, pendiente de valoracion visual.

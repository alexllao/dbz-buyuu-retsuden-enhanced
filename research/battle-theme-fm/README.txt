PRUEBA DE AUDICION FM, 11/11/2026.

No es un parche del juego. No cambia la ROM Enhanced ni el selector BGM.
player.asm/hex: reproductor 68000 original e independiente, base200.
build-native.py: cartucho de prueba, registros YM2612/PSG y presets FM.
analyze.py: estimacion automatica de notas y percusion; NO transcripcion certificada.
render.py: audio directo de Genesis Plus GX y verificacion de afinacion/volumen.
package.py: procedencia, resultados y copia de fuentes; audio solo local.

Para reproducir: requiere MP3 privado aportado por el usuario, auxiliar del
emulador en work/emulator/, NumPy en work/simulation-deps, FFmpeg y Ghidra local.
source.f32 se obtiene de los primeros25s a22050Hz mono float32 con FFmpeg.
analyze.py genera score.json; build-native.py tone/draft genera cartuchos
locales; render.py tone/draft captura audio. El modo tone comprueba440Hz.

No se incluyen el MP3, WAV, cartuchos BIN, score musical, DLL o dependencias.
La secuencia y los audios permanecen en el espacio local del usuario.
El primer borrador necesita revision de oido y edicion musical; no se presenta
como musica definitiva ni como implementacion de BGM8 dentro del juego.

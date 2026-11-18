# Sonido de aterrizaje después de las ondas

18 de noviembre de 2026. **v1.0 build `20261118-145200`**, SHA-256 `98c242aab3bf22ab1169c38948aa06b74e43c02e2663a11ce1fc00f908d27c17`. Alex señala que Goku y Vegeta caen sin sonido después del remate aéreo. La caída propia de la persecución llegaba al suelo y limpiaba el estado sin solicitar el efecto que dispara el salto normal al finalizar.

Se reutiliza la orden nativa **0x49**, observada al aterrizar Goku y Vegeta en saltos normales del build143144. La nueva orden se envía al tocar suelo el perseguidor vivo en fase3, antes de abandonarla: una vez por aterrizaje, sin repetirla en la caída del rival o en un KO. La corrección no añade un sonido durante todo el descenso ni mezcla audio en posproducción.

La matriz de **28 casos** verifica la solicitud/consumo del efecto junto al aterrizaje: ambos mandos, ambos sentidos y siete rutas, incluidos Kamehameha, Super, Final Flash y Meteor. Se repiten los10 negativos existentes. Las cinco nuevas tomas mantienen los daños89/92/114 de las ondas y los programas esperados, con recursos de Namek intactos. En Kame/Super/Final Flash el PCM coincide con la revisión anterior hasta después de aterrizar, cuando aparece la primera diferencia de audio. Esto comprueba una diferencia real de la grabación, no certifica volumen o comodidad en consola.

**Short v3:22,895 s,1080×1920**, archivo local `outputs/YouTube-Short-Persecuciones-Aereas-v3/DBZ-Combos-Aereos-Short.mp4`. Sonido íntegro de la ROM, velocidad normal, pantalla/HUD completos. Texto público sin preguntas a la audiencia ni menciones a IA, conforme a la indicación de Alex. No se modifica ni sobrescribe el Short de Meteor143144; esta es la nueva revisión del Short de ondas. La ROM experimental permanece local.

[Vista](../assets/media/air-pursuit-landing-sfx/short-v3.png) · [Título y descripción](short-air-pursuit-v3-texto.txt) · [Matriz con aterrizajes](../evidence/air-pursuit-landing-sfx/matrix.json) · [Audio antes/después](../evidence/air-pursuit-landing-sfx/audio-difference.json) · [Manifiesto del Short](../evidence/air-pursuit-landing-sfx/short-manifest.json) · [ASM](../research/air-pursuit-landing-sfx/pursuit.asm).

Se conservan los límites del prototipo anterior: prueba con mando, tolerancia extrema de comandos, interrupciones/KO durante la cola, equilibrio e investigación general de HITS y stun pendientes. Esta corrección no los declara resueltos.

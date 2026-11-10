# Namek R10: cristal opaco, nubes y marcas del suelo

**Valoración posterior:** el usuario responde «perfecto» y pide un [Short](short-namek-r10.md) con esta revisión. Se conserva el build sin modificaciones para la grabación.

10 de noviembre de2026. Se atienden los tres fallos señalados con recortes: ventana de la casa que deja ver el cielo, nubes con cortes/formas rectas y una nube demasiado cerca de un árbol; también los rectángulos repetidos del suelo. Se conserva R9 como comparación. **R10 está integrada y grabada desde la ROM, pendiente de valoración visual del usuario.**

[**Antes/después de los tres fallos, capturas reales**](../assets/media/namek-native-r10/Correcciones-R9-R10-ROM.png) · [Tres escenarios completos](../assets/media/namek-native-r10/R10-tres-variantes-ROM.png).

## Correcciones

- **Ventanas:** la máscara de la fuente dejaba fuera azul conectado al exterior, especialmente el ventanal circular y la puerta. Se recuperan los píxeles azules dentro de la envolvente de paredes y se verifica la opacidad de37 píxeles nativos de cristal/puerta. El centro del ventanal es azul en los tres recursos. No se añade contorno negro grueso; misma casa58×32 y mismo hash en las tres variantes. La transparencia aparente era cielo pintado en huecos de la máscara, no una semitransparencia del VDP.
- **Nubes:** se retiran las siluetas viejas del aire y se reutiliza la nube completa existente, adaptando sus dos niveles de color a cielo diurno, ceniza y noche. Se colocan por encima deY304, con una nube baja visible en suelo. La nube que se cruzaba con la copa ya no ocupa esa zona; árboles y paisaje conectados al suelo se protegen. En el devastado se reutiliza una misma nube mediana para ahorrar patrones sin aproximar su dibujo. Los especiales y el vuelo muestran su desplazamiento normal con la cámara.
- **Suelo:** se localiza el recorte en el vídeo R9 alrededor de0:52, no se atribuye finalmente a sobrescritura de VRAM ni a una prioridad de capas. El patrón ya estaba en la textura adaptada de Porunga: la selección de representantes de R6 había sustituido detalles del suelo por una textura demasiado geométrica; R7/R9 la heredaron. En el mapa de Porunga había10 copias exactas del patrón señalado y5 en el fotograma de prueba. Se usa la textura limpia del suelo de R9 normal desdeY392 en las variantes, conservando la arquitectura/humo real de las ruinas. En los tres mapas nuevos hay0 copias exactas del patrón; en el mismo fotograma de la ROM hay0.

Se mantienen las paletas de R9 byte a byte, los colores comunes, la dirección de Porunga y el combate. Empaquetado exacto: normal655 patrones, devastado712 y Porunga649, máximo736. El cielo vacío no se rellena con texturas de césped. Porunga, lava, humo y nubes siguen estáticos como elementos del fondo; no se añade flotación ni un sprite independiente.

## Vídeo privado y comprobaciones

Build experimental **v1.0 `20261110-094744`**, SHA-256 `85d7090885e83cba884ecaf161c1913feb80a118d0aa3c86f58f7945de2483cf`. Padre de jugabilidad aprobado200852, Namek original conservado. Vídeo de78 s en `outputs/Namek-R10-revision/DBZ-v1.0-Namek-R10-20261110-094744.mp4`: normal0:00, devastado0:26, Porunga0:52. Incluye suelo, vuelo/aterrizaje y Kamehameha normal/con pantalla partida. Captura directa del framebuffer y audio de la ROM; juego320×224 presentado a escala entera2×, velocidad normal y rótulos externos. No se reemplaza el fondo en posproducción. Vídeo y ROM quedan locales, sin publicar.

Los15 recursos se reconstruyen idénticos y los9 embebidos coinciden con la ROM. Los tres escenarios se seleccionan desde el menú con estados nuevos del build final. Hay33 comprobaciones de VRAM y las32 palabras de color en suelo, vuelo, carga y antes/después de los especiales. Se verifica el patrón señalado en mapa y fotograma, además del azul de la ventana. FFmpeg decodifica el vídeo completo. Genesis Plus GX; hardware físico pendiente. Estas comprobaciones no sustituyen la aprobación estética ni demuestran ausencia de todo posible fallo.

Capturas: [normal](../assets/media/namek-native-r10/normal-ROM.png), [devastado](../assets/media/namek-native-r10/aldea-ROM.png), [Porunga](../assets/media/namek-native-r10/porunga-ROM.png). Mapas completos: [normal](../assets/media/namek-native-r10/normal-mapa.png), [devastado](../assets/media/namek-native-r10/aldea-mapa.png), [Porunga](../assets/media/namek-native-r10/porunga-mapa.png).

[Build y cambios permitidos](../evidence/namek-native-r10/integrated-build.json) · [Reproducibilidad, ventanas y conteo del patrón](../evidence/namek-native-r10/reproducibility.json) · [Antes/después del fotograma](../evidence/namek-native-r10/detail-validation.json) · [VRAM/paletas](../evidence/namek-native-r10/runtime-validation.json) · [Grabación](../evidence/namek-native-r10/delivery-manifest.json) · [Código](../research/namek-native-r10/README.txt) · [Procedencia de la reparación de máscara](../assets/concepts/namek-native-r10/provenance.json).

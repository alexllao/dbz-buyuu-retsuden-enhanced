from pathlib import Path
import json,shutil,hashlib
R=Path('repository');T=Path('work/namek-native-r10');O=Path('outputs/Namek-R10-revision')
E=R/'evidence/namek-native-r10';S=R/'research/namek-native-r10';M=R/'assets/media/namek-native-r10';A=R/'assets/concepts/namek-native-r10'
for p in [E,S,M,A]:p.mkdir(parents=True,exist_ok=True)
for name in ['integrated-build.json','runtime-validation.json','reproducibility.json','delivery-manifest.json','detail-validation.json']:shutil.copy2(T/name,E/name)
shutil.copy2(T/'states-final-r10b/selection-proof.json',E/'selection-proof.json')
for slug in ['normal','aldea','porunga']:
 for filename,suffix in [('build.json','build.json')]:shutil.copy2(T/slug/filename,E/(slug+'-'+suffix))
 shutil.copy2(T/'states-final-r10b'/slug/'capture-manifest.json',E/(slug+'-capture-manifest.json'))
 for filename in [slug+'-ROM.png',slug+'-01-vuelo.png',slug+'-06-pantalla-partida.png']:shutil.copy2(O/filename,M/filename)
 shutil.copy2(T/slug/'compiled-map.png',M/(slug+'-mapa.png'))
for filename in ['R10-tres-variantes-ROM.png','Comparacion-R9-R10-1x.png','Casa-y-roca-R9-R10.png','Cielo-Porunga-R9-R10.png','Correcciones-R9-R10-ROM.png']:shutil.copy2(O/filename,M/filename)
for filename,src in [('house-native.png',T/'normal/house-native.png'),('porunga-native.png',T/'porunga/porunga-native.png'),('reported-stamp-R9-1x.png',T/'reported-stamp-R9-1x.png')]:shutil.copy2(src,M/filename)
for filename in ['build.py','integrate.py','prepare-scenes.py','record.py','resource_check.py','verify-runtime.py','verify-build.py','package.py','fix-detail-qa.py']:
 (S/filename).write_text((T/filename).read_text(encoding='utf-8-sig').rstrip()+'\n',encoding='utf-8',newline='\n')
shutil.copy2('work/publish-namek-r10.py',S/'publish-namek-r10.py')
shutil.copy2(T/'house-import-repaired.png',A/'house-source-repaired.png')
(A/'provenance.json').write_text(json.dumps(dict(date='2026-11-10',sourceHouse='../namek-native-r9/house-source.png',sourceCloud='../namek-native-r9/cloud-guide.png',mode='Deterministic native resource import/edit; no new generated art',houseRepair='Restore opaque blue source pixels inside warm wall row envelope; green sky stays outside alpha',floor='Reuse R9 normal indexed terrain fromY392; preserve ruined architecture/smoke',sha256=hashlib.sha256((A/'house-source-repaired.png').read_bytes()).hexdigest()),indent=2)+'\n',encoding='utf-8')
(S/'README.txt').write_text('R10 native resource corrections. Run from project root with the existing R6/R9 working pipeline and original user ROM.\nNo ROM or video is included. build.py imports R9 resources and existing house/cloud artwork.\nbuild.py -> integrate.py -> fresh prepare-scenes.py -> record.py for each variant -> verify-runtime.py -> verify-build.py -> package.py -> fix-detail-qa.py.\nUse a fresh, consistent state folder after any changed ROM. Final evidence uses states-final-r10b.\nChanges are native graphics only; no new generated artwork, gameplay modifications, VDP sprite animation or postproduction background replacement.\n',encoding='utf-8')
meta=json.loads((T/'integrated-build.json').read_text())
doc=f'''# Namek R10: cristal opaco, nubes y marcas del suelo

10 de noviembre de2026. Se atienden los tres fallos señalados con recortes: ventana de la casa que deja ver el cielo, nubes con cortes/formas rectas y una nube demasiado cerca de un árbol; también los rectángulos repetidos del suelo. Se conserva R9 como comparación. **R10 está integrada y grabada desde la ROM, pendiente de valoración visual del usuario.**

[**Antes/después de los tres fallos, capturas reales**](../assets/media/namek-native-r10/Correcciones-R9-R10-ROM.png) · [Tres escenarios completos](../assets/media/namek-native-r10/R10-tres-variantes-ROM.png).

## Correcciones

- **Ventanas:** la máscara de la fuente dejaba fuera azul conectado al exterior, especialmente el ventanal circular y la puerta. Se recuperan los píxeles azules dentro de la envolvente de paredes y se verifica la opacidad de37 píxeles nativos de cristal/puerta. El centro del ventanal es azul en los tres recursos. No se añade contorno negro grueso; misma casa58×32 y mismo hash en las tres variantes. La transparencia aparente era cielo pintado en huecos de la máscara, no una semitransparencia del VDP.
- **Nubes:** se retiran las siluetas viejas del aire y se reutiliza la nube completa existente, adaptando sus dos niveles de color a cielo diurno, ceniza y noche. Se colocan por encima deY304, con una nube baja visible en suelo. La nube que se cruzaba con la copa ya no ocupa esa zona; árboles y paisaje conectados al suelo se protegen. En el devastado se reutiliza una misma nube mediana para ahorrar patrones sin aproximar su dibujo. Los especiales y el vuelo muestran su desplazamiento normal con la cámara.
- **Suelo:** se localiza el recorte en el vídeo R9 alrededor de0:52, no se atribuye finalmente a sobrescritura de VRAM ni a una prioridad de capas. El patrón ya estaba en la textura adaptada de Porunga: la selección de representantes de R6 había sustituido detalles del suelo por una textura demasiado geométrica; R7/R9 la heredaron. En el mapa de Porunga había10 copias exactas del patrón señalado y5 en el fotograma de prueba. Se usa la textura limpia del suelo de R9 normal desdeY392 en las variantes, conservando la arquitectura/humo real de las ruinas. En los tres mapas nuevos hay0 copias exactas del patrón; en el mismo fotograma de la ROM hay0.

Se mantienen las paletas de R9 byte a byte, los colores comunes, la dirección de Porunga y el combate. Empaquetado exacto: normal655 patrones, devastado712 y Porunga649, máximo736. El cielo vacío no se rellena con texturas de césped. Porunga, lava, humo y nubes siguen estáticos como elementos del fondo; no se añade flotación ni un sprite independiente.

## Vídeo privado y comprobaciones

Build experimental **v1.0 `{meta['buildId']}`**, SHA-256 `{meta['sha256']}`. Padre de jugabilidad aprobado200852, Namek original conservado. Vídeo de78 s en `outputs/Namek-R10-revision/DBZ-v1.0-Namek-R10-{meta['buildId']}.mp4`: normal0:00, devastado0:26, Porunga0:52. Incluye suelo, vuelo/aterrizaje y Kamehameha normal/con pantalla partida. Captura directa del framebuffer y audio de la ROM; juego320×224 presentado a escala entera2×, velocidad normal y rótulos externos. No se reemplaza el fondo en posproducción. Vídeo y ROM quedan locales, sin publicar.

Los15 recursos se reconstruyen idénticos y los9 embebidos coinciden con la ROM. Los tres escenarios se seleccionan desde el menú con estados nuevos del build final. Hay33 comprobaciones de VRAM y las32 palabras de color en suelo, vuelo, carga y antes/después de los especiales. Se verifica el patrón señalado en mapa y fotograma, además del azul de la ventana. FFmpeg decodifica el vídeo completo. Genesis Plus GX; hardware físico pendiente. Estas comprobaciones no sustituyen la aprobación estética ni demuestran ausencia de todo posible fallo.

Capturas: [normal](../assets/media/namek-native-r10/normal-ROM.png), [devastado](../assets/media/namek-native-r10/aldea-ROM.png), [Porunga](../assets/media/namek-native-r10/porunga-ROM.png). Mapas completos: [normal](../assets/media/namek-native-r10/normal-mapa.png), [devastado](../assets/media/namek-native-r10/aldea-mapa.png), [Porunga](../assets/media/namek-native-r10/porunga-mapa.png).

[Build y cambios permitidos](../evidence/namek-native-r10/integrated-build.json) · [Reproducibilidad, ventanas y conteo del patrón](../evidence/namek-native-r10/reproducibility.json) · [Antes/después del fotograma](../evidence/namek-native-r10/detail-validation.json) · [VRAM/paletas](../evidence/namek-native-r10/runtime-validation.json) · [Grabación](../evidence/namek-native-r10/delivery-manifest.json) · [Código](../research/namek-native-r10/README.txt) · [Procedencia de la reparación de máscara](../assets/concepts/namek-native-r10/provenance.json).
'''
(R/'docs/namek-native-r10.md').write_text(doc,encoding='utf-8',newline='\n')
p=R/'README.md';s=p.read_text(encoding='utf-8');parts=s.split('\n\n');parts=[p for p in parts if not p.startswith('**Revisión actual: Namek R9')]
parts.insert(2,'**Revisión actual: Namek R10 · ventana, nubes y suelo corregidos en la ROM.** [**Antes/después real de los tres fallos**](assets/media/namek-native-r10/Correcciones-R9-R10-ROM.png) · [**Tres escenarios completos**](assets/media/namek-native-r10/R10-tres-variantes-ROM.png). Ventana azul opaca, nubes completas separadas de las copas y patrón rectangular del suelo eliminado:10 copias a0 en el mapa señalado,5 a0 en el fotograma. Vídeo privado de78 s, suelo/vuelo/especiales, build v1.0 `'+meta['buildId']+'`. Pendiente de valoración visual. [Cambios y comprobaciones](docs/namek-native-r10.md). R9 se conserva como antecedente.')
p.write_text('\n\n'.join(parts),encoding='utf-8',newline='\n')
p=R/'docs/decisions.md';s=p.read_text(encoding='utf-8');head,rest=s.split('\n',1);p.write_text(head+'\n\n**10/11/2026 — R10 corrige ventana, nubes y textura repetida:** se localiza el recorte exacto en Porunga0:52 de R9. Era una textura heredada de la adaptación, no una sobrescritura de gráficos. Se recuperan cristal/puerta opacos, se separan las nubes de los árboles y se comparte el suelo limpio de normal. Mapas y fotograma ya no contienen el patrón señalado. Vídeo real local, aprobación estética pendiente. [R10](namek-native-r10.md).\n'+rest,encoding='utf-8',newline='\n')
p=R/'docs/namek-native-r9.md';s=p.read_text(encoding='utf-8');head,rest=s.split('\n',1);p.write_text(head+'\n\n**Seguimiento posterior:** los recortes se localizan y corrigen en [R10](namek-native-r10.md). El patrón estaba en la variante Porunga, heredado de la adaptación del suelo. Las notas siguientes reflejan el estado de la investigación al entregar R9.\n'+rest,encoding='utf-8',newline='\n')
print('R10 evidence, PNGs, sources and README saved. Video stays local.')

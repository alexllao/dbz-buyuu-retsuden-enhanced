from pathlib import Path
import json
R=Path('repository');v=json.loads(Path('work/responsive-v3/version.json').read_text());m=json.loads(Path('work/responsive-v3/build.json').read_text())
def write(p,s):p.write_text(s.rstrip()+'\n',encoding='utf8',newline='\n')
p=R/'README.md';s=p.read_text(encoding='utf8');tail=s[s.index('## Vídeos: combos, HITS y jugabilidad'):]
head='''# Dragon Ball Z: Buyuu Retsuden Enhanced

Mod de **Mega Drive / Genesis** para mejorar controles y paletas de *Dragon Ball Z: Buyuu Retsuden (Japan)*, con el anime y Hyper Dragon Ball Z como referencias.

**Actualizado: 6 de noviembre de 2026 · rama `development`. Versión actual: 1.0 · build `20261106-100534` (10:05:34, Madrid).** Versión y fecha identifican el archivo, los títulos internos de la ROM y su manifiesto. El módulo de desarrollo se llama `responsive-v3`; la entrega pública es **v1.0**.

[**VER ANUNCIO — 1:25 de juego real con sonido**](assets/media/release-v1-0/DBZ-Enhanced-v1.0-build-20261106-100534-Anuncio.mp4) · [**Guía y resumen completo de v1.0**](docs/version-1-0.md) · [**Build y huella de la ROM**](patches/release-v1-0/manifest.json)

[![Abrir anuncio v1.0: combos, cruces, Meteor, lanzamientos y especiales](assets/media/release-v1-0/captura.png)](assets/media/release-v1-0/DBZ-Enhanced-v1.0-build-20261106-100534-Anuncio.mp4)

El vídeo abre con BANDAI y ALEX LLAO. Muestra básicos → cruce → Meteor de Goku con **6 HITS**, tres bolas con **3 impactos**, Meteor de Vegeta y Piccolo, lanzamientos seguidos de **Masenko, Final Flash y Kamehameha**, los **13 impactos de Cell** y respuestas entre dos mandos. Juego a velocidad normal, audio original y contador nativo; tomas coordinadas para demostración, sin acelerar ataques. Los enlaces mostrados no se anuncian como inevitables: el rival puede defenderse según la situación.

**Lectura del mando corregida:** se evita que el temporizador posterior a golpes salte lecturas durante actualizaciones elegibles de combate, y que se borre el historial tras finalizar el agarre mientras el rival cae. Comprobadas **110/110 técnicas tras lanzar** entre los once personajes, más **10/10 con Goku en P2**. Se mantienen las pausas y cinematografías nativas. El contador también conserva su ventana durante técnicas ofensivas de ki: la ráfaga de Goku ya suma sus tres contactos.

Se repiten 200 variantes de comandos, diez acordes de Meteor, ocho muestras de lectura de un fotograma entre los dos puertos y siete casos negativos. Las pruebas largas suman **24,5 minutos acumulados**, once personajes y nueve escenarios; son entradas automatizadas con restauraciones entre tandas. La sensación con mando, el equilibrio, la auditoría exhaustiva de HITS y la consola original siguen pendientes. No se modifica la fórmula nativa de daño, colisiones o mareo respecto a Respuesta v2. [Pruebas y límites](docs/version-1-0.md).

Se conservan las once paletas de combate, Goku G2 HDBZ, Goku grande cálido en título/intro con reparto pequeño original, créditos BANDAI y ALEX LLAO, nueve fondos entregados, auras C2 de color individual **sin rayos**, barras de mareo y HITS. También carrera mantenida, inercia breve, salto normal más bajo, carga con salida rápida, buffer y cancels de básicos, cruces y agarres con control recuperado antes. **Los retratos/HUD H4, vibración nueva, árbol/nave de Namek y décimo escenario nevado siguen sin integrar.** [Resumen por área](docs/version-1-0.md#mejoras-que-conserva-esta-versión).

| Goku mirando a la derecha | Comando actual |
| --- | --- |
| Kamehameha | ← ↙ ↓ ↘ → + A |
| Super Kamehameha | ← ↙ ↓ ↘ →, ← ↙ ↓ ↘ → + A |
| Meteor | ← ↙ ↓ ↘ →, ← ↙ ↓ ↘ → + A+B |
| Tres bolas | ↓ ↘ → + A |

A+B sin el movimiento completo carga ki. Cambio de lado: → ← → + C, cerca del rival. Los demás personajes y la CPU conservan sus comandos. [Tabla completa de Goku](docs/respuesta-v2.md).

Archivo: `DBZ_Buyuu_Retsuden_Enhanced_v1.0_build_20261106-100534.bin`. Arranca desde cero, a velocidad normal, sin estados anteriores. Construcción: `pnpm build:review --rom ruta/a/original.bin --version v1.0`. La opción sin versión conserva v6.6.

[Historial Respuesta v2 y vídeo de controles](docs/respuesta-v2.md) · [Prueba anterior de lanzamiento/Kamehameha: documenta el fallo corregido en v1.0](docs/lanzamiento-kamehameha-v2.md) · [Presentación elegida](#pantalla-de-presentación-elegida) · [Decisiones](docs/decisions.md).

'''
tail=tail.replace('la prueba actual es Respuesta v2, descrita arriba','la prueba actual es v1.0, descrita arriba').replace('ROM actual **HUD HITS v3**','ROM actual **v1.0**').replace('La última prueba genera `dist/Buyuu_Retsuden_Enhanced_HUD_Hits_v3.bin`.','La entrega actual genera `dist/'+v['filename']+'` mediante `--version v1.0`.')
write(p,head+tail)
p=R/'tools/build-review.mjs';s=p.read_text(encoding='utf8');s=s.replace("const versions = { ","const versions = { 'v1.0': 'release-v1-0', 'responsive-v3': 'release-v1-0', ");s=s.replace('--version responsive-v2|','--version v1.0|responsive-v3|responsive-v2|');s=s.replace('responsive-v1 o responsive-v2.','responsive-v1, responsive-v2 o v1.0.');write(p,s)
p=R/'tools/verify.mjs';s=p.read_text(encoding='utf8');anchor="const responsiveV2 = await json('patches/responsive-v2/manifest.json');";code='''const releaseV1 = await json('patches/release-v1-0/manifest.json');
const releaseV1Validation = await json('evidence/release-v1-0/validation.json');
const releaseV1Promo = await json('evidence/release-v1-0/promo.json');
assert.equal(releaseV1.version, '1.0');
assert.equal(releaseV1.buildId, '20261106-100534');
assert.equal(releaseV1Validation.romSha256, releaseV1.target.sha256);
assert(releaseV1Validation.passed && releaseV1Validation.postThrowKiPassed === 120);
assert(releaseV1Validation.scriptedFrames === 88200 && releaseV1Validation.singleFramePollTests === 8);
assert(!releaseV1Validation.nativeCollisionChanges && !releaseV1Validation.nativeDamageChanges && !releaseV1Validation.stunFormulaChanges);
assert.equal(sha256(await readFile(resolve(root, releaseV1.patch.path))), releaseV1.patch.sha256);
assert.equal(releaseV1Promo.romSha256, releaseV1.target.sha256);
assert(!releaseV1Promo.gameplayTimeScaling && releaseV1Promo.nativeAudio && releaseV1Promo.nativeHitsHud);
assert.equal(sha256(await readFile(resolve(root, releaseV1Promo.video.path))), releaseV1Promo.video.sha256);
assert.deepEqual([1, 2, 4, 9].map(i => releaseV1Validation.clips[i].maxHits), [6, 3, 8, 13]);
''';assert anchor in s;s=s.replace(anchor,code+anchor);write(p,s)
p=R/'project/decisions.json';d=json.loads(p.read_text(encoding='utf8'));d['releaseV1']=dict(**v,romSha256=m['targetSha256'],guide='docs/version-1-0.md',status='Experimental build for human playtesting',controllerFix='Native poll each eligible combat update; preserve history after own throw recovery',postThrowTests=120,kiCounterPause=True,stunFormulaUnchanged=True,video='assets/media/release-v1-0/DBZ-Enhanced-v1.0-build-20261106-100534-Anuncio.mp4');write(p,json.dumps(d,ensure_ascii=False,indent=2))
p=R/'docs/decisions.md';s=p.read_text(encoding='utf8');s=s.replace('Última ROM de prueba: [HUD HITS v3](hud-hits-v3.md)','Última ROM de prueba: [v1.0, build 20261106-100534](version-1-0.md)');s+='\n\n## Versión 1.0 · 6 de noviembre de 2026\n\nVersión y build en nombre de ROM, cabeceras y manifiesto. Corregidas la reducción de lecturas después de golpes y la pérdida de historial tras agarres; 120 técnicas tras lanzar reconocidas en las muestras. El contador pausa durante ki ofensivo; tres bolas de Goku, Meteor y trece impactos de Cell comprobados. Sin cambios de daño, colisiones ni fórmula de mareo respecto a Respuesta v2. Se mantienen los ajustes de carga, buffer, cancels, movimiento y gráficos. [Guía, anuncio real de 1:25 y límites de las pruebas](version-1-0.md).\n';write(p,s)
p=R/'docs/roadmap.md';s=p.read_text(encoding='utf8');s+='\n\n- [x] [v1.0 / build 20261106-100534](version-1-0.md): identificar ROM, corregir lecturas tras impactos y lanzamiento, conservar HITS durante ki y grabar anuncio real de 1:25.\n- [ ] Revisión humana de v1.0 con mando y auditoría exhaustiva de técnicas; el recorrido automatizado no sustituye esa validación.\n';write(p,s)

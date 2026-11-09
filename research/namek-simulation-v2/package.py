from pathlib import Path
import subprocess,shutil,json,hashlib,zipfile
n=Path('work/namek-simulation');v=n/'video/simulation';o=Path('outputs/Namek-simulacion-vuelo-y-combate');o.mkdir(parents=True,exist_ok=True);r=Path('repository');m=r/'assets/media/namek-simulation';m.mkdir(parents=True,exist_ok=True)
clips=[v/(x+'.mp4') for x in ['01-vuelo','02-goku','03-gohan','04-vegeta','05-cell','06-pantalla-partida']]
lst=n/'concat.txt';lst.write_text('\n'.join("file '"+p.resolve().as_posix()+"'" for p in clips),encoding='utf-8')
video=o/'Namek-comparacion-pixel-art.mp4';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(lst),'-c','copy','-movflags','+faststart',str(video)],check=True)
cover=o/'Comparacion-Namek.png';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','9','-i',str(video),'-frames:v','1',str(cover)],check=True)
shutil.copy2(video,m/'comparacion.mp4');shutil.copy2(cover,m/'portada.png');shutil.copy2(r/'assets/concepts/namek-redraw-v2/Variantes-Namek.png',o/'Variantes-Namek.png')
manifest=json.loads((n/'capture-manifest.json').read_text());manifest.update(dict(videoSha256=hashlib.sha256(video.read_bytes()).hexdigest(),pixelArt='512x512 panorama sampled nearest; native composition 320x224 per view; no interpolation',verticalArtFraming='130+(nativeY-248)*1.4, clamped',rasterCamera='Read-only native background patch registration during large-attack cinematic',art=[dict(path=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in (r/'assets/concepts/namek-redraw-v2').glob('*.png')]))
(m/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(o/'LEEME.txt').write_text('NAMEK: SIMULACION COMPARATIVA EN PIXEL ART\n\nIzquierda: fondo original. Derecha: propuesta de fondo.\nAmbos lados conservan el mismo combate del build v1.0 20261108-200852.\nVuelo, Goku, Gohan, Vegeta, Cell y Kamehameha grande.\nMovimiento a velocidad normal y sonido real del juego.\n\nEl fondo se compone en posproduccion: aun NO esta integrado en la ROM.\nLas tres variantes son conceptos para valorar.\nhttps://github.com/alexllao/dbz-buyuu-retsuden-enhanced/blob/development/docs/namek-redraw-v2.md\n',encoding='utf-8')
with zipfile.ZipFile(o/'Namek-simulacion.zip','w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
 for p in [video,cover,o/'Variantes-Namek.png',o/'LEEME.txt']:z.write(p,p.name)
subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],check=True)
subprocess.run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,width,height,r_frame_rate','-of','json',str(video)],check=True)
print('Packaged',video)

from pathlib import Path
import json,subprocess,shutil,hashlib,zipfile
P=Path('work/namek-native/promo');O=Path('outputs/Namek-cuatro-videos-nativos');O.mkdir(exist_ok=True,parents=True);M=Path('repository/assets/media/namek-native-v1');M.mkdir(exist_ok=True,parents=True)
orders={'original':['02-goku','03-gohan','04-vegeta','05-cell','01-vuelo','06-pantalla-partida'],'normal':['01-vuelo','03-gohan','02-goku','04-vegeta','05-cell','06-pantalla-partida'],'aldea':['04-vegeta','02-goku','03-gohan','05-cell','01-vuelo','06-pantalla-partida'],'porunga':['05-cell','04-vegeta','02-goku','03-gohan','01-vuelo','06-pantalla-partida']}
names={'original':'01-Namek-original','normal':'02-Namek-Gran-Patriarca','aldea':'03-Namek-aldea-devastada','porunga':'04-Namek-Porunga'};manifest=[]
for slug,order in orders.items():
 listing=P/slug/'montage.txt';listing.write_text('\n'.join("file '"+(P/slug/(label+'.mp4')).resolve().as_posix()+"'" for label in order),encoding='utf-8');out=O/(names[slug]+'.mp4')
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(out)],check=True)
 subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,width,height,avg_frame_rate','-of','json',str(out)],text=True));shutil.copy2(out,M/('promo-'+slug+'.mp4'))
 cover=O/(names[slug]+'.png');subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','3','-i',str(out),'-frames:v','1',str(cover)],check=True);shutil.copy2(cover,M/('promo-'+slug+'.png'))
 manifest.append(dict(scenario=slug,filename=out.name,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),probe=probe,chapters=order));print('READY PROMO',slug,probe['format']['duration'],flush=True)
(M/'promos-manifest.json').write_text(json.dumps(dict(romBuild='20261109-050003',romSha256='f45950acb6b7cc7ea7f5a272c1cd17c1ca98fb9bcc7a3bc49370c15a076e0e43',nativeBackgrounds=True,postproductionBackgroundCompositing=False,normalGameSpeed=True,romDelivered=False,videos=manifest),indent=2))
(O/'LEEME.txt').write_text('CUATRO VIDEOS: NAMEK ORIGINAL Y TRES ESCENARIOS NUEVOS\n\n1. Namek original (fondo original con jugabilidad Enhanced).\n2. Namek nuevo con casa del Gran Patriarca.\n3. Aldea devastada.\n4. Invocacion de Porunga.\n\nCapturas reales del emulador con los fondos cargados desde la ROM interna de prueba.\nGoku, Gohan, Vegeta y Cell: combos, cruce, Meteors, vuelo y Kamehameha grande.\nVelocidad normal y sonido del juego. Tomas coordinadas; no todos los enlaces son inevitables.\nLa casa usa exactamente el mismo recurso y dimensiones en las tres variantes.\nTramado suave selectivo en el cielo; paleta y tiles nativos.\nLa adaptacion cambia colores y detalle respecto a la simulacion anterior.\nNo se incluye ROM ni parche, segun la peticion del usuario.\nBuild interno v1.0 20261109-050003; emulador verificado, consola fisica pendiente.\n',encoding='utf-8')
with zipfile.ZipFile(O/'Cuatro-videos-Namek.zip','w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
 for p in sorted(O.iterdir()):
  if p.suffix in ['.mp4','.png','.txt']:z.write(p,p.name)

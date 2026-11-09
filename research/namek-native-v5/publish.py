from pathlib import Path
import json,subprocess,shutil,gzip,zipfile,hashlib
P=Path('work/namek-native-v5');OLD=Path('work/namek-native-v4');O=Path('outputs/Namek-terreno-corregido-v5');R=Path('repository');M=R/'assets/media/namek-native-v5';E=R/'evidence/namek-native-v5';S=R/'research/namek-native-v5';fps=59.92274340431231
for d in [O,M,E,S]:d.mkdir(parents=True,exist_ok=True)
build=json.loads((P/'integrated-build.json').read_text());reports=[];videos=[];parts=[]
def run(args):subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y']+args,check=True)
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,width,height,avg_frame_rate','-of','json',str(p)],text=True))
def concat(files,dest):
 listing=dest.with_suffix('.concat.txt');listing.write_text('\n'.join("file '"+f.resolve().as_posix()+"'" for f in files),encoding='utf-8')
 run(['-f','concat','-safe','0','-i',str(listing),'-r',str(fps),'-fps_mode','cfr','-c:v','libx264','-preset','veryfast','-crf','17','-c:a','aac','-b:a','128k','-af','aresample=async=1:first_pts=0','-movflags','+faststart',str(dest)])
for slug in ['normal','aldea','porunga']:
 clips=[]
 for label in ['01-vuelo','02-goku']:
  root=P/'promo'/slug;report=json.loads((root/(label+'-report.json')).read_text());assert report['romSha256']==build['sha256'];rows=json.loads((root/(label+'.json')).read_text());v={'normal':1,'aldea':2,'porunga':3}[slug]
  assert all(r['physicalStage']==6 and r['nativeVariant']==v for r in rows);assert rows[-1]['scene']==0 and rows[-1]['cinema']==0
  reports.append(dict(scenario=slug,**report));clips.append(root/(label+'.mp4'))
  with gzip.open(E/(slug+'-'+label+'.json.gz'),'wb') as z:z.write((root/(label+'.json')).read_bytes())
  title={'normal':'NAMEK NORMAL','aldea':'NAMEK DEVASTADO','porunga':'NAMEK / PORUNGA'}[slug]
  vf="[0:v]crop=960:672:0:82,scale=640:448:flags=neighbor,setpts=PTS-STARTPTS[a];[1:v]crop=960:672:0:82,scale=640:448:flags=neighbor,setpts=PTS-STARTPTS[b];[a][b]hstack=shortest=1,pad=1280:520:0:72:color=0x10151c,drawtext=fontfile='work/namek-three/arialbd.ttf':text='"+title+"':x=14:y=5:fontsize=22:fontcolor=0xffd35a,drawtext=fontfile='work/namek-three/arial.ttf':text='ANTES / V4 - RESTOS DE TRONCO':x=14:y=39:fontsize=20:fontcolor=white,drawtext=fontfile='work/namek-three/arial.ttf':text='AHORA / V5 - TERRENO CORREGIDO':x=654:y=39:fontsize=20:fontcolor=white[v]"
  dest=O/(slug+'-'+label+'-comparacion.mp4');run(['-i',str(OLD/'promo'/slug/(label+'.mp4')),'-i',str(root/(label+'.mp4')),'-filter_complex',vf,'-map','[v]','-map','1:a','-shortest','-c:v','libx264','-preset','veryfast','-crf','17','-c:a','aac','-b:a','128k',str(dest)]);parts.append(dest)
 dest=O/('Namek-'+slug+'-V5.mp4');concat(clips,dest);run(['-i',str(dest),'-f','null','-']);shutil.copy2(dest,M/(slug+'.mp4'));shutil.copy2(P/slug/'native-ground.png',O/(slug+'.png'));shutil.copy2(P/slug/'native-ground.png',M/(slug+'.png'));videos.append(dict(scenario=slug,path=dest.name,sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),probe=probe(dest)))
 native=R/'assets/native/namek-v5'/slug;native.mkdir(parents=True,exist_ok=True)
 for file in ['gfx.lz','compiled-map.png']:shutil.copy2(P/slug/file,native/file)
 for file in ['map.bin','palette.bin']:(native/(file.split('.')[0]+'.hex')).write_text((P/slug/file).read_bytes().hex()+'\n')
 for file in ['build.json','runtime-check.json']:shutil.copy2(P/slug/file,E/(slug+'-'+file))
 print('READY',slug,flush=True)
comparison=O/'Namek-tres-variantes-antes-despues-V5.mp4';concat(parts,comparison);run(['-i',str(comparison),'-f','null','-']);shutil.copy2(comparison,M/'comparacion.mp4')
vf="[0:v]crop=130:180:160:130,scale=390:540:flags=neighbor[a];[1:v]crop=130:180:160:130,scale=390:540:flags=neighbor[b];[a][b]hstack,pad=780:588:0:48:color=0x10151c,drawtext=fontfile='work/namek-three/arialbd.ttf':text='ANTES / V4':x=14:y=12:fontsize=23:fontcolor=white,drawtext=fontfile='work/namek-three/arialbd.ttf':text='AHORA / V5':x=404:y=12:fontsize=23:fontcolor=white[v]"
cover=O/'Detalle-troncos-antes-despues.png';run(['-i',str(OLD/'normal/native-ground.png'),'-i',str(P/'normal/native-ground.png'),'-filter_complex',vf,'-map','[v]','-frames:v','1',str(cover)]);shutil.copy2(cover,M/'comparacion.png')
manifest=dict(buildId=build['buildId'],romSha256=build['sha256'],nativeCaptures=True,backgroundCompositing=False,normalSpeed=True,romDelivered=False,paletteV4Exact=True,userApprovalPending=True,physicalConsoleTested=False,comparison=probe(comparison),videos=videos,notes='V4 versus V5, all three variants. Native reused terrain module cleaned of cropped original trees. Existing concept slopes and connected stems protected. Porunga remains static.')
(M/'manifest.json').write_text(json.dumps(manifest,indent=2));(E/'captures.json').write_text(json.dumps(reports,indent=2))
for file in ['integrated-build.json','audit.json']:shutil.copy2(P/file,E/file)
shutil.copy2(P/'states-reviewed/selection-proof.json',E/'selection-proof.json')
for file in ['build.py','integrate.py','verify-resources.py','prepare-scenes.py','record-colors.py','audit.py','publish.py']:shutil.copy2(P/file,S/file)
S.joinpath('README.txt').write_text('NAMEK V5 / LIMPIEZA DEL TERRENO\n\nbuild.py parte de los indices V4. Requiere sus helpers y recursos locales de investigacion.\nLee el modulo nativo de la base privada200852 para sustituir fragmentos de arboles sin copa.\nCopia tiles vecinos a escala1:1 antes de espejo/repeticion; protege laderas y tallos conectados.\nLas48bytes de paleta coinciden exactamente con V4 en cada variante.\nEmpaquetado exacto, sin remuestreo ni aproximacion.\nAudit compara seis trazas de actores/entradas fotograma a fotograma con V4.\nEjecutar desde el workspace con work/ y repository/. Pillow/NumPy en work/simulation-deps.\nCore, ROM y estados privados no incluidos. Consola fisica y acabado final pendientes.\n',encoding='utf-8')
O.joinpath('LEEME.txt').write_text('NAMEK V5 / TRONCOS RECORTADOS\n\nLimpieza aplicada a Namek normal, devastado y Porunga.\nColores V4 conservados exactamente. Casa y dibujos existentes preservados.\nCapturas nativas de suelo, vuelo/aterrizaje y combate a velocidad normal.\nIncluye comparacion V4/V5 de las tres variantes, detalle del fallo y clips nuevos.\nPorunga sigue estatico. Sin ROM ni parche en esta entrega.\nBuild interno '+build['buildId']+'\n',encoding='utf-8')
with zipfile.ZipFile(O/'Namek-tres-variantes-V5.zip','w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
 for f in sorted(O.iterdir()):
  if f.name in ['Namek-tres-variantes-antes-despues-V5.mp4','Detalle-troncos-antes-despues.png','LEEME.txt','normal.png','aldea.png','porunga.png']+[v['path'] for v in videos]:z.write(f,f.name)
print('PUBLISHED',probe(comparison)['format']['duration'],flush=True)

from pathlib import Path
import json,subprocess,shutil,hashlib,gzip,zipfile
P=Path('work/namek-native-v4');OLD=Path('work/namek-native-v3');O=Path('outputs/Namek-paleta-cielo-v4');R=Path('repository');M=R/'assets/media/namek-native-v4';E=R/'evidence/namek-native-v4';S=R/'research/namek-native-v4'
for d in [O,M,E,S]:d.mkdir(parents=True,exist_ok=True)
build=json.loads((P/'integrated-build.json').read_text());fps=59.92274340431231
def run(args):subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y']+args,check=True)
def concat(files,dest):
 listing=dest.with_suffix('.concat.txt');listing.write_text('\n'.join("file '"+f.resolve().as_posix()+"'" for f in files),encoding='utf-8')
 run(['-f','concat','-safe','0','-i',str(listing),'-r',str(fps),'-fps_mode','cfr','-c:v','libx264','-preset','veryfast','-crf','17','-c:a','aac','-b:a','128k','-af','aresample=async=1:first_pts=0','-movflags','+faststart',str(dest)])
def probe(path):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,width,height,avg_frame_rate','-of','json',str(path)],text=True))
reports=[];videos=[]
for slug in ['normal','aldea','porunga']:
 clips=[]
 for label in ['01-vuelo','02-goku']:
  root=P/'promo'/slug;report=json.loads((root/(label+'-report.json')).read_text());assert report['romSha256']==build['sha256'];rows=json.loads((root/(label+'.json')).read_text());v={'normal':1,'aldea':2,'porunga':3}[slug]
  assert all(r['physicalStage']==6 and r['nativeVariant']==v for r in rows);assert rows[-1]['scene']==0 and rows[-1]['cinema']==0
  reports.append(dict(scenario=slug,**report));clips.append(root/(label+'.mp4'))
  with gzip.open(E/(slug+'-'+label+'.json.gz'),'wb') as z:z.write((root/(label+'.json')).read_bytes())
 dest=O/('Namek-'+slug+'-V4.mp4');concat(clips,dest);run(['-i',str(dest),'-f','null','-']);shutil.copy2(dest,M/(slug+'.mp4'));shutil.copy2(P/slug/'native-ground.png',O/(slug+'.png'));shutil.copy2(P/slug/'native-ground.png',M/(slug+'.png'))
 videos.append(dict(scenario=slug,filename=dest.name,sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),probe=probe(dest)));print('READY',slug,flush=True)
vf="[0:v][1:v]hstack,pad=1280:496:0:48:color=0x10151c,drawtext=fontfile='work/namek-three/arialbd.ttf':text='ANTES / V3':x=14:y=12:fontsize=23:fontcolor=white,drawtext=fontfile='work/namek-three/arialbd.ttf':text='AHORA / V4 - PIEDRA NEUTRA Y MARFIL':x=654:y=12:fontsize=23:fontcolor=white[v]"
cover=O/'Namek-paleta-cielo-antes-despues.png';run(['-i',str(OLD/'normal/native-ground.png'),'-i',str(P/'normal/native-ground.png'),'-filter_complex',vf,'-map','[v]','-frames:v','1',str(cover)]);shutil.copy2(cover,M/'comparacion.png')
parts=[]
for label in ['01-vuelo','02-goku']:
 old=OLD/'promo/normal'/(label+'.mp4');new=P/'promo/normal'/(label+'.mp4');dest=O/(label+'-comparacion.mp4')
 vf="[0:v]crop=960:672:0:82,scale=640:448:flags=neighbor,setpts=PTS-STARTPTS[a];[1:v]crop=960:672:0:82,scale=640:448:flags=neighbor,setpts=PTS-STARTPTS[b];[a][b]hstack=shortest=1,pad=1280:504:0:56:color=0x10151c,drawtext=fontfile='work/namek-three/arialbd.ttf':text='ANTES / V3 - ROJIZO Y FRANJA':x=14:y=14:fontsize=21:fontcolor=white,drawtext=fontfile='work/namek-three/arialbd.ttf':text='AHORA / V4 - PIEDRA Y MARFIL':x=654:y=14:fontsize=21:fontcolor=white[v]"
 run(['-i',str(old),'-i',str(new),'-filter_complex',vf,'-map','[v]','-map','1:a','-shortest','-c:v','libx264','-preset','veryfast','-crf','17','-c:a','aac','-b:a','128k',str(dest)]);parts.append(dest)
comparison=O/'Namek-paleta-cielo-antes-despues.mp4';concat(parts,comparison);run(['-i',str(comparison),'-f','null','-']);shutil.copy2(comparison,M/'comparacion.mp4')
manifest=dict(buildId=build['buildId'],romSha256=build['sha256'],nativeCaptures=True,backgroundCompositing=False,normalSpeed=True,romDelivered=False,userApprovalPending=True,physicalConsoleTested=False,comparison=probe(comparison),videos=videos,notes='V3 versus V4. Only palettes and house pixel color indices change; shapes/textures and gameplay retained. Sky band removed in normal Namek by equal green entries. Porunga remains static.')
(M/'manifest.json').write_text(json.dumps(manifest,indent=2));(E/'captures.json').write_text(json.dumps(reports,indent=2))
for file in ['build.py','integrate.py','verify-resources.py','prepare-scenes.py','record-colors.py','publish.py']:shutil.copy2(P/file,S/file)
for file in ['integrated-build.json']:shutil.copy2(P/file,E/file)
shutil.copy2(P/'states-reviewed/selection-proof.json',E/'selection-proof.json')
for slug in ['normal','aldea','porunga']:
 for file in ['build.json','runtime-check.json']:shutil.copy2(P/slug/file,E/(slug+'-'+file))
 native=R/'assets/native/namek-v4'/slug;native.mkdir(parents=True,exist_ok=True)
 for file in ['gfx.lz','compiled-map.png']:shutil.copy2(P/slug/file,native/file)
 for file in ['map.bin','palette.bin']:(native/(file.split('.')[0]+'.hex')).write_text((P/slug/file).read_bytes().hex()+'\n')
S.joinpath('README.txt').write_text('NAMEK V4 / COLOR Y CONTINUIDAD DEL CIELO\n\nbuild.py parte de los indices V3 privados: no remuestrea ni aproxima texturas.\nCambia la paleta y348 pixeles de color de la casa, dentro de la misma mascara.\nDeduplicacion exacta por simetrias; resultado730/733/733 tiles.\nEl cielo normal usa el mismo verde para sus dos antiguas entradas: sin franja.\nLos scripts de captura usan las herramientas de V1 y el core local, no incluidos.\nEjecutar desde el workspace con work/ y repository/. Requiere Pillow/NumPy.\nSin ROM ni estados publicados. Consola fisica y aprobacion visual pendientes.\n',encoding='utf-8')
O.joinpath('LEEME.txt').write_text('NAMEK V4 / PALETA Y CIELO\n\nMontanas y terreno en tonos de piedra neutra, sin el rojizo anterior.\nCasa marfil con el mismo tamano y color en las tres variantes.\nFranja del cielo del Namek normal eliminada unificando las dos entradas verdes.\nDetalle V3 conservado sin remuestreo. Capturas nativas, velocidad normal.\nIncluye comparacion V3/V4 e imagenes y clips de las tres variantes.\nPorunga sigue estatico. No se entrega ROM ni parche.\nBuild interno '+build['buildId']+'\n',encoding='utf-8')
with zipfile.ZipFile(O/'Namek-paleta-cielo-V4.zip','w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
 for f in sorted(O.iterdir()):
  if f.suffix in ['.mp4','.png','.txt'] and not f.name.endswith('.concat.txt') and not f.name.startswith(('01-','02-')):z.write(f,f.name)
print('PUBLISHED',probe(comparison)['format']['duration'],flush=True)

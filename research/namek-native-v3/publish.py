from pathlib import Path
import json,subprocess,shutil,hashlib,gzip,zipfile
P=Path('work/namek-native-v3');O=Path('outputs/Namek-revision-nativa-v3');M=Path('repository/assets/media/namek-native-v3');E=Path('repository/evidence/namek-native-v3')
for d in [O,M,E]:d.mkdir(parents=True,exist_ok=True)
build=json.loads((P/'integrated-build.json').read_text());fps=59.92274340431231
names={'normal':'Namek-Gran-Patriarca','aldea':'Namek-aldea-devastada','porunga':'Namek-Porunga'}
orders={'normal':['01-vuelo','02-goku','03-gohan','04-vegeta','05-cell','06-pantalla-partida'],'aldea':['04-vegeta','02-goku','03-gohan','05-cell','01-vuelo','06-pantalla-partida'],'porunga':['05-cell','04-vegeta','02-goku','03-gohan','01-vuelo','06-pantalla-partida']}
def run(args):subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y']+args,check=True)
def probe(path):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,width,height,avg_frame_rate','-of','json',str(path)],text=True))
def concat(files,dest):
 listing=dest.with_suffix('.concat.txt');listing.write_text('\n'.join("file '"+f.resolve().as_posix()+"'" for f in files),encoding='utf-8');run(['-f','concat','-safe','0','-i',str(listing),'-r',str(fps),'-fps_mode','cfr','-c:v','libx264','-preset','veryfast','-crf','17','-c:a','aac','-b:a','128k','-af','aresample=async=1:first_pts=0','-movflags','+faststart',str(dest)])
reports=[];videos=[]
for slug,order in orders.items():
 root=P/'promo'/slug
 for label in order:
  report=json.loads((root/(label+'-report.json')).read_text());assert report['romSha256']==build['sha256'];rows=json.loads((root/(label+'.json')).read_text());v={'normal':1,'aldea':2,'porunga':3}[slug]
  assert all(r['physicalStage']==6 and r['nativeVariant']==v for r in rows)
  assert rows[-1]['scene']==0 and rows[-1]['cinema']==0
  if label=='05-cell':assert 0x843 in report['programs']
  with gzip.open(E/(slug+'-'+label+'.json.gz'),'wb') as z:z.write((root/(label+'.json')).read_bytes())
  reports.append(dict(scenario=slug,**report))
 target=O/(names[slug]+'.mp4');concat([root/(label+'.mp4') for label in order],target);run(['-i',str(target),'-f','null','-'])
 info=probe(target);shutil.copy2(target,M/('promo-'+slug+'.mp4'))
 cover=O/(names[slug]+'.png');run(['-ss','3','-i',str(target),'-frames:v','1',str(cover)]);shutil.copy2(cover,M/('promo-'+slug+'.png'))
 videos.append(dict(scenario=slug,filename=target.name,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),probe=info,chapters=order));print('PROMO READY',slug,info['format']['duration'],flush=True)
comparison=[]
for slug in names:
 for label in ['01-vuelo','02-goku']:
  old=Path('work/namek-native/promo')/slug/(label+'.mp4');new=P/'promo'/slug/(label+'.mp4');dest=O/(slug+'-'+label+'-comparacion.mp4')
  title={'normal':'NAMEK / GRAN PATRIARCA','aldea':'NAMEK / ALDEA DEVASTADA','porunga':'NAMEK / PORUNGA'}[slug]
  vf="[0:v]crop=960:672:0:82,scale=640:448:flags=neighbor,setpts=PTS-STARTPTS[a];[1:v]crop=960:672:0:82,scale=640:448:flags=neighbor,setpts=PTS-STARTPTS[b];[a][b]hstack=shortest=1,pad=1280:520:0:72:color=0x10151c,drawtext=fontfile='work/namek-three/arialbd.ttf':text='"+title+"':x=14:y=5:fontsize=22:fontcolor=0xffd35a,drawtext=fontfile='work/namek-three/arial.ttf':text='ANTES / ADAPTACION DESCARTADA':x=14:y=39:fontsize=20:fontcolor=white,drawtext=fontfile='work/namek-three/arial.ttf':text='AHORA / RECURSOS NATIVOS A UN PIXEL':x=654:y=39:fontsize=20:fontcolor=white[v]"
  run(['-i',str(old),'-i',str(new),'-filter_complex',vf,'-map','[v]','-map','1:a','-shortest','-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(dest)]);comparison.append(dest)
out=O/'Namek-antes-y-ahora.mp4';concat(comparison,out);run(['-i',str(out),'-f','null','-']);shutil.copy2(out,M/'comparacion.mp4');info=probe(out)
run(['-ss','9','-i',str(out),'-frames:v','1',str(O/'Namek-antes-y-ahora.png')]);shutil.copy2(O/'Namek-antes-y-ahora.png',M/'comparacion.png')
shutil.copy2('outputs/Namek-cuatro-videos-nativos/01-Namek-original.mp4',O/'Namek-original-referencia.mp4')
manifest=dict(buildId=build['buildId'],romSha256=build['sha256'],nativeBackgrounds=True,backgroundCompositing=False,normalSpeed=True,romDelivered=False,physicalConsoleTested=False,userApprovalPending=True,porungaAnimated=False,videos=videos,comparison=info,comparisonMeaning='Earlier native adaptation versus new native assets; same scripted routes at normal speed, not guaranteed identical actor animation phase. Audio from new capture.',originalReference='Existing050003 recording: original stage assets with Enhanced gameplay; unchanged in current build.')
(M/'manifest.json').write_text(json.dumps(manifest,indent=2));(E/'promo-validation.json').write_text(json.dumps(reports,indent=2))
for file in ['integrated-build.json','reproducibility.json','matrix-modes-variants.json']:shutil.copy2(P/file,E/file)
shutil.copy2(P/'states-reviewed/selection-proof.json',E/'selection-proof.json')
for slug in names:
 for file in ['build.json','runtime-check.json']:shutil.copy2(P/slug/file,E/(slug+'-'+file))
O.joinpath('LEEME.txt').write_text('NAMEK / REVISION NATIVA V3\n\nAntes/despues de las tres variantes y tres demostraciones completas.\nReferencia original incluida: escenario original, jugabilidad Enhanced.\nCapturas reales de la ROM interna, velocidad normal, sin sustituir el fondo en edicion.\nTerreno rehecho con textura nativa reutilizada a un pixel, no miniaturas ampliadas.\nLa composicion del primer plano cambia al usar modulos de suelo; no es una copia exacta de los conceptos.\nCasa compartida con la misma escala y color en las tres variantes.\nPorunga permanece estatico: flotacion como sprite pendiente.\nV2 de baja definicion descartada. Acabado V3 pendiente de valoracion del usuario.\nSin ROM ni parche en esta entrega. Consola fisica aun sin probar.\nBuild interno '+build['buildId']+'\n',encoding='utf-8')
with zipfile.ZipFile(O/'Namek-revision-nativa-v3.zip','w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
 for f in sorted(O.glob('*')):
  if f.name in [v['filename'] for v in videos]+['Namek-antes-y-ahora.mp4','Namek-antes-y-ahora.png','Namek-original-referencia.mp4','LEEME.txt']:z.write(f,f.name)
print('PUBLISHED',info['format']['duration'],flush=True)

from pathlib import Path
import sys,json,hashlib,subprocess,shutil
sys.path.insert(0,'work/simulation-deps')
from PIL import Image,ImageDraw,ImageFont
T=Path('work/namek-native-r7');OLD=Path('work/namek-native-r6');O=Path('outputs/Namek-roca-R7');O.mkdir(exist_ok=True,parents=True)
labels=['01-vuelo','02-goku','06-pantalla-partida'];slugs=['normal','aldea','porunga']
files=[];takes=[];chapters=[];cursor=0
build=json.loads((T/'integrated-build.json').read_text())
for slug in slugs:
 start=cursor
 for label in labels:
  path=T/'promo'/slug/(label+'.mp4');files.append(path)
  report=json.loads((T/'promo'/slug/(label+'-report.json')).read_text());assert report['romSha256']==build['sha256'];takes.append(dict(variant=slug,**report));cursor+=report['seconds']
  rows=json.loads((T/'promo'/slug/(label+'.json')).read_text())
  assert all(r['physicalStage']==6 and r['nativeVariant']==slugs.index(slug)+1 for r in rows)
 chapters.append(dict(variant=slug,start=start,end=cursor))
listing=T/'concat.txt';listing.write_text('\n'.join("file '"+f.resolve().as_posix()+"'" for f in files),encoding='utf-8')
full=O/'Namek-R7-ROM-tres-escenarios.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(full)],check=True)
# Ambos lados son capturas reales. Igual escala entera y sin acelerar el juego.
compareParts=[]
for label in ['01-vuelo','06-pantalla-partida']:
 before=OLD/'promo/normal'/(label+'.mp4');after=T/'promo/normal'/(label+'.mp4');target=T/(label+'-compare.mp4');compareParts.append(target)
 font='work/namek-three/arialbd.ttf'
 vf="[0:v]crop=960:672:0:82,scale=640:448:flags=neighbor,pad=640:486:0:38:color=0x10151c,drawtext=fontfile='"+font+"':text='R6 - ANTES':x=12:y=8:fontsize=21:fontcolor=white[a];[1:v]crop=960:672:0:82,scale=640:448:flags=neighbor,pad=640:486:0:38:color=0x10151c,drawtext=fontfile='"+font+"':text='R7 - TEXTURA FINA':x=12:y=8:fontsize=21:fontcolor=0xffd35a[b];[a][b]hstack=shortest=1[v]"
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(before),'-i',str(after),'-filter_complex',vf,'-map','[v]','-map','1:a','-shortest','-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(target)],check=True)
listing=T/'compare-concat.txt';listing.write_text('\n'.join("file '"+f.resolve().as_posix()+"'" for f in compareParts),encoding='utf-8')
comparison=O/'Comparacion-ROM-R6-R7.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(comparison)],check=True)
font=ImageFont.truetype('work/namek-three/arialbd.ttf',16)
before=Image.open(OLD/'promo/normal/02-goku-qa-0001.png').convert('RGB');after=Image.open(T/'promo/normal/02-goku-qa-0001.png').convert('RGB')
assert before.size==after.size==(640,448)
# QA: guardar vistas completas a 1x y2x, y el mismo recorte en ambos lados.
for scale in [1,2]:
 w,h=320*scale,224*scale;canvas=Image.new('RGB',(w*2,h+32),(16,21,28));d=ImageDraw.Draw(canvas)
 for x,im,title in [(0,before,'R6 - ANTES'),(w,after,'R7 - TEXTURA FINA')]:
  d.text((x+8,7),title,font=font,fill='white');canvas.paste(im.resize((w,h),Image.Resampling.NEAREST),(x,32))
 canvas.save(O/f'Comparacion-ROM-{scale}x.png')
box=(252,118,628,260);canvas=Image.new('RGB',(752,176),(16,21,28));d=ImageDraw.Draw(canvas)
for x,im,title in [(0,before,'R6 - ANTES'),(376,after,'R7 - TEXTURA FINA')]:
 d.text((x+8,6),title,font=font,fill='white');canvas.paste(im.crop(box),(x,32))
canvas.save(O/'Detalle-roca-misma-escala.png')
original=Image.open('work/namek-native/promo/original/02-goku-qa-0001.png').convert('RGB')
canvas=Image.new('RGB',(960,256),(16,21,28));d=ImageDraw.Draw(canvas)
for x,im,title in [(0,original,'FONDO DEL JUEGO'),(320,before,'R6'),(640,after,'R7')]:
 d.text((x+8,7),title,font=font,fill='white');canvas.paste(im.resize((320,224),Image.Resampling.NEAREST),(x,32))
canvas.save(O/'Referencia-original-R6-R7-1x.png')
media=[]
for video in [full,comparison]:
 subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],check=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,width,height,r_frame_rate','-of','json',str(video)],text=True))
 media.append(dict(path=video.resolve().as_posix(),sha256=hashlib.sha256(video.read_bytes()).hexdigest(),probe=probe,decodeComplete=True));print(video.name,probe['format']['duration'],flush=True)
manifest=dict(date='2026-11-09',build=build,backgroundIntegrated=True,privateReview=True,published=False,postproductionBackgroundReplacement=False,integerComparisonScale=2,validation=json.loads((T/'runtime-validation.json').read_text()),selection=json.loads((T/'states-final/selection-proof.json').read_text()),chapters=chapters,takes=takes,media=media,approvalPending=True)
(O/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(T/'delivery-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for slug in slugs:
 shutil.copy2(T/'promo'/slug/'02-goku-qa-0001.png',O/(slug+'-ROM.png'));shutil.copy2(T/slug/'compiled-map.png',O/(slug+'-mapa.png'))
(O/'LEEME.txt').write_text('PRUEBA R7 - TEXTURA FINA\n\nComparacion de capturas reales R6/R7 a la misma escala entera2x.\nVideo adicional con los tres fondos R7, vuelo y Kamehameha con pantalla partida.\nResolucion de juego320x224, mismo color, casa, suelo y siluetas.\nLas copas tienen ajustes pequenos; la mejora principal es la roca.\nNo hay suavizado ni reemplazo de fondos en posproduccion.\nVideos locales sin publicar. R7 pendiente de valoracion.\n',encoding='utf-8')

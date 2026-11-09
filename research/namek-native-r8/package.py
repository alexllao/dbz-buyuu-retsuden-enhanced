from pathlib import Path
import sys,json,hashlib,subprocess,shutil
sys.path.insert(0,'work/simulation-deps')
from PIL import Image,ImageDraw,ImageFont
T=Path('work/namek-native-r8');OLD=Path('work/namek-native-r6');O=Path('outputs/Namek-R8-revision');O.mkdir(exist_ok=True,parents=True)
labels=['01-vuelo','02-goku','06-pantalla-partida'];slugs=['normal','aldea','porunga'];titles=['NAMEK NORMAL','DEVASTADO / LAVA','PORUNGA']
build=json.loads((T/'integrated-build.json').read_text());files=[];takes=[];phaseChecks=[];chapters=[];cursor=0
for slug in slugs:
 start=cursor
 for label in labels:
  files.append(T/'promo'/slug/(label+'.mp4'));report=json.loads((T/'promo'/slug/(label+'-report.json')).read_text());assert report['romSha256']==build['sha256'];takes.append(dict(variant=slug,**report));cursor+=report['seconds']
  rows=json.loads((T/'promo'/slug/(label+'.json')).read_text());assert all(r['physicalStage']==6 and r['nativeVariant']==slugs.index(slug)+1 for r in rows)
 phaseChecks.extend(json.loads((T/'states-final-r8'/slug/'capture-manifest.json').read_text())['checks'])
 chapters.append(dict(variant=slug,start=start,end=cursor))
listing=T/'concat.txt';listing.write_text('\n'.join("file '"+p.resolve().as_posix()+"'" for p in files),encoding='utf-8')
metadata=T/'chapters.ffmeta';metadata.write_text(';FFMETADATA1\ntitle=DBZ v1.0 Namek R8 '+build['buildId']+'\n'+''.join('[CHAPTER]\nTIMEBASE=1/1000\nSTART='+str(round(c['start']*1000))+'\nEND='+str(round(c['end']*1000))+'\ntitle='+c['variant']+'\n' for c in chapters),encoding='utf-8')
video=O/('DBZ-v1.0-Namek-R8-'+build['buildId']+'.mp4')
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(listing),'-i',str(metadata),'-map_metadata','1','-map_chapters','1','-c','copy','-movflags','+faststart',str(video)],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,width,height,r_frame_rate:chapter=start_time,end_time,tags','-of','json',str(video)],text=True))
font=ImageFont.truetype('work/namek-three/arialbd.ttf',16)
canvas=Image.new('RGB',(960,256),(16,21,28));d=ImageDraw.Draw(canvas)
comparison=Image.new('RGB',(960,512),(16,21,28));dc=ImageDraw.Draw(comparison)
for i,(slug,title) in enumerate(zip(slugs,titles)):
 current=Image.open(T/'promo'/slug/'02-goku-qa-0001.png').convert('RGB');assert current.size==(640,448)
 before=Image.open(OLD/'promo'/slug/'02-goku-qa-0001.png').convert('RGB');assert before.size==current.size
 canvas.paste(current.resize((320,224),Image.Resampling.NEAREST),(i*320,32));d.text((i*320+8,7),'R8 - '+title,font=font,fill='white')
 for row,im,label in [(0,before,'ANTES R6'),(1,current,'AHORA R8')]:
  comparison.paste(im.resize((320,224),Image.Resampling.NEAREST),(i*320,row*256+32));dc.text((i*320+8,row*256+7),label+' - '+title,font=font,fill='white')
 shutil.copy2(T/'promo'/slug/'02-goku-qa-0001.png',O/(slug+'-ROM.png'));shutil.copy2(T/slug/'compiled-map.png',O/(slug+'-mapa-512.png'))
canvas.save(O/'R8-tres-variantes-ROM.png');comparison.save(O/'Comparacion-R6-R8-1x.png')
for slug,name in [('normal','Casa-y-roca-R6-R8'),('porunga','Cielo-Porunga-R6-R8')]:
 before=Image.open(OLD/'promo'/slug/'02-goku-qa-0001.png').convert('RGB');current=Image.open(T/'promo'/slug/'02-goku-qa-0001.png').convert('RGB')
 if slug=='normal':box=(252,64,632,260)
 else:box=(0,64,640,272)
 w,h=box[2]-box[0],box[3]-box[1];out=Image.new('RGB',(w*2,h+32),(16,21,28));dr=ImageDraw.Draw(out)
 for x,im,label in [(0,before,'ANTES R6'),(w,current,'AHORA R8')]:dr.text((x+8,7),label,font=font,fill='white');out.paste(im.crop(box),(x,32))
 out.save(O/(name+'.png'))
for slug in slugs:
 for label,frame in [('01-vuelo',181),('06-pantalla-partida',361)]:shutil.copy2(T/'promo'/slug/(label+f'-qa-{frame:04}.png'),O/(slug+'-'+label+'.png'))
manifest=dict(date='2026-11-09',privateReview=True,published=False,backgroundIntegrated=True,postproductionBackgroundReplacement=False,nativeFrame=[320,224],integerPresentationScale=2,build=build,chapters=chapters,takes=takes,phaseResourceChecks=phaseChecks,runtime=json.loads((T/'runtime-validation.json').read_text()),selection=json.loads((T/'states-final-r8/selection-proof.json').read_text()),video=dict(path=video.resolve().as_posix(),sha256=hashlib.sha256(video.read_bytes()).hexdigest(),probe=probe,decodeComplete=True),approvalPending=True)
(O/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(T/'delivery-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(O/'LEEME.txt').write_text('NAMEK R8 - REVISION NATIVA\n\nVideo real de los tres fondos, suelo, vuelo, combate y pantalla partida.\nJuego320x224 mostrado a2x entero, con sonido y velocidad normal.\nCasa con contorno y proporciones corregidos, roca fina, Porunga redibujado,\ncielo nocturno reconstruido con nubes completas y sin franjas ni restos.\nPorunga, humo y lava siguen estaticos en el fondo.\nSe conservan R6, R7 y los maestros anteriores. R8 pendiente de valoracion.\nVideo local sin publicar; no se entrega ROM.\n',encoding='utf-8')
print(json.dumps(dict(video=video.as_posix(),seconds=probe['format']['duration'],chapters=chapters,resourceChecks=len(phaseChecks)+len(manifest['runtime']['checks'])),ensure_ascii=False),flush=True)

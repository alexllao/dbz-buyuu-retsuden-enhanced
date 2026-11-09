from pathlib import Path
import json,subprocess,hashlib,shutil
T=Path('work/namek-native-r6');O=Path('outputs/Namek-R6-ROM-revision');O.mkdir(parents=True,exist_ok=True)
labels=['01-vuelo','02-goku','03-gohan','04-vegeta','05-cell','06-pantalla-partida']
files=[];chapters=[];cursor=0;reports=[]
for slug,title in [('normal','Namek normal'),('aldea','Namek devastado con lava'),('porunga','Invocacion de Porunga')]:
 start=cursor
 for label in labels:
  f=T/'promo'/slug/(label+'.mp4');files.append(f)
  report=json.loads((T/'promo'/slug/(label+'-report.json')).read_text());reports.append(dict(variant=slug,**report));cursor+=report['seconds']
  rows=json.loads((T/'promo'/slug/(label+'.json')).read_text())
  assert all(r['physicalStage']==6 and r['nativeVariant']==['normal','aldea','porunga'].index(slug)+1 for r in rows)
 chapters.append(dict(title=title,start=start,end=cursor))
listing=T/'revision-concat.txt';listing.write_text('\n'.join("file '"+f.resolve().as_posix()+"'" for f in files),encoding='utf-8')
metadata=T/'chapters.ffmeta';metadata.write_text(';FFMETADATA1\ntitle=Namek R6 - Revision privada de ROM\n'+''.join('[CHAPTER]\nTIMEBASE=1/1000\nSTART='+str(round(c['start']*1000))+'\nEND='+str(round(c['end']*1000))+'\ntitle='+c['title']+'\n' for c in chapters),encoding='utf-8')
video=O/'Namek-R6-ROM-tres-escenarios.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(listing),'-i',str(metadata),'-map_metadata','1','-map_chapters','1','-c','copy','-movflags','+faststart',str(video)],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,width,height,r_frame_rate:chapter=start_time,end_time,tags','-of','json',str(video)],text=True))
for slug in ['normal','aldea','porunga']:
 shutil.copy2(T/'promo'/slug/'02-goku-qa-0001.png',O/(slug+'-captura-ROM.png'))
 shutil.copy2(T/slug/'compiled-map.png',O/(slug+'-mapa-compilado.png'))
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','0','-i',str(video),'-frames:v','1',str(O/'portada.png')],check=True)
manifest=dict(date='2026-11-09',privateReview=True,published=False,backgroundIntegrated=True,postproductionBackgroundReplacement=False,backgroundEffectsAnimated=False,build=json.loads((T/'integrated-build.json').read_text()),validation=json.loads((T/'runtime-validation.json').read_text()),selection=json.loads((T/'states-q3/selection-proof.json').read_text()),chapters=chapters,takes=reports,video=dict(path=video.resolve().as_posix(),sha256=hashlib.sha256(video.read_bytes()).hexdigest(),probe=probe))
(O/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(T/'delivery-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(O/'LEEME.txt').write_text('NAMEK R6 - REVISION PRIVADA\n\nCaptura real del framebuffer y sonido de la ROM experimental.\nTres fondos, vuelo, combos, Meteor y ataque grande con pantalla partida.\nVelocidad normal; sin sustitucion de fondos en posproduccion.\nLos PNG maestros aprobados se conservan aparte. La adaptacion nativa queda para tu revision.\nLava, humo y Porunga son elementos estaticos de fondo en esta prueba.\nVideo local: no publicado ni subido al repositorio. No se incluye ROM.\n',encoding='utf-8')
print(json.dumps(dict(video=str(video),seconds=probe['format']['duration'],chapters=chapters,decodeComplete=True),ensure_ascii=False),flush=True)

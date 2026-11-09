from pathlib import Path
import json,hashlib,shutil
R=Path('repository');A=R/'assets/concepts/namek-revision-r6';p=A/'manifest.json'
m=json.loads(p.read_text(encoding='utf-8-sig'))
for f in m['files']:
 if f['file']=='porunga-propuesta.png':f['status']='approved'
 if f['file']=='aldea-propuesta.png':f['status']='archived_superseded_by_lava'
m['files']=[f for f in m['files'] if f['file']!='aldea-lava-aprobado.png']+[dict(file='aldea-lava-aprobado.png',status='approved',sha256=hashlib.sha256((A/'aldea-lava-aprobado.png').read_bytes()).hexdigest(),width=1254,height=1254,source='exec-d4b1e520-5fd9-44c9-b651-c7245df9dda7.png',byteIdenticalCopy=True)]
m['approval']='perfctos los tres, kedan muy bien, almenso como yo lo veo'
m['lavaApproval']='si, mucho mejor'
m['scope']='Art masters approved; native adaptation requires separate review'
m.pop('romModified',None);m['romModifiedDuringArtGeneration']=False
m['nativeIntegrationAuthorized']=True;m['nativeRequest']='el video ke sea de la rom'
p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
shutil.copy2(p,Path('outputs/Namek-revision-grafica-R6/manifest.json'))
T=Path('work/namek-native-r6');E=R/'evidence/namek-native-r6';E.mkdir(parents=True,exist_ok=True)
for f in ['integrated-build.json','runtime-validation.json','delivery-manifest.json']:
 if (T/f).exists():shutil.copy2(T/f,E/f)
if (T/'states-q3/selection-proof.json').exists():shutil.copy2(T/'states-q3/selection-proof.json',E/'selection-proof.json')
sources=R/'research/namek-native-r6';sources.mkdir(parents=True,exist_ok=True)
for f in ['build.py','integrate.py','prepare-scenes.py','record-promo.py','verify-runtime.py','package.py','update-records.py']:shutil.copy2(T/f,sources/f)
for slug in ['normal','aldea','porunga']:shutil.copy2(T/slug/'build.json',E/(slug+'-build.json'))
M=R/'assets/media/namek-native-r6';M.mkdir(parents=True,exist_ok=True)
for slug in ['normal','aldea','porunga']:
 shutil.copy2(T/slug/'compiled-map.png',M/(slug+'-mapa.png'))
 capture=T/'promo'/slug/'02-goku-qa-0001.png'
 if capture.exists():shutil.copy2(capture,M/(slug+'-ROM.png'))
# El vídeo de revisión se queda local: no copiar MP4 al repositorio.
print('Records updated; video remains local',flush=True)

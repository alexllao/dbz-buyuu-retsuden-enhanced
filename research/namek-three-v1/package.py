from pathlib import Path
import subprocess,shutil,json,hashlib,zipfile
T=Path('work/namek-three');V=T/'video';O=Path('outputs/Namek-tres-escenarios-pixel-art');O.mkdir(parents=True,exist_ok=True);R=Path('repository');M=R/'assets/media/namek-three-v1';M.mkdir(parents=True,exist_ok=True)
labels=['01-vuelo','02-goku','03-gohan','04-vegeta','05-cell','06-pantalla-partida'];names={'normal':'Namek-normal','aldea':'Namek-aldea-devastada','porunga':'Namek-Porunga','tres':'Namek-tres-escenarios'};results=[]
for slug,name in names.items():
 listing=T/(slug+'-concat.txt');listing.write_text('\n'.join("file '"+(V/slug/(label+'.mp4')).resolve().as_posix()+"'" for label in labels),encoding='utf-8');out=O/(name+'.mp4')
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(out)],check=True)
 subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,width,height,r_frame_rate','-of','json',str(out)],text=True))
 shutil.copy2(out,M/(slug+'.mp4'));results.append(dict(slug=slug,path=(M/(slug+'.mp4')).as_posix(),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),probe=probe));print('VERIFIED',slug,probe['format']['duration'],flush=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','9','-i',str(O/(names['tres']+'.mp4')),'-frames:v','1',str(O/'Portada-tres-escenarios.png')],check=True)
shutil.copy2(O/'Portada-tres-escenarios.png',M/'portada.png')
audit=json.loads((T/'replay-audit.json').read_text());manifest=dict(date='2026-11-09',sourceBuild='20261108-200852',sourceRomSha256=hashlib.sha256(Path('work/combo-startup/candidate.bin').read_bytes()).hexdigest(),backgroundIntegrated=False,house='Approximately 75-80% of preceding normal-house dimensions; mountains unchanged in intention',variants=['normal','aldea devastada','invocacion de Porunga'],assets=[dict(path=p.as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in (R/'assets/concepts/namek-three-v1').glob('*.png')],audit=audit,media=results)
(M/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(O/'LEEME.txt').write_text('NAMEK: TRES ESCENARIOS EN PIXEL ART\n\nCasa del Gran Patriarca algo mas pequena respecto a la montana.\nNormal, aldea devastada e invocacion de Porunga.\nIncluye video simultaneo e individuales, de unos 51 segundos.\nVuelo, cuatro personajes, combos, Meteor y Kamehameha de pantalla partida.\n\nPersonajes, movimiento, impactos, sonido y HUD del build aprobado 20261108-200852.\nLos fondos se componen en posproduccion: NO estan integrados en la ROM todavia.\nEl panorama y sus objetos son estaticos; el movimiento viene del combate y del scroll nativo.\n\nhttps://github.com/alexllao/dbz-buyuu-retsuden-enhanced/blob/development/docs/namek-three-v1.md\n',encoding='utf-8')
with zipfile.ZipFile(O/'Namek-tres-escenarios.zip','w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
 for p in sorted(O.iterdir()):
  if p.suffix in ['.mp4','.png','.txt']:z.write(p,p.name)
print('PACKAGED',O,flush=True)

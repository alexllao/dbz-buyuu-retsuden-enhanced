from pathlib import Path
import json,hashlib,subprocess,shutil,concurrent.futures,html,struct
ROOT=Path('work/auras/colors-v4');OUT=Path('outputs/ki-colores-v4');OUT.mkdir(exist_ok=True)
for folder in ['Solo-nuevo','Capturas']: (OUT/folder).mkdir(exist_ok=True)
build=json.loads((ROOT/'build.json').read_text(encoding='utf-8'));expected=build['target_sha256']
names=['Goku-SSJ','Gohan-SSJ2','Piccolo','Vegeta-SSJ','Trunks-SSJ','Cell','A18','Krilin','Freezer','Recoome','Ginyu']
colors=['DORADO','DORADO','BLANCO AZULADO','DORADO','DORADO','DORADO','BLANCO AZULADO','BLANCO','BLANCO AZULADO','BLANCO Y VIOLETA','LILA']
font='work/auras/arial.ttf'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ff(args):subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',*args],check=True)
def package(cid):
 folder=ROOT/'runtime'/f'cid{cid:02}';trace=json.loads((folder/'trace.json').read_text());checks=json.loads((folder/'colors.json').read_text())
 assert trace['rom_sha256']==checks['source_sha256']==expected
 assert all(s['atlas_exact'] and s['dirty']==0 and all(p['exact'] for p in s['palettes']) for s in checks['samples'])
 rows=trace['frames'];assert rows[-1]['phase']==0 and rows[-1]['action']==0 and any(r['native_aura'] for r in rows)
 budgets=dict(sprites=max(r['sprite_count'] for r in rows),scanline_sprites=max(r['scanline_peak'] for r in rows),scanline_pixels=max(r['scanline_pixels_peak'] for r in rows))
 assert budgets['sprites']<=80 and budgets['scanline_sprites']<=20 and budgets['scanline_pixels']<=320
 filename=f'{cid:02}-{names[cid]}.mp4';new=OUT/'Solo-nuevo'/filename;shutil.copyfile(folder/'gameplay.mp4',new)
 old=Path('work/auras/runtime')/f'cid{cid:02}-before'/'gameplay.mp4'
 oldTrace=json.loads((old.parent/'trace.json').read_text());assert oldTrace['rom_sha256']=='6460ad414fda368526bfb13170e14ead6908b2e588b10d2605c993872c2b63e4'
 vf=f"[0:v]fps=60,setpts=PTS-STARTPTS[a];[1:v]fps=60,setpts=PTS-STARTPTS[b];[a][b]hstack=inputs=2:shortest=1,pad=iw:ih+56:0:56:color=0x101723,drawtext=fontfile={font}:text='KI ORIGINAL - {names[cid]}':x=18:y=10:fontsize=21:fontcolor=white,drawtext=fontfile={font}:text='KI NUEVO - {colors[cid]} - SIN RAYOS':x=658:y=10:fontsize=20:fontcolor=white,drawtext=fontfile={font}:text='Carga - suelta - vuelta al movimiento':x=18:y=35:fontsize=14:fontcolor=0xb5c1d2"
 ff(['-i',str(old),'-i',str(new),'-filter_complex',vf,'-an','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/filename)])
 frame=max([90,91],key=lambda i:rows[i]['sprite_count']);imageName=f'{cid:02}-{names[cid]}.png';shutil.copyfile(folder/f'frame-{frame:03}.png',OUT/'Capturas'/imageName)
 slow=ROOT/'slow'/filename;slow.parent.mkdir(exist_ok=True)
 ff(['-i',str(OUT/filename),'-vf',f"trim=start_frame=140:end_frame=190,setpts=4*(PTS-STARTPTS),pad=iw:ih+30:0:0:color=0x101723,drawtext=fontfile={font}:text='SALIDA A 1/4 DE VELOCIDAD':x=18:y=510:fontsize=18:fontcolor=white",'-an','-r','60','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p',str(slow)])
 print('Packaged',names[cid],flush=True)
 return dict(character_id=cid,name=names[cid],color=colors[cid],comparison_video=filename,comparison_sha256=sha(OUT/filename),new_only_video='Solo-nuevo/'+filename,new_only_sha256=sha(new),screenshot='Capturas/'+imageName,screenshot_sha256=sha(OUT/'Capturas'/imageName),recorded_frames=len(rows),palette_samples=len(checks['samples']),all_palette_and_atlas_samples_exact=True,graphics_budgets=budgets,lightning=False)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:entries=list(pool.map(package,range(11)))
def concat(paths,target):
 listing=ROOT/(target+'.txt');listing.write_text(''.join("file '"+str(p.resolve()).replace('\\','/')+"'\n" for p in paths),encoding='utf-8')
 ff(['-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(OUT/target)])
concat([OUT/e['comparison_video'] for e in entries],'Ki-todos-antes-despues.mp4')
concat([ROOT/'slow'/e['comparison_video'] for e in entries],'Salida-ki-todos-lenta.mp4')
rom=(ROOT/'candidate.bin').read_bytes();base=Path('work/rom/original.bin').read_bytes();padded=base+bytes(len(rom)-len(base));patch=bytearray(b'PATCH');i=0
while i<len(rom):
 if padded[i]==rom[i]:i+=1;continue
 start=i;i+=1
 while i<len(rom) and padded[i]!=rom[i] and i-start<65535:i+=1
 patch+=start.to_bytes(3,'big')+(i-start).to_bytes(2,'big')+rom[start:i]
patch+=b'EOF'+len(rom).to_bytes(3,'big');(OUT/'Auras-Colores-v4.ips').write_bytes(patch)
romFilename='Jugabilidad_v1_Colores_v1_Ki_Individual_v4.bin';shutil.copyfile(ROOT/'candidate.bin',OUT/romFilename)
report=dict(revision='c2-v4-character-colors',source_sha256=sha('work/rom/original.bin'),target_sha256=expected,target_bytes=len(rom),rom_filename=romFilename,patch_sha256=sha(OUT/'Auras-Colores-v4.ips'),characters=entries,comparison_source=dict(sha256='6460ad414fda368526bfb13170e14ead6908b2e588b10d2605c993872c2b63e4',description='Native original Ki effect with previously accepted controls/colors v1. This is not the untouched ROM as a whole.'),montage=dict(path='Ki-todos-antes-despues.mp4',sha256=sha(OUT/'Ki-todos-antes-despues.mp4')),slow_exit=dict(path='Salida-ki-todos-lenta.mp4',sha256=sha(OUT/'Salida-ki-todos-lenta.mp4')),visual_user_approval='Pending for these individual aura palettes',limits=['Recorded with Genesis Plus GX v1.7.4 f27655b; normal speed, controlled idle opponent, one native charge/release/movement sequence per fighter.','Videos have no audio. Slow exit is an explicitly labelled playback at one quarter speed.','Shape and dust preserved. Palette mapping is a Mega Drive adaptation, not exact anime hex sampling.','Separate character palette/mirror and shared-effect QA reports accompany the prototype; not an exhaustive claim for all special attacks, stages or physical hardware.','Presentation G, credit, selection portraits, HUD H4 and snow stage are not integrated in this ROM.'])
(OUT/'Verificacion.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
cards=[]
for e in entries:
 cards.append(f'''<article><h2>{html.escape(e['name'].replace('-',' '))}</h2><p>{html.escape(e['color'].capitalize())} · sin rayos</p><video controls preload="none" poster="{e['screenshot']}" src="{e['comparison_video']}"></video><a href="{e['new_only_video']}">Ver sólo la versión nueva</a></article>''')
page='''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ki por personaje · validación v4</title><style>body{margin:0;background:#101723;color:#eaf1fc;font:17px/1.5 system-ui}main{max-width:1400px;margin:auto;padding:28px}h1{font-size:30px}p{max-width:960px}video{display:block;width:100%;background:#060a10;border-radius:8px}a{color:#9edaff}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(480px,1fr));gap:24px}article{background:#1c2738;padding:20px;border-radius:12px}article h2{margin:0}.note{border-left:4px solid #f6ce60;padding:14px 18px;background:#263043}.hero{margin-bottom:28px}.links{margin:16px 0 28px}@media(max-width:550px){main{padding:14px}.grid{grid-template-columns:1fr}article{padding:12px}}</style><main><h1>Ki de los once personajes · paletas para validar</h1><p>Grabaciones reales del juego: carga, suelta, retirada del aura y vuelta al movimiento. Todas las auras van sin rayos. Cell comparte dorado con los Super Saiyan.</p><p class="note">Izquierda: efecto de ki original con las paletas v1 ya aceptadas. Derecha: nuevo contorno y colores por personaje. Esta prueba todavía requiere tu valoración visual.</p><section class="hero"><h2>Todos, antes y después</h2><video controls preload="metadata" src="Ki-todos-antes-despues.mp4"></video><div class="links"><a href="Salida-ki-todos-lenta.mp4">Revisar las once salidas a cámara lenta (1/4)</a> · <a href="Verificacion.json">Registro de la prueba</a></div></section><section class="grid">'''+''.join(cards)+'''</section><p>Los vídeos no tienen audio. Emulador: Genesis Plus GX. Prueba de paletas y contorno; no contiene todavía presentación, HUD o décimo escenario nuevos.</p></main></html>'''
(OUT/'Validacion-ki.html').write_bytes(page.encode('utf-8'))
(OUT/'LEEME.txt').write_text('KI INDIVIDUAL v4 — VALIDACIÓN VISUAL\n\nAbre Validacion-ki.html para revisar los once personajes. Cada vídeo compara el efecto de ki original (con controles/colores v1) frente al nuevo. Todos sin rayos; Cell dorado como los SSJ, Ginyu lila, Recoome blanco/violeta, Piccolo/A18/Freezer blanco azulado y Krilin blanco.\n\nTambién están los vídeos nuevos sin comparación y una recopilación de las salidas al cuarto de velocidad. Son grabaciones reales; aún falta tu aprobación de estas paletas. No tienen audio.\n\nEl BIN de prueba es de4MiB y el IPS se aplica a la ROM japonesa original indicada en Verificacion.json. Fuente y pruebas se guardan en development. No contiene aún presentaciónG,crédito,selección,HUDH4 ni escenario nevado.\n',encoding='utf-8')
print('Packaged all eleven real Ki videos and offline review gallery.')

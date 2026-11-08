from pathlib import Path
import json,hashlib,shutil,zipfile,subprocess
P=Path('work/shorts-updates');R=Path('repository');O=Path('outputs/YouTube-Shorts-mejoras')
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf8',newline='\n')
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
texts='''SHORT 1 — SALTOS
Título: DBZ Buyuu Retsuden Enhanced: dos saltos para Goku #Shorts
Descripción: Salto normal más corto y salto con mayor alcance al correr. Prueba de Goku dentro del juego, a velocidad normal. Mod de Mega Drive / Genesis desarrollado en mis ratos libres con ayuda de IA.
#DragonBallZ #MegaDrive #Genesis #Romhack #Shorts

SHORT 2 — LANZAMIENTO Y ESPECIALES
Título: Lanzamiento + Kamehameha y otros remates en Mega Drive #Shorts
Descripción: Goku, Vegeta, Gohan, Piccolo, Cell y Krilin enlazan un lanzamiento con su especial. El momento importa y no todas las secuencias impiden defenderse. Juego real a velocidad normal. Mod en desarrollo con ayuda de IA.
#DragonBallZ #MegaDrive #Genesis #Romhack #Shorts

SHORT 3 — CINCO DISPAROS
Título: ¡Ráfagas de cinco disparos en DBZ Buyuu Retsuden! #Shorts
Descripción: Goku, Vegeta, Cell, A18, Krilin y Recoome lanzan cinco proyectiles con sus poses originales. Daño repartido y mismo consumo total de ki. Cinco disparos no garantizan cinco impactos. Mod de Mega Drive / Genesis en desarrollo con ayuda de IA.
#DragonBallZ #MegaDrive #Genesis #Romhack #Shorts
'''
write(O/'Titulos-y-descripciones-Shorts.txt',texts);reports=[]
for mode in ['saltos','enlaces','rafagas']:
 d=json.loads((O/f'{mode}-montaje.json').read_text(encoding='utf8'));path=O/d['file'];assert d['onlyImprovedFootage'] and not d['gameplaySpeedScaling'];assert d['sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]));v=next(x for x in probe['streams'] if x['codec_type']=='video');a=next(x for x in probe['streams'] if x['codec_type']=='audio');assert (v['width'],v['height'],v['codec_name'],a['codec_name'])==(1080,1920,'h264','aac');assert float(probe['format']['duration'])<60
 subprocess.run(['ffmpeg','-v','error','-i',str(path),'-f','null','-'],check=True)
 for clip in d['clips']:assert '/before/' not in clip['source'] and '/control/' not in clip['source']
 for f in [path,path.with_suffix('.png')]:cp(f,R/'assets/media/shorts-updates'/f.name)
 reports.append(d)
validation=dict(date='2026-11-08',romChanged=False,publishedToYouTube=False,width=1080,height=1920,aspect='9:16',onlyImprovedFootage=True,noBeforeAfterComparisons=True,fullGameAndNativeHudPreserved=True,gameplaySpeedScaling=False,audio='Native game audio with18/25ms cut fades, no added music',shorts=reports,notes=['Saltos is the separate Goku jump trial; links is the corrected throw build; barrages is the approved six-character build.','The jump clip is shown twice as a normal-speed replay; scenes are trimmed, not accelerated.','Native in-game split-screen, where present, remains part of the game; no before/after panel is used.'])
write(O/'montaje-y-versiones.json',json.dumps(validation,ensure_ascii=False,indent=2)+'\n');write(R/'evidence/shorts-updates/validation.json',json.dumps(validation,ensure_ascii=False,indent=2)+'\n');write(R/'docs/shorts-updates-textos.txt',texts)
for n in ['render.py','package.py']:cp(P/n,R/'research/shorts-updates'/n)
with zipfile.ZipFile(O/'Tres-YouTube-Shorts-mejoras.zip','w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
 for f in [*(O/d['file'] for d in reports),*(O/Path(d['file']).with_suffix('.png') for d in reports),O/'Titulos-y-descripciones-Shorts.txt',O/'montaje-y-versiones.json']:z.write(f,f.name)
print('PACKAGED SHORTS',[(d['mode'],d['seconds']) for d in reports])

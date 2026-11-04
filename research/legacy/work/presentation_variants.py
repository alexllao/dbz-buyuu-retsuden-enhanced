from pathlib import Path
import struct,json,subprocess,sys,hashlib
ROOT=Path('outputs/presentacion-variantes');ROOT.mkdir(exist_ok=True)
source=Path('work/rom/graphics-title-selection-preview.bin').read_bytes()
variants=[
 {'id':'A','label':'Anime claro','note':'Crema claro y sombras melocoton; inspirado en la referencia de Toei.','skin':{3:0x068C,5:0x08AE,9:0x0EEE,10:0x0CEE}},
 {'id':'B','label':'HDBZ calido','note':'Tono dorado calido y sombras mas marcadas, inspirado en la captura de HDBZ con aura.','skin':{3:0x046A,5:0x06AC,9:0x0CEE,10:0x08CE}},
 {'id':'C','label':'Equilibrado','note':'La ultima version aclarada: contraste moderado y piel beige melocoton.','skin':{3:0x068C,5:0x08AC,9:0x0CEE,10:0x0ACE}},
 {'id':'D','label':'Melocoton suave','note':'Piel rosada clara, luces blancas y sombras suaves.','skin':{3:0x068A,5:0x08AC,9:0x0EEE,10:0x0CCE}}
]
base_steps=json.loads(Path('work/emulator/steps-presentation.json').read_text())[:7]
for s in base_steps:s.pop('save',None);s.pop('dump_ram',None)
for variant in variants:
 rom=bytearray(source);allowed={0x18e,0x18f}
 for index,value in variant['skin'].items():
  offset=0x1ade32+2*index;struct.pack_into('>H',rom,offset,value);allowed.update([offset,offset+1])
 checksum=sum(struct.unpack('>1048320H',rom[512:]))&65535;struct.pack_into('>H',rom,0x18e,checksum)
 assert all(i in allowed for i,(a,b) in enumerate(zip(source,rom)) if a!=b)
 path=Path(f'work/rom/presentation-variant-{variant["id"]}.bin');path.write_bytes(rom)
 steps=json.loads(json.dumps(base_steps));steps[-1]['save']=str(ROOT/f'Goku-{variant["id"]}.png')
 stepsfile=Path(f'work/emulator/presentation-variant-{variant["id"]}.json');stepsfile.write_text(json.dumps(steps))
 result=subprocess.run([sys.executable,'work/emulator/check_rom.py',str(path),str(stepsfile)],capture_output=True,text=True)
 assert result.returncode==0,result.stderr
 variant['rom_sha256']=hashlib.sha256(rom).hexdigest();variant['checksum']=f'{checksum:04X}'
 print(variant['id'],variant['label'],'capturada',flush=True)
(ROOT/'Variantes.json').write_text(json.dumps({'variants':variants,'method':'Actual Genesis Plus GX captures; same input sequence/frame count, only four skin entries and checksum changed.','anime_reference':'https://www.toei-animation-usa.com/images/dragonBall/TV/dragonBallZ.jpg','hdbz_reference':'https://network.mugenguild.com/balthazar/hyperdbz/character-info.html?name=SSJ%20Goku','hdbz_image':'https://network.mugenguild.com/balthazar/hyperdbz/img/characters/ingame/ssjgoku3.png','note':'Artist interpretation, not official palette samples. References have different lighting. No variant chosen yet.'},ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'LEEME.txt').write_text('CUATRO VARIANTES DE LA PIEL DE GOKU EN LA PRESENTACION\n\nA - Anime claro: crema claro con sombras melocoton.\nB - HDBZ calido: matiz dorado y contraste mas marcado.\nC - Equilibrado: ultima version aclarada, beige melocoton.\nD - Melocoton suave: tono mas rosado y luces blancas.\n\nSon capturas reales del emulador. Solo cambian cuatro entradas de piel de la misma paleta; pelo, ropa, fondo y dibujo conservan sus datos. No se entrega una nueva ROM ni se selecciona una version por el usuario.\n\nReferencias visuales: imagen del anime publicada por Toei Animation USA y captura oficial de SSJ Goku de Team Z2. Son interpretaciones ajustadas a los tonos disponibles en Mega Drive; las capturas de referencia tienen iluminacion diferente y no son muestras de un unico color canonico. En la imagen de HDBZ, el aura contribuye a la luz dorada.\n\nAnime: https://www.toei-animation-usa.com/dragon-ball.html\nHDBZ: https://network.mugenguild.com/balthazar/hyperdbz/character-info.html?name=SSJ%20Goku\n',encoding='utf-8')

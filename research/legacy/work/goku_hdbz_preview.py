import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from extract_sprite import frame,palette,png,rgb
out=Path('outputs/goku-palette-hdbz');out.mkdir(exist_ok=True)
original=palette(0);proposal=original.copy()
edits={1:0x046A,2:0x08AC,3:0x0AEE,4:0x0246,5:0x006C,6:0x04AE,7:0x0246,8:0x0640,9:0x0420,11:0x0862,12:0x04AC,13:0x0068}
for i,v in edits.items():proposal[i]=v
assert all(v&~0xEEE==0 for v in proposal)
frames=[]
for fid in [0,1,4]:
 W,H,pix,meta=frame(0,fid)
 png(out/f'goku-{fid:02}-original.png',W,H,pix,original)
 png(out/f'goku-{fid:02}-hdbz.png',W,H,pix,proposal)
 meta['pixel_index_sha256']=hashlib.sha256(bytes(pix)).hexdigest()
 frames.append(meta)
record={'character':'Goku SSJ','status':'Propuesta visual inspirada en Hyper DBZ; no aplicada a ROM ni probada en emulador','reference':'https://network.mugenguild.com/balthazar/hyperdbz/character-info.html?name=SSJ%20Goku','reference_image':'https://network.mugenguild.com/balthazar/hyperdbz/img/characters/ingame/ssjgoku1.png','method':'Interpretacion visual de la captura publicada por Team Z2. No son valores extraidos de la paleta MUGEN.','palette_before':[f'{v:04X}' for v in original],'palette_proposal':[f'{v:04X}' for v in proposal],'frames':frames,'limitations':['Render estatico; RGB lineal aproximado.','El indice 3 aparece tanto en piel como en pelo.','Solo se cambian colores, no los indices de pixel, el dibujo, las sombras o la animacion.','Falta revisar dentro del juego, todos los movimientos, efectos y variante del segundo jugador.']}
(out/'paleta-y-referencia.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
(out/'LEEME.txt').write_text('GOKU: PROPUESTA INSPIRADA EN HYPER DRAGON BALL Z\n\nReferencia de Team Z2:\n'+record['reference']+'\nCaptura consultada: '+record['reference_image']+'\n\nSe ha tomado como guia visual el naranja dorado del traje, los azules verdosos oscuros, las sombras de piel mas apagadas y los tonos dorados del pelo. Es una interpretacion dentro de la paleta de Mega Drive; no se ha extraido la paleta del archivo de personaje MUGEN.\n\nLa comparacion muestra la misma pose, mismos indices de pixel y misma escala entera, sin filtros. Solo se sustituyen las entradas de color. El indice de transparencia se conserva. Los indices 3 de piel y pelo son compartidos.\n\nSe incluyen tres poses: IDs 0, 1 y 4. El JSON registra offsets, paleta original y propuesta y huellas de indices de pixel. La propuesta anterior v1 permanece guardada por separado.\n\nLa ROM original no se ha modificado. Esta es una vista estatica y requiere probarse en el juego. No se han cambiado fondos, efectos, controles ni otros personajes.\n',encoding='utf-8')
print('Created HDBZ-inspired previews for 3 poses.')

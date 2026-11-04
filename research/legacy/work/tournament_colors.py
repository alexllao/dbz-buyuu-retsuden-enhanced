from pathlib import Path
import json,sys,hashlib
sys.path.insert(0,str(Path(__file__).parent))
from stage_preview import render_stage,stage_palette,png_rgba
from extract_sprite import frame,rgb
out=Path('outputs/torneo-paleta-v1');out.mkdir(exist_ok=True)
original=stage_palette(0);proposal=original.copy()
edits={1:0x0248,3:0x0262,4:0x0244,5:0x0466,6:0x08AA,7:0x0688,8:0x0CA6,10:0x0468,12:0x06AC,13:0x0246,14:0x0ACC,17:0x0EEE,18:0x0CA6,19:0x0CCA,20:0x0CA8,21:0x0A84}
for idx,color in edits.items():proposal[32+idx]=color
assert all(v&~0xEEE==0 for v in proposal)
W,H,before,meta=render_stage(0,original)
_,_,after,_=render_stage(0,proposal)
png_rgba(out/'torneo-fondo-original.png',W,H,before)
png_rgba(out/'torneo-fondo-propuesta.png',W,H,after)
goku=json.loads(Path('outputs/goku-palette-hdbz/paleta-y-referencia.json').read_text(encoding='utf-8'))
gpal=[int(v,16) for v in goku['palette_proposal']]
gw,gh,indices,gmeta=frame(0,0)
def composite(pixels,x,y,width,height):
 result=[pixels[(y+dy)*W+x+dx] for dy in range(height) for dx in range(width)]
 # Same sprite, pose, palette and position on both backgrounds.
 gx=64;gy=height-16-gh
 for sy in range(gh):
  for sx in range(gw):
   idx=indices[sy*gw+sx]
   if idx:result[(gy+sy)*width+gx+sx]=(*rgb(gpal[idx]),255)
 return result
for label,pixels in [('original',before),('propuesta',after)]:
 comp=composite(pixels,96,272,320,224)
 png_rgba(out/f'torneo-con-goku-{label}.png',320,224,comp,scale=2)
report={'status':'Propuesta visual, ROM sin modificar; no es captura de emulador','scene':'Torneo de Artes Marciales','stage_id':0,'reference':'https://network.mugenguild.com/balthazar/hyperdbz/stage-info.html?name=tenkaichi%20budokai','palette_original':[f'{v:04X}' for v in original[32:54]],'palette_proposal':[f'{v:04X}' for v in proposal[32:54]],'changed_indices':edits,'source':meta,'goku_same_palette_both_images':goku['palette_proposal'],'crop':{'x':96,'y':272,'width':320,'height':224},'notes':['22 colores de escenario cargados desde 0x19E51E.','Los 10 colores compartidos de 0x9102 se conservan.','Goku usa la propuesta HDBZ elegida en ambos lados para aislar el cambio de fondo.','Interpretacion visual; no se han extraido valores RGB de HDBZ.']}
(out/'paleta-y-referencia.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
(out/'LEEME.txt').write_text('TORNEO DE ARTES MARCIALES: PROPUESTA DE COLOR\n\nReferencia de Team Z2:\n'+report['reference']+'\n\nLa reconstruccion usa los mismos graficos y mapa originales; solo cambian 16 entradas de las 22 que carga el escenario. Se conservan los otros 10 colores compartidos de la cuarta paleta. El cambio se ha inspirado visualmente en la piedra beige, las sombras tierra y la vegetacion del escenario de HDBZ; no es una copia exacta de su paleta.\n\nLa comparacion con Goku usa la misma pose, posicion y paleta HDBZ elegida en ambos lados. El encuadre es una composicion estatica para comparar el color: no una captura del juego en marcha. Los fondos completos tambien se incluyen.\n\nROM sin modificar. Falta comprobar movimiento de camara, capas, efectos, iluminacion y todos los personajes dentro del juego.\n\nCorreccion del analisis anterior: la rutina 0x90E4 copia 0x16 colores (22 decimal), no 16; 0x90F6 copia 0x0A (10 decimal), no 11. Se ha comprobado la instruccion en los bytes originales con Capstone.\n',encoding='utf-8')
print('Created tournament before/after with identical Goku overlay.')

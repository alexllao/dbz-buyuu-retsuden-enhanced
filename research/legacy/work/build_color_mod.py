from pathlib import Path
import sys,json,struct,hashlib,zipfile,html
sys.path.insert(0,str(Path(__file__).parent))
from color_plan import *
from extract_sprite import b,palette,frame,png,rgb,u16
from stage_preview import stage_palette,render_stage,png_rgba

ROOT=Path('outputs/dbz-colores-v1');IM=ROOT/'imagenes'
ROOT.mkdir(exist_ok=True);IM.mkdir(exist_ok=True)
EXPECTED='217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557'
assert hashlib.sha256(b).hexdigest()==EXPECTED
patched=bytearray(b);records=[];allowed=set()
def words(buf,offset,n):return list(struct.unpack_from('>'+str(n)+'H',buf,offset))
def change(offset,values,kind,identity):
 assert all((v&~0xEEE)==0 for v in values)
 previous=words(b,offset,len(values))
 struct.pack_into('>'+str(len(values))+'H',patched,offset,*values)
 allowed.update(range(offset,offset+2*len(values)))
 records.append({'kind':kind,'name':identity,'offset':hex(offset),'before':[f'{v:04X}' for v in previous],'after':[f'{v:04X}' for v in values]})

char_palettes=[]
for cid,name in enumerate(CHAR_NAMES):
 before=palette(cid);after=before.copy()
 for idx,v in CHAR_EDITS[cid].items():after[idx]=v
 old_alt=words(b,0x801E4+32*cid,16)
 new_alt=[after[i] if old_alt[i]==before[i] else old_alt[i] for i in range(16)]
 for idx,v in ALT_EDITS[cid].items():new_alt[idx]=v
 assert before[0]==after[0] and old_alt[0]==new_alt[0]
 assert after!=new_alt
 change(0x80064+32*cid,after,'personaje',name)
 change(0x801E4+32*cid,new_alt,'alternativa',name)
 char_palettes.append((before,after,old_alt,new_alt))

stage_palettes=[]
for sid,name in enumerate(STAGE_NAMES):
 old=stage_palette(sid);new=old.copy()
 for idx,v in STAGE_EDITS[sid].items():new[32+idx]=v
 # Tiles in separate palette banks can share the same backdrop color.
 # Preserve these equalities to avoid visible rectangles around clouds.
 equivalent={}
 for idx in range(32,54):
  if old[idx] in equivalent:new[idx]=equivalent[old[idx]]
  else:equivalent[old[idx]]=new[idx]
 for i in range(32,54):
  for j in range(32,54):
   if old[i]==old[j]:assert new[i]==new[j]
 change(0x19E51E+48*sid,new[32:54],'escenario',name)
 stage_palettes.append((old,new))

# Guard the already accepted examples against unintentional redesign.
goku=json.loads(Path('outputs/goku-palette-hdbz/paleta-y-referencia.json').read_text(encoding='utf-8'))
assert char_palettes[0][1]==[int(v,16) for v in goku['palette_proposal']]
tournament=json.loads(Path('outputs/torneo-paleta-v1/paleta-y-referencia.json').read_text(encoding='utf-8'))
assert stage_palettes[0][1][32:54]==[int(v,16) for v in tournament['palette_proposal']]

checksum=sum(struct.unpack('>'+str((len(patched)-512)//2)+'H',patched[512:]))&0xFFFF
struct.pack_into('>H',patched,0x18E,checksum);allowed.update((0x18E,0x18F))
changed=[i for i,(a,c) in enumerate(zip(b,patched)) if a!=c]
assert len(b)==len(patched)==2097152
assert all(i in allowed for i in changed)
assert b[0:0x18E]==patched[0:0x18E] and b[0x190:0x200]==patched[0x190:0x200]
assert b[0x80064+11*32:0x80064+12*32]==patched[0x80064+11*32:0x80064+12*32]
assert b[0x801E4+11*32:0x801E4+12*32]==patched[0x801E4+11*32:0x801E4+12*32]
rom_name='Buyuu_Retsuden_Colores_v1.bin'
(ROOT/rom_name).write_bytes(patched)

def ips_build(source,target):
 out=bytearray(b'PATCH');pos=0
 while pos<len(source):
  if source[pos]==target[pos]:pos+=1;continue
  start=pos
  while pos<len(source) and source[pos]!=target[pos] and pos-start<65535:pos+=1
  out.extend(start.to_bytes(3,'big'));out.extend((pos-start).to_bytes(2,'big'));out.extend(target[start:pos])
 return bytes(out)+b'EOF'
def ips_apply(source,patch):
 assert patch[:5]==b'PATCH';out=bytearray(source);pos=5
 while patch[pos:pos+3]!=b'EOF':
  off=int.from_bytes(patch[pos:pos+3],'big');length=int.from_bytes(patch[pos+3:pos+5],'big');pos+=5
  assert length>0;out[off:off+length]=patch[pos:pos+length];pos+=length
 return bytes(out)
ips=ips_build(b,patched);assert ips_apply(b,ips)==bytes(patched)
(ROOT/'Buyuu_Retsuden_Colores_v1.ips').write_bytes(ips)

poses=[]
for cid,name in enumerate(CHAR_NAMES):
 count=0
 for fid in [0,1,4,2,3,5,6]:
  if count>=3:break
  try:W,H,idx,meta=frame(cid,fid)
  except (ValueError,AssertionError):continue
  assert len(idx)==W*H and all(0<=v<16 for v in idx)
  for suffix,pal in zip(['antes','despues','alt-antes','alt-despues'],char_palettes[cid]):
   png(IM/f'personaje-{cid:02}-pose-{fid:02}-{suffix}.png',W,H,idx,pal)
  meta['name']=name;meta['pixel_index_sha256']=hashlib.sha256(bytes(idx)).hexdigest()
  poses.append(meta);count+=1
 assert count>=1,(cid,name)
 print('Personaje',cid,name,'poses',count,flush=True)

stages=[]
gw,gh,gidx,gmeta=frame(0,0);gpal=char_palettes[0][1]
for sid,name in enumerate(STAGE_NAMES):
 old,new=stage_palettes[sid]
 W,H,original,meta=render_stage(sid,old)
 _,_,modified,_=render_stage(sid,new)
 assert W==u16(0x915E+sid*2) and H==512
 cx=(W-512)//2
 for suffix,pixels in [('antes',original),('despues',modified)]:
  crop=[pixels[y*W+cx+x] for y in range(512) for x in range(512)]
  png_rgba(IM/f'escenario-{sid:02}-{suffix}.png',512,512,crop)
  png_rgba(IM/f'escenario-{sid:02}-completo-{suffix}.png',W,H,pixels)
  x=(W-320)//2;y=272
  scene=[pixels[(y+dy)*W+x+dx] for dy in range(224) for dx in range(320)]
  for sy in range(gh):
   for sx in range(gw):
    c=gidx[sy*gw+sx]
    if c:scene[(224-16-gh+sy)*320+64+sx]=(*rgb(gpal[c]),255)
  png_rgba(IM/f'escenario-{sid:02}-goku-{suffix}.png',320,224,scene,scale=2)
 meta['name']=name;stages.append(meta)
 print('Escenario',sid,name,W,H,flush=True)

report={'version':'Colores v1 - primera version de prueba','original_sha256':EXPECTED,'modified_sha256':hashlib.sha256(patched).hexdigest(),'rom_bytes':len(patched),'changed_bytes':len(changed),'checksum':f'{checksum:04X}','character_count':11,'alternate_character_count':11,'stage_count':9,'palette_records':records,'poses':poses,'stages':stages,'verification':{'ips_roundtrip':True,'only_palette_ranges_and_checksum_changed':True,'approved_goku_and_tournament_preserved':True,'unknown_slot_11_preserved':True,'emulator_tested':False},'references':['https://network.mugenguild.com/balthazar/hyperdbz/characters.html','https://network.mugenguild.com/balthazar/hyperdbz/stages.html'],'limitations':['Inspiracion visual, no copia exacta de valores RGB de HDBZ.','Trunks, Cell, Recoome y Ginyu armonizados con la direccion elegida sobre sus colores originales; no se usaron equivalentes directos del reparto HDBZ.','Colores compartidos entre distintas partes del personaje limitan los ajustes independientes.','Galeria reconstruida estaticamente desde la ROM; no son capturas del emulador.','No se han modificado la velocidad ni la respuesta de los controles.']}
(ROOT/'verificacion.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')

chars=''.join(f'''<article><h2>{html.escape(name)}</h2><p>{html.escape(CHAR_NOTES[cid])}</p><a href="imagenes/personaje-{cid:02}-comparacion.png"><img loading="lazy" src="imagenes/personaje-{cid:02}-comparacion.png" alt="{html.escape(name)} antes y despues, paleta normal y alternativa"></a><details><summary>Ver otras poses</summary><div class="poses">'''+''.join(f'<figure><img loading="lazy" src="imagenes/personaje-{cid:02}-pose-{p["frame_id"]:02}-antes.png" alt="Antes"><img loading="lazy" src="imagenes/personaje-{cid:02}-pose-{p["frame_id"]:02}-despues.png" alt="Despues"><figcaption>Pose {p["frame_id"]}: antes / despues</figcaption></figure>' for p in poses if p['character_id']==cid)+f'</div></details></article>' for cid,name in enumerate(CHAR_NAMES))
scenes=''.join(f'''<article><h2>{html.escape(name)}</h2><a href="imagenes/escenario-{sid:02}-comparacion.png"><img loading="lazy" src="imagenes/escenario-{sid:02}-comparacion.png" alt="{html.escape(name)} antes y despues"></a><p><a href="imagenes/escenario-{sid:02}-completo-antes.png">Mapa completo original</a> · <a href="imagenes/escenario-{sid:02}-completo-despues.png">Mapa completo modificado</a></p><details><summary>Ver con Goku (misma paleta en ambos lados)</summary><div class="scene-pair"><img loading="lazy" src="imagenes/escenario-{sid:02}-goku-antes.png" alt="Fondo original con Goku"><img loading="lazy" src="imagenes/escenario-{sid:02}-goku-despues.png" alt="Fondo modificado con Goku"></div><p>Composicion estatica para comparar el contraste, no una captura del juego.</p></details></article>''' for sid,name in enumerate(STAGE_NAMES))
doc='''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Buyuu Retsuden · Colores v1</title><style>*{box-sizing:border-box}body{margin:0;background:#171c24;color:#f0f2f5;font:16px/1.55 system-ui,sans-serif}main{max-width:1160px;margin:auto;padding:36px 22px}h1{font-size:36px;margin-bottom:8px}h2{margin-top:0}a{color:#8ecdd5}p{color:#c8cdd7}nav{display:flex;gap:20px;flex-wrap:wrap;margin:24px 0}article{border:1px solid #414957;background:#1e2530;border-radius:16px;padding:22px;margin:24px 0}img{max-width:100%;height:auto;image-rendering:pixelated}article>a>img{display:block;width:100%}.poses{display:flex;gap:20px;flex-wrap:wrap}figure{margin:16px 0}.poses img{max-height:300px;width:auto;margin-right:10px}figcaption,summary{color:#bac5d5}.scene-pair{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px}.pill{display:inline-block;background:#314a4c;color:#bce6d6;border-radius:20px;padding:5px 13px}details{margin:16px 0}summary{cursor:pointer}section{scroll-margin-top:20px}.button{padding:10px 16px;border-radius:8px;background:#8ecdd5;color:#142129;font-weight:600;text-decoration:none;display:inline-block}footer{margin-top:50px;color:#a9b3c4}@media(max-width:600px){h1{font-size:28px}.scene-pair{grid-template-columns:1fr}article{padding:12px}}</style><main><span class="pill">Primera version de prueba</span><h1>Dragon Ball Z · Colores v1</h1><p>11 luchadores, sus 11 paletas alternativas y 9 escenarios. Inspiracion visual en Hyper Dragon Ball Z, adaptada a los colores de Mega Drive.</p><nav><a href="#personajes">Personajes</a><a href="#escenarios">Escenarios</a><a href="#probar">Probar la ROM</a></nav><p>En cada comparacion se conserva el mismo dibujo, pose y escala. Solo cambian los colores. Las imagenes son reconstrucciones estaticas de los datos de la ROM.</p><section id="probar"><h2>Probar en tu emulador</h2><p>Abre el archivo .bin como cualquier ROM de Mega Drive. El original sigue intacto. Empieza una partida desde el arranque para que se carguen las paletas nuevas; un estado guardado antiguo puede conservar los colores anteriores.</p><p><a class="button" href="Buyuu_Retsuden_Colores_v1.bin">ROM .bin</a> <a href="Buyuu_Retsuden_Colores_v1.ips">Parche IPS</a></p><p>Se ha comprobado el checksum, el parche y que los cambios esten limitados a las tablas de color. Pendiente de validar en emulador. La velocidad y los controles conservan el comportamiento original.</p></section><section id="personajes"><h1>Personajes</h1>'''+chars+'''</section><section id="escenarios"><h1>Escenarios</h1>'''+scenes+'''</section><footer>Referencia artistica: <a href="https://network.mugenguild.com/balthazar/hyperdbz/characters.html">Team Z2 · personajes</a> y <a href="https://network.mugenguild.com/balthazar/hyperdbz/stages.html">escenarios</a>. No se han copiado sprites de HDBZ. Sus paletas no se han extraido directamente; se han interpretado visualmente. Trunks, Cell, Recoome y Ginyu se han armonizado a partir del diseno de la ROM. Los colores compartidos entre zonas del dibujo imponen limites al ajuste individual. Los nombres de escenarios son etiquetas descriptivas de esta galeria.</footer></main></html>'''
(ROOT/'Comparaciones.html').write_text(doc,encoding='utf-8')
(ROOT/'LEEME.txt').write_text('DRAGON BALL Z - BUYUU RETSUDEN: COLORES V1\n\nPrimera version de prueba: 11 personajes, 11 alternativas y 9 escenarios.\n\nPARA JUGAR\nAbre Buyuu_Retsuden_Colores_v1.bin en tu emulador de Mega Drive. Empieza desde el arranque; cargar un estado guardado antiguo puede recuperar la paleta anterior de la RAM. La ROM original no se ha modificado.\n\nPARA COMPARAR\nAbre Comparaciones.html en un navegador. Incluye el antes y despues de cada personaje y escenario, alternativas, tres poses por personaje cuando se han podido reconstruir y mapas completos de los fondos. Las comparaciones son reconstrucciones estaticas, no capturas del emulador.\n\nPARCHE\nEl IPS sirve para aplicar estos cambios a la ROM original exacta, de 2097152 bytes, SHA-256:\n'+EXPECTED+'\nNo es necesario aplicar el IPS si usas el .bin ya modificado.\n\nVALIDACION\nChecksum recalculado: '+f'{checksum:04X}'+'\n'+str(len(changed))+' bytes cambiados, exclusivamente dentro de las tablas de paleta y el campo de checksum. El parche IPS reconstruye exactamente el .bin. Las paletas elegidas de Goku y Torneo se conservan. No se ha modificado el codigo de juego, controles ni velocidad.\n\nLIMITES\nPendiente de probar en emulador: efectos, animaciones, cambios de camara y enfrentamientos espejo pueden necesitar ajustes. Inspiracion visual en Team Z2, no paletas RGB copiadas de MUGEN. Trunks, Cell, Recoome y Ginyu se han armonizado sobre el original sin equivalente directo usado de HDBZ. Los colores compartidos por diferentes partes de un personaje no se pueden editar por separado solo con estas tablas. Se conserva el slot adicional 11 de la tabla para recursos no identificados como luchadores.\n',encoding='utf-8')
print('ROM',hashlib.sha256(patched).hexdigest(),'changed bytes',len(changed),'checksum',hex(checksum),flush=True)

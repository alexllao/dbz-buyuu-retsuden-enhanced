from pathlib import Path
import json,hashlib,struct,shutil,subprocess,zipfile,csv

out=Path('outputs/dbz-jugabilidad-v1');out.mkdir(parents=True,exist_ok=True)
work=Path('work/gameplay')
original=Path('work/rom/original.bin').read_bytes();modified=Path('work/rom/controls-v1.bin').read_bytes()
build=json.loads(Path('work/controls-build.json').read_text())
assert hashlib.sha256(modified).hexdigest()==build['output_sha256']
build['status']='Emulator-tested release candidate; 11 characters in normal/turbo and combat regressions passed.'
matrix=json.loads((work/'matrix/results.json').read_text())
assert len(matrix)==22 and all(x['passed'] for x in matrix)
for mode in ['normal','turbo']:
 for cid in range(11):
  trace=json.loads((work/f'matrix/{mode}/cid{cid:02}/traces.json').read_text())
  assert trace['rom_sha256']==build['output_sha256']
old=json.loads((work/'deep-original/results.json').read_text())
new=json.loads((work/'deep-controls/results.json').read_text())
assert new['rom_sha256']==build['output_sha256']
assert all(x['p1']==y['p1'] and x['p2']==y['p2'] for x,y in zip(old['collisions'],new['collisions']))
assert len(new['queued_hit_interruptions'])>0
assert all(not x['restarts_after_hit'] for x in new['queued_hit_interruptions'])

main=out/'Buyuu_Retsuden_Jugabilidad_v1.bin';main.write_bytes(modified)
color=bytearray(Path('outputs/dbz-colores-v1/Buyuu_Retsuden_Colores_v1.bin').read_bytes())
for h in build['hooks']:
 a=int(h['offset'],16);expected=bytes.fromhex(h['original']);patched=bytes.fromhex(h['replacement'])
 assert color[a:a+len(expected)]==expected
 color[a:a+len(patched)]=patched
start,end=map(lambda s:int(s,16),build['code_range'])
assert set(color[start:end])=={255}
color[start:end]=modified[start:end]
color[0x18e:0x190]=struct.pack('>H',sum(struct.unpack('>'+str((len(color)-0x200)//2)+'H',color[0x200:]))&0xffff)
colored=out/'Buyuu_Retsuden_Jugabilidad_v1_Colores_v1.bin';colored.write_bytes(color)

# A reversible IPS against the exact original supplied by the user.
ips=bytearray(b'PATCH');i=0
while i<len(original):
 if original[i]==modified[i]:i+=1;continue
 begin=i
 while i<len(original) and original[i]!=modified[i] and i-begin<65535:i+=1
 ips+=begin.to_bytes(3,'big')+(i-begin).to_bytes(2,'big')+modified[begin:i]
ips+=b'EOF';(out/'Jugabilidad_v1_sobre_original.ips').write_bytes(ips)
restored=bytearray(original);p=5
while ips[p:p+3]!=b'EOF':
 address=int.from_bytes(ips[p:p+3],'big');size=int.from_bytes(ips[p+3:p+5],'big');p+=5
 assert size>0
 restored[address:address+size]=ips[p:p+size];p+=size
assert restored==modified
assert hashlib.sha256(Path('work/rom/original.bin').read_bytes()).hexdigest()==build['source_sha256']

verification={
 'version':'Jugabilidad v1 experimental',
 'features':{
  '1':'Ground movement stops on release, retaining a minimum movement tick for short taps.',
  '2':'One A/B edge is remembered for five subsequent input updates while a ground basic attack is recovering. Early edges expire. Queue cleared by other states and control handoff.',
  '3':'Up to two final animation ticks removed from eligible ground basic attack recovery. Positive-weight simple scripts only; current pose must match final recovery pose.',
  '4':'Two/three pose updates bridge ground walking/basic recovery back to guard using existing sprite frames. New actions cancel the visual settle immediately.'
 },
 'roms':{'original_graphics':{'path':main.name,'sha256':hashlib.sha256(modified).hexdigest()},'colors_v1':{'path':colored.name,'sha256':hashlib.sha256(color).hexdigest()}},
 'matrix':matrix,
 'combat':{'situations':len(new['collisions']),'damage_and_block_results_match_original':True,'queued_hit_interruptions_without_delayed_attack':len(new['queued_hit_interruptions']),'second_controller_checked':True,'random_play_with_cpu_checked':True},
 'native_speed_unchanged':True,
 'scope_limits':['Ground movement and basic ground attacks; air/special-move rules remain native.','Headless Genesis Plus GX testing; physical Mega Drive and other emulators not tested.','Not a complete balance validation for every matchup.','HUD and C2 aura remain mockups and are not included.','Very brief physical inputs still depend on the native pad scanning cadence.'],
 'patch_layout':build,
 'ips_roundtrip_verified':True,
 'original_preserved':True,
}
color_smoke=work/'delivered-colors-smoke/traces.json'
if color_smoke.exists():
 smoke=json.loads(color_smoke.read_text())
 assert smoke['rom_sha256']==hashlib.sha256(color).hexdigest()
 verification['colored_rom_smoke_test']='Passed actual boot, movement, basic attacks and late input tests with Goku.'
(out/'Verificacion.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2),encoding='utf-8')

readme='''DRAGON BALL Z - BUYUU RETSUDEN
JUGABILIDAD V1 - PRIMERA VERSION DE PRUEBA

ABRIR EN EL EMULADOR
Buyuu_Retsuden_Jugabilidad_v1.bin: controles nuevos y colores originales.
Buyuu_Retsuden_Jugabilidad_v1_Colores_v1.bin: los mismos controles y las paletas Colores v1 que ya habiamos preparado.
Elige uno de los dos BIN. No se aplican uno encima del otro.
Arranca el juego desde cero. No cargues un estado guardado de otra ROM.

LAS CUATRO MEJORAS
1. Parada mas inmediata al soltar la direccion en el suelo. Los toques breves conservan un minimo desplazamiento.
2. Pulsacion pendiente: durante un golpe basico en tierra se recuerda brevemente una nueva pulsacion de puno o patada. Si el personaje recupera el control a tiempo, la ejecuta. La entrada caduca en cinco actualizaciones; no repite ataques por mantener el boton.
3. Recuperacion: se recorta de forma moderada el tramo final de las secuencias simples de golpes basicos. Se mantienen la velocidad general y el turbo original.
4. Transicion visual: unas pocas poses existentes enlazan caminar o terminar un golpe con volver a guardia. Empezar otra accion cancela esa transicion para no retrasar el control.

ALCANCE DE ESTA VERSION
Los ajustes se centran en movimiento terrestre y golpes basicos. Salto, vuelo y especiales conservan sus reglas originales.
El HUD propuesto y el aura C2 todavia no estan implementados. La version con colores contiene Colores v1; las elecciones graficas de manana siguen pendientes.
Es una version para probar sensaciones; falta tu prueba con mando y una comprobacion en Mega Drive real si quieres usarla en consola.

COMPROBADO
Once personajes en normal y turbo: parada, pulsacion pendiente de puno/patada, no repeticion al mantener el boton, retorno de salto/carga y estabilidad del estado del parche.
Segundo mando, defensa y dano en 32 situaciones, interrupciones por golpes y una secuencia prolongada contra CPU. Las 32 situaciones conservan el dano del original; en 15 casos una entrada pendiente no se dispara despues de recibir dano.
Las pruebas son en Genesis Plus GX. No equivalen a comprobar todos los combos y enfrentamientos ni el retraso de un mando/television fisicos.

ARCHIVOS
Los BIN ya estan preparados para jugar. El IPS es opcional y se aplica solo a la ROM japonesa original exacta de 2 MB proporcionada, SHA-256:
'''+build['source_sha256']+'''
La ROM original se conserva sin cambios.
'''
(out/'LEEME.txt').write_text(readme,encoding='utf-8')

# Actual gameplay recordings: same inputs, original versus modified ROM.
sequence=json.loads((work/'video-controls/sequence.json').read_text());fps=sequence['fps']
font='work/gameplay/arial.ttf'
filter_parts=[
 '[0:v]crop=210:160:0:64,scale=630:480:flags=neighbor,setsar=1[a]',
 '[1:v]crop=210:160:0:64,scale=630:480:flags=neighbor,setsar=1[b]',
 '[a][b]hstack=inputs=2,pad=1260:624:0:48:color=0x171c24'+
 f",drawtext=fontfile={font}:text='ORIGINAL':fontcolor=white:fontsize=24:x=18:y=12"+
 f",drawtext=fontfile={font}:text='JUGABILIDAD V1':fontcolor=white:fontsize=24:x=648:y=12"
]
tail=filter_parts.pop()
for index,scene in enumerate(sequence['scenes']):
 label=work/f'controls-scene-{index}.txt';label.write_text(f'{index+1}. '+scene['name'],encoding='utf-8')
 t0=index*120/fps;t1=(index+1)*120/fps
 tail+=f",drawtext=fontfile={font}:textfile={label.as_posix()}:fontcolor=white:fontsize=23:x=18:y=540:enable='gte(t,{t0})*lt(t,{t1})'"
 events=[];last=None
 for f,keys in enumerate(scene['schedule']):
  text=' + '.join(keys) if keys else 'SOLTADO'
  if text!=last:
   if events:events[-1]['end']=f
   events.append({'start':f,'end':120,'text':text});last=text
 for event in events:
  textpath=work/f'controls-input-{index}-{event["start"]}.txt';textpath.write_text('MANDO: '+event['text'],encoding='utf-8')
  begin=(index*120+event['start'])/fps;endtime=(index*120+event['end'])/fps
  tail+=f",drawtext=fontfile={font}:textfile={textpath.as_posix()}:fontcolor=0xFFD66B:fontsize=20:x=18:y=577:enable='gte(t,{begin})*lt(t,{endtime})'"
tail+='[v]';filter_parts.append(tail)
video=out/'Original-vs-Jugabilidad-v1.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(work/'video-original/gameplay.mp4'),'-i',str(work/'video-controls/gameplay.mp4'),'-filter_complex',';'.join(filter_parts),'-map','[v]','-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(video),'-t','6.01','-filter_complex','[0:v]fps=20,scale=840:416:flags=neighbor,split[a][b];[a]palettegen=max_colors=160[p];[b][p]paletteuse=dither=none','-loop','0',str(out/'Vista-previa-controles.gif')],check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(video),'-f','null','-'],check=True)

manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file() and p.name!='Inventario-SHA256.json'}
(out/'Inventario-SHA256.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
archive=Path('outputs/Buyuu_Retsuden_Jugabilidad_v1.zip')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for p in out.iterdir():
  if p.is_file():z.write(p,'Jugabilidad-v1/'+p.name)
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 for name,digest in manifest.items():assert hashlib.sha256(z.read('Jugabilidad-v1/'+name)).hexdigest()==digest

statepath=Path('work/project-state.json');state=json.loads(statepath.read_text(encoding='utf-8'))
state['gameplay_mod']={'version':'v1 experimental','rom':str(main),'rom_with_colors':str(colored),'archive':str(archive),'rom_sha256':build['output_sha256'],'features':verification['features'],'verification':str(out/'Verificacion.json'),'video':str(video),'scope_limits':verification['scope_limits'],'status':'Implemented and emulator-tested; ready for user playtest'}
state['remaining']=[x for x in state['remaining'] if x!='Trace control acceptance and turbo logic before implementing gameplay changes']
state['remaining'].append('User playtest Jugabilidad v1 ground-control prototype; tune timing and balance from feedback')
statepath.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'rom':str(main),'colored_rom':str(colored),'archive':str(archive),'checks':{'character_modes':len(matrix),'combat_cases':len(new['collisions']),'queued_hit_interruptions':len(new['queued_hit_interruptions'])}},ensure_ascii=False))

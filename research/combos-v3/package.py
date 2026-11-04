from pathlib import Path
import json,hashlib,shutil,struct,zipfile,sys
sys.path.insert(0,'work/deps');from capstone import *
P=Path('work/generic-combos');R=Path('repository');O=Path('outputs/combos-v3-generico');O.mkdir(parents=True,exist_ok=True)
def read(p):return p.read_text(encoding='utf8')
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf8')
def cp(s,d):d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(s,d)
def sha(b):return hashlib.sha256(b).hexdigest()
base=Path('outputs/intro-personajes-originales-v6-6/Buyuu_Retsuden_Enhanced_v6_6.bin').read_bytes();rom=(P/'candidate.bin').read_bytes();code=(P/'combos-v3.bin').read_bytes();target=sha(rom)
for n in ['matrix.json','side-regression.json','native-regression.json']:
 d=json.loads(read(P/n));assert d['passed'] and d['targetSha256' if n=='native-regression.json' else 'romSha256']==target,(n,d.get('passed'))
finishers=[]
for c in range(11):
 d=json.loads(read(P/'finishers'/str(c)/'report.json'));assert d['romSha256']==target
 r=next(r for r in d['results'] if r['summary']['mode']=='downB' and not r['summary']['charged']);assert r['summary']['committed'] and len(r['summary']['hits'])==4,(c,r['summary'])
 finishers.append({'cid':c,'cases':[{**r['summary'],'actualFinisherPrograms':[n for n in r['summary']['programs'] if n>=0x800]} for r in d['results']]})
repeat=[]
for c in [0,1,3,6,10]:
 d=json.loads(read(P/'repeat-finishers'/str(c)/'report.json'));assert d['romSha256']==target
 for r in d['results']:
  assert all(r['summary']['checks'].values()),(c,r['summary'])
  assert all(not (t['p']['combo']&32 and (t['p']['combo']&0xc8)==0x88 and not (t['p']['combo']&4)) or t['p']['program']>=0x800 for t in r['trace']),(c,'stale finisher eligibility')
 repeat.append({'cid':c,'cases':[r['summary'] for r in d['results']]})
write(P/'finisher-validation.json',json.dumps({'romSha256':target,'cases':176,'allElevenDownBConnectAfterABA':True,'jobs':finishers,'limits':['Native command token and own repertoire/requirements retained; commitment alone does not guarantee hit','Charged branch reaches only about148 Ki by native A+B; this does not validate >205 Ki Meteor conditions','No full121 matchups, corner/air/CPU/turbo combo implementation or universal infinite-combo proof']},indent=2)+'\n')
write(P/'repeat-validation.json',json.dumps({'romSha256':target,'cases':15,'passed':True,'jobs':repeat,'scope':'Repeated special motions for720frames after ABA, five attackers; no budget reset without six neutral frames, no stale finisher contact exception once native program ended','limits':['Native ordinary specials remain available after recovery; no global change to their original rules','Bounded tests only, not proof against every possible infinite']},indent=2)+'\n')
decoded=list(Cs(CS_ARCH_M68K,CS_MODE_BIG_ENDIAN|CS_MODE_M68K_000).disasm(code,0x3d0000));assert sum(i.size for i in decoded)==len(code)
anim=base.find(bytes.fromhex('4eb900020a4c'),0x7b000,0x7b400);allowed=[(0x18e,2),(0x8dcc,6),(0x11e14,6),(0x11ff8,6),(0x11ef4,6),(0x120d4,6),(anim,6),(0x3d0000,len(code))]
changed=[i for i,(a,b) in enumerate(zip(base,rom)) if a!=b];assert all(any(a<=i<a+n for a,n in allowed) for i in changed)
preserved={name:rom[a:z]==base[a:z] for name,a,z in [('nativeDamage',0x21b4e,0x21b54),('auraCode',0x7b400,0x7d000),('sideSwitch',0x3e0000,0x3e1000),('battlePalettes',0x80064,0x80064+11*32),('stagePalettes',0x19e51e,0x19e51e+9*48),('introAndTitle',0x1a6306,0x1ae000),('credits',0x3f0000,0x3f0900),('nativeAnimationData',0x1eb26,0x209dc)]};assert all(preserved.values())
write(P/'static.json',json.dumps({'targetSha256':target,'codeSha256':sha(code),'codeBytes':len(code),'decodedBytes':sum(i.size for i in decoded),'changedBytes':len(changed),'outsideAllowedChangedBytes':0,'allowedRanges':allowed,'preserved':preserved},indent=2)+'\n')
patch=(R/'patches/review-v6-6/enhanced-v6-6.ips').read_bytes();assert patch[-6:-3]==b'EOF';patch=bytearray(patch[:-6]);i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 a=i
 while i<len(rom) and rom[i]!=base[i] and i-a<65535:i+=1
 patch+=a.to_bytes(3,'big')+(i-a).to_bytes(2,'big')+rom[a:i]
patch+=b'EOF'+len(rom).to_bytes(3,'big');folder=R/'patches/combos-v3';folder.mkdir(parents=True,exist_ok=True);(folder/'experimental.ips').write_bytes(patch)
manifest={'source':{'sha256':'217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557','bytes':2097152},'baseReviewSha256':sha(base),'target':{'filename':'Buyuu_Retsuden_Enhanced_Combos_v3.bin','sha256':target,'bytes':len(rom)},'patch':{'path':'patches/combos-v3/experimental.ips','sha256':sha(patch)},'experimental':True,'defaultBuildUnchanged':'v6.6','scope':'All11 human characters, normal speed, up to3 standing A/B basics and1 native special/Meteor with original motion/conditions; native finisher damage retained; no in-ROM counter','inheritsGameplay':'patches/review-v3/manifest.json'}
write(folder/'manifest.json',json.dumps(manifest,indent=2)+'\n')
# Repair only comment encoding; assembled instructions are unchanged.
s=read(P/'combos-v3.asm');lines=[]
for line in s.splitlines():
 if line.lstrip().startswith(';'):
  try:line=line.encode('cp1252').decode('utf8')
  except (UnicodeError,LookupError):pass
 lines.append(line)
write(R/'src/gameplay/combos-v3/combos.asm','\n'.join(lines)+'\n');cp(P/'combos-v3.labels.txt',R/'src/gameplay/combos-v3/combos.labels.txt');write(R/'src/gameplay/combos-v3/combos.hex',code.hex()+'\n')
for f in ['build.json','matrix.json','side-regression.json','native-regression.json','finisher-validation.json','repeat-validation.json','static.json','video-validation.json']:cp(P/f,R/'evidence/combos-v3'/f)
for f in ['build.py','test_routes.py','test_delay.py','run_matrix_delay.py','test_finishers.py','run_finishers.py','test_repeat.py','record_demo.py','record_all.py','final_validate.py','run_side_regression.py','probe_regression.py','verify_native_regression.py','inspect_native.py','native-commands.json']:cp(P/f,R/'research/combos-v3'/f)
for f in ['Combos-v3-once-personajes.mp4','Goku-ABA-Meteor.mp4','Goku-ABA-rafaga.mp4','Comparacion-combos-v3.png']:cp(O/f,R/'assets/media/combos-v3'/f)
cp(P/'candidate.bin',O/manifest['target']['filename']);cp(folder/'experimental.ips',O/'Combos-v3.ips')
p=R/'tools/build-review.mjs';s=read(p);s=s.replace("const versions = { ","const versions = { 'combos-v3': 'combos-v3', ").replace('combos-v2|combos-v1','combos-v3|combos-v2|combos-v1').replace('combos-v1 o combos-v2.','combos-v1, combos-v2 o combos-v3.');write(p,s)
p=R/'project/decisions.json';d=json.loads(read(p));d['combosExperimentalV3']={'status':'Optional prototype implemented; manual playtest and visual approval pending','characters':'All11 human characters','speed':'Normal, ground; CPU/turbo combo changes disabled','inputs':'Mix standing A/B freely on confirmed hit; finish with own native special/Meteor motion and requirements','antiLoop':'Max3 basics and1 finisher; no reverse cancel; close exceptions when finisher program ends; reset budget only after6 consecutive neutral updates for both actors','damage':'Native finisher damage unchanged; v2 quarter-kick rule is not inherited','window':'36 eligible updates after confirmed basic hit','counter':'Not implemented in ROM; videos have no counter overlay','limitations':'Not all routes connect: original range/hurt poses retained, timings differ; bounded tests against Goku, no universal infinite proof','defaultReview':'v6.6 retained','romSha256':target,'docs':'docs/combos-v3.md'};write(p,json.dumps(d,indent=2,ensure_ascii=False)+'\n')
p=R/'README.md';s=read(p);marker='## Prueba opcional de combos v2: puños y patadas';a=s.index(marker);s=s[:a]+'''## Prueba opcional de combos v3: los once personajes

Mezcla hasta **tres básicos A/B** al acertar y remata con una técnica propia o Meteor, introduciendo su comando original. Primera prueba común para los once personajes humanos en suelo y velocidad normal. El remate cierra las ayudas de la cadena; sólo se recupera el presupuesto tras seis actualizaciones con ambos luchadores libres. Pendiente de probar con mando.

[Vídeo real de los once personajes](assets/media/combos-v3/Combos-v3-once-personajes.mp4) · [Goku A-B-A → Meteor](assets/media/combos-v3/Goku-ABA-Meteor.mp4) · [Goku A-B-A → ráfaga](assets/media/combos-v3/Goku-ABA-rafaga.mp4) · [Reglas, resultados y límites](docs/combos-v3.md). Los vídeos no llevan contador: todavía no está en la ROM.

Construcción: `pnpm build:review --rom ruta/a/original.bin --version combos-v3`. **La opción por defecto sigue siendo v6.6** y se conservan v1/v2. Se mantienen alcance, cajas, condiciones y daño nativos del remate; algunas rutas fallan por distancia o pose. Las pruebas reducen riesgos de bucles, sin demostrar que todo infinito sea imposible.

'''+s[a:]
for name in ['Goku','Gohan','Piccolo','Vegeta','Trunks','Cell','A18','Krilin','Freezer','Recoome','Ginyu']:
 marker=f'<summary>{name}: movimientos</summary>\n\n| Técnica | Combinación |\n| --- | --- |\n'
 if marker in s:s=s.replace(marker,marker+'| **Cadena común (prueba opcional Combos v3, normal)** | Hasta tres básicos de pie A/B al acertar → comando nativo de una técnica propia. [Reglas y ejemplos](docs/combos-v3.md) |\n',1)
write(p,s)
write(O/'LEEME.txt','''COMBOS V3 — PROTOTIPO OPCIONAL PARA LOS ONCE PERSONAJES
Hasta3 básicos de pie A/B al acertar y1 técnica o Meteor, con su comando y requisitos originales. Normal/humanos; no se activa para CPU, aire ni turbo. Requiere estado normal de energía, >=125 Ki y sin fatiga. No cancelar al fallar o contra guardia.
Ejemplo mirando a la derecha: A, soltar, B al conectar, soltar, A al conectar; después adelante, abajo+B para la técnica B nativa común. Goku también admite su Meteor: adelante, diagonal abajo-adelante, abajo, diagonal abajo-atrás, atrás, adelante+B. Los tiempos y alcances varían; no todos los órdenes conectan.
El remate cierra la cadena. No se cancela de vuelta a básicos. Al acabar su programa se cierran las excepciones de contacto y reacción; el presupuesto se reinicia tras6 actualizaciones consecutivas con ambos actores libres. Esto reduce bucles; no garantiza ausencia universal de infinitos.
Las técnicas y su daño siguen siendo nativos. No hereda la reducción de patadas de v2. Las reacciones de daño de pie se prolongan durante enlaces confirmados; no aumenta la espera en el suelo. Los vídeos son capturas reales sin contador, sin audio, con posición y orientación iniciales fijadas; vida/ki/acciones/temporizadores no forzados. El contador todavía no está integrado.
Construcción principal v6.6 conservada. Arrancar sin estados guardados de otras versiones. Pendiente de probar sensación/equilibrio con mando. ASM de este parche en el repositorio; el mapa completo de estudio anterior corresponde a v6.2.
SHA256: '''+target+'\n')
with zipfile.ZipFile('outputs/Buyuu-Retsuden-prueba-Combos-v3-generico.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in O.iterdir():
  if f.is_file():z.write(f,f.name)
print('PACKAGED',target)

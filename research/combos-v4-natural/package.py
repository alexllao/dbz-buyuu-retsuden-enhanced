from pathlib import Path
import hashlib,json,struct,shutil,sys,zipfile
sys.path.insert(0,'work/deps');from capstone import *
P=Path('work/natural-combos');R=Path('repository');O=Path('outputs/combos-v4-natural')
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf8')
def cp(s,d):d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(s,d)
base=Path('outputs/intro-personajes-originales-v6-6/Buyuu_Retsuden_Enhanced_v6_6.bin').read_bytes();rom=(P/'candidate.bin').read_bytes();code=(P/'combos-v4.bin').read_bytes();target=sha(rom)
for n,key in [('matrix.json','romSha256'),('side-regression.json','romSha256'),('timing-validation.json','targetSha256')]:
 d=json.loads((P/n).read_text(encoding='utf8'));assert d['passed'] and d[key]==target,n
fin=[]
for c in range(11):
 d=json.loads((P/f'finishers-single/{c}/report.json').read_text());assert d['romSha256']==target
 q=next(r for r in d['results'] if r['summary']['mode']=='downB');assert q['summary']['committed'] and len(q['summary']['hits'])==2,(c,q['summary'])
 fin.append({'cid':c,'cases':[r['summary'] for r in d['results']]})
write(P/'finisher-validation.json',json.dumps({'romSha256':target,'passed':True,'cases':22,'allElevenOneBasicAndNativeBConnect':True,'jobs':fin,'scope':'One confirmed A, completed animation, own native F-D+B or F-B-F+B; commands retain native requirements. Not all routes connect.'},indent=2)+'\n')
decoded=list(Cs(CS_ARCH_M68K,CS_MODE_BIG_ENDIAN|CS_MODE_M68K_000).disasm(code,0x3d0000));assert sum(i.size for i in decoded)==len(code)
assert bytes.fromhex('4eb900020ba0') not in code
s=(P/'combos-v4.asm').read_text(encoding='utf8');assert 'addq.w #0x08,(0x0a,A0)' not in s and 'clr.w (A0)' not in s and 'clr.b (0x5b,A0)' not in s
anim=base.find(bytes.fromhex('4eb900020a4c'),0x7b000,0x7b400);recovery=base.find(bytes.fromhex('54680006'),0x7b000,0x7b400);assert rom[recovery:recovery+4].hex()=='4e714e71'
allowed=[(0x18e,2),(0x8dcc,6),(0x11e14,6),(0x11ff8,6),(0x11ef4,6),(0x120d4,6),(anim,6),(recovery,4),(0x3d0000,len(code))];changed=[i for i,(a,b) in enumerate(zip(base,rom)) if a!=b];assert all(any(a<=i<a+n for a,n in allowed) for i in changed)
preserved={name:rom[a:z]==base[a:z] for name,a,z in [('nativeDamage',0x21b4e,0x21b54),('auraCode',0x7b400,0x7d000),('sideSwitch',0x3e0000,0x3e1000),('battlePalettes',0x80064,0x80064+11*32),('stagePalettes',0x19e51e,0x19e51e+9*48),('introAndTitle',0x1a6306,0x1ae000),('credits',0x3f0000,0x3f0900),('nativeAnimationData',0x1eb26,0x209dc)]};assert all(preserved.values())
write(P/'static.json',json.dumps({'targetSha256':target,'codeSha256':sha(code),'codeBytes':len(code),'decodedBytes':sum(i.size for i in decoded),'changedBytes':len(changed),'outsideAllowedChangedBytes':0,'allowedRanges':allowed,'nativeRecoverySkipDisabledAt':hex(recovery),'preserved':preserved,'queueDoesNotResetOwnProgramActionCursor':True,'noInstantFollowupStep':True},indent=2)+'\n')
patch=(R/'patches/review-v6-6/enhanced-v6-6.ips').read_bytes();assert patch[-6:-3]==b'EOF';patch=bytearray(patch[:-6]);i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 a=i
 while i<len(rom) and rom[i]!=base[i] and i-a<65535:i+=1
 patch+=a.to_bytes(3,'big')+(i-a).to_bytes(2,'big')+rom[a:i]
patch+=b'EOF'+len(rom).to_bytes(3,'big');folder=R/'patches/combos-v4-natural';folder.mkdir(parents=True,exist_ok=True);(folder/'experimental.ips').write_bytes(patch)
manifest={'source':{'sha256':'217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557','bytes':2097152},'baseReviewSha256':sha(base),'target':{'filename':'Buyuu_Retsuden_Enhanced_Combos_v4_Natural.bin','sha256':target,'bytes':len(rom)},'patch':{'path':'patches/combos-v4-natural/experimental.ips','sha256':sha(patch)},'experimental':True,'defaultBuildUnchanged':'v6.6','scope':'Natural attack completion: queued follow-ups, no early animation cancellation, inherited2-unit recovery skip disabled, no instant8px step; human/normal/ground; up to3 basics and1 native finisher. Old routes require tuning.'};write(folder/'manifest.json',json.dumps(manifest,indent=2)+'\n')
cp(P/'combos-v4.asm',R/'src/gameplay/combos-v4-natural/combos.asm');cp(P/'combos-v4.labels.txt',R/'src/gameplay/combos-v4-natural/combos.labels.txt');write(R/'src/gameplay/combos-v4-natural/combos.hex',code.hex()+'\n')
for n in ['build.json','matrix.json','side-regression.json','timing-validation.json','finisher-validation.json','static.json','video-validation.json']:cp(P/n,R/'evidence/combos-v4-natural'/n)
for n in ['build.py','test_delay.py','run_matrix_delay.py','test_timing.py','run_timing.py','test_single_finisher.py','run_single_finishers.py','run_side_regression.py','record_long.py','run_long.py','render_long.py']:cp(P/n,R/'research/combos-v4-natural'/n)
cp(O/'Combos-v4-ritmo-natural-4min.mp4',R/'assets/media/combos-v4-natural/Combos-v4-ritmo-natural-4min.mp4')
cp(P/'candidate.bin',O/manifest['target']['filename']);cp(folder/'experimental.ips',O/'Combos-v4-natural.ips')
p=R/'tools/build-review.mjs';s=p.read_text(encoding='utf8').replace("const versions = { ","const versions = { 'combos-v4-natural': 'combos-v4-natural', ").replace('combos-v3|combos-v2','combos-v4-natural|combos-v3|combos-v2').replace('combos-v2 o combos-v3.','combos-v2, combos-v3 o combos-v4-natural.');write(p,s)
p=R/'README.md';s=p.read_text(encoding='utf8');a=s.index('## Prueba opcional de combos v3:');s=s[:a]+'''## Prueba opcional actual: Combos v4 con ritmo natural

**Cada ataque termina su animación antes del siguiente.** Se guardan las órdenes durante el contacto y se ejecutan al acabar el movimiento: se elimina el corte anticipado de v3, se restaura la recuperación final completa y se retira el paso instantáneo de seguimiento. No se acelera el vídeo ni el reloj de animación. La ampliación sigue siendo para humanos, en suelo y velocidad normal.

[**Ver vídeo largo nuevo con sonido (4 min 45 s)**](assets/media/combos-v4-natural/Combos-v4-ritmo-natural-4min.mp4) · [Reglas, comparación con el original y límites](docs/combos-v4-natural.md). Son ocho combates o fragmentos reales con dos mandos automatizados, sin contador superpuesto.

Al conservar duración, alcance y retroceso, algunas rutas de tres golpes de v3 dejan de conectar; se registran y quedan pendientes de ajustar jugando. Hay un máximo de tres básicos y una técnica asistida, sin asegurar que todo orden impacte. Se conservan v1/v2/v3 y la ROM principal v6.6. Construcción opcional: `pnpm build:review --rom ruta/a/original.bin --version combos-v4-natural`.

'''+s[a:];write(p,s)
p=R/'project/decisions.json';d=json.loads(p.read_text(encoding='utf8'));d['combosExperimentalV4Natural']={'status':'Implemented optional candidate; manual playtest and natural-feel approval pending','userPreference':'Do not accelerate movements; natural rhythm','changes':['Queue confirmed follow-up until native movement finishes','Disable inherited2-unit basic-recovery cursor advance','Remove instant8px following step'],'unchanged':['Native attack animation tables and time unit','Global normal/turbo selection','Approved graphics/auras/title/credits','Previously approved floor-hold shortening and dash inertia'],'scope':'Human ground normal only, all11 characters; max3 basics and1 own native finisher','limits':'Native range/knockback/knockdown break some old3-hit routes; tune per-character routes without accelerating, do not force hits','timingValidation':'22 original-vs-candidate A/B comparisons: same attack pose order and cursor sequence; frame-level durations include input/pauses and are recorded','romSha256':target,'docs':'docs/combos-v4-natural.md'};write(p,json.dumps(d,indent=2,ensure_ascii=False)+'\n')
write(O/'LEEME.txt','''COMBOS V4 — RITMO NATURAL
Cada ataque completa su animación antes de empezar el siguiente. La orden queda pendiente, sin cortar la animación, reiniciar su cursor ni adelantar la recuperación. Se elimina el recorte heredado de2 unidades en básicos y el salto instantáneo de8 píxeles de seguimiento. Vídeo a los FPS nativos y con audio del emulador, sin acelerar reproducción.
Se mantienen los límites de hasta3 básicos y1 técnica propia; humanos, suelo, normal. Algunas rutas de v3 dejan de conectar por duración, distancia o derribo originales. Hay que ajustarlas jugando; no se fuerzan impactos ni se garantiza ausencia universal de infinitos.
22comparaciones de animación con el original,396casos de cola/límites,374del cambio de lado y22sondeos de técnicas. Los11 personajes conectan un A y su técnica B nativa de muestra, pero no todas las combinaciones de tres básicos.
Vídeo largo: ocho combates o fragmentos de hasta36 segundos, dos mandos automatizados, sonido nativo, sin contador. Posiciones iniciales, vida, energía, acciones y temporizadores nativos; sólo las banderas de control se fijan a humano. No es una partida humana ni la IA original.
Se conservan los cambios de carrera, levantarse y gráficos acordados anteriormente. La versión principal v6.6 sigue disponible; esta prueba es independiente. Arrancar sin estados guardados anteriores.
SHA256: '''+target+'\n')
with zipfile.ZipFile('outputs/Buyuu-Retsuden-Combos-v4-natural.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in O.iterdir():
  if f.is_file():z.write(f,f.name)
print('PACKAGED',target)

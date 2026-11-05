from pathlib import Path
import json,hashlib,struct,shutil,zipfile,sys
P=Path('work/stun-break');R=Path('repository');O=Path('outputs/stun-primer-golpe-v2')
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def js(p,d):write(p,json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
base=Path('work/stun-hud/candidate.bin').read_bytes();rom=(P/'candidate.bin').read_bytes();code=(P/'hud.bin').read_bytes();added=code[478:]
assert len(added)==32 and code[:478]==Path('work/stun-hud/hud.bin').read_bytes()
changed=[i for i,(a,b) in enumerate(zip(base,rom)) if a!=b];allowed=[(0x18e,2),(0x21a0e,6),(0x3b01de,32)]
assert all(any(a<=i<a+n for a,n in allowed) for i in changed)
report=json.loads((P/'runtime-validation.json').read_text());assert report['passed'] and report['romSha256']==sha(rom)
stat=dict(sourceSha256=sha(base),targetSha256=sha(rom),outsideAllowedChangedBytes=0,changedBytes=len(changed),allowedRanges=allowed,codeSha256=sha(added),codeAddress='3B01DE',bytes=32,preserved={name:base[a:z]==rom[a:z] for name,a,z in [('hudAndSpriteHooks',0x6e00,0x720e),('hudCode',0x3b0000,0x3b01de),('hudResources',0x3b4000,0x3b5740),('controlsAndAura',0x7b000,0x7d000),('animationTiming',0x209dc,0x20ab8),('combos',0x3d0000,0x3d1000),('stagePalettes',0x19e51e,0x19e6ce),('titleAndIntro',0x1a6306,0x1ae000)]})
assert all(stat['preserved'].values());js(P/'static-validation.json',stat)
patch=bytearray((R/'patches/hud-stun-v1/hud-stun-v1.ips').read_bytes());assert patch[-6:-3]==b'EOF';patch=patch[:-6];i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 a=i
 while i<len(rom) and rom[i]!=base[i] and i-a<65535:i+=1
 patch+=a.to_bytes(3,'big')+(i-a).to_bytes(2,'big')+rom[a:i]
patch+=b'EOF'+len(rom).to_bytes(3,'big')
folder=R/'patches/stun-break-v2';folder.mkdir(parents=True,exist_ok=True);(folder/'stun-break-v2.ips').write_bytes(patch)
m=dict(source=dict(sha256=sha(Path('work/rom/original.bin').read_bytes()),bytes=2097152),baseReviewSha256=sha(base),target=dict(filename='Buyuu_Retsuden_Enhanced_Stun_Primer_Golpe_v2.bin',sha256=sha(rom),bytes=len(rom)),patch=dict(path='patches/stun-break-v2/stun-break-v2.ips',sha256=sha(patch)),experimental=True,defaultBuildUnchanged='v6.6',scope='Native HUD v1 plus exit active dizzy on first accepted unblocked impact; clear native accumulation and recovery, then retain native hit reaction. Namek palettes unchanged; proposals kept separately. HITS counter pending.')
js(folder/'manifest.json',m)
asm=(P/'hud.asm').read_text(encoding='utf-8');write(R/'src/gameplay/stun-break-v2/on-hit.asm',asm[asm.index('; Salida de aturdimiento'):]);write(R/'src/gameplay/stun-break-v2/on-hit.hex',added.hex()+'\n')
for name in ['build.json','runtime-validation.json','static-validation.json','demo-events.json']:cp(P/name,R/'evidence/stun-break-v2'/name)
cp(P/'tests/previous-3-p2-0/report.json',R/'evidence/stun-break-v2/previous-version.json')
for name in ['hud.asm','test_break.py','run_tests.py','record.py','capture_namek.py','propose_palettes.py']:cp(P/name,R/'research/stun-break-v2'/name)
cp(P/'candidate.bin',O/m['target']['filename']);cp(folder/'stun-break-v2.ips',O/'stun-break-v2.ips');cp(O/'Namek-stun-primer-golpe.mp4',R/'assets/media/stun-break-v2/Namek-stun-primer-golpe.mp4')
write(O/'LEEME.txt','STUN V2: el primer impacto aceptado y no bloqueado quita el aturdimiento activo y reinicia su acumulación. Continúa la reacción normal al daño; los golpes siguientes conservan sus reglas nativas. Las barras siguen sin texto. No se cambian los tiempos de ataque. Namek conserva su paleta anterior: las propuestas están guardadas por separado, pendientes de elección. Contador global HITS pendiente. Arrancar desde cero, sin cargar estados anteriores.\n')
with zipfile.ZipFile('outputs/Buyuu-Retsuden-Stun-primer-golpe-v2.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in O.iterdir():z.write(f,f.name)
# Preserve the visual proposals, exact palette edits and real emulator capture provenance.
proposal=json.loads((P/'namek-palettes.json').read_text());captures=[]
for stage in [6,7]:
 for tag in ['actual','propuesta']:
  d=json.loads((P/f'namek-{stage}-{tag}.json').read_text());assert d['stage']==stage;captures.append(d)
  cp(Path('outputs/namek-paletas')/d['file'],R/'assets/media/namek-anime-v1'/d['file'])
for name in ['Namek-comparacion.png','Namek-destruido-comparacion.png']:cp(Path('outputs/namek-paletas')/name,R/'assets/media/namek-anime-v1'/name)
proposal['captures']=captures;proposal['proposalNotMergedIntoGameplayRom']=True
js(R/'research/palettes/namek-anime-v1.json',proposal)
# Only color-word addresses recorded in proposal may differ from the new gameplay ROM.
nrom=(P/'namek-proposal.bin').read_bytes();nranges=[(0x18e,2),(0x19e63e,44),(0x19e66e,44)]+[(int(x['offset'],16),2) for x in proposal['changes'] if 'dynamicPhase' in x]
assert all(any(a<=i<a+n for a,n in nranges) for i,(a,b) in enumerate(zip(rom,nrom)) if a!=b)
js(R/'evidence/stun-break-v2/namek-proposal-validation.json',dict(passed=True,sourceSha256=sha(rom),proposalSha256=sha(nrom),onlyRecordedPaletteColorsAndChecksumChanged=True,pendingUserSelection=True,captures=captures))
# Build registry and durable decisions.
p=R/'tools/build-review.mjs';s=p.read_text(encoding='utf-8').replace("const versions = { ","const versions = { 'stun-break-v2': 'stun-break-v2', ").replace('[--version hud-stun-v1|','[--version stun-break-v2|hud-stun-v1|').replace('o hud-stun-v1.','hud-stun-v1 o stun-break-v2.');write(p,s)
p=R/'project/decisions.json';d=json.loads(p.read_text(encoding='utf-8'));d['stunBreakV2']=dict(status='User requested; implemented and emulator-verified',behavior='First accepted unblocked hit exits active native dizzy and resets accumulator; native damage reaction continues. Misses and idle keep dizzy running. Ordinary hits outside dizzy keep accumulating.',targetSha256=sha(rom),manifest='patches/stun-break-v2/manifest.json',tests='evidence/stun-break-v2/runtime-validation.json',globalHitsCounter='Pending');d['namekAnimeV1']=dict(status='Actual captures plus palette proposals, pending user choice',normal='Green sky, blue terrain, pink rock',destroyed='Dark red sky, orange/yellow lava, blue surviving terrain; keep native palette phase timing',record='research/palettes/namek-anime-v1.json',notInStunBreakRom=True);js(p,d)
print(sha(rom),sha(nrom))

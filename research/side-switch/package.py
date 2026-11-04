from pathlib import Path
import json,hashlib,shutil,subprocess,zipfile
p=Path('work/side-switch');repo=Path('repository');out=Path('outputs/cambio-de-lado-v6');out.mkdir(parents=True,exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
base=Path('outputs/revision-fluidez-v5-2/Buyuu_Retsuden_Enhanced_v5_2.bin').read_bytes();rom=(p/'candidate.bin').read_bytes();build=json.loads((p/'build.json').read_text());matrix=json.loads((p/'matrix.json').read_text())
assert matrix['passed'] and matrix['romSha256']==sha(rom)
allowed=[(0x18e,0x190),(0x8dcc,0x8dd2),(0x8f58,0x8f60),(0x209dc,0x209e4),(0x20a46,0x20a4c),(0x7b000,0x7b400),(0x3e0000,0x3e0000+build['sideBytes'])]
diff=[i for i,(a,b) in enumerate(zip(base,rom)) if a!=b];assert len(base)==len(rom) and all(any(a<=i<b for a,b in allowed) for i in diff)
ranges={'nativeInputHistoryAndAttackParser':(0x9170,0x9491),'characterMoveTables':(0x2216a,0x22742),'nativeSideSwitchHandler':(0x1631c,0x164ee),'nativeSideSwitchAnimation':(0x1fed5,0x1fef0),'collisionTables':(0x19e6ce,0x1a8ea2),'groundReactionA1A4A5':(0x1f39f,0x1f3cd),'approvedTitleAndCreditResources':(0x3f0000,0x3f0800)}
proof={'sourceSha256':sha(base),'targetSha256':sha(rom),'onlyAllowedRangesChanged':True,'changedBytes':len(diff),'allowedRanges':[[hex(a),hex(b)] for a,b in allowed],'preserved':{}}
for name,(a,b) in ranges.items():
 assert base[a:b]==rom[a:b],name
 proof['preserved'][name]={'start':hex(a),'endExclusive':hex(b),'sha256':sha(rom[a:b]),'unchanged':True}
(p/'static-verification.json').write_text(json.dumps(proof,indent=2))
patch=Path('repository/patches/review-v2/enhanced-v5.ips').read_bytes();assert patch[-6:-3]==b'EOF';patch=bytearray(patch[:-6]);i=0
while i<len(rom):
 if base[i]==rom[i]:i+=1;continue
 start=i;i+=1
 while i<len(rom) and base[i]!=rom[i] and i-start<65535:i+=1
 d=rom[start:i];patch.extend(start.to_bytes(3,'big')+len(d).to_bytes(2,'big')+d)
patch.extend(b'EOF'+len(rom).to_bytes(3,'big'))
(out/'Buyuu_Retsuden_Enhanced_v6.bin').write_bytes(rom);(out/'Buyuu_Retsuden_Enhanced_v6.ips').write_bytes(patch)
def copy(src,dest):
 dest=repo/dest;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
copy(out/'Buyuu_Retsuden_Enhanced_v6.ips','patches/review-v3/enhanced-v6.ips')
code={}
for key,name,addr in [('controls','controls-v3',0x7b000),('side','side',0x3e0000)]:
 copy(p/f'{name}.asm',f'src/gameplay/v3/{key}.asm');copy(p/f'{name}.labels.txt',f'src/gameplay/v3/{key}.labels.txt')
 b=(p/f'{name}.bin').read_bytes();f=repo/f'src/gameplay/v3/{key}.hex';f.write_text(b.hex()+'\n');code[key]={'path':f'src/gameplay/v3/{key}.hex','bytes':len(b),'sha256':sha(b),'address':hex(addr)}
manifest={'source':{'sha256':sha(Path('work/rom/original.bin').read_bytes()),'bytes':2097152},'baseReviewSha256':sha(base),'target':{'filename':'Buyuu_Retsuden_Enhanced_v6.bin','sha256':sha(rom),'bytes':len(rom)},'patch':{'path':'patches/review-v3/enhanced-v6.ips','sha256':sha(patch)},'code':code,'command':build['command'],'scope':build['gates'],'status':'Experimental review build, actual controller-command tests passed, user feel pending'}
(repo/'patches/review-v3/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
for file in ['matrix.json','static-verification.json','input-audit.json','build.json']:copy(p/file,'evidence/side-switch/'+file)
copy(p/'native/summary.json','evidence/side-switch/native-summary.json');copy(p/'native/pose-audit.json','evidence/side-switch/pose-audit.json')
for file in ['build.py','side.asm','controls-v3.asm','test_commands.py','run_matrix.py','record_demo.py','package.py']:copy(p/file,'research/side-switch/'+file)
copy(Path('work/scripts/AssembleSide.java'),'tools/assembly/AssembleSide.java')
playlist=[]
names=['Goku','Gohan','Piccolo','Vegeta','Trunks','Cell','A18','Krilin','Freezer','Recoome','Ginyu']
for cid,name in enumerate(names):
 src=p/'demo'/f'{cid:02}'/'Cambio-de-lado.mp4';dest=out/f'{cid:02}-{name}.mp4';shutil.copyfile(src,dest);playlist.append("file '"+dest.resolve().as_posix()+"'")
 copy(dest,'assets/media/side-switch/'+dest.name)
f=p/'demo/concat.txt';f.write_text('\n'.join(playlist)+'\n')
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(f),'-c','copy','-movflags','+faststart',str(out/'Todos-cambio-de-lado.mp4')],check=True)
copy(out/'Todos-cambio-de-lado.mp4','assets/media/side-switch/Todos-cambio-de-lado.mp4')
shutil.copyfile(p/'demo/02/F035.png',out/'Piccolo-cambio-de-lado.png');copy(out/'Piccolo-cambio-de-lado.png','assets/media/side-switch/Piccolo-cambio-de-lado.png')
(out/'Informe.json').write_text(json.dumps(manifest,indent=2));(out/'Pruebas.json').write_text(json.dumps({'matrix':matrix,'static':proof},indent=2))
(out/'LEEME.txt').write_text('ROM v6 de prueba: adelante, atrás, adelante+C por defecto; último adelante y C pueden ir juntos. Cerca del rival, sin A/B simultáneos. Disponible para11personajes y ambos mandos humanos. Mismo plano yaltura cercana; no cancela ataques ni daño; bordes nativos.\nCambio de lado sin golpe: no activaataque ni hace daño. C se consume mientras lo mantienes trasla maniobra; al soltar recupera sufunciónnormal. Combinaciones A/B originales conservadas.\nMantiene título G, ©BANDAI1994 y ALEX LLAO juntos, reposoterrestre12ticks yki v4 sinrayos.\n374casos de comando real en emulador; falta valorar sensación ybalanceconmando/hardware. Vídeos: secuencias reales con posiciones iniciales controladas, sinforzarprograma/HP, sinaudio. Arrancar desdecero; no cargar estados de otraROM.\n',encoding='utf-8')
print(json.dumps({'targetSha256':sha(rom),'cases':matrix['cases'],'onlyAllowedChanges':True,'outputs':str(out)}))

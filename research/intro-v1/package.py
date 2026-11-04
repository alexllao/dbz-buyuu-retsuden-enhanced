from pathlib import Path
import json,hashlib,shutil,subprocess,zipfile
p=Path('work/intro-consistency');repo=Path('repository');out=Path('outputs/intro-paleta-G-v6-1');out.mkdir(parents=True,exist_ok=True)
base=Path('outputs/cambio-de-lado-v6/Buyuu_Retsuden_Enhanced_v6.bin').read_bytes();rom=(p/'candidate.bin').read_bytes();sha=lambda x:hashlib.sha256(x).hexdigest();build=json.loads((p/'build.json').read_text())
before=p/'boot/Buyuu_Retsuden_Enhanced_v6';after=p/'boot/candidate';a=json.loads((before/'report.json').read_text());b=json.loads((after/'report.json').read_text())
assert [(x['frame'],x['state'],x['substate']) for x in a['samples']]==[(x['frame'],x['state'],x['substate']) for x in b['samples']]
assert (before/'F1800.png').read_bytes()==(after/'F1800.png').read_bytes()
assert (before/'F0360.png').read_bytes()==(after/'F0360.png').read_bytes()
assert rom[0x1addb4:0x1addd2]==rom[0x1ade34:0x1ade52]
ram=(after/'F0960.ram').read_bytes();rb=lambda a:ram[(a&65535)^1];rw=lambda a:rb(a)*256+rb(a+1)
assert [rw(0xe454+i*2) for i in range(1,16)]==[int.from_bytes(rom[0x1ade32+i*2:0x1ade34+i*2],'big') for i in range(1,16)]
for bank,index,value in [(1,9,0xcce),(1,11,0x68a),(1,6,0x246),(2,3,0xcce),(2,4,0x68a),(2,5,0x246)]:assert rw(0xe454+bank*32+index*2)==value
patch=Path('repository/patches/review-v3/enhanced-v6.ips').read_bytes();assert patch[-6:-3]==b'EOF';patch=bytearray(patch[:-6]);i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 start=i;i+=1
 while i<len(rom) and rom[i]!=base[i] and i-start<65535:i+=1
 data=rom[start:i];patch.extend(start.to_bytes(3,'big')+len(data).to_bytes(2,'big')+data)
patch.extend(b'EOF'+len(rom).to_bytes(3,'big'))
(out/'Buyuu_Retsuden_Enhanced_v6_1.bin').write_bytes(rom);(out/'Buyuu_Retsuden_Enhanced_v6_1.ips').write_bytes(patch)
def copy(src,dest):
 dest=repo/dest;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
copy(out/'Buyuu_Retsuden_Enhanced_v6_1.ips','patches/review-v6-1/enhanced-v6-1.ips')
manifest={'source':{'sha256':sha(Path('work/rom/original.bin').read_bytes()),'bytes':2097152},'baseReviewSha256':sha(base),'target':{'filename':'Buyuu_Retsuden_Enhanced_v6_1.bin','sha256':sha(rom),'bytes':len(rom)},'patch':{'path':'patches/review-v6-1/enhanced-v6-1.ips','sha256':sha(patch)},'scope':'Opening face palette equals approved G;6shared full-body skin entries use G light/mid/shadow;31byte differences including checksum; no code or graphics change','inheritsGameplay':'patches/review-v3/manifest.json'}
(repo/'patches/review-v6-1/manifest.json').parent.mkdir(parents=True,exist_ok=True);(repo/'patches/review-v6-1/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
copy(p/'build.json','src/palettes/intro-v1/changes.json');copy(p/'static.json','evidence/intro-v1/static-source.json')
capture=[]
for frame,name in [(720,'Cara-inicial'),(960,'Personajes-completos')]:
 for folder,label in [(before,'antes'),(after,'despues')]:
  dest=out/f'{name}-{label}.png';shutil.copyfile(folder/f'F{frame:04}.png',dest);copy(dest,'assets/media/intro-v1/'+dest.name);capture.append({'path':'assets/media/intro-v1/'+dest.name,'sha256':sha(dest.read_bytes()),'romSha256':sha(base) if label=='antes' else sha(rom),'frameFromColdBoot':frame})
 dest=out/f'{name}-comparacion.png'
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(out/f'{name}-antes.png'),'-i',str(out/f'{name}-despues.png'),'-filter_complex','[0:v][1:v]hstack=inputs=2[v]','-map','[v]','-frames:v','1','-update','1',str(dest)],check=True)
 copy(dest,'assets/media/intro-v1/'+dest.name)
validation={'sourceSha256':sha(base),'targetSha256':sha(rom),'checks':{'openingPaletteEqualsApprovedG':True,'openingBackdropEntryPreserved':rom[0x1addb2:0x1addb4]==base[0x1addb2:0x1addb4],'sharedSkinEntriesMatchApprovedGRamp':True,'laterTitleFramePixelExact':True,'segaFramePixelExact':True,'nativeSceneScheduleUnchanged':True,'onlyPaletteEntriesAndChecksumChanged':True},'scope':'Cold boot, no buttons or RAM writes, sampled through frame2160; stopped before battle state0C. No CPU autoplay. No gameplay rerun required: code and all other bytes verified unchanged.','captures':capture,'sharedPaletteLimit':'Six skin entries also shade some boots or armor; alien colors, black/white entries and sprite shapes were retained.'}
(repo/'evidence/intro-v1/validation.json').write_text(json.dumps(validation,indent=2)+'\n');(out/'Informe.json').write_text(json.dumps({'manifest':manifest,'validation':validation},indent=2))
for f in ['build.py','scan_boot.py','package.py']:copy(p/f,'research/intro-v1/'+f)
print(json.dumps({'target':manifest['target'],'checks':validation['checks']}))

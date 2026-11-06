from pathlib import Path
import json,hashlib,shutil,gzip
P=Path('work/piccolo-hits');R=Path('repository');v=json.loads((P/'version.json').read_text());folder='release-v1-0-build-'+v['buildId'];O=Path('outputs/v1.0-build-'+v['buildId']);sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf8',newline='\n')
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
rom=(P/'candidate.bin').read_bytes();base=Path('work/ki-startup/candidate.bin').read_bytes();meta=json.loads((P/'build.json').read_text());assert sha(rom)==meta['targetSha256'] and sha(base)==meta['sourceSha256']
cases=[]
for port in [1,2]:
 d=json.loads((P/f'validation-port{port}.json').read_text());assert d['passed'] and d['romSha256']==sha(rom);cases+=d['cases']
assert len(cases)==12 and all(t['maxHits']==(9 if t['mode']=='hit' else 0) for t in cases)
comparison=[]
for tag in ['before','after']:
 t=json.loads((P/f'comparison/{tag}/Piccolo Meteor.json').read_text());comparison.append(dict(build=tag,maxHits=max(x['p']['hits'] for x in t),damage=t[0]['e']['hp']-t[-1]['e']['hp']))
assert [t['maxHits'] for t in comparison]==[2,9] and all(t['damage']==43 for t in comparison)
promo=json.loads((P/'video/promo.json').read_text());assert promo['romSha256']==sha(rom) and not promo['gameplayTimeScaling'];clips=[]
for c in promo['chapters']:
 trace=json.loads((P/'video'/(c['label']+'.json')).read_text());clips.append(dict(label=c['label'],maxHits=max(t['p']['hits'] for t in trace),damage=trace[0]['e']['hp']-trace[-1]['e']['hp']))
assert [clips[i]['maxHits'] for i in [1,2,4,5,9,10]]==[6,3,8,9,13,3]
trace=json.loads((P/'video/11 cruces y meteor.json').read_text());starts=[]
for i,t in enumerate(trace):
 for k in ['p','e']:
  if t[k]['program']==0x843 and (i==0 or trace[i-1][k]['program']!=0x843):starts.append(dict(frame=i,player=k))
assert [t['player'] for t in starts]==['p','e','p'];gaps=[starts[i]['frame']-starts[i-1]['frame'] for i in [1,2]];assert all(x<=18 for x in gaps) and clips[10]['damage']==35
oldFolder='release-v1-0-build-20261106-103002';patch=bytearray((R/'patches'/oldFolder/'DBZ-Enhanced-v1.0-build-20261106-103002.ips').read_bytes());assert patch[-6:-3]==b'EOF';patch=patch[:-6];i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 start=i
 while i<len(rom) and rom[i]!=base[i] and i-start<65535:i+=1
 patch+=start.to_bytes(3,'big')+(i-start).to_bytes(2,'big')+rom[start:i]
patch+=b'EOF'+len(rom).to_bytes(3,'big');patchName='DBZ-Enhanced-v1.0-build-'+v['buildId']+'.ips';(R/'patches'/folder).mkdir(parents=True,exist_ok=True);(R/'patches'/folder/patchName).write_bytes(patch)
manifest=dict(**v,source=dict(sha256='217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557',bytes=2097152),baseReviewSha256=sha(base),target=dict(filename=v['filename'],sha256=sha(rom),bytes=len(rom)),patch=dict(path='patches/'+folder+'/'+patchName,sha256=sha(patch)),experimental=True,scope='Count seven native confirmed Piccolo Meteor contacts; preserve sound, damage, physics and prior ki startup adjustment. Faster crossovers are coordinated pad execution, not ROM animation changes.')
write(R/'patches'/folder/'manifest.json',json.dumps(manifest,indent=2)+'\n')
media=[]
for f in O.glob('*.mp4'):
 dest=R/'assets/media'/folder/f.name;cp(f,dest);media.append(dict(path=dest.relative_to(R).as_posix(),sha256=sha(f.read_bytes())))
for name in ['captura.png','Comparacion-preparacion.png']:cp(O/name,R/'assets/media'/folder/name)
summary=dict(passed=True,romSha256=sha(rom),baseRomSha256=sha(base),build=v,piccoloCases=cases,comparison=comparison,clips=clips,crossStarts=starts,crossGaps=gaps,previousCrossGaps=[40,40],romCrossAnimationChanged=False,gameplayTimeScaling=False,damageUnchanged=True,collisionDataChanged=False,stunFormulaChanged=False,kiStartupTablesUnchanged=True,promoSeconds=promo['seconds'],media=media,limitations=['Scripted emulator inputs at normal speed; physical-controller feel and original hardware not certified.','Focused Piccolo Meteor coverage, not an audit of every special.','Counter contact handler retains its existing combo-window/inactivity updates; damage and stun accumulation formulas unchanged.'])
write(P/'validation.json',json.dumps(summary,indent=2)+'\n')
for n in ['build.json','version.json','validation.json','validation-port1.json','validation-port2.json']:cp(P/n,R/'evidence'/folder/n)
write(R/'evidence'/folder/'promo.json',json.dumps(promo,indent=2)+'\n')
for f in P.glob('trace-*.json'):
 dest=R/'evidence'/folder/(f.stem+'.json.gz');dest.write_bytes(gzip.compress(f.read_bytes(),mtime=0))
(R/'evidence'/folder/'cruces-rapidos.json.gz').write_bytes(gzip.compress(json.dumps(trace,separators=(',',':')).encode(),mtime=0))
for n in ['contact.asm','contact.labels.txt','contact.listing.txt']:cp(P/n,R/'src/hud/piccolo-hits-v1'/n)
write(R/'src/hud/piccolo-hits-v1/contact.hex',(P/'contact.bin').read_bytes().hex()+'\n')
for f in P.glob('*.py'):cp(f,R/'research/piccolo-hits-v1'/f.name)
cp(P/'assemble.ps1',R/'research/piccolo-hits-v1/assemble.ps1');cp('work/scripts/AssemblePiccoloHits.java',R/'research/piccolo-hits-v1/AssemblePiccoloHits.java');cp('work/probe-fast-cross.py',R/'research/piccolo-hits-v1/probe-fast-cross.py')
cp(P/'candidate.bin',O/v['filename']);cp(R/'patches'/folder/patchName,O/patchName);write(O/'version.json',json.dumps(manifest,indent=2)+'\n');cp(P/'validation.json',O/'validation.json');print('PACKAGED',v['buildId'],sha(rom),gaps)

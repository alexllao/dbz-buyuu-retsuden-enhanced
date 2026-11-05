from pathlib import Path
import json,hashlib,shutil,zipfile,subprocess
P=Path('work/responsive-cancels-v1');R=Path('repository');O=Path('outputs/respuesta-v1');O.mkdir(parents=True,exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf8',newline='\n')
def cp(s,d):d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(s,d)
base=Path('work/hits-hud-v3/candidate.bin').read_bytes();rom=(P/'candidate.bin').read_bytes();meta=json.loads((P/'build.json').read_text())
assert sha(rom)==meta['targetSha256']
reports=[]
for cid in range(11):
 d=json.loads((P/f'runtime-after-{cid}.json').read_text());ch=d['charge'];full=d['full-charge'];
 aura=next(i for i,t in enumerate(ch[:90]) if t['aura']);movement=next(i for i,t in enumerate(ch[90:]) if t['p']['action'] in [1,2])
 assert aura<=3 and movement<=3
 assert all(t['p']['action']!=15 for t in full[10:60])
 assert all(t['magic']==211 for t in full)
 reports.append(dict(cid=cid,auraFirstFrame=aura,movementAfterRelease=movement,fullBarStops=True,comboContacts=sum(b['e']['hp']<a['e']['hp'] for a,b in zip(d['combo'],d['combo'][1:]))))
d=json.loads((P/'runtime-after-0.json').read_text());assert any(t['p']['program']==0xc04 for t in d['buffer'][75:]);assert not any(t['p']['program']==0xc04 for t in d['buffer'][:75])
expected={'kame':0xc04,'super':0xc05,'energy':0xc00,'barrage':0xc01,'kiai':0xc02,'elbow':0x800,'solar':0xc03,'flurry':0x803,'knee':0x802,'slide':0x801,'meteor':0x83e,'teleport':0x840}
for name,program in expected.items():assert any(t['p']['program']==program for t in d['command-'+name]),name
extra=json.loads((P/'extra-runtime.json').read_text());assert 'p2-mirrored-buffer' in extra
summary=dict(romSha256=sha(rom),passed=True,characters=reports,expectedGokuPrograms=expected,extra=list(extra),limits=['Normal-speed human training fixtures; no exhaustive hardware/turbo/balance validation.','Standing hit-confirm cancels only, maximum three basics and one native finisher; original hurt reactions retained.','HITS and stun known user-reported discrepancies deliberately left unchanged.','Buffers use separate F700..F70F state, not native actor118..11F. Static direct-address scan plus 11-character runtime; indexed/bulk RAM accesses not exhaustively proved absent.'])
write(P/'validation.json',json.dumps(summary,indent=2)+'\n')
# Append a delta to the existing original-ROM IPS, preserving existing resources.
patch=(R/'patches/hud-hits-v3/hud-hits-v3.ips').read_bytes();assert patch[-6:-3]==b'EOF';patch=bytearray(patch[:-6]);i=0
while i<len(rom):
 if rom[i]==base[i]:i+=1;continue
 a=i
 while i<len(rom) and rom[i]!=base[i] and i-a<65535:i+=1
 patch+=a.to_bytes(3,'big')+(i-a).to_bytes(2,'big')+rom[a:i]
patch+=b'EOF'+len(rom).to_bytes(3,'big')
folder=R/'patches/responsive-v1';folder.mkdir(parents=True,exist_ok=True);(folder/'responsive-v1.ips').write_bytes(patch)
manifest=dict(source=dict(sha256='217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557',bytes=2097152),baseReviewSha256=sha(base),target=dict(filename='Buyuu_Retsuden_Enhanced_Respuesta_v1.bin',sha256=sha(rom),bytes=len(rom)),patch=dict(path='patches/responsive-v1/responsive-v1.ips',sha256=sha(patch)),experimental=True,defaultBuildUnchanged='v6.6',scope='Faster charge start/release/full-bar stop; short charge command buffer; standing confirmed-basic recovery cancels; unlock recovered thrower before victim lands; Goku-only SF-style commands. HITS/stun preserved.')
write(folder/'manifest.json',json.dumps(manifest,indent=2)+'\n')
for n in ['responsive.asm','responsive.labels.txt']:cp(P/n,R/'src/gameplay/responsive-v1'/n)
write(R/'src/gameplay/responsive-v1/responsive.hex',(P/'responsive.bin').read_bytes().hex()+'\n')
for n in ['build.json','validation.json']:cp(P/n,R/'evidence/responsive-v1'/n)
for n in ['build.py','test-runtime.py','test-extra.py','probe-throw-detail.py','test-throw.py','record.py','package.py']:cp(P/n,R/'research/responsive-v1'/n)
cp('work/scripts/AssembleResponsive.java',R/'research/responsive-v1/AssembleResponsive.java')
cp(P/'candidate.bin',O/manifest['target']['filename']);cp(folder/'responsive-v1.ips',O/'Respuesta-v1.ips');write(O/'version.json',json.dumps(manifest,indent=2))
print('PACKAGE',sha(rom),flush=True)

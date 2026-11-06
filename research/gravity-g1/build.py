from pathlib import Path
import json,hashlib,struct
P=Path('work/gravity-probe');base=Path('work/gohan-hits/candidate.bin').read_bytes();sha=lambda b:hashlib.sha256(b).hexdigest();assert sha(base)=='f3c1bf1690bbdbf35b018ce729fcdfc72c5faa49936a36b75c06c3aa6eb57484'
labels={k:int(v,16) for k,v in (s.split('=') for s in (P/'gravity.labels.txt').read_text().splitlines())};code=(P/'gravity.bin').read_bytes();assert len(code)<4096 and set(base[0x3d6000:0x3d6000+len(code)])=={255}
for trial in [False,True]:
 rom=bytearray(base);rom[0x3d6000:0x3d6000+len(code)]=code
 assert base[0x3d3000:0x3d3006].hex()=='48e7fffe40e7';rom[0x3d3000:0x3d3006]=bytes.fromhex('4ef9')+struct.pack('>I',labels['frame_entry'])
 assert base[0x3d348a:0x3d348c].hex()=='700f';rom[0x3d348a:0x3d348c]=bytes.fromhex('7013')
 allowed=[(0x3d6000,len(code)),(0x3d3000,6),(0x3d348a,2),(0x120,96),(0x18e,2)];changes=[]
 if trial:
  assert base[0x20a90:0x20a96].hex()=='4eba004a4e71';rom[0x20a90:0x20a96]=bytes.fromhex('4eb9')+struct.pack('>I',labels['duration'])
  assert base[0x13110:0x13116].hex()=='4eb900021e9c';rom[0x13110:0x13116]=bytes.fromhex('4eb9')+struct.pack('>I',labels['vertical']);allowed += [(0x20a90,6),(0x13110,6)]
  velocity=[0]+[round((i-12)*60/11) for i in range(1,24)];encoded=bytes(0x80|abs(v) if v<=0 else v for v in velocity)
  assert base[0x16b01:0x16b19]==base[0x18af0:0x18b08] and sum(abs(v) for v in velocity if v<0)==360 and sum(velocity)==0
  for at in [0x16b01,0x18af0]:rom[at:at+24]=encoded;allowed.append((at,24))
  changes=dict(normalHeightScale='4/5',runningHeightScale='(4/5)*(16/9)',normalTimeUnit=3,runningTimeUnit=4,meteorVerticalPerUnit=velocity,meteorHeight=360,meteorTimingUnchanged=True)
 tag='gravity-g1' if trial else 'dash-fix';header='DBZ BUYUU V1.0 '+('GRAV G1' if trial else 'DASH FIX')+' 2026-11-06 14:09Z'
 for at in [0x120,0x150]:rom[at:at+48]=header.encode().ljust(48,b' ')
 struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
 assert all(any(a<=i<a+n for a,n in allowed) for i,(x,y) in enumerate(zip(base,rom)) if x!=y)
 (P/(tag+'.bin')).write_bytes(rom);(P/(tag+'-build.json')).write_text(json.dumps(dict(sourceSha256=sha(base),targetSha256=sha(rom),version='1.0',buildId='20261106-150944',variant=tag,header=header,codeBytes=len(code),allowed=allowed,changes=changes),indent=2)+'\n');print(tag,sha(rom),flush=True)

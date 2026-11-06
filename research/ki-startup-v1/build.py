from pathlib import Path
import json,hashlib,struct
P=Path('work/ki-startup');R=Path('repository');base=Path('work/responsive-v3/candidate.bin').read_bytes();rom=bytearray(base);sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(base)=='357aecc091e358ec4742e214a056e9dfc6ceb13ad76ebd7fee5eebf46b83a861'
edits=[]
for program,table,oldHeader,oldFirst,newFirst,tail in [(0xc04,0x20380,132,3,1,3),(0xc0f,0x203e4,132,7,3,4)]:
 assert int.from_bytes(base[table:table+2],'big')==oldHeader and base[table+2:table+5]==bytes([oldFirst,tail,0])
 unit=oldHeader//(oldFirst+tail);newHeader=unit*(newFirst+tail)
 rom[table:table+2]=newHeader.to_bytes(2,'big');rom[table+2]=newFirst
 edits.append(dict(program=program,table=table,beforeHeader=oldHeader,afterHeader=newHeader,beforePreparationWeight=oldFirst,afterPreparationWeight=newFirst,releaseWeight=tail,animationUnit=unit,releaseUnitUnchanged=newHeader//(newFirst+tail)==unit))
v=dict(version='1.0',buildId='20261106-103002',buildDate='2026-11-06',buildTimestamp='2026-11-06T10:30:02+01:00',timezone='Europe/Madrid',headerTitle='DBZ BUYUU ENHANCED V1.0 2026-11-06 09:30Z',filename='DBZ_Buyuu_Retsuden_Enhanced_v1.0_build_20261106-103002.bin')
for p in [0x120,0x150]:rom[p:p+48]=v['headerTitle'].encode().ljust(48,b' ')
struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
allowed=[(0x120,96),(0x18e,2),(0x20380,3),(0x203e4,3)];assert all(any(a<=i<a+n for a,n in allowed) for i,(x,y) in enumerate(zip(base,rom)) if x!=y)
(P/'candidate.bin').write_bytes(rom);(P/'version.json').write_text(json.dumps(v,indent=2)+'\n');(P/'build.json').write_text(json.dumps(dict(sourceSha256=sha(base),targetSha256=sha(rom),edits=edits,allowed=allowed),indent=2)+'\n');print(sha(rom))

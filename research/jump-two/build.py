from pathlib import Path
import json,hashlib,struct
from datetime import datetime,timezone,timedelta
P=Path('work/jump-two');base=Path('work/barrage-roster/candidate.bin').read_bytes();labels={k:int(v,16) for k,v in (s.split('=') for s in (P/'jump.labels.txt').read_text().splitlines())};code=(P/'jump.bin').read_bytes();assert len(code)<0x1800 and set(base[0x3d6000:0x3d6000+len(code)])=={255};now=datetime.now(timezone(timedelta(hours=1)));bid=now.strftime('%Y%m%d-%H%M%S');reports=[]
for variant in ['control','candidate']:
 r=bytearray(base);r[0x3d6000:0x3d6000+len(code)]=code;edits=[]
 for at,name,op in ([(0x3d3000,'frame_entry','4ef9')] if variant=='control' else [(0x3d3000,'frame_entry','4ef9'),(0x20a90,'duration','4eb9'),(0x13110,'vertical','4eb9'),(0x1a1ba,'horizontal','4eb9'),(0x1a2b0,'horizontal','4eb9')]):
  edits.append(dict(address=at,before=base[at:at+6].hex(),label=name));r[at:at+6]=bytes.fromhex(op)+struct.pack('>I',labels[name])
 r[0x3d348a:0x3d348c]=bytes.fromhex('7013');head=('DBZ V1.0 JUMP2 ' if variant=='candidate' else 'DBZ V1.0 RUN CONTROL ')+now.strftime('%Y%m%d %H%M')
 for at in [0x120,0x150]:r[at:at+48]=head.encode().ljust(48,b' ')
 struct.pack_into('>H',r,0x18e,sum(struct.unpack('>'+str((len(r)-512)//2)+'H',r[512:]))&65535)
 allowed=[(0x120,96),(0x18e,2),(0x3d6000,len(code)),(0x3d348a,2)]+[(e['address'],6) for e in edits];assert all(any(a<=i<a+n for a,n in allowed) for i,(x,y) in enumerate(zip(base,r)) if x!=y)
 (P/f'{variant}.bin').write_bytes(r);reports.append(dict(variant=variant,sha256=hashlib.sha256(r).hexdigest(),edits=edits,allowed=allowed,header=head))
(P/'build.json').write_text(json.dumps(dict(buildId=bid,sourceSha256=hashlib.sha256(base).hexdigest(),variants=reports,scope='Goku only; native dash fix in both comparison variants; K4/six barrages preserved'),indent=2));print(bid,[(x['variant'],x['sha256']) for x in reports])

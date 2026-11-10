from pathlib import Path
from datetime import datetime,timezone,timedelta
import struct,json,hashlib
P=Path('work/combo-charge-all');base=Path('work/namek-native-r10/integrated.bin').read_bytes();r=bytearray(base)
assert hashlib.sha256(base).hexdigest()=='85d7090885e83cba884ecaf161c1913feb80a118d0aa3c86f58f7945de2483cf'
catalog={}
def add(source,program,prefix=None):
 header=int.from_bytes(base[source:source+2],'big');at=source+2;weights=[]
 while base[at] and len(weights)<24:weights.append(base[at]);at+=1
 if base[at] or not weights or len(weights)<2:return
 poses=list(base[at+1:at+1+len(weights)])
 if not (0<header<256) or not any(0<w<128 for w in weights):return
 if prefix is None:
  if poses[0]>=0x4a:
   prefix=next((i for i,w in enumerate(weights) if w>=128),len(weights)-1)
  else:prefix=1
 if program in [0xc27,0xc32]:prefix=2
 if program==0xc31:prefix=5
 if program in [0xc33,0xc34,0xc35]:prefix=6
 if not prefix:return
 pre=sum(w for w in weights[:prefix] if w<128);total=sum(w for w in weights if w<128)
 if not pre or pre>=total and all(w<128 for w in weights):return
 item=dict(source=source,programs=[program],header=header,weights=weights,poses=poses,prefixPoses=prefix,prefixWeight=pre,totalWeight=total,originalPreparationTicks=(header//total)*pre)
 if source in catalog:
  assert catalog[source]['prefixWeight']==pre,(hex(source),catalog[source],item)
  catalog[source]['programs'].append(program)
 else:catalog[source]=item
for program in range(0xc00,0xc7f):
 at=0x2025c+(program-0xc00)*2;source=at+int.from_bytes(base[at:at+2],'big',signed=True)
 if 0x2035a<=source<0x20900:add(source,program)
for cid in [0,3,5,6,7,9]:add(0x3db000+cid*64+2,0x10000+cid,1)
at=0x1faae+(0x84a-0x800)*2;add(at+int.from_bytes(base[at:at+2],'big',signed=True),0x84a,2)
assert all(t['prefixPoses']<=8 and all(w<128 for w in t['weights'][:t['prefixPoses']]) for t in catalog.values())
payload=b''.join(struct.pack('>IHBB',t['source'],t['totalWeight'],t['prefixPoses'],0)+bytes(t['weights'][:t['prefixPoses']]).ljust(8,b'\0') for t in catalog.values())+bytes(16)
code=(P/'charge.bin').read_bytes();assert len(code)<0x1000 and len(payload)<0x1000
labels={k:int(v,16) for k,v in (l.split('=') for l in (P/'charge.labels.txt').read_text().splitlines())}
for at,data in [(0x3e1000,code),(0x3e3000,payload)]:assert set(base[at:at+len(data)])=={255};r[at:at+len(data)]=data
assert base[0x20a8a:0x20a96].hex()=='1019e04810194eba004a4e71',base[0x20a8a:0x20a96].hex()
r[0x20a8a:0x20a96]=bytes.fromhex('4eb9003e10004e714e714e71')
assert base[0x20a7a:0x20a80].hex()=='4eb9003df000'
r[0x20a7a:0x20a80]=bytes.fromhex('4eb9003da272')
assert base[0x11c1e:0x11c24].hex()=='424010280058'
r[0x11c1e:0x11c24]=bytes.fromhex('4ef9')+struct.pack('>I',labels['boxes'])
for at,old,label in [(0x11ef4,'4ef9003d03ae','projectile_p1'),(0x120d4,'4ef9003d03cc','projectile_p2')]:
 assert base[at:at+6].hex()==old
 r[at:at+6]=bytes.fromhex('4ef9')+struct.pack('>I',labels[label])
assert base[0x73f4:0x73fa].hex()=='4eb9003df128'
r[0x73f4:0x73fa]=bytes.fromhex('4eb9')+struct.pack('>I',labels['round_reset'])
bid=datetime.now(timezone(timedelta(hours=1))).strftime('%Y%m%d-%H%M%S');title=('DBZ V1.0 COMBO CHARGE '+bid).encode().ljust(48,b' ')
for at in [0x120,0x150]:r[at:at+48]=title
struct.pack_into('>H',r,0x18e,sum(struct.unpack('>'+str((len(r)-512)//2)+'H',r[512:]))&65535)
allowed=[(0x3e1000,len(code)),(0x3e3000,len(payload)),(0x20a8a,12),(0x20a7a,6),(0x11c1e,6),(0x11ef4,6),(0x120d4,6),(0x73f4,6),(0x120,96),(0x18e,2)]
assert all(any(a<=i<a+n for a,n in allowed) for i,(x,y) in enumerate(zip(base,r)) if x!=y)
for at,n in [(0x300000,0x30000),(0x3df000,310),(0x2025c,0x700)]:assert r[at:at+n]==base[at:at+n]
(P/'candidate.bin').write_bytes(r);(P/'catalog.json').write_text(json.dumps(list(catalog.values()),indent=2))
(P/'build.json').write_text(json.dumps(dict(buildId=bid,sourceSha256=hashlib.sha256(base).hexdigest(),targetSha256=hashlib.sha256(r).hexdigest(),codeBytes=len(code),catalogEntries=len(catalog),allowed=allowed,minimumPreparationClockTicks=dict(singlePose=3,multiPoseEach=1),originalAnimationTablesUnchanged=True,graphicsR10Unchanged=True,state='F7B0..F7B7: program, fast latch and phase. F7D0..F7EF: native hurt rectangles with CID/facing/plane tags; all reset each round.'),indent=2))
print(bid,'catalog',len(catalog),'code',len(code),hashlib.sha256(r).hexdigest())

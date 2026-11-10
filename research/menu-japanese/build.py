from pathlib import Path
from datetime import datetime,timezone,timedelta
import json,hashlib,struct
P=Path('work/menu-japanese');base=Path('work/combo-charge-all/candidate.bin').read_bytes();r=bytearray(base)
assert hashlib.sha256(base).hexdigest()=='7c35a85d50855b7b33868b8111158fc86a2cc9a57732e2bf6e7d1595af107d32'
ops=[]
def put(at,data,why):
 data=bytes(data);ops.append(dict(address=at,before=base[at:at+len(data)].hex(),after=data.hex(),reason=why));r[at:at+len(data)]=data
assert base[0x33015c:0x330166].hex()=='303c03004eb900001780'
# D0=0: glifos sin remapeo, igual que la ruta original de escenarios.
# Sustituir DMA del atlas latino propio por el cargador de texto nativo.
put(0x33015c,bytes.fromhex('42404e714eb900001fee'),'CLR.W D0; NOP; JSR 1FEE, cargador japones original')
labels=[('normal','最長老のいえ','Casa del Gran Patriarca',[0x03a0,0x04e8,0x058c,0x0060,0x0002,0x0006]),('aldea','ナメック爆発','Namek en explosión',[0x0148,0x0182,0x01e0,0x010e,0x02c8,0x02ca]),('porunga','ポルンガ','Porunga',[0x4131,0x01a0,0x01a8,0x4119])]
# 05E2 es una celda vacia original. Rellenar hasta seis caracteres borra
# el resto del nombre anterior sin variar la anchura reservada del selector.
records=[]
for i,(slug,japanese,spanish,words) in enumerate(labels):
 padded=words+[0x05e2]*(6-len(words));data=struct.pack('>7H',*padded,0xffff).ljust(0x300,b'\0')
 put(0x331000+i*0x300,data,'Texto nativo '+japanese)
 put(0x332100+i*8,bytes(range(6))+b'\xff\x00','Seis glifos con relleno vacio')
 records.append(dict(variant=slug,japanese=japanese,spanish=spanish,nativeWords=[f'{w:04X}' for w in words],paddedWords=[f'{w:04X}' for w in padded]))
bid=datetime.now(timezone(timedelta(hours=1))).strftime('%Y%m%d-%H%M%S');title=('DBZ V1.0 NAMEK JP '+bid).encode().ljust(48,b' ')
for at in [0x120,0x150]:r[at:at+48]=title
struct.pack_into('>H',r,0x18e,sum(struct.unpack('>'+str((len(r)-512)//2)+'H',r[512:]))&65535)
allowed=[(o['address'],len(bytes.fromhex(o['after']))) for o in ops]+[(0x120,96),(0x18e,2)]
assert all(any(a<=i<a+n for a,n in allowed) for i,(x,y) in enumerate(zip(base,r)) if x!=y)
for at,n in [(0x300000,0x30000),(0x3e1000,692),(0x3e3000,1776)]:assert base[at:at+n]==r[at:at+n]
(P/'candidate.bin').write_bytes(r)
(P/'build.json').write_text(json.dumps(dict(version='1.0',buildId=bid,sourceSha256=hashlib.sha256(base).hexdigest(),targetSha256=hashlib.sha256(r).hexdigest(),labels=records,operations=ops,unchanged=['Combat code including combo charge patch','All three Namek R10 resources','Original nine stage labels and original font resources'],font='Original ROM renderer 1FEE and original glyph dictionaries; mode4 composes ポ and ガ through table6A44.'),ensure_ascii=False,indent=2),encoding='utf-8')
print(bid,hashlib.sha256(r).hexdigest())

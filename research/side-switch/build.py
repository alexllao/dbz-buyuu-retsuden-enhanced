from pathlib import Path
import struct,json,hashlib
p=Path('work/side-switch');base=Path('outputs/revision-fluidez-v5-2/Buyuu_Retsuden_Enhanced_v5_2.bin').read_bytes();rom=bytearray(base)
assert hashlib.sha256(base).hexdigest()=='60427353f8538f44dedbec86811f27e33187f56b8e7c096885c11d67959e3ecc'
control=(p/'controls-v3.bin').read_bytes();side=(p/'side.bin').read_bytes()
assert len(control)<0x400 and len(side)<0x1000
assert set(rom[0x3e0000:0x3e0000+len(side)])=={255}
labels={k:int(v,16) for k,v in (l.split('=') for l in (p/'controls-v3.labels.txt').read_text().splitlines())}
rom[0x7b000:0x7b400]=b'\xff'*0x400;rom[0x7b000:0x7b000+len(control)]=control
for a,label,n in [(0x8f58,'input_entry',8),(0x209dc,'animation_entry',8),(0x20a46,'animation_exit',6)]:
 rom[a:a+n]=bytes.fromhex('4ef9')+struct.pack('>I',labels[label])+bytes.fromhex('4e71')*((n-6)//2)
assert rom[0x8dcc:0x8dd2].hex()=='4eb900011c9c'
rom[0x8dcc:0x8dd2]=bytes.fromhex('4eb9003e0000')
rom[0x3e0000:0x3e0000+len(side)]=side
struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
(p/'candidate.bin').write_bytes(rom)
meta={'sourceSha256':hashlib.sha256(base).hexdigest(),'sha256':hashlib.sha256(rom).hexdigest(),'controlBytes':len(control),'sideBytes':len(side),'hook':'0x8DCC replaces JSR11C9C; wrapper tailcalls original','sideCodeBase':'0x3E0000','latch':'actor108 bit3: C7/CF; masked validation in all v3 control helper entries','nativeMatcher':'0x92B2, full actor94..BB snapshot/restoration before deciding','command':'Forward, Back, Forward + logical C/flight; no simultaneous A or B','gates':'Human only; action0..8; same plane; dx<=96 and dy<=32; no cinematic/KO/input gate'}
(p/'build.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta))

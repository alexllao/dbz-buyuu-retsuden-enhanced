from pathlib import Path
import struct,json,hashlib
base=Path('work/stun-break/candidate.bin').read_bytes();rom=bytearray(base)
# 22 stage-specific CRAM entries. Common HUD colors and all character palettes unchanged.
pals={6:[0x0000,0x0620,0x0840,0x0a62,0x0c84,0x0ea6,0x0cae,0x0a8c,0x086a,0x0648,0x0426,0x0264,0x04a6,0x08ea,0x0640,0x0eee,0x0444,0x0264,0x04a6,0x08ea,0x0eee,0x00e0],7:[0x0000,0x0004,0x0640,0x0862,0x0a84,0x0ca6,0x068a,0x0468,0x0246,0x0024,0x0002,0x0002,0x006e,0x0028,0x00ae,0x0004,0x0000,0x0002,0x0006,0x0028,0x004a,0x006c]}
changes=[]
for stage,values in pals.items():
 a=0x19e51e+stage*48;old=[int.from_bytes(base[a+i*2:a+i*2+2],'big') for i in range(22)]
 rom[a:a+44]=struct.pack('>22H',*values);changes.append(dict(stage=stage,offset=hex(a),before=[f'{v:04X}' for v in old],after=[f'{v:04X}' for v in values]))
# Destruction stage native four environmental phases and two lava flicker records.
# Same timing and palette entry layout, only color words replaced.
for table,count in [(0x9b88,4),(0x9b92,2)]:
 for phase in range(count):
  pointer=table+phase*2; address=pointer+int.from_bytes(base[pointer:pointer+2],'big'); cursor=address+1
  while base[cursor]<128:
   index=base[cursor]//2-32
   if 0<=index<22:
    value=pals[7][index]
    if table==0x9b88:
     if index==1:value=[0x0004,0x0024,0x0002,0x0000][phase]
     elif index in range(2,11) and phase>=2:
      value=sum(max(0,((value>>shift)&14)-2)*(1<<shift) for shift in [0,4,8])
     elif index>=17 and phase>=2:
      value=sum(max(0,((value>>shift)&14)-2)*(1<<shift) for shift in [0,4,8])
    # Preserve alternate lava brightness, not a frozen-color animation.
    if table==0x9b92:
     value=({11:[0x0002,0x0024],12:[0x006e,0x008e],14:[0x00ae,0x02ce],15:[0x0004,0x0006]}[index][phase])
    old=int.from_bytes(base[cursor+1:cursor+3],'big');rom[cursor+1:cursor+3]=struct.pack('>H',value)
    changes.append(dict(dynamicPhase=phase,table=hex(table),offset=hex(cursor+1),paletteIndex=index,before=f'{old:04X}',after=f'{value:04X}'))
   cursor+=3
struct.pack_into('>H',rom,0x18e,sum(struct.unpack('>'+str((len(rom)-512)//2)+'H',rom[512:]))&65535)
Path('work/stun-break/namek-proposal.bin').write_bytes(rom)
Path('work/stun-break/namek-palettes.json').write_text(json.dumps(dict(status='Visual proposal, pending user selection',sourceSha256=hashlib.sha256(base).hexdigest(),targetSha256=hashlib.sha256(rom).hexdigest(),reference='Three user-supplied anime screenshots: green sky, blue terrain and pink rock; red-black destruction sky and warm lava',changes=changes),indent=2),encoding='utf-8')

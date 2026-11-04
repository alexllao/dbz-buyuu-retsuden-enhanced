from pathlib import Path
import struct
b=Path('work/rom/original.bin').read_bytes()
for cid in [0,3]:
 p=0x2216a+cid*2;a=p+struct.unpack_from('>h',b,p)[0];print(cid,hex(a))
 for i in range(40):
  entry=b[a+i*12:a+i*12+12]
  if entry[0]&128:break
  print(entry.hex(), 'token',hex(entry[1]),'program',hex(int.from_bytes(entry[2:4],'big')),'action',hex(entry[4]),'kind',hex(entry[5]))

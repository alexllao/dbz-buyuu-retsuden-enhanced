from pathlib import Path
import sys,struct,json
sys.path.insert(0,'work/deps');from capstone import *
b=Path('work/rom/original.bin').read_bytes();m=Cs(CS_ARCH_M68K,CS_MODE_BIG_ENDIAN|CS_MODE_M68K_000)
for a,z in [(0x2118c,0x213a6),(0x213a6,0x214a0)]:
 print('RANGE',hex(a))
 for i in m.disasm(b[a:z],a):print(f'{i.address:06X} {i.mnemonic} {i.op_str}')
allEntries={}
for cid in range(11):
 p=0x2216a+cid*2;a=p+struct.unpack_from('>h',b,p)[0];entries=[]
 for n in range(40):
  q=a+n*12;e=b[q:q+12]
  if e[0]&128:break
  entries.append({'address':q,'token':e[1],'program':int.from_bytes(e[2:4],'big'),'action':e[4],'kind':e[5],'bytes':e.hex()})
 allEntries[str(cid)]=entries;print('CID',cid,[(hex(e['token']),hex(e['program']),hex(e['action'])) for e in entries])
Path('work/generic-combos/native-commands.json').write_text(json.dumps(allEntries,indent=2)+'\n')

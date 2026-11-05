import re,sys
sys.path.insert(0,'work/deps')
from capstone import Cs,CS_ARCH_M68K,CS_MODE_BIG_ENDIAN,CS_MODE_M68K_000
dis=Cs(CS_ARCH_M68K,CS_MODE_BIG_ENDIAN|CS_MODE_M68K_000)
listings=['work/side-switch/controls-v3.listing.txt','work/auras/colors-v4/aura.listing.txt','work/native-stun-fix/combos-v5.listing.txt','work/teleport-advantage/side.listing.txt','work/hits-hud-v3/hud.listing.txt','work/responsive-cancels-v1/responsive.listing.txt']
state=set(range(0x104,0x118))|set(range(0x120,0x126));delta=0xc00
absolute={a+offset:a+offset+delta for a in [0xe75e,0xe886] for offset in state}
relocations=[];seen=set()
for file in listings:
 for line in Path(file).read_text(encoding='utf8').splitlines():
  match=re.match(r'([0-9a-f]+):\s+([0-9a-f]+)\s+(.+)',line)
  if not match or match[3].startswith('.hex'):continue
  at=int(match[1],16)
  if at in seen:continue
  seen.add(at)
  ins=next(dis.disasm(bytes(rom[at:at+12]),at,count=1),None)
  if ins is None:continue
  words=set()
  for n in re.findall(r'\$([0-9a-f]+)\(a[0-6]\)',ins.op_str):
   old=int(n,16)
   if old in state:words.add((old,old+delta))
  for n in re.findall(r'\$(?:ffff)?([ef][0-9a-f]{3})\.(?:w|l)',ins.op_str):
   old=int(n,16)
   if old in absolute:words.add((old,absolute[old]))
  if not words:continue
  original=bytes(rom[at:at+ins.size]);patched=bytearray(original)
  for old,new in words:
   locations=[i for i in range(2,len(patched)-1,2) if int.from_bytes(patched[i:i+2],'big')==old]
   assert len(locations)==1,(hex(at),ins.mnemonic,ins.op_str,hex(old),locations)
   i=locations[0];patched[i:i+2]=new.to_bytes(2,'big')
  rom[at:at+ins.size]=patched
  relocations.append(dict(address=at,bytes=ins.size,original=original.hex(),patched=patched.hex(),instruction=ins.mnemonic+' '+ins.op_str,source=file))
assert len(relocations)>100,len(relocations)
(P/'relocations.json').write_text(json.dumps(dict(delta=delta,p1='F462..F483',p2='F58A..F5AB',count=len(relocations),entries=relocations),indent=2))
print('MOD_STATE_RELOCATED',len(relocations),flush=True)

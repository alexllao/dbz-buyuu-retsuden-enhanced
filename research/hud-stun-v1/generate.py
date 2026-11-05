from pathlib import Path
P=Path('work/stun-hud')
def pack_half(p):
 return bytes(p[y*32+x]<<4|p[y*32+x+1] for tx in range(0,32,8) for y in range(4) for x in range(tx,tx+8,2))
data=bytearray()
for color in [12,8,10]:
 for fill in range(31):
  p=[0]*128
  for y in range(4):
   for x in range(32):
    if y in [0,3] and x not in [0,31]:p[y*32+x]=15
    elif y in [1,2]:p[y*32+x]=15 if x in [0,31] else color if x<=fill else 14
  data+=pack_half(p)
assert len(data)==0x1740
(P/'resources.bin').write_bytes(data)

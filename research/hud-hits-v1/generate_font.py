from pathlib import Path
import json
R=Path('repository');font=json.loads((R/'src/hud/hits-v1/glyphs.json').read_text());patterns=bytearray()
for n in range(100):
 pix=[[0]*24 for _ in range(8)];points=[];x=1
 if n:
  for word in [str(n),'HIT' if n==1 else 'HITS']:
   for i,ch in enumerate(word):
    for yy,row in enumerate(font[ch]):
     for xx,val in enumerate(row):
      if val=='1' and x+xx<24:points.append((x+xx,yy+1))
    x+=3+(1 if i<len(word)-1 else 0)
   x+=1
  for xx,yy in points:
   for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
    if 0<=xx+dx<24 and 0<=yy+dy<8:pix[yy+dy][xx+dx]=14
  for xx,yy in points:pix[yy][xx]=15
 for tile in range(3):
  for y in range(8):
   for x in range(0,8,2):patterns.append(pix[y][tile*8+x]*16+pix[y][tile*8+x+1])
assert bytes(patterns)==bytes.fromhex((R/'src/hud/hits-v1/font.hex').read_text().strip())
Path('work/hits-hud/font.bin').write_bytes(patterns)
print('9600 bytes de fuente verificados; la entrada1 no se muestra por la regla de visibilidad.')

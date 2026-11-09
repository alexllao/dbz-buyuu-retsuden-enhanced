"""Comprobar recursos que la ROM ha cargado, sin reescribir VRAM/CRAM."""
from pathlib import Path
import sys,json,hashlib
sys.argv=['verify']
setup=Path('work/namek-native-r7/record.py').read_text().split('\ntry:\n begin(0,')[0]
sys.argv=['record','normal'];exec(compile(setup,'r6-runtime-setup','exec'),globals())
T=Path('work/namek-native-r7');results=[]
def check(slug,label):
 data=snap();at=0x12425;vram=data[at:at+65536];linear=bytearray(65536);linear[0::2]=vram[1::2];linear[1::2]=vram[0::2]
 assert linear[:0x5c00]==(T/slug/'tiles.bin').read_bytes()[:0x5c00],(slug,label,'VRAM')
 p=(T/slug/'palette.bin').read_bytes();words=[int.from_bytes(p[i:i+2],'big') for i in range(0,44,2)];expected=[((v>>1)&7)|(((v>>5)&7)<<3)|(((v>>9)&7)<<6) for v in words]
 native=[int.from_bytes(data[at+65536+i*2:at+65536+i*2+2],'little') for i in range(32,54)]
 assert native==expected,(slug,label,'CRAM')
 assert rb(0xe741)==6 and rb(0xf7c0)==['normal','aldea','porunga'].index(slug)+1
 results.append(dict(variant=slug,label=label,backgroundVramExact=True,palette22WordsExact=True,stage=rb(0xe741),variantByte=rb(0xf7c0)))
try:
 for slug in ['normal','aldea','porunga']:
  restore((T/'states-final'/slug/'seed-0.state').read_bytes())
  ww(P1+0xa,300);ww(P2+0xa,580);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(8):rawtick()
  check(slug,'ground')
  for _ in range(3):rawtick(['C'])
  for _ in range(90):rawtick()
  assert st(P1)['plane'];check(slug,'flight-one')
  for _ in range(3):rawtick([],['C'])
  for _ in range(90):rawtick()
  assert st(P1)['plane'] and st(P2)['plane'];check(slug,'flight-both')
  for _ in range(3):rawtick(['C'])
  for _ in range(90):rawtick()
  for _ in range(3):rawtick([],['C'])
  for _ in range(90):rawtick()
  check(slug,'landed')
  for _ in range(90):rawtick(['A','B'])
  check(slug,'aura')
 (T/'runtime-validation.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),checks=results),indent=2))
 print('VERIFIED',len(results),'native resource checks',flush=True)
finally:core.retro_unload_game();core.retro_deinit()

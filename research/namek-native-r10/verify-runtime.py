from pathlib import Path
import sys,json,hashlib
sys.argv=['record','normal'];setup=Path('work/namek-native-r10/record.py').read_text().split('\ntry:\n begin(0,')[0]
exec(compile(setup,'r10-verify-runtime','exec'),globals())
results=[]
try:
 for slug in ['normal','aldea','porunga']:
  restore((T/'states-final-r10b'/slug/'seed-0.state').read_bytes());ww(P1+0xa,300);ww(P2+0xa,580);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(8):rawtick()
  results.append(inspect(snap(),T,slug,'ground'))
  for _ in range(3):rawtick(['C'])
  for _ in range(90):rawtick()
  assert st(P1)['plane'];results.append(inspect(snap(),T,slug,'flight-one'))
  for _ in range(3):rawtick([],['C'])
  for _ in range(90):rawtick()
  assert st(P1)['plane'] and st(P2)['plane'];results.append(inspect(snap(),T,slug,'flight-both'))
  for _ in range(3):rawtick(['C'])
  for _ in range(90):rawtick()
  for _ in range(3):rawtick([],['C'])
  for _ in range(90):rawtick()
  results.append(inspect(snap(),T,slug,'landed'))
  for _ in range(90):rawtick(['A','B'])
  results.append(inspect(snap(),T,slug,'aura'))
 (T/'runtime-validation.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),checks=results),indent=2))
 print('VERIFIED',len(results),'VRAM and full32 palette checks',flush=True)
finally:core.retro_unload_game();core.retro_deinit()

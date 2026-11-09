from pathlib import Path
import sys,json
s=Path('work/namek-simulation/record.py').read_text().split('\ntry:\n if capture_from')[0]
sys.argv=['replay'];exec(compile(s,'replay-native-setup','exec'),globals())
try:
 for label,cid,distance in [('01-vuelo',0,280),('02-goku',0,32),('03-gohan',1,32),('04-vegeta',3,32),('05-cell',5,32),('06-pantalla-partida',0,400)]:
  restore((N/(f'critical-{cid}.state' if cid in [3,5] else f'seed-{cid}.state')).read_bytes());wb(P1+0xbe,0);wb(P2+0xbe,0);ww(P1+0xa,300);ww(P2+0xa,300+distance);ww(P1+0xc,0);ww(P2+0xc,0);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(8):rawtick()
  oldrows=json.loads((root/(label+'.json')).read_text())
  for f,ref in enumerate(oldrows):
   rawtick(ref['keys1'],ref['keys2']);assert st(P1)==ref['p'] and st(P2)==ref['e'],(label,f,st(P1),ref['p'])
  print('REPLAY EXACT',label,len(oldrows),flush=True)
finally:core.retro_unload_game();core.retro_deinit()

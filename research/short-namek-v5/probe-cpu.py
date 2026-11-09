from pathlib import Path
import sys,json
sys.argv=['probe','normal']
s=Path('work/namek-native/record-promo.py').read_text().split('\ntry:\n if capture_from==1:')[0].replace('work/namek-native/','work/namek-native-v5/').replace('work/namek-native-v5/states','work/namek-native-v5/states-reviewed')
exec(compile(s,'v5-cpu-run-probe','exec'),globals())
try:
 for kind in [255,1]:
  restore((N/'seed-3.state').read_bytes());wb(P1+0xbe,kind);wb(P2+0xbe,0);ww(P1+0xa,300);ww(P2+0xa,700);ww(P1+0xc,0);ww(P2+0xc,0);wb(P1+0x59,0);wb(P2+0x59,1)
  found=[];actions=set()
  for f in range(1800):
   if rw(P2+0x24)==0:break
   before=snap();tick();a=st(P1);actions.add(a['action'])
   if a['action'] in [7,8]:
    Path('work/namek-v5-short/cpu-run-state.bin').write_bytes(before);found.append(dict(frame=f,actor=a));break
  print('CPU',kind,'actions',sorted(actions),'run',found,flush=True)
  if found:break
finally:core.retro_unload_game();core.retro_deinit()

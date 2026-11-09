from pathlib import Path
import sys,json
s=Path('work/namek-native/record-promo.py').read_text().split('\ntry:\n if capture_from==1:')[0].replace('work/namek-native/','work/namek-native-v5/').replace('work/namek-native-v5/states','work/namek-native-v5/states-reviewed').replace("root=baseDir/'work/namek-native-v5/promo'/promoSlug","root=baseDir/'work/namek-v5-short/captures'/promoSlug")
exec(compile(s,'v5-short-runtime','exec'),globals())
try:
 if promoSlug=='normal':
  restore((N/'seed-3.state').read_bytes());wb(P1+0xbe,255);wb(P2+0xbe,0);ww(P1+0xa,300);ww(P2+0xa,700);ww(P1+0xc,0);ww(P2+0xc,0);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(8):tick()
  start('01-carrera',snap(),'VEGETA / MOVIMIENTO NATIVO CPU');sim_phase='movimiento-cpu'
  for _ in range(1150):tick()
  run_frames=[t for t in rows if t['p']['action'] in [7,8]]
  assert run_frames,'CPU did not execute its native quick movement'
  summarize()
 begin(0,'02-onda-partida','KAMEHAMEHA / PANTALLA PARTIDA',400);sim_phase='onda-pantalla-partida';f,b=face();command([[b],['DOWN',b],['DOWN'],['DOWN',f],[f]],['A'],4)
 for i in range(900):
  tick()
  if i>360 and rw(P1)<0x400 and not rb(0xe73c) and not rw(0xe9c4):break
 assert any(t['scene'] or t['cinema'] for t in rows)
 assert rows[0]['e']['hp']>rows[-1]['e']['hp']
 summarize(0xc04)
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()

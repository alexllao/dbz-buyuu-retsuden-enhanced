from pathlib import Path
s=Path('work/namek-native/record-promo.py').read_text().split('\ntry:\n if capture_from==1:')[0].replace('work/namek-native/','work/namek-native-v5/').replace('work/namek-native-v5/states','work/namek-native-v5/states-reviewed')
exec(compile(s,'v5-color-recording-runtime','exec'),globals())
try:
 begin(0,'01-vuelo','TERRENO CORREGIDO / SUELO Y VUELO',280);sim_phase='vuelo'
 for a,b,n in [([],[],30),(['C'],[],3),([],[],90),([],['C'],3),([],[],90),(['RIGHT'],['RIGHT'],35),(['C'],[],3),([],[],90),([],['C'],3),([],[],90)]:
  for _ in range(n):tick(a,b)
 assert any(t['p']['plane'] for t in rows) and any(t['e']['plane'] for t in rows)
 summarize()
 begin(0,'02-goku','SIN RESTOS DE TRONCO / BASICOS Y KAMEHAMEHA');sim_phase='basicos';hits=basics();assert len(hits)==3
 for _ in range(3):tick()
 sim_phase='kamehameha';f,b=face();command([[b],['DOWN',b],['DOWN'],['DOWN',f],[f]],['A'],4)
 for _ in range(270):tick()
 summarize(0xc04)
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()

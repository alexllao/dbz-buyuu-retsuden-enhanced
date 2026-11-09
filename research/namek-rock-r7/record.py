from pathlib import Path
import sys,json,hashlib
setup=Path('work/namek-native-r6/record-promo.py').read_text().split('\ntry:\n if capture_from==1:')[0].replace('work/namek-native-r6/','work/namek-native-r7/').replace('states-q3','states-final').replace('R6 / ROM REAL','R7 / ROM REAL')
exec(compile(setup,'r7-native-record-runtime','exec'),globals())
try:
 begin(0,'01-vuelo','TEXTURA FINA / SUELO - VUELO - ATERRIZAJE',280);sim_phase='vuelo'
 for a,b,n in [([],[],30),(['C'],[],3),([],[],90),([],['C'],3),([],[],90),(['RIGHT'],['RIGHT'],35),(['C'],[],3),([],[],90),([],['C'],3),([],[],90)]:
  for _ in range(n):tick(a,b)
 assert any(t['p']['plane'] for t in rows) and any(t['e']['plane'] for t in rows)
 summarize()
 begin(0,'02-goku','TEXTURA FINA / BASICOS Y KAMEHAMEHA');sim_phase='basicos';hits=basics();assert len(hits)==3
 for _ in range(3):tick()
 sim_phase='kamehameha';f,b=face();command([[b],['DOWN',b],['DOWN'],['DOWN',f],[f]],['A'],4)
 for _ in range(270):tick()
 summarize(0xc04)
 begin(0,'06-pantalla-partida','TEXTURA FINA / KAMEHAMEHA Y PANTALLA PARTIDA',400);sim_phase='especial-pantalla-partida';f,b=face();command([[b],['DOWN',b],['DOWN'],['DOWN',f],[f]],['A'],4)
 for i in range(900):
  tick()
  if i>360 and rw(P1)<0x400 and not rb(0xe73c) and not rw(0xe9c4):break
 assert any(t['scene'] or t['cinema'] for t in rows)
 summarize(0xc04)
 (N/'capture-manifest.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),backgroundIntegrated=True,method='Direct native ROM framebuffer/audio; no background replacement',takes=[json.loads(p.read_text()) for p in sorted(root.glob('*-report.json'))]),indent=2))
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()

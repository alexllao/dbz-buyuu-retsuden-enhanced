from pathlib import Path
import sys
s=Path('work/basic-chains/record.py').read_text();a=s.index('try:\n for pattern');s=s[:a]+'''try:
 start('Gohan-lanzamiento-Masenko',setup(1))
 for _ in range(3):tick(['RIGHT','A'])
 for _ in range(180):
  if rb(P1+0x5b)<=8:break
  tick()
 for _ in range(48):tick()
 f='LEFT' if rb(P1+0x59) else 'RIGHT';b='RIGHT' if f=='LEFT' else 'LEFT'
 for k in [k for k in [[b],['DOWN',b],['DOWN'],['DOWN',f],[f],[b]] for _ in range(4)]+[[b,'A']]*4+[[]]*400:tick(k)
 finish()
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()
''';sys.argv=['record','after'];exec(compile(s,'gohan-retake','exec'),globals())

from pathlib import Path
import sys,json
mode=sys.argv[1]
s=Path('work/input-v2/record.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0]
s=s.replace("root=baseDir/'work/input-v2/video'/which", "root=baseDir/'work/input-links/video'/which")
s=s.replace("rompath='work/input-v2/candidate.bin' if which=='after' else 'work/responsive-cancels-v1/candidate.bin'", "rompath='work/input-links/candidate.bin' if which=='after' else 'work/basic-chains/candidate.bin'")
s=s.replace("if which=='after':", 'if True:').replace("('RESPUESTA V2' if which=='after' else 'RESPUESTA V1')", "('BUFFER NUEVO' if which=='after' else 'BASE ANTERIOR')")
sys.argv=['record',mode];exec(compile(s,'record-input-link','exec'),globals())
try:
 state=Path('work/throw-links/seeds/0.state').read_bytes();restore(state);ww(P1+0xa,300);ww(P2+0xa,332);wb(P1+0x59,0);wb(P2+0x59,1)
 start('AAB-Kamehameha',snap());hp=rw(P2+0x24);contacts=[]
 for f in range(120):
  k=['A'] if f<3 else []
  for i,t in enumerate(contacts[:2]):
   if t+3<=f<t+6:k=[['A','B'][i]]
  tick(k);now=rw(P2+0x24)
  if now<hp:contacts.append(f)
  hp=now
  if len(contacts)>=3:break
 for _ in range(3):tick()
 for k in [k for k in [['LEFT'],['DOWN','LEFT'],['DOWN'],['DOWN','RIGHT'],['RIGHT']] for _ in range(4)]+[['RIGHT','A']]*3+[[]]*220:tick(k)
 finish()
 (root/'chapters.json').write_text(json.dumps(chapters,indent=2))
finally:
 if captureEncoder:captureEncoder.stdin.close();captureEncoder.wait()
 if audio_file:audio_file.close()
 core.retro_unload_game();core.retro_deinit()

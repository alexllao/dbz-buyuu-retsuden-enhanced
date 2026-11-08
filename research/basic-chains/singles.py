from pathlib import Path
import sys,json
s=Path('work/basic-chains/probe.py').read_text().split('try:\n for pattern')[0];sys.argv=['probe','before'];exec(compile(s,'single-header','exec'),globals())
try:
 for distance in [32,64,80,110,150]:
  for button in ['A','B']:
   restore(Path('work/throw-links/seeds/0.state').read_bytes());ww(P1+0xa,300);ww(P2+0xa,300+distance);wb(P1+0x59,0);wb(P2+0x59,1)
   for _ in range(8):tick()
   rows=[]
   for f in range(100):tick([button] if f<3 else []);rows.append(dict(f=f,p=st(P1),e=st(P2),pose=rb(P1+4)))
   print(distance,button,sorted(set(hex(t['p']['program']) for t in rows)),sorted(set(t['pose'] for t in rows if t['p']['program']>=0x400)),rows[0]['e']['hp']-rows[-1]['e']['hp'])
   (P/f'single-{distance}-{button}.json').write_text(json.dumps(rows))
finally:core.retro_unload_game();core.retro_deinit()

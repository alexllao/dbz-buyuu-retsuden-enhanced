from pathlib import Path

import sys,json,hashlib

source=sys.argv[1];tag=sys.argv[2];sys.argv=['probe','0']

s=Path('work/hits-hud-v3/prepare.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0]

s=s.replace("romfile=BASE/'work/hits-hud-v3/candidate.bin'",'romfile=BASE/source')

exec(compile(s,'guard-camera-setup','exec'),globals())

D=BASE/'work/hits-hud-v3/guard'/tag;D.mkdir(parents=True,exist_ok=True)

try:

 for j,entry in enumerate(steps[:-1]):

  if j==11:

   for _ in range(4):tick(['DOWN'])

   for _ in range(16):tick()

  for _ in range(entry.get('frames',1)):tick([] if j==11 else entry.get('buttons',[]))

 wb(P1+0xbe,0);wb(P2+0xbe,0)

 for _ in range(300):tick()

 ww(P1+0xa,300);ww(P2+0xa,332);ww(P1+0xc,0);ww(P2+0xc,0);wb(P1+0x59,0);wb(P2+0x59,1)

 for _ in range(60):tick()

 base=snap();rows=[]

 for mode in ['idle','blocked']:

  restore(base);frames=[];state=[]

  for f in range(100):

   tick(['A'] if mode=='blocked' and f<6 else [],['RIGHT'])

   w,h,pitch,data=latest;frames.append(data);state.append(dict(f=f,p=st(P1),e=st(P2),scene=rb(0xe73c),freeze=rw(0xe9c4)))

  # Fondo estático sobre los personajes. Buscar desplazamiento de hasta4 píxeles.

  shifts=[];ref=frames[0]

  for f,data in enumerate(frames):

   best=None

   for dy in range(-4,5):

    for dx in range(-4,5):

     score=sum(data[y*pitch+80*2:y*pitch+200*2]!=ref[(y+dy)*pitch+(80+dx)*2:(y+dy)*pitch+(200+dx)*2] for y in range(70,140))

     rank=(score,abs(dx)+abs(dy),dx,dy)

     if best is None or rank<best:best=rank

   shifts.append(dict(f=f,score=best[0],dx=best[2],dy=best[3]))

  rows.append(dict(mode=mode,trace=state,backgroundShifts=shifts))

 (D/'report.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),rows=rows),indent=2))

 print(tag,[(r['mode'],[(x['f'],x['dx'],x['dy'],x['score']) for x in r['backgroundShifts'] if x['dx'] or x['dy']],[(x['f'],x['p']['action'],x['e']['action']) for x in r['trace'] if x['e']['action']==10][:3]) for r in rows],flush=True)

finally:core.retro_unload_game();core.retro_deinit()

from pathlib import Path
import sys,json
args=sys.argv[1:]
out=Path('work/gameplay-review')/args[1];out.mkdir(parents=True,exist_ok=True)
sys.argv=['probe','--native','--rom',args[0],'--out',str(out)]+args[2:]
header=Path('work/gameplay_probe.py').read_text().split('try:\n for index,step in enumerate(steps[:-1]):')[0]
header=header.replace('BASE=Path(__file__).resolve().parent.parent','BASE=Path.cwd()')
exec(compile(header,'movement-setup','exec'),globals())
def actor(base):
 return {k:v for k,v in [('action',rb(base+0x5b)),('program',rw(base)),('pose',rb(base+4)),('anim',rw(base+6)),('f40',rw(base+0x40)),('f42',rw(base+0x42)),('bd',rb(base+0xbd)),('c8',rb(base+0xc8)),('cb',rb(base+0xcb)),('x',rw(base+10)),('y',rw(base+16)),('hp',rw(base+0x24)),('held',rb(base+0x1b)),('pressed',rb(base+0x1d))]}
try:
 for index,step in enumerate(steps[:-1]):
  if index==9 and selected_character:
   for direction,count in [('DOWN',selected_character//3),('RIGHT',selected_character%3)]:
    for _ in range(count):
     for _ in range(4):tick([direction])
     for _ in range(16):tick()
  keys=step.get('buttons',[])
  if boot_turbo and index<2:keys=list(set(keys+['A','B']))
  for _ in range(step.get('frames',1)):tick(keys)
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(180):tick()
 baseline=snap();results=[]
 moving=P2 if '--port2' in args else P1
 for direction in ['LEFT','RIGHT']:
  for gap in [0,1,2,4,8,12,20]:
   restore(baseline)
   schedule=[[direction]]*3+[[]]*gap+[[direction]]*30+[[]]*25
   trace=[]
   for keys in schedule:
    tick([] if moving==P2 else keys,keys if moving==P2 else []);trace.append(actor(moving))
   results.append({'direction':direction,'gap':gap,'trace':trace})
 for direction in ['LEFT','RIGHT']:
  for hold in [15,60,120]:
   restore(baseline)
   trace=[]
   schedule=[[direction]]*3+[[]]*4+[[direction]]*hold+[[]]*40
   for keys in schedule:
    tick([] if moving==P2 else keys,keys if moving==P2 else []);trace.append(actor(moving))
   results.append({'direction':direction,'gap':4,'hold':hold,'releaseFrame':7+hold,'trace':trace})
 (out/'movement.json').write_text(json.dumps({'rom':hashlib.sha256(rom).hexdigest(),'fps':av.timing.fps,'results':results},indent=2))
 for r in results:
  t=r['trace'];print(r['direction'],r['gap'],'actions',sorted(set(x['action'] for x in t)),'programs',sorted(set(x['program'] for x in t)),'dx',t[-26]['x']-t[0]['x'],flush=True)
finally:
 core.retro_unload_game();core.retro_deinit()

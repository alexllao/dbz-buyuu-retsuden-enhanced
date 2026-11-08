from pathlib import Path
import sys,json
s=Path('work/throw-links/port2.py').read_text().split('try:\n reports=[]')[0];exec(compile(s,'p2-refine','exec'),globals())
try:
 out=[]
 for delay in [77,78,79,80]:
  for guard in [False,True]:out.append(run_case(7,Path('work/throw-links/seeds-p2/7.state').read_bytes(),delay,guard=guard))
 (P/'extras.json').write_text(json.dumps(out,indent=2));print([(x['delay'],x['guard'],x['totalDamage'],x['maxHits']) for x in out])
finally:core.retro_unload_game();core.retro_deinit()

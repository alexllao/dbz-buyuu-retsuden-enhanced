from pathlib import Path
import sys,json
s=Path('work/throw-links/audit.py').read_text().split('try:\n for cid in requested:')[0].replace("P=Path('work/throw-links')","P=Path('work/throw-links/after')").replace("'work/barrage-roster/candidate.bin'","'work/throw-links/candidate.bin'");sys.argv=['audit','0'];exec(compile(s,'throw-extras','exec'),globals())
try:
 results=[]
 for cid,delays in [(0,[120]),(7,[68,72,76,80])]:
  for delay in delays:
   for guard in ([True] if cid==0 else [False,True]):results.append(run_case(cid,Path(f'work/throw-links/seeds/{cid}.state').read_bytes(),delay,guard=guard))
 (P/'extras.json').write_text(json.dumps(results,indent=2));print([(x['cid'],x['delay'],x['guard'],x['totalDamage'],x['maxHits']) for x in results])
finally:core.retro_unload_game();core.retro_deinit()

from pathlib import Path
import sys,json
s=Path('work/basic-chains/probe.py').read_text().split('try:\n for pattern')[0].replace('work/basic-chains/candidate.bin','work/input-links/candidate.bin');sys.argv=['probe','after'];exec(compile(s,'negative-link-header','exec'),globals());report=[]
try:
 for label,distance,defense in [('guard',32,['RIGHT']),('whiff',180,[])]:
  restore(Path('work/input-links/charged.state').read_bytes());ww(P1+0xa,300);ww(P2+0xa,300+distance);wb(P1+0x59,0);wb(P2+0x59,1)
  for _ in range(8):tick()
  r=[];seq=[['A']]*3+[k for k in [['LEFT'],['DOWN','LEFT'],['DOWN'],['DOWN','RIGHT'],['RIGHT']] for _ in range(2)]+[['RIGHT','A']]*3+[[]]*180
  for k in seq:
   tick(k,defense);r.append(dict(program=rw(P1),action=rb(P1+0x5b),queue=rb(0xf72e),token=rb(P1+0xb9),enemyHp=rw(P2+0x24)))
  result=dict(label=label,specialStarted=any(t['program']==0xc04 for t in r),queueSeen=any(t['queue'] for t in r),queueExpired=r[-1]['queue']==0,damage=200-r[-1]['enemyHp'],hits=rb(P1+0xd20)&127)
  assert not result['specialStarted'] and result['queueExpired'] and result['damage']==0,result
  report.append(result)
 Path('work/input-links/negative-links.json').write_text(json.dumps(report,indent=2));print(report,flush=True)
finally:core.retro_unload_game();core.retro_deinit()

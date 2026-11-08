from pathlib import Path
import sys,json
s=Path('work/basic-chains/probe.py').read_text().split('try:\n for pattern')[0].replace('work/basic-chains/candidate.bin','work/combo-startup/candidate.bin');sys.argv=['probe','after'];exec(compile(s,'repeat-startup-header','exec'),globals());cases=[]
try:
 for cid,expected in [(1,0xc0f),(3,0xc27)]:
  restore(Path(f'work/throw-links/seeds/{cid}.state').read_bytes());ww(P1+0xa,300);ww(P2+0xa,332);wb(P1+0x59,0);wb(P2+0x59,1)
  for at in range(0xf7b0,0xf7b8):wb(at,0)
  for _ in range(8):tick()
  rows=[];contacts=[];hp=rw(P2+0x24);repeat_phase='combo'
  def step(k=()):
   global hp
   tick(k);now=rw(P2+0x24)
   if now<hp:contacts.append(len(rows))
   hp=now;rows.append(dict(phase=repeat_phase,program=rw(P1),cursor=rw(P1+6),fast=rb(0xf7b2)))
  def special():
   f='LEFT' if rb(P1+0x59) else 'RIGHT';b='RIGHT' if f=='LEFT' else 'LEFT'
   dirs=[[b],['DOWN',b],['DOWN'],['DOWN',f],[f],[b]] if cid==1 else [['DOWN'],['DOWN',b],[b],[f]]
   for k in [k for k in dirs for _ in range(4)]+[dirs[-1]+['A']]*4:step(k)
  for f in range(100):
   k=['A'] if f<3 else []
   for i,t in enumerate(contacts[:2]):
    if t+3<=f<t+6:k=[['A','B'][i]]
   step(k)
   if len(contacts)>=3:break
  for _ in range(3):step()
  special()
  for _ in range(480):step()
  repeat_phase='solo';special()
  for _ in range(300):step()
  first=[t for t in rows if t['phase']=='combo' and t['program']==expected and t['cursor']>0];second=[t for t in rows if t['phase']=='solo' and t['program']==expected and t['cursor']>0]
  assert first and any(t['fast'] for t in first) and second and not any(t['fast'] for t in second),(cid,len(first),len(second),sum(t['fast'] for t in first),sum(t['fast'] for t in second))
  cases.append(dict(cid=cid,firstFast=True,secondSoloFast=False))
 Path('work/combo-startup/repeated-cast.json').write_text(json.dumps(cases,indent=2));print(cases)
finally:core.retro_unload_game();core.retro_deinit()

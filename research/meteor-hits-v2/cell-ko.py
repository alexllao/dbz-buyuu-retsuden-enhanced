from pathlib import Path
import sys,json
s=Path('work/gravity-probe/baseline.py').read_text().split('try:\n for j,entry')[0].replace("rompath='work/gohan-hits/candidate.bin' if which=='after' else 'work/gohan-hits/candidate.bin'","rompath='work/meteor-hits/candidate.bin'");sys.argv=['probe','after','5'];exec(compile(s,'cell-counter-audit','exec'),globals());report=[];P=Path('work/meteor-hits')
try:
 restore(Path('work/piccolo-hits/routes/5/low-hp.state').read_bytes());ww(P1+0xa,300);ww(P2+0xa,332);wb(P1+0x59,0);wb(P2+0x59,1)
 for _ in range(8):tick()
 punches=0
 while rw(P2+0x24)>66 and punches<25:
  for i in range(90):tick(['A'] if i<4 else [])
  for _ in range(130):
   if abs(rw(P1+0xa)-rw(P2+0xa))<=30:break
   tick(['RIGHT'] if rw(P1+0xa)<rw(P2+0xa) else ['LEFT'])
  for _ in range(15):tick()
  punches+=1
 for _ in range(700):tick()
 print('NATURAL TARGET HP',rw(P2+0x24),'punches',punches,flush=True)
 (P/'cell-ko-seed.state').write_bytes(snap());prev=rw(P2+0x24);drops=[];rr=[];f='RIGHT' if rb(P1+0x59)==0 else 'LEFT';b='LEFT' if f=='RIGHT' else 'RIGHT';dirs=[['DOWN'],['DOWN',f],[f],[b]];seq=[k for k in dirs for _ in range(3)]+[dirs[-1]+['B']]*4
 for i,k in enumerate(seq+[[]]*1200):
  tick(k);now=rw(P2+0x24)
  if now<prev:drops.append(dict(frame=i,damage=prev-now,hits=rb(P1+0xd20)&127))
  prev=now;rr.append(dict(frame=i,p=st(P1),e=st(P2),keys=k))
  if now==0:break
 result=dict(style='natural-KO',maxHits=max(t['p']['hits'] for t in rr),contacts=len(drops),drops=drops,finalHP=rw(P2+0x24));assert result['maxHits']==len(drops),result;report.append(result);print(result,flush=True)
 (P/'cell-natural-ko.json').write_text(json.dumps(rr))
 (P/'cell-ko-audit.json').write_text(json.dumps(report,indent=2))
finally:core.retro_unload_game();core.retro_deinit()

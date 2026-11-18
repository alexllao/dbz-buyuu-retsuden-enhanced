from pathlib import Path
import sys,json,hashlib
setup=Path('work/combo-charge-all/runtime.py').read_text().replace('work/combo-charge-all/candidate.bin','work/air-recovery/candidate.bin')
sys.argv=['negative','after'];exec(compile(setup,'pursuit-negative-runtime','exec'),globals());exec(compile(Path('work/air-recovery/sequences.py').read_text(),'negative-sequences','exec'),globals());reports=[]
def tick(a=(),b=()):
 rawtick(a,b);rows.append(dict(f=len(rows),p=st(P1),e=st(P2),phase=rb(0xf800),airHits=rb(0xf802),queue=rb(0xf813),ttl=rb(0xf814)))
def chase(cid,ki=None):
 prepare(cid,'normal' if cid==0 else 'aldea')
 for _ in range(3):tick(['RIGHT','A'])
 assert wait_for(lambda:rb(P1+0x5b)<=0xe and rb(P2+0x5b)==0x17 and rw(P2+16)<416,130)
 if ki is not None:ww(P1+0x28,ki) # Declared pre-attempt fixture; never used in a video.
 for _ in range(3):tick(['UP','C'])
def save(cid,name):
 reports.append(dict(cid=cid,test=name,maxAirHits=max(t['airHits'] for t in rows),phases=sorted({t['phase'] for t in rows}),maxHits=max(t['p']['hits'] for t in rows),damage=200-rw(P2+0x24),pEnd=st(P1),eEnd=st(P2)))
try:
 for cid in [0,3]:
  prepare(cid,'normal' if cid==0 else 'aldea')
  for _ in range(3):tick(['UP','C'])
  idle(250);assert not any(t['phase'] in [2,3,4] for t in rows);save(cid,'UP+C without own throw does not pursue')
  prepare(cid,'normal' if cid==0 else 'aldea')
  for _ in range(3):tick(['RIGHT','A'])
  idle(350);assert not any(t['phase'] in [2,3,4] for t in rows);assert 200-rw(P2+0x24)==(10 if cid==0 else 9);save(cid,'native throw without chase keeps its original single damage')
  chase(cid,0);idle(240);assert not any(t['phase'] in [2,3,4] for t in rows);save(cid,'zero KI rejects pursuit')
  chase(cid);assert wait_for(lambda:rb(0xf800)==3,50)
  toward='LEFT' if rb(P1+0x59) else 'RIGHT'
  for _ in range(200):tick([toward,'A'])
  idle(200);assert max(t['airHits'] for t in rows)<=1;save(cid,'holding A does not repeat air basics automatically')
  sequence(cid,'none')
  for _ in range(3):tick(['UP','C'])
  idle(180);entries=sum(t['phase']==2 and (i==0 or rows[i-1]['phase']!=2) for i,t in enumerate(rows));assert entries==1;save(cid,'UP+C after landing does not create a second pursuit')
 Path('work/air-recovery/negative.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),cases=reports,fixture='Native compatible states; spacing/facing before each sequence. Zero-KI test alone sets KI=0 immediately before the attempted command. All other actions through real inputs.'),indent=2));print('NEGATIVE PASSED',len(reports),flush=True)
finally:core.retro_unload_game();core.retro_deinit()




from pathlib import Path
import json
def prepare(cid,slug,side=0,critical=False):
 global rows
 state=Path('work/air-pursuit/states-final')/slug/(f'critical-{cid}.state' if critical else f'seed-{cid}.state')
 if P1!=0xe75e:state=Path('work/combo-charge-all/states-p2/normal')/str(cid)/'seed-0.state'
 if P1!=0xe75e and critical:state=Path('work/air-pursuit-fall/states-p2/critical-3.state')
 restore(state.read_bytes());ww(P1+10,700 if not side else 732);ww(P2+10,732 if not side else 700);ww(P1+12,0);ww(P2+12,0);wb(P1+0x59,side);wb(P2+0x59,1-side)
 for _ in range(8):rawtick()
 rows=[]
def wait_for(test,limit=150,keys=()):
 for _ in range(limit):
  if test():return True
  tick(keys)
 return bool(test())
def sequence(cid,finish='none',side=0,slug=None,prepared=False):
 slot=0xf800 if P1==0xe75e else 0xf840
 if not prepared:prepare(cid,slug or ('normal' if cid==0 else 'aldea'),side,cid==3 and finish=='meteor')
 f='LEFT' if side else 'RIGHT'
 for _ in range(3):tick([f,'A'])
 assert rb(P1+0x5b)==0x3a
 assert wait_for(lambda:rb(P1+0x5b)<=0x0e and rb(P2+0x5b)==0x17 and rw(P2+16)<416,130)
 for _ in range(3):tick(['UP','C'])
 assert wait_for(lambda:rb(slot)==3,50)
 chaseStart=len(rows);towards='LEFT' if rb(P1+0x59) else 'RIGHT'
 for _ in range(3):tick([towards,'A'])
 assert wait_for(lambda:rb(slot+2)>=1,50,[towards]),('first',cid,finish,len(rows),st(P1),st(P2))
 for _ in range(3):tick([towards])
 for _ in range(3):tick([towards,'B'])
 second=wait_for(lambda:rb(slot+2)>=2,60,[towards])
 if not second:return dict(cid=cid,finish=finish,second=False,p=st(P1),e=st(P2),frames=len(rows))
 startFinish=len(rows);f,b=face();hcf=[[b],['DOWN',b],['DOWN'],['DOWN',f],[f]]
 if finish=='kame':command(hcf,['A'],2)
 elif finish=='super':command(hcf*2,['A'],2)
 elif finish=='flash':command([['DOWN'],['DOWN',b],[b],[f]],['A'],3)
 elif finish=='meteor':command(hcf*2,['A','B'],2) if cid==0 else command([[f],['DOWN',f],['DOWN'],['DOWN',b],[b],[f]],['B'],3)
 idle(700 if finish=='meteor' else 400)
 return dict(cid=cid,finish=finish,second=second,chaseStart=chaseStart,startFinish=startFinish,frames=len(rows),programs=sorted({t['p']['program'] for t in rows[startFinish:]}),maxHits=max(t['p']['hits'] for t in rows),damage=200-rows[-1]['e']['hp'])





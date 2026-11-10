from pathlib import Path
import sys,json,hashlib
variant=sys.argv[1] if len(sys.argv)>1 else 'after';promoSlug='porunga';sys.argv=['record',promoSlug]
setup=Path('work/namek-native-r6/record-promo.py').read_text().split('\ntry:\n if capture_from==1:')[0].replace('work/namek-native-r6/','work/namek-native-r10/').replace('states-q3','states-final-r10b')
if variant=='after':setup=setup.replace('work/namek-native-r10/integrated.bin','work/combo-charge-all/candidate.bin')
exec(compile(setup,'local-charge-runtime','exec'),globals())
S=Path('work/combo-charge-all');events=[]

def tick(a=(),b=()):
 rawtick(a,b)
 rows.append(dict(f=len(rows),p=st(P1),e=st(P2),clock=rw(P1+6),pose=rb(P1+4),fast=rb(0xf7b2),fast2=rb(0xf7b6),keys=list(a),keys2=list(b),types=[rb(P1+0xe2+i*30) for i in range(3)]))

def idle(n):
 for _ in range(n):tick()

def staged(slug,cid,critical=False):
 global rows
 state=Path('work/namek-r10-short/states')/slug/(f'critical-{cid}.state' if critical else f'seed-{cid}.state')
 restore(state.read_bytes());ww(P1+10,300);ww(P2+10,332);ww(P1+12,0);ww(P2+12,0);wb(P1+0x59,0);wb(P2+0x59,1)
 for _ in range(8):rawtick()
 rows=[]

def chain(pattern='AAB'):
 contacts=[];hp=rw(P2+0x24)
 for f in range(150):
  k=[pattern[0]] if f<3 else []
  for i,t in enumerate(contacts[:len(pattern)-1]):
   if t+3<=f<t+6:k=[pattern[i+1]]
  tick(k);now=rw(P2+0x24)
  if now<hp:contacts.append(f)
  hp=now
  if len(contacts)==len(pattern):break
 assert len(contacts)==len(pattern),(pattern,contacts)

def cross():
 for _ in range(100):
  if rb(P1+0x5b)<=8 and rw(P1)!=0x843 and rw(P2)!=0x843:break
  tick()
 before=rw(P1+10)-rw(P2+10);f,b=face()
 for k in [[f]]*4+[[b]]*4+[[f,'C']]*4+[[]]*4:tick(k)
 for _ in range(100):
  if rw(P1)!=0x843 and rb(P1+0x5b)<=8:break
  tick()
 assert before*(rw(P1+10)-rw(P2+10))<0

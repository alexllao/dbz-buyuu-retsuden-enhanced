from pathlib import Path

def prep_recovery(def_cid=0,side=0,attack_port=1,slug='normal'):
 global AP,DP,AS,DS,attackPort,rows,events
 attackPort=attack_port;AP,DP=(0xe75e,0xe886) if attackPort==1 else (0xe886,0xe75e);AS,DS=(0xf800,0xf840) if attackPort==1 else (0xf840,0xf800)
 physical_cid=(3 if def_cid==0 else 0) if attackPort==1 else def_cid
 restore((Path('work/air-recovery/states-final')/slug/f'seed-{physical_cid}.state').read_bytes())
 assert rb(DP+0x58)==def_cid and rb(AP+0x58) in [0,3]
 ww(AP+10,700 if not side else 732);ww(DP+10,732 if not side else 700);ww(AP+12,0);ww(DP+12,0);wb(AP+0x59,side);wb(DP+0x59,1-side)
 for _ in range(8):rawtick()
 rows=[];events=[]

def step_recovery(a=(),d=()):tick(a,d) if attackPort==1 else tick(d,a)

def wait_recovery(test,limit=150,a=(),d=()):
 for _ in range(limit):
  if test():return True
  step_recovery(a,d)
 return bool(test())

def command_recovery(dirs,buttons,defender=True,speed=4):
 for keys in [k for k in dirs for _ in range(speed)]+[dirs[-1]+buttons]*3:
  step_recovery([],keys) if defender else step_recovery(keys,[])

def run_recovery(def_cid=0,side=0,attack_port=1,slug='normal',mode='valid',counter=True,prepared=False):
 if not prepared:prep_recovery(def_cid,side,attack_port,slug)
 initial_hp=rw(DP+0x24);initial_enemy_hp=rw(AP+0x24)
 f='LEFT' if side else 'RIGHT'
 for _ in range(3):step_recovery([f,'A'])
 assert rb(AP+0x5b)==0x3a
 assert wait_recovery(lambda:rb(AP+0x5b)<=0xe and rb(DP+0x5b)==0x17 and rw(DP+16)<416,130)
 for _ in range(3):step_recovery(['UP','C'])
 assert wait_recovery(lambda:rb(AS)==3,50)
 towards='LEFT' if rb(AP+0x59) else 'RIGHT';held=['A','C'] if mode=='held' else []
 if mode=='held':
  for _ in range(8):step_recovery([],held)
 for _ in range(3):step_recovery([towards,'A'],held)
 assert wait_recovery(lambda:rb(AS+2)>=1,50,[towards],held)
 first=len(rows);after_first=rw(DP+0x24);events.append(dict(name='firstAirContact',frame=first))
 if mode=='low_ki':ww(DP+0x28,0) # Explicit negative fixture, never a recorded take.
 if mode=='used':wb(DS+0x2a,1) # Isolated gate fixture, never a recorded take.
 if mode=='late':
  for _ in range(32):step_recovery()
 if mode in ['valid','low_ki','used','late']:
  for _ in range(3):step_recovery([towards],['A','C'])
 else:
  for _ in range(3):step_recovery([towards],held)
 for _ in range(6):step_recovery([towards,'B'],held)
 escaped=any(t['dPhase']==6 for t in rows)
 assert wait_recovery(lambda:rw(AP+16)==448 and rw(DP+16)==448 and rb(DP+0x5b)<=8 and rb(AP+0x5b)<=8,300)
 ground=len(rows);events.append(dict(name='bothGrounded',frame=ground))
 after_pressure=rw(DP+0x24);expected=0xc04 if def_cid==0 else 0xc27
 if counter:
  forward='LEFT' if rb(DP+0x59) else 'RIGHT';backward='RIGHT' if forward=='LEFT' else 'LEFT'
  dirs=[[backward],['DOWN',backward],['DOWN'],['DOWN',forward],[forward]] if def_cid==0 else [['DOWN'],['DOWN',backward],[backward],[forward]]
  events.append(dict(name='counterCommand',frame=len(rows)))
  command_recovery(dirs,['A'])
  for _ in range(260):step_recovery()
  assert any(t['defender']['program']==expected for t in rows[ground:]),('counter absent',def_cid,side,attack_port)
  assert rw(AP+0x24)<initial_enemy_hp
 else:
  for _ in range(200):step_recovery()
 entries=[i for i,t in enumerate(rows) if t['dPhase']==6 and (i==0 or rows[i-1]['dPhase']!=6)]
 result=dict(defenderCid=def_cid,attackPort=attack_port,side=side,scenario=slug,mode=mode,escaped=escaped,escapeEntries=entries,firstAirContact=first,grounded=ground,damageReceived=initial_hp-after_pressure,hpAfterFirst=after_first,hpAfterPressure=after_pressure,counter=expected if counter else None,counterDamage=initial_enemy_hp-rw(AP+0x24),frames=len(rows),events=events)
 if escaped:
  i=entries[0];result['KIAtRecovery']=[rows[i-1]['defender']['ki'],rows[i]['defender']['ki']];assert result['KIAtRecovery'][0]-result['KIAtRecovery'][1]==32,result
 if mode=='valid':assert escaped and len(entries)==1 and after_pressure==after_first,result
 else:assert not escaped,result
 return result

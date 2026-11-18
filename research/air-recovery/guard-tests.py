"""Pruebas aisladas de puertas defensivas; fixtures declarados, no son vídeo."""
from pathlib import Path
import sys,json,hashlib
setup=Path('work/combo-charge-all/runtime.py').read_text().replace('work/combo-charge-all/candidate.bin','work/air-recovery/candidate.bin')
sys.argv=['guards','after'];exec(compile(setup,'defense-guards-runtime','exec'),globals());exec(compile(Path('work/air-recovery/recovery-sequences.py').read_text(),'defense-sequences','exec'),globals())
def tick(a=(),b=()):rawtick(a,b)
reports=[]
try:
 prep_recovery(0)
 for _ in range(3):step_recovery(['RIGHT','A'])
 assert wait_recovery(lambda:rb(AP+0x5b)<=0xe and rb(DP+0x5b)==0x17 and rw(DP+16)<416,130)
 for _ in range(3):step_recovery(['UP','C'])
 assert wait_recovery(lambda:rb(AS)==3,50)
 toward='LEFT' if rb(AP+0x59) else 'RIGHT'
 for _ in range(3):step_recovery([toward,'A'])
 assert wait_recovery(lambda:rb(AS+2)>=1,50,[toward]);baseline=snap()
 for name,keys in [('ground',['A','C']),('KO',['A','C']),('strong-hurt',['A','C']),('Meteor-action',['A','C']),('KI-action',['A','C']),('turbo',['A','C']),('A-only',['A']),('C-only',['C']),('KI31',['A','C']),('KI32',['A','C'])]:
  restore(baseline);accepted=False
  if name=='KI32':ww(DP+0x28,32)
  for _ in range(3):
   if name=='ground':ww(DP+16,448);ww(DS+8,448);ww(DS+10,0)
   elif name=='KO':ww(DP+0x24,0)
   elif name=='strong-hurt':wb(DP+0x5b,0x13)
   elif name=='Meteor-action':wb(AP+0x5b,0x40)
   elif name=='KI-action':wb(AP+0x5b,0x39)
   elif name=='turbo':ww(0xe756,0x140);ww(0xe758,0xcc)
   elif name=='KI31':ww(DP+0x28,31)
   step_recovery([],keys);accepted|=rb(DS)==6
  assert accepted==(name=='KI32'),(name,rb(DS));reports.append(dict(test=name,accepted=accepted))
 Path('work/air-recovery/guard-tests.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),fixture='A real native first contact creates the eligible baseline. Each guard is then isolated by explicitly setting its condition before three frames (ground Y, HP0, incoming action, strong-hurt action, or turbo speed). These are synthetic guard checks, not complete playable Meteor/KO scenarios or recorded takes.',cases=reports),indent=2));print('GUARDS PASSED',len(reports),flush=True)
finally:core.retro_unload_game();core.retro_deinit()

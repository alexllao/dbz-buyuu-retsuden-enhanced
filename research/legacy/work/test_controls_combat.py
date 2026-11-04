from pathlib import Path
import sys,json

deep_arguments=list(sys.argv)
deep_source=Path(deep_arguments[1]);deep_out=Path(deep_arguments[2]);deep_out.mkdir(parents=True,exist_ok=True)
sys.argv=['probe','--native','--rom',str(deep_source),'--out',str(deep_out)]
header=Path('work/gameplay_probe.py').read_text().split('try:\n for index,step in enumerate(steps[:-1]):')[0]
exec(compile(header,'local-combat-setup','exec'),globals())

def astate(base):
 return {'action':rb(base+0x5b),'program':rw(base),'pose':rb(base+4),'x':rw(base+0xa),'y':rw(base+0x10),'hp':rw(base+0x24),'air':bool(rw(base+0x1e)&0x1000),'scratch':bytes(rb(base+i) for i in range(0x108,0x110)).hex()}
def run(schedule):
 trace=[]
 for a,b in schedule:
  tick(a,b);trace.append({'p1':astate(P1),'p2':astate(P2)})
 return trace
def damage(trace):
 return {'p1':200-min(x['p1']['hp'] for x in trace),'p2':200-min(x['p2']['hp'] for x in trace),'hit_frames_p1':[i+1 for i,x in enumerate(trace) if x['p1']['hp']<(200 if i==0 else trace[i-1]['p1']['hp'])],'hit_frames_p2':[i+1 for i,x in enumerate(trace) if x['p2']['hp']<(200 if i==0 else trace[i-1]['p2']['hp'])]}
try:
 for step in steps[:-1]:
  for _ in range(step.get('frames',1)):tick(step.get('buttons',[]))
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for _ in range(180):tick()
 baseline=snap()
 def fixture(distance=200):
  restore(baseline)
  for base,x,facing in [(P1,300,0),(P2,300+distance,1)]:
   ww(base+0xa,x);ww(base+0xc,0);wb(base+0x59,facing)
   for o in (0x22,0x24,0x26):ww(base+o,200)
  for _ in range(3):tick()
  return snap()
 results={'rom_sha256':hashlib.sha256(rom).hexdigest(),'collisions':[],'inputs':{},'interruption_cases':[],'special_input_sequences':{}}
 for distance in [24,32,40,48,56,64,80,120]:
  for button in ['A','B']:
   for block in [False,True]:
    restore(fixture(distance))
    trace=run([([button] if f<2 else [],['RIGHT'] if block else []) for f in range(80)])
    results['collisions'].append({'distance':distance,'button':button,'block':block,**damage(trace),'p1_actions':sorted(set(x['p1']['action'] for x in trace))})
 restore(fixture())
 p2stop=run([([],['LEFT'] if f<5 else []) for f in range(60)])
 results['inputs']['p2_stop']=p2stop
 restore(fixture())
 p2single=run([([],['A'] if f<2 else []) for f in range(80)])
 end=next(i+1 for i,x in enumerate(p2single) if i>0 and x['p2']['action']==0 and p2single[i-1]['p2']['action']!=0)
 restore(fixture())
 results['inputs']['p2_late_punch']=run([([],['A'] if f<2 or end-3<=f<end-1 else []) for f in range(90)])
 restore(fixture())
 results['inputs']['flight_stop']=run([(['C'] if f<2 else ['RIGHT'] if 90<=f<95 else [],[]) for f in range(160)])
 # A later opponent strike can interrupt the final-recovery queued input.
 for enemy_start in range(8,20):
  restore(fixture(38))
  trace=run([(['A'] if f<2 or 17<=f<19 else [],['B'] if enemy_start<=f<enemy_start+2 else []) for f in range(110)])
  results['interruption_cases'].append({'enemy_start':enemy_start,'damage':damage(trace),'trace':trace})
 results['queued_hit_interruptions']=[]
 for distance in [24,40,64]:
  for start in [2,3,4]:
   for enemy_button in ['A','B']:
    restore(fixture(distance))
    trace=run([(['A'] if start<=f<start+2 else ['B'] if start+4<=f<start+7 else [],[enemy_button] if f<2 else []) for f in range(100)])
    hits=damage(trace)['hit_frames_p1']
    if hits:
     hit=hits[0]
     queued=any(bytes.fromhex(x['p1']['scratch'])[1]>0 for x in trace[max(0,hit-4):hit])
     if queued:
      restarts=[i+1 for i,x in enumerate(trace) if i>hit+3 and 0x20<=x['p1']['action']<=0x27 and x['p1']['action']!=trace[i-1]['p1']['action']]
      results['queued_hit_interruptions'].append({'distance':distance,'p1_start':start,'enemy_button':enemy_button,'first_hit':hit,'restarts_after_hit':restarts,'trace':trace})
 for button in ['A','B']:
  restore(fixture(200))
  schedule=[(['DOWN'],[])]*4+[(['DOWN','RIGHT'],[])]*4+[(['RIGHT',button],[])]*4+[([],[])]*168
  trace=run(schedule)
  results['special_input_sequences'][button]={'actions':sorted(set(x['p1']['action'] for x in trace)),'damage':damage(trace)}
 restore(fixture(100))
 wb(P2+0xbe,1)
 import random
 rng=random.Random(1234)
 choices=[[],['RIGHT'],['LEFT'],['DOWN'],['UP'],['A'],['B'],['C'],['A','B'],['DOWN','RIGHT'],['RIGHT','A']]
 stress=[]
 for _ in range(220):
  command=rng.choice(choices)
  for _ in range(rng.randint(2,9)):
   tick(command)
   if total%30==0:stress.append({'p1':astate(P1),'p2':astate(P2)})
 results['stress_samples']=stress
 results['stress_final_state']=[rw(0xe6a4),rw(0xe6a6)]
 save_image(deep_out/'stress-final.png')
 (deep_out/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
 print(json.dumps({'collisions':len(results['collisions']),'p2_punch_return':end,'special_input_sequences':results['special_input_sequences'],'stress_samples':len(stress),'final_state':results['stress_final_state']}),flush=True)
finally:
 core.retro_unload_game();core.retro_deinit()

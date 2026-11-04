from pathlib import Path
import subprocess,concurrent.futures,json

root=Path('work/gameplay/matrix');root.mkdir(parents=True,exist_ok=True)
def job(mode,cid):
 out=root/mode/f'cid{cid:02}';out.mkdir(parents=True,exist_ok=True)
 cmd=['python','work/gameplay_probe.py','--quick','--turbo' if mode=='turbo' else '--native','--rom','work/rom/controls-v1.bin','--out',str(out),'--character',str(cid)]
 with (out/'run.log').open('w',encoding='utf-8') as log:
  subprocess.run(cmd,check=True,stdout=log,stderr=subprocess.STDOUT)
 data=json.loads((out/'traces.json').read_text())
 rows={r['label'].removeprefix('native-'):r for r in data['results']}
 def starts(row):
  r=rows[row];return [(i+1,s['action']) for i,s in enumerate(r['frames']) if s['action']!=(r['initial']['action'] if i==0 else r['frames'][i-1]['action']) and 0x20<=s['action']<=0x27]
 checks={
  'idle_stable':all(s['action']==0 and s['x']==rows['idle']['initial']['x'] for s in rows['idle']['frames']),
  'scratch_magic_stable':all(bytes.fromhex(s['native_player_hex'])[0x108]==0xc7 for r in rows.values() for s in r['frames']),
  'stop_after_release':all(s['action']==0 for s in rows['right-05-stop']['frames'][10:]),
  'held_punch_not_autorepeated':len(starts('punch-held'))==1,
  'late_punch_executed':len(starts('punch-late-dynamic'))==2,
  'late_kick_executed':len(starts('kick-late-dynamic'))==2,
  'jump_returns_to_idle':rows['jump-tap']['frames'][-1]['action']==0,
  'charge_returns_to_idle':rows['charge-release']['frames'][-1]['action']==0,
 }
 result={'mode':mode,'character_id':cid,'checks':checks,'punch_events':starts('punch-late-dynamic'),'kick_events':starts('kick-late-dynamic'),'passed':all(checks.values())}
 print(json.dumps(result),flush=True)
 return result
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 futures=[pool.submit(job,mode,cid) for mode in ['normal','turbo'] for cid in range(11)]
 for f in concurrent.futures.as_completed(futures):results.append(f.result())
(root/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
assert all(r['passed'] for r in results),'Check matrix results for failures'
print('MATRIX PASSED',len(results),'character/mode combinations')

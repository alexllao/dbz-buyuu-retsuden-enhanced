from pathlib import Path
import sys,json,hashlib
setup=Path('work/combo-charge-all/runtime.py').read_text().replace('work/combo-charge-all/candidate.bin','work/air-recovery/candidate.bin')
sys.argv=['test','after'];exec(compile(setup,'recovery-test-runtime','exec'),globals());exec(compile(Path('work/air-recovery/recovery-sequences.py').read_text(),'defense-sequences','exec'),globals());results=[]
def tick(a=(),b=()):
 rawtick(a,b);rows.append(dict(f=len(rows),attacker=st(AP),defender=st(DP),aPhase=rb(AS),dPhase=rb(DS),airHits=rb(AS+2),used=rb(DS+0x2a),window=rb(DS+0x2b),keys=list(a),keys2=list(b)))
try:
 for cid in [0,3]:
  for port in [1,2]:
   for side in [0,1]:
    for mode in ['valid','none','held','low_ki','late','used']:
     r=run_recovery(cid,side,port,'normal',mode,counter=mode=='valid');results.append(r);print(cid,port,side,mode,r['escaped'],r['damageReceived'],r['counterDamage'],flush=True)
 Path('work/air-recovery/defense-matrix.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),cases=results,fixture='Fresh menu seeds; spacing/facing before each take. Negative low_ki and used explicitly change KI/credit immediately before attempted input; no such writes in valid or held/late/control cases.'),indent=2))
finally:core.retro_unload_game();core.retro_deinit()

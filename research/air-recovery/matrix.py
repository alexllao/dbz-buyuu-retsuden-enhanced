from pathlib import Path
import sys,json,hashlib
setup=Path('work/combo-charge-all/runtime.py').read_text().replace('work/combo-charge-all/candidate.bin','work/air-recovery/candidate.bin')
sys.argv=['matrix','after'];exec(compile(setup,'air-matrix-runtime','exec'),globals());exec(compile(Path('work/air-recovery/sequences.py').read_text(),'air-sequences','exec'),globals());O=Path('work/air-recovery');real_rawtick=rawtick
results=[]
def rawtick(a=(),b=()):real_rawtick(a,b) if port==1 else real_rawtick(b,a)
def tick(a=(),b=()):
 rawtick(a,b);rows.append(dict(f=len(rows),p=st(P1),e=st(P2),phase=rb(slot),victimPhase=rb(otherSlot),airHits=rb(slot+2),pose=rb(P1+4),sound=rb(0x5000),lastSound=rb(0x5001),keys=list(a),keys2=list(b)))
try:
 for port in [1,2]:
  P1,P2=(0xe75e,0xe886) if port==1 else (0xe886,0xe75e);slot,otherSlot=(0xf800,0xf840) if port==1 else (0xf840,0xf800)
  for side in [0,1]:
   for cid,finish,expected in [(0,'none',None),(3,'none',None),(0,'kame',0xc04),(3,'flash',0xc27),(0,'super',0xc05),(0,'meteor',0x83e),(3,'meteor',0x846)]:
    r=sequence(cid,finish,side);r.update(port=port,side=side,expected=expected,pEnd=st(P1),eEnd=st(P2),ownerState=rb(slot),enemyState=rb(otherSlot))
    assert r['second'],r
    if expected is not None:assert expected in r['programs'],r
    assert r['pEnd']['y']==448 and r['eEnd']['y']==448 and r['ownerState']==r['enemyState']==0,r
    landing=next(i for i in range(1,len(rows)) if rows[i-1]['phase']==3 and rows[i-1]['p']['y']<448 and rows[i]['p']['y']==448)
    emitted=[t['f'] for t in rows[landing:landing+3] if t['sound']==0x49 or t['lastSound']==0x49]
    assert emitted,('landing sound absent',port,side,cid,finish,landing)
    r['landingFrame']=landing;r['nativeLandingSound']=0x49;r['soundObservedFrames']=emitted
    outside=[(t['f'],t['p']['y'],t['e']['y'],t['phase'],t['victimPhase']) for t in rows if not(0<=t['p']['y']<=448 and 0<=t['e']['y']<=448)]
    r['outsideNativeGround']=outside
    assert all(0<=t['p']['y']<=448 for t in rows if t['phase'] in [2,3,4]),r
    results.append(r);print(port,side,cid,finish,'hits',r['maxHits'],'damage',r['damage'],flush=True)
    if port==2 and finish in ['kame','flash']:(O/f'matrix-p2-{side}-{cid}.json').write_text(json.dumps(rows))
 (O/'matrix.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),cases=results,scope='Goku/Vegeta, both ports and directions, normal speed, real inputs. P2 uses compatible menu seeds from prior build with identical native actor/RAM layout.'),indent=2))
finally:core.retro_unload_game();core.retro_deinit()






from pathlib import Path
import subprocess,sys,hashlib,json,concurrent.futures
rom=Path(sys.argv[1]);sha=hashlib.sha256(rom.read_bytes()).hexdigest();script=Path('work/combos/test_combo.py')
jobs=[(cid,port,turbo) for cid in [0,3] for port in [1,2] for turbo in [False,True]]
def run(job):
 cid,port,turbo=job;cmd=[sys.executable,str(script),str(rom),str(cid),str(port)]+(['--turbo'] if turbo else [])
 if '--summarize-only' not in sys.argv:
  p=subprocess.run(cmd,capture_output=True,text=True);assert p.returncode==0,(job,p.stderr)
 report=json.loads((Path('work/combos/tests')/f'{sha[:8]}-{cid}-p{port}-{int(turbo)}'/'report.json').read_text());results=report['results'];chains=[r for r in results if r['summary']['mode']=='chain']
 checks={'bothDirectionsLinked':all(any(r['summary']['reverse']==reverse and len(r['summary']['hits'])>=2 and 1 in r['summary']['stages'] for r in chains) for reverse in [False,True]),'finisherCancelObserved':any(2 in r['summary']['stages'] for r in chains),'guardNoCancel':all(r['summary']['stages']==[0] for r in results if r['summary']['mode']=='guard'),'whiffNoCancel':all(r['summary']['stages']==[0] for r in results if r['summary']['mode']=='whiff'),'heldOnlyOneContinuation':all(max(r['summary']['stages'])<=1 and len(r['summary']['hits'])<=2 for r in results if r['summary']['mode']=='held-button')}
 trueLinks=[];normalThirds=[]
 for r in results:
  trace=r['trace'];hits=r['summary']['hits']
  if r['summary']['mode']=='chain' and len(hits)>=2:
   trueLinks.append(all(t['enemy']['action'] in [11,12] for t in trace[hits[0]:hits[1]]))
  if r['summary']['mode']=='spam':
   runLength=1
   for a,b in zip(hits,hits[1:]):
    runLength=runLength+1 if all(t['enemy']['action'] in [11,12] for t in trace[a:b]) else 1
    if runLength>2 and trace[b]['p']['program'] in [0x400,0x424]:normalThirds.append([a,b])
 checks['trueTwoHitLinkObserved']=any(trueLinks)
 checks['defenderRegainsControlBeforeLaterNormalHits']=not normalThirds
 if turbo:
  checks={'normalSpeedOnlyGate':all(r['summary']['stages']==[0] for r in results)}
 return {'cid':cid,'port':port,'turbo':turbo,'cases':len(results),'checks':checks,'betweenSnapshotRecoveryAmbiguities':normalThirds,'summaries':[r['summary'] for r in results],'passed':all(checks.values())}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(run,jobs))
report={'romSha256':sha,'jobs':results,'cases':sum(r['cases'] for r in results),'passed':all(r['passed'] for r in results),'limits':['Normal speed only; turbo gate preserves native combat','Three-hit damage string not guaranteed to be uninterrupted; projectile keeps native startup/range','Only Goku and Vegeta; only standing close punch links','No exhaustive infinite-combo proof; bounded spam and held-input tests']}
Path('work/combos/matrix.json').write_text(json.dumps(report,indent=2));print(json.dumps({'cases':report['cases'],'passed':report['passed'],'jobs':[{'cid':r['cid'],'port':r['port'],'turbo':r['turbo'],'checks':r['checks']} for r in results]}));assert report['passed']

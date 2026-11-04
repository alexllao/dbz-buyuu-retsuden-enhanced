from pathlib import Path
import subprocess,sys,hashlib,json,concurrent.futures
rom=Path(sys.argv[1]);sha=hashlib.sha256(rom.read_bytes()).hexdigest();jobs=[(cid,port,turbo) for cid in [0,3] for port in [1,2] for turbo in [False,True]]
def run(job):
 cid,port,turbo=job;cmd=[sys.executable,'work/kick-combos/test_combo.py',str(rom),str(cid),str(port)]+(['--turbo'] if turbo else [])
 if '--summarize-only' not in sys.argv:
  p=subprocess.run(cmd,capture_output=True,text=True);assert p.returncode==0,(job,p.stderr)
 d=json.loads((Path('work/kick-combos/tests')/f'{sha[:8]}-{cid}-p{port}-{int(turbo)}'/'report.json').read_text());results=d['results'];chains=[r for r in results if r['summary']['mode']=='chain'];expected=5 if cid==0 else 4
 summaries=[]
 for r in results:
  s=dict(r['summary']);hits=s['hits'];tr=r['trace'];s['uninterruptedToLastHit']=len(hits)>1 and all(t['enemy']['action'] in [11,12] for t in tr[hits[0]:hits[-1]])
  s['damagePerHit']=[(r['initial'][1]['hp'] if not i else tr[hits[i-1]]['enemy']['hp'])-tr[f]['enemy']['hp'] for i,f in enumerate(hits)];summaries.append(s)
 if turbo:checks={'normalOnly':all(r['summary']['stages']==[0] for r in results)}
 else:
  checks={'fullComboBothDirections':all(any(s['mode']=='chain' and s['reverse']==rev and len(s['hits'])==expected and s['uninterruptedToLastHit'] for s in summaries) for rev in [False,True]),'singleCommandBounded':all(len(r['summary']['hits'])<=expected for r in chains),'guardNoCancel':all(r['summary']['stages']==[0] for r in results if r['summary']['mode']=='guard'),'whiffNoCancel':all(r['summary']['stages']==[0] for r in results if r['summary']['mode']=='whiff'),'heldAOnlyTwoPunches':all(len(r['summary']['hits'])<=2 for r in results if r['summary']['mode']=='held-button'),'chainReturnsIdle':all(r['summary']['idleAtEnd'] for r in chains),'kickDamageModerated':all(all(0<n<=10 for n in s['damagePerHit'][2:]) for s in summaries if s['mode']=='chain')}
 return {'cid':cid,'port':port,'turbo':turbo,'cases':len(results),'checks':checks,'summaries':summaries,'passed':all(checks.values())}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(run,jobs))
report={'romSha256':sha,'jobs':results,'cases':sum(r['cases'] for r in results),'passed':all(r['passed'] for r in results),'limits':['Normal speed, close standing AA then B only','Bounded tests against default Goku defender; not all matchups or infinite-combo proof','Combo counter not in ROM; video counter is a postproduction preview']}
Path('work/kick-combos/matrix.json').write_text(json.dumps(report,indent=2));print(json.dumps({'cases':report['cases'],'passed':report['passed'],'checks':[{'cid':r['cid'],'port':r['port'],'turbo':r['turbo'],'checks':r['checks']} for r in results]}));assert report['passed']

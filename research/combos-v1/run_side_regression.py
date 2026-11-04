from pathlib import Path
import concurrent.futures,subprocess,sys,json,hashlib
p=Path('work/side-switch');rom=Path(sys.argv[1]);sha=hashlib.sha256(rom.read_bytes()).hexdigest()
def run(job):
 cid,port,turbo=job
 command=[sys.executable,str(p/'test_commands.py'),str(rom),str(cid),str(port)]+(['--turbo'] if turbo else [])
 proc=subprocess.run(command,capture_output=True,text=True);assert proc.returncode==0,(command,proc.stderr)
 d=json.loads((p/'tests'/f'{sha[:8]}-{cid:02}-p{port}-{int(turbo)}'/'report.json').read_text())
 return {'cid':cid,'port':port,'turbo':turbo,'romSha256':sha,'cases':[{k:r[k] for k in ['mode','reverse','air','checks','passed','programs']} for r in d['results']]}
jobs=[(cid,1,False) for cid in range(11)]+[(cid,2,True) for cid in range(11)]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(run,jobs))
failures=[{'cid':r['cid'],'port':r['port'],'turbo':r['turbo'],**c} for r in results for c in r['cases'] if not c['passed']]
summary={'romSha256':sha,'jobs':len(jobs),'cases':sum(len(r['cases']) for r in results),'results':results,'failures':failures,'passed':not failures,'scope':'Actual new command through native history and both controller ports; eleven CID P1 normal and P2 turbo; both directions, native jump, plain C and attack commands, long-held C, distance and timeout gates. No CPU autoplay.'}
Path('work/combos/side-regression.json').write_text(json.dumps(summary,indent=2));print(json.dumps({k:summary[k] for k in ['jobs','cases','failures','passed']}),flush=True)
assert not failures

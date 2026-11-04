from pathlib import Path
import subprocess,sys,concurrent.futures,json
P=Path('work/natural-combos');jobs=[(c,t) for c in range(11) for t in ['original','natural']]
def run(j):
 c,t=j;rom='work/rom/original.bin' if t=='original' else str(P/'candidate.bin');r=subprocess.run([sys.executable,str(P/'test_timing.py'),rom,str(c),t],capture_output=True,text=True);assert r.returncode==0,(j,r.stderr)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(run,jobs))
results=[]
for c in range(11):
 a=json.loads((P/f'timing/original-{c}/report.json').read_text());b=json.loads((P/f'timing/natural-{c}/report.json').read_text())
 for x,y in zip(a['results'],b['results']):
  checks={'sameProgram':x['program']==y['program'],'sameAttackPoseOrder':x['poses'][1:]==y['poses'][1:],'sameAnimationCursors':x['cursors']==y['cursors']}
  results.append({'cid':c,'button':x['button'],'checks':checks,'originalFrames':x['activeFrames'],'naturalFrames':y['activeFrames'],'originalCursors':x['cursors'],'naturalCursors':y['cursors'],'passed':all(checks.values())})
report={'sourceSha256':a['romSha256'],'targetSha256':b['romSha256'],'passed':all(r['passed'] for r in results),'cases':results,'scope':'Independent standing A/B attacks of all11 characters versus original ROM; identical program, attack pose order after initial idle sample and unique animation cursor sequence; frame durations recorded separately because polling/pauses can shift by a frame. No timing or HP forcing.'};(P/'timing-validation.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps({'passed':report['passed'],'failed':[r for r in results if not r['passed']],'durations':[(r['cid'],r['button'],r['originalFrames'],r['naturalFrames']) for r in results]}));assert report['passed']

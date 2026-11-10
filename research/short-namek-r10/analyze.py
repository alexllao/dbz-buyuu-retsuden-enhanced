from pathlib import Path
import json
out=[];root=Path('work/namek-r10-short/captures')
for path in sorted(root.glob('*/*-report.json')):
 report=json.loads(path.read_text());label=path.stem.replace('-report','');rows=json.loads((path.parent/(label+'.json')).read_text())
 hits=[i for i,(a,b) in enumerate(zip(rows,rows[1:]),1) if b['e']['hp']<a['e']['hp']]
 starts=[(i,hex(t['p']['program'])) for i,t in enumerate(rows) if i==0 or t['p']['program']!=rows[i-1]['p']['program']]
 out.append(dict(stage=path.parent.name,label=label,frames=len(rows),contacts=hits,starts=starts,maxHits=report['maxHits']))
Path('work/namek-r10-short/timeline-analysis.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))

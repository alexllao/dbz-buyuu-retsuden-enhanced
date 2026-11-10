from pathlib import Path
import sys,json
audit_variant=sys.argv[1];setup=Path('work/combo-charge-all/runtime.py').read_text();exec(compile(setup,'charge-probe-setup','exec'),globals());cases=[]
try:
 for slug,cid,kind,critical in [('normal',0,'kame',False),('normal',0,'super',False),('aldea',3,'flash',False),('porunga',5,'cell',True)]:
  for context in ['solo','combo','cross','late','guard','whiff']:
   staged(slug,cid,critical);initialHP=rw(P2+0x24)
   if context in ['combo','cross','late']:chain()
   if context=='cross':cross()
   if context=='late':idle(180)
   if context in ['guard','whiff']:
    if context=='whiff':ww(P2+10,500)
    for f in range(90):tick(['A'] if f<3 else [],['RIGHT'] if context=='guard' else [])
   idle(3);f,b=face();hcf=[[b],['DOWN',b],['DOWN'],['DOWN',f],[f]]
   dirs=hcf if kind=='kame' else hcf*2 if kind=='super' else [['DOWN'],['DOWN',b],[b],[f]] if kind=='flash' else [['DOWN'],['DOWN',f],[f],[b]]
   expected={'kame':0xc04,'super':0xc05,'flash':0xc27,'cell':0x84a}[kind]
   command(dirs,['B'] if kind=='cell' else ['A'],3)
   idle(850 if kind=='cell' else 700)
   accepted=next((t['f'] for t in rows if t['p']['program']==expected),None)
   if accepted is None:raise AssertionError((audit_variant,kind,context,'not accepted'))
   launch=next((t['f'] for t in rows if t['f']>=accepted and (t['pose']==0x51 if kind=='cell' else any(t['types']))),None)
   hits=[i for i,(a,t) in enumerate(zip(rows,rows[1:]),1) if t['e']['hp']<a['e']['hp']]
   result=dict(kind=kind,context=context,program=expected,accepted=accepted,launch=launch,startup=launch-accepted if launch is not None else None,damage=initialHP-rows[-1]['e']['hp'],hitEvents=hits,relativeHits=[i-launch for i in hits if launch is not None and i>=launch],maxHits=max(t['p']['hits'] for t in rows),fastUsed=any(t['fast']&2 for t in rows),returnedToIdle=rows[-1]['p']['program']==0)
   cases.append(result)
   if context in ['solo','combo','cross']:(S/f'{audit_variant}-{kind}-{context}.json').write_text(json.dumps(rows))
   print(audit_variant,kind,context,'startup',result['startup'],'damage',result['damage'],'hits',result['maxHits'],'fast',result['fastUsed'],flush=True)
 (S/(audit_variant+'-cases.json')).write_text(json.dumps(cases,indent=2))
finally:core.retro_unload_game();core.retro_deinit()

from pathlib import Path
import sys,json
P=Path('work/short-roster-links');scenes=[]
techs=['Kamehameha','Masenko','Makankosappo','Final Flash','Burning Attack','Makankosappo','Energy Flame','Kamehameha','Mega Buster','Eraser Gun','Terra Smash']
for take in json.loads((P/'takes.json').read_text()):
 cid=take['cid'];path=P/f'video/after/{take["name"]}.mp4';r=json.loads(path.with_suffix('.json').read_text());last=take['contactFrames'][-1];end=min(len(r),last+34)
 caption='Puño + '+techs[cid] if take['pattern']=='A' else 'Tres básicos + '+techs[cid]
 scenes.append((path.as_posix(),0,end,take['name'].upper(),caption))
path=Path('work/long-chain/video/after/Cell-16-impactos.mp4');r=json.loads(path.with_suffix('.json').read_text());end=max(i for i,(a,t) in enumerate(zip(r,r[1:]),1) if t['e']['hp']<a['e']['hp'])+38
scenes.append((path.as_posix(),0,end,'CELL / 16 IMPACTOS','Básicos + cambio de lado + Meteor'))
c=dict(title='GOLPES + ESPECIALES',tag='11 PERSONAJES / REMATE DE CELL',bottom='Secuencias reales / mod en desarrollo',filename='Short-Once-personajes-y-Cell-16.mp4',build='20261108-175044',status='Valid build. Goku recovery buffer; other characters keep native commands. Cell16 is a staged route, not certified unavoidable.',scenes=scenes)
s=Path('work/shorts-updates/render.py').read_text(encoding='utf-8').replace("P=Path('work/shorts-updates')","P=Path('work/short-roster-links/render')").replace("O=Path('outputs/YouTube-Shorts-mejoras')","O=Path('outputs/Short-once-personajes-y-Cell')")
s=s.replace("c=configs[mode];","configs['roster']="+repr(c)+"\nc=configs[mode];")
# Keep the main heading within the vertical safe area.
s=s.replace("c['title'],352,62", "c['title'],352,57")
sys.argv=['render','roster'];exec(compile(s,'roster-short-render','exec'),globals())

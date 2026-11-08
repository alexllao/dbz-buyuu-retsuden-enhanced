from pathlib import Path
import json,sys
P=Path('work/basic-chains');scenes=[]
for label,start,caption,sub in [
 ('AAB-meteor',0,'GOKU / A-A-B + METEOR','Puño, recto, patada y remate'),
 ('Vegeta-Meteor',12,'VEGETA','Su Meteor de ocho impactos'),
 ('Piccolo-Meteor',12,'PICCOLO','Nueve impactos de su Meteor'),
 ('Cell-cinco-disparos',100,'CELL','Ráfaga de cinco proyectiles'),
 ('Gohan-lanzamiento-Masenko',0,'GOHAN','Lanzamiento + Masenko'),
 ('A18-Meteor',12,'A18','Meteor de tres impactos'),
 ('Freezer-Meteor',12,'FREEZER','Remate de tres impactos'),
 ('AAB-kame',0,'GOKU / A-A-B + KAMEHAMEHA','Puños, patada y Kamehameha')]:
 path=P/f'video/after/{label}.mp4';r=json.loads(path.with_suffix('.json').read_text());last=max(i for i,(a,t) in enumerate(zip(r,r[1:]),1) if t['e']['hp']<a['e']['hp']);end=min(len(r),last+32);scenes.append((path.as_posix(),start,end,caption,sub))
c=dict(title='COMBOS Y REMATES',tag='GOKU Y OTROS PERSONAJES',bottom='Nuevas cadenas / especiales del juego',filename='Short-Combos-y-remates.mp4',build=json.loads((P/'build.json').read_text())['buildId'],status='Prueba de variantes de Goku y ataques existentes del plantel',scenes=scenes)
s=Path('work/shorts-updates/render.py').read_text(encoding='utf8').replace("P=Path('work/shorts-updates')","P=Path('work/basic-chains/short')").replace("O=Path('outputs/YouTube-Shorts-mejoras')","O=Path('outputs/Combos-Goku-y-Short')");s=s.replace('c=configs[mode];',"configs['combos']="+repr(c)+"\nc=configs[mode];");sys.argv=['render','combos'];exec(compile(s,'combo-short-render','exec'),globals())

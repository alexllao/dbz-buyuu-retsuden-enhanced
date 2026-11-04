from pathlib import Path
groups=[
('Goku','Energy Blast|LR A;Consecutive Energy Blast|CD QCB A;Kiai Cannon|CD QCF A;Solar Flare|F LR A;Dash Elbow|QCB A;Jump Knee Lift|DB UF B;Flurry Kick|HCF B;Kamehameha|HCB A;Super Kamehameha|QCB F A;Sliding Kick|QCD B;Slashdown Kick|AIR QCD B;High Speed Move|F LR B;Super Meteor Smash|HCBF B'),
('Gohan','Energy Blast|LR A;Kiai Cannon|CD QCF A;Shock Wave|F LR A;Bakuretsu Punch|HCF A;Super Straight Punch|QCF A;Bakuretsu Kick|HCF B;Flying Kick|AIR QCD B;Masenko|HCFB A;Kamehameha|QCB F A;Sliding Kick|QCD B;High Speed Move|F LR B;Chou Bakuretsu Rush|HCBF B'),
('Piccolo','Energy Shot|LR A;Energy Shock|QCBD A;Shock Wave|F LR A;Dash Elbow|QCB A;Knee Upper|QCBD B;Sonic Kick|F LR B;Flying Kick|AIR QCD B;Special Beam Cannon|QCB F A;Light Grenade|HCB A;Sliding Kick|QCD B;Namekian Style: Moukou Retsuken|HCFB B'),
('Vegeta','Energy Blast|LR A;Consecutive Energy Blast|CD QCB A;Destructo Disc|CD QCF A;Ground Flare|QCF A;Slash Arrow Kick|QCF B;Driving Elbow Attack|QCB A;Super Crush|QCBD A;Big Bang Attack|HCFB A;Final Flash|QCB F A;Sliding Kick|QCD B;Final Brid Attack|HCBF B'),
('Trunks','Energy Cannon|LR A;Energy Slash|CD QCB A;Double Energy Blast|F LR A;Ground Flare|QCF A;Slashdown Kick|AIR QCD B;Consecutive Kick|F LR B;Bakuretsu Punch|HCF A;Burning Attack|QCB F A;Finish Blaster|HCFB A;Sliding Kick|QCD B;Tornado Breaker|HCBF B'),
('Cell','Energy Shot|LR A;Consecutive Energy Blast|CD QCB A;Kiai Cannon|CD QCF A;Wave Shock|QCBD A;Ground Slider|QCBD B;Dash Headbutt|QCB A;Ground Flare|AIR QCBD A;Special Beam Cannon|QCB F A;Kamehameha|HCB A;Sliding Kick|QCD B;High Speed Move|F LR B;Needle Rush|HCFB B'),
('A18','Flash Beam|LR A;Consecutive Energy Blast|CD QCB A;Energy Slash|F LR A;Critical Attack|QCF A;Slash Dance|AIR QCD B;Dash Elbow|QCB A;Dash Attack|QCBD A;Super Energy Wave|HCF A;Energy Flame|QCB F A;Sliding Kick|QCD B;Bloody Drive|HCFB B'),
('Krilin','Energy Blast|LR A;Consecutive Energy Blast|CD QCB A;Destructo Disc|CD QCF A;Solar Flare|F LR A;Bakuretsu Kick|HCF B;Kamehame Attack|QCB A;Kamehame Down Attack|AIR QCD A;Super Kiai Cannon|HCB A;Kamehameha|QCB F A;Sliding Kick|QCD B;Turtle School Style: Gekishuu Ranbu|HCBF B'),
('Freezer','Frieza Beam|LR A;Destructo Disc|CD QCF A;Frieza Cutter|F LR A;Ground Flare|QCF A;Tail Cut|F LR B;Head Attack|QCBD A;Dash Elbow|QCB A;Mega Buster|QCB F A;Death Ball|HCFB A;Sliding Kick|QCD B;Frieza Tail Buster|HCFB B;Frieza Psychokinesis|HCBF B'),
('Recoome','Energy Blast|LR A;Consecutive Energy Blast|CD QCB A;Energy Defense|F LR A;Mach Attack|QCF A;Power Bomb|QCBD A;Crush Down|QCF B;Recoome Kick|QCBD B;Fighting Bomber|HCB A;Eraser Gun|QCB F A;Sliding Kick|QCD B;Ultra Fighting Dance|F LR B;Recoome Death Driver|HCBF B'),
('Ginyu','Energy Blast|LR A;Energy Cannon|CD QCF A;Ground Explosion|F LR A;Ground Flare|QCF A;Straight Kick|F LR B;Dash Elbow|QCB A;Dynamite Punch|HCF A;Terra Smash|QCB F A;Sliding Kick|QCD B;Body Change|HCFB B')]
tokens={'LR':'← →','CD':'mantener ↓','QCB':'↓ ↙ ←','QCF':'↓ ↘ →','F':'→','DB':'↙','UF':'↗','HCF':'← ↙ ↓ ↘ →','HCB':'→ ↘ ↓ ↙ ←','HCBF':'→ ↘ ↓ ↙ ← →','HCFB':'← ↙ ↓ ↘ → ←','QCD':'→ ↘ ↓','QCBD':'← ↙ ↓','AIR':'en el aire:'}
intro='''## Controles y movimientos

**Mando por defecto:** A = puño, B = patada, C = cambiar entre suelo y vuelo; A+B = cargar ki. Si reasignas los botones, usa su función equivalente.

| Acción | Entrada |
| --- | --- |
| Caminar | Mantener adelante o atrás. |
| Correr hacia delante | Adelante, soltar brevemente, adelante y mantener. |
| Correr hacia atrás | Atrás, soltar brevemente, atrás y mantener. |
| Frenar | Soltar la dirección; conservar una breve inercia como en el original es la conducta elegida para la revisión v2. |
| Saltar / agacharse | Arriba / abajo. |
| Defender | Mantener atrás frente al ataque. |
| Cargar ki | Mantener A+B. |

Las flechas de las tablas suponen que miras a la **derecha**: → = hacia el rival, ← = alejarse. Invierte las direcciones cuando mires a la izquierda. Haz las direcciones en secuencia y pulsa el botón junto a la última. «Mantener ↓» indica carga previa; «en el aire» exige estar saltando o volando. La distancia, el ki y el estado de ambos luchadores también pueden condicionar una técnica.

**Guía del juego original:** combinaciones adaptadas de [StrategyWiki: Moves](https://strategywiki.org/wiki/Dragon_Ball_Z:_Buyuu_Retsuden/Moves), revisión [1096353](https://strategywiki.org/w/index.php?title=Dragon_Ball_Z:_Buyuu_Retsuden/Moves&oldid=1096353), aportada por el usuario. Se conservan sus nombres para facilitar la consulta. Las tablas describen los comandos originales, no una validación completa de todos los especiales en el parche.

El **High Speed Move** de Goku, Gohan y Cell usa → ← → + B: es una técnica ofensiva que puede cruzar al otro lado, no una esquiva universal. La propuesta de añadir a todos un cambio de lado cercano **sin golpe** queda guardada para después; todavía no está implementada.

'''
parts=[intro]
for name,rows in groups:
 parts.append(f'<details>\n<summary>{name}: movimientos</summary>\n\n| Técnica | Combinación |\n| --- | --- |\n')
 for row in rows.split(';'):
  label,code=row.split('|');items=code.split();button=items.pop();command=' '.join(tokens[x] for x in items)+' + '+button
  parts.append(f'| {label} | {command} |\n')
 parts.append('\n</details>\n\n')
parts.append('Atribución: colaboradores de StrategyWiki, enlace y revisión indicados arriba. Esta adaptación de sus tablas se ofrece bajo [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/); se han convertido los iconos a texto, añadido la correspondencia A/B y notas del proyecto. Esa licencia se aplica a esta adaptación documental, no declara una licencia para la ROM ni para todo el repositorio.\n\n')
p=Path('repository/README.md');text=p.read_text(encoding='utf-8');anchor='## Las cuatro mejoras de jugabilidad';assert '## Controles y movimientos' not in text;text=text.replace(anchor,''.join(parts)+anchor);p.write_text(text,encoding='utf-8')
Path('work/gameplay-review/moves-readme.json').write_text(__import__('json').dumps({'characters':len(groups),'moves':sum(len(x[1].split(';')) for x in groups),'source':'https://strategywiki.org/wiki/Dragon_Ball_Z:_Buyuu_Retsuden/Moves','revision':1096353,'read_via':'Browser DOM links for the direction icons; symbols converted to text.','license':'CC BY-SA 4.0 for adapted tables only'},indent=2))
print('README updated: 11 characters,',sum(len(x[1].split(';')) for x in groups),'moves')

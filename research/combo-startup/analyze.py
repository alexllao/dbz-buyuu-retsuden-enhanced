from pathlib import Path
import json
P=Path('work/combo-startup/matrix');a=json.loads((P/'before.json').read_text())['cases'];b=json.loads((P/'after.json').read_text())['cases'];assert len(a)==len(b)==168
key=lambda t:(t['cid'],t['port'],t['side'],t['context'],t['speed'])
assert [key(t) for t in a]==[key(t) for t in b]
print('damage differences',[(key(x),x['damage'],y['damage'],y['fastUsed']) for x,y in zip(a,b) if x['damage']!=y['damage']])
print('KI differences',[(key(x),x['kiDebits'],y['kiDebits']) for x,y in zip(a,b) if x['kiDebits']!=y['kiDebits']])
print('lost starts',[(key(x),x['accepted'],y['accepted']) for x,y in zip(a,b) if x['accepted'] is not None and y['accepted'] is None])
print('fast cases',sum(t['fastUsed'] for t in b));print('solo delta',[(key(x),x['startup'],y['startup']) for x,y in zip(a,b) if x['context']=='solo'])

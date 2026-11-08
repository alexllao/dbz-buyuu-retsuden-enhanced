from pathlib import Path
import sys,json
P=Path('work/barrage-five');P.mkdir(exist_ok=True);which=sys.argv[1] if len(sys.argv)>1 else 'before';rompath='work/knockdown-k4/candidate.bin' if which=='before' else 'work/barrage-five/candidate.bin'
src=Path('work/hits-hud-v3/prepare.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0].replace("romfile=BASE/'work/hits-hud-v3/candidate.bin'",f"romfile=BASE/'{rompath}'")
for old in [0x104,0x106,0x117,0x120,0x121,0x122,0x124]:src=src.replace('b+'+hex(old)+')','b+'+hex(old+0xc00)+')')
sys.argv=['prepare','0'];exec(compile(src,'barrage-probe','exec'),globals())
try:
 restore(Path('work/responsive-v3/routes/0/charged.state').read_bytes())
 wb(P1+0xbe,0);wb(P2+0xbe,0)
 for b,x,facing in [(P1,300,0),(P2,420,1)]:ww(b+0xa,x);ww(b+0xc,0);wb(b+0x59,facing)
 for _ in range(15):tick()
 schedule=[['DOWN']]*4+[['DOWN','RIGHT']]*4+[['RIGHT']]*4+[['RIGHT','A']]*3+[[]]*300;r=[]
 for f,k in enumerate(schedule):
  tick(k);r.append(dict(f=f,p=st(P1),e=st(P2),pose=rb(P1+4),native=bytes(ram[P1:P1+0x128]).hex() if False else [rb(P1+i) for i in range(0x128)]))
 (P/f'{which}.json').write_text(json.dumps(r));print([(t['f'],hex(t['p']['program']),t['pose'],t['p']['ki']) for a,t in zip(r,r[1:]) if (t['p']['program'],t['pose'])!=(a['p']['program'],a['pose'])]);print('contacts',[(t['f'],t['e']['hp'],t['p']['hits']) for a,t in zip(r,r[1:]) if t['e']['hp']<a['e']['hp']])
finally:core.retro_unload_game();core.retro_deinit()

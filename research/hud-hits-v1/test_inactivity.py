from pathlib import Path
import sys,json,hashlib
sys.argv=['probe','5'];raw=Path('work/hits-hud/prepare.py').read_text().split('try:\n for j,entry in enumerate(steps[:-1]):')[0];exec(compile(raw,'inactivity-setup','exec'),globals())
try:
 restore((out/'low-hp-charged.state').read_bytes());ww(P1+0xa,300);ww(P2+0xa,332);ww(P1+0xc,0);ww(P2+0xc,0);wb(P1+0x59,0);wb(P2+0x59,1)
 for _ in range(8):tick()
 before=rw(P2+0x24);rows=[];hit=None;cleared=None
 for f in range(1300):
  old=st(P2);tick(['A'] if f<6 else []);now=st(P2);rows.append(dict(f=f,before=old,after=now))
  if now['hp']<before and hit is None:hit=f;value=now['stun'];assert 0<value<now['threshold']
  if hit is not None and f>hit and now['stun']==0:
   cleared=f;assert old['periodic']>=598 and now['periodic']==0,(f,old,now);break
  if hit is not None:assert now['stun']==value and now['hp']==rows[hit]['after']['hp']
 assert hit is not None and cleared is not None
 Path('work/hits-hud/inactivity-validation.json').write_text(json.dumps(dict(passed=True,romSha256=hashlib.sha256(rom).hexdigest(),hitFrame=hit,clearFrame=cleared,stunAfterHit=value,elapsedDisplayFrames=cleared-hit,nativeCounterBeforeClear=rows[-1]['before']['periodic'],stunOnlyClearedAfterNativeInactivityLimit=True,rows=rows),indent=2));print(hit,cleared,value,flush=True)
finally:core.retro_unload_game();core.retro_deinit()

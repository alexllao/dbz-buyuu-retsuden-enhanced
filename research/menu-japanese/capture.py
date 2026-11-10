from pathlib import Path
import json,hashlib
menuOut=Path('outputs/Selector-Namek-japones');menuOut.mkdir(parents=True,exist_ok=True)
source=Path('work/combo-charge-all/prepare-roster.py').read_text().split('\nif any(')[0].replace('work/combo-charge-all/candidate.bin','work/menu-japanese/candidate.bin')
source=source.replace(" press(['START'],3,20)"," save_image(menuOut/(promoSlug+'.png'))\n (menuOut/(promoSlug+'.state')).write_bytes(snap())\n return")
exec(compile(source,'native-japanese-menu-capture','exec'),globals())
try:
 for promoSlug in ['original','normal','aldea','porunga']:boot_stage(0,8)
 (menuOut/'procedencia.json').write_text(json.dumps(dict(romSha256=hashlib.sha256(rom).hexdigest(),captures=selectionProof,method='Native menu buttons and direct framebuffer. No text overlay, stage writes or replacement font.'),indent=2))
finally:core.retro_unload_game();core.retro_deinit()

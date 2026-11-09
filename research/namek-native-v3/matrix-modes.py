from pathlib import Path
s=Path('work/namek-native/matrix-modes.py').read_text().replace('work/namek-native/','work/namek-native-v3/').replace("O=Path('work/namek-native')","O=Path('work/namek-native-v3')")
exec(compile(s,'v3-mode-validation','exec'),globals())

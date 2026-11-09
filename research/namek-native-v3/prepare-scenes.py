from pathlib import Path
s=Path('work/namek-native/prepare-scenes.py').read_text().replace('work/namek-native/','work/namek-native-v3/').replace('work/namek-native-v3/states','work/namek-native-v3/states-reviewed')
exec(compile(s,'v3-native-scenes','exec'),globals())

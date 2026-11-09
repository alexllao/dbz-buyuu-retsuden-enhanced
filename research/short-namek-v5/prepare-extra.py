from pathlib import Path
s=Path('work/namek-native/prepare-scenes.py').read_text().replace('work/namek-native/','work/namek-native-v5/').replace('work/namek-native-v5/states','work/namek-native-v5/states-reviewed').replace('[(0,8),(1,0),(3,0),(5,0)]','[(3,0)]')
exec(compile(s,'v5-short-extra-seeds','exec'),globals())

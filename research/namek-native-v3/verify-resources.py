from pathlib import Path
s=Path('work/namek-native/verify-resources.py').read_text().replace('work/namek-native/','work/namek-native-v3/')
exec(compile(s,'v3-resource-verification','exec'),globals())

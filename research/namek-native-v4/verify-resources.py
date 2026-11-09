from pathlib import Path
s=Path('work/namek-native/verify-resources.py').read_text().replace('work/namek-native/','work/namek-native-v4/')
s=s.replace(' return dict(label=label,'," assert nativeVariant!='normal' or nativeCram[11]==nativeCram[12]\n return dict(normalSkyGreenEntriesEqual=(nativeCram[11]==nativeCram[12]) if nativeVariant=='normal' else None,label=label,")
exec(compile(s,'v4-resource-verification','exec'),globals())

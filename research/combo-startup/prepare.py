from pathlib import Path
P=Path('work/combo-startup');P.mkdir(exist_ok=True)
java=Path('work/scripts/AssembleInputLinks.java').read_text().replace('AssembleInputLinks','AssembleComboStartup').replace('base=0x3de000','base=0x3df000');Path('work/scripts/AssembleComboStartup.java').write_text(java)
(P/'assemble.ps1').write_text(Path('work/input-links/assemble.ps1').read_text().replace('AssembleInputLinks.java','AssembleComboStartup.java'))
labels=dict(l.split('=') for l in Path('work/input-links/inputs.labels.txt').read_text().splitlines())
s=(P/'startup.asm').read_text();import re
s=re.sub(r'jmp 0x003de[0-9a-f]+\.l',f"jmp 0x{int(labels['round_reset'],16):08x}.l",s)
(P/'startup.asm').write_text(s,encoding='utf-8')

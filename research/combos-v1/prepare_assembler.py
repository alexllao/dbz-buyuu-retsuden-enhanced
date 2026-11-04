from pathlib import Path
p=Path('work/scripts/AssembleSide.java');s=p.read_text().replace('public class AssembleSide','public class AssembleCombo').replace('long base=0x3e0000','long base=0x3d0000')
Path('work/scripts/AssembleCombo.java').write_text(s)
p=Path('work/side-switch/assemble_side.ps1');s=p.read_text().replace('AssembleSide.java','AssembleCombo.java')
Path('work/combos/assemble.ps1').write_text(s)

param([string]$Source='work/assembler-test.asm',[string]$Output='work/assembler-test')
$env:JAVA_HOME='C:/Users/usuari/Documents/Codex/tools/java21/jdk-21.0.12.1+1'
$env:APPDATA=(Resolve-Path work/appdata).Path
$env:JAVA_TOOL_OPTIONS='-Duser.home=C:/Users/usuari/Documents/Codex/2026-11-03/sa/work/ghidra-home'
& 'C:/Users/usuari/Documents/Codex/tools/ghidra/ghidra_12.1.4_PUBLIC/support/analyzeHeadless.bat' (Resolve-Path work/ghidra).Path DBZ -process original.bin -noanalysis -readOnly -scriptPath (Resolve-Path work/scripts).Path -postScript AssembleAura.java (Join-Path (Get-Location) $Source) (Join-Path (Get-Location) $Output) -log (Join-Path (Get-Location) 'work/assemble-ghidra.log') -scriptlog (Join-Path (Get-Location) 'work/assemble-script.log')
exit $LASTEXITCODE

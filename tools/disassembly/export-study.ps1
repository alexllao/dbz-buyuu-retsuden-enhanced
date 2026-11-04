param(
  [Parameter(Mandatory=$true)][string]$GhidraHome,
  [Parameter(Mandatory=$true)][string]$Rom,
  [string]$JavaHome,
  [string]$WorkDir='work/local-disassembly',
  [string]$Output='outputs/codigo-asm-castellano',
  [string]$CapstoneDir,
  [string]$PatchRepo
)
$ErrorActionPreference='Stop'
$romPath=(Resolve-Path -LiteralPath $Rom).Path
$expected='217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557'
if((Get-FileHash -LiteralPath $romPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expected){throw 'La ROM no coincide con la base japonesa auditada.'}
$taskWork=[IO.Path]::GetFullPath($WorkDir)
$taskOutput=[IO.Path]::GetFullPath($Output)
$uniqueProject=Join-Path $taskWork ('ghidra-study-'+[Guid]::NewGuid().ToString('N').Substring(0,12))
$listingDir=Join-Path $uniqueProject 'export'
New-Item -ItemType Directory -Force -Path $uniqueProject,$listingDir,$taskOutput | Out-Null
if($JavaHome){$env:JAVA_HOME=[IO.Path]::GetFullPath($JavaHome)}
$launcher=Join-Path $GhidraHome 'support/analyzeHeadless.bat'
if(-not(Test-Path -LiteralPath $launcher)){throw 'No se encuentra analyzeHeadless.bat en GhidraHome.'}
# Always create a new private analysis project; never edit the project's working DBZ database.
& $launcher $uniqueProject Estudio -import $romPath -loader BinaryLoader -processor '68000:BE:32:default' -loader-baseAddr 0 -analysisTimeoutPerFile 90 -scriptPath $PSScriptRoot -preScript SeedSpanishStudy.java $listingDir -postScript ExpandSpanishTables.java $listingDir -postScript ExportSpanishStudy.java $listingDir -log (Join-Path $uniqueProject 'analysis.log') -scriptlog (Join-Path $uniqueProject 'scripts.log')
if($LASTEXITCODE -ne 0){throw 'Ghidra no completó la exportación. Consulta los registros del proyecto privado.'}
$pythonArgs=@((Join-Path $PSScriptRoot 'generate-study-es.py'),'--rom',$romPath,'--listing',(Join-Path $listingDir 'instructions.tsv'),'--functions',(Join-Path $listingDir 'functions.tsv'),'--out',$taskOutput)
if($CapstoneDir){$pythonArgs+=@('--capstone-dir',[IO.Path]::GetFullPath($CapstoneDir))}
if($PatchRepo){$pythonArgs+=@('--patch-repo',[IO.Path]::GetFullPath($PatchRepo))}
& python @pythonArgs
if($LASTEXITCODE -ne 0){throw 'No se pudo generar el mapa de estudio.'}
Write-Output ('Mapa de estudio generado en '+$taskOutput)

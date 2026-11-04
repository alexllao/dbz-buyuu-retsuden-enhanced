param(
  [string]$GhidraHome=$env:GHIDRA_HOME,
  [string]$JavaHome=$env:JAVA_HOME,
  [string]$Rom
)
$ErrorActionPreference='Stop'
$repoRoot=(Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
if (-not $Rom) { $Rom=Join-Path $repoRoot 'roms/original.bin' }
$romPath=(Resolve-Path -LiteralPath $Rom).Path
if ((Get-FileHash -LiteralPath $romPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne '217fc312deeced6bbe3caa02ed3f72e067d6dbd6a0ee64a281ebf2e60f479557') { throw 'La ROM base no coincide con el SHA-256 admitido.' }
if (-not $GhidraHome -or -not $JavaHome) { throw 'Facilita -GhidraHome y -JavaHome o define GHIDRA_HOME y JAVA_HOME.' }
$launcher=Join-Path $GhidraHome 'support/analyzeHeadless.bat'
if (-not (Test-Path -LiteralPath $launcher)) { throw 'No se encuentra analyzeHeadless.bat.' }
$scratch=Join-Path $repoRoot ('build-local/assembly/'+[guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $scratch -Force | Out-Null
$scratchHome=Join-Path $scratch 'home'
$appData=Join-Path $scratch 'appdata'
New-Item -ItemType Directory -Path $scratchHome,$appData -Force | Out-Null
$env:JAVA_HOME=(Resolve-Path -LiteralPath $JavaHome).Path
$env:JAVA_TOOL_OPTIONS='-Duser.home="'+$scratchHome+'"'
$env:APPDATA=$appData
$output=Join-Path $scratch 'controls'
& $launcher $scratch BuildControls -import $romPath -loader BinaryLoader -processor '68000:BE:32:default' -noanalysis -scriptPath $PSScriptRoot -postScript AssembleControls.java (Join-Path $repoRoot 'src/gameplay/v1/controls.asm') $output -deleteProject -log (Join-Path $scratch 'ghidra.log') -scriptlog (Join-Path $scratch 'script.log')
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath ($output+'.bin'))) { throw ('El ensamblado no ha finalizado. Consulta '+$scratch) }
& node (Join-Path $PSScriptRoot 'verify-assembly.mjs') ($output+'.bin')
if ($LASTEXITCODE -ne 0) { throw 'Los bytes ensamblados no coinciden con la versión revisada.' }

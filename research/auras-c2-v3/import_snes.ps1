Add-Type -AssemblyName System.Drawing
$im=[System.Drawing.Bitmap]::FromFile((Join-Path (Get-Location) 'repository/assets/references/super-butoden-2/Aura-rayos-variante-3.png'))
$xmin=110;$xmax=0;$ymin=$im.Height;$ymax=0
for($y=0;$y -lt $im.Height;$y++){for($x=0;$x -lt [Math]::Min(106,$im.Width);$x++){$p=$im.GetPixel($x,$y);if($p.R -gt 80 -and $p.G -gt 60){$xmin=[Math]::Min($xmin,$x);$xmax=[Math]::Max($xmax,$x);$ymin=[Math]::Min($ymin,$y);$ymax=[Math]::Max($ymax,$y)}}}
$bytes=[byte[]]::new(80*128*4)
for($y=0;$y -lt 128;$y++){for($x=0;$x -lt 80;$x++){
 $sx=[Math]::Min($im.Width-1,[int]($xmin+($x+0.5)*($xmax-$xmin+1)/80));$sy=[Math]::Min($im.Height-1,[int]($ymin+($y+0.5)*($ymax-$ymin+1)/128));$p=$im.GetPixel($sx,$sy);$i=4*($y*80+$x)
 $bytes[$i]=$p.R;$bytes[$i+1]=$p.G;$bytes[$i+2]=$p.B;$bytes[$i+3]=[byte]$(if($p.R -gt 80 -and $p.G -gt 60){255}else{0})
}}
[IO.File]::WriteAllBytes((Join-Path (Get-Location) 'work/auras/v3/snes-aura-source.rgba'),$bytes);$im.Dispose()

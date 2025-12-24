# Aggregate per-run results and pick best temperature per model
Set-Location -Path (Split-Path -Path $MyInvocation.MyCommand.Path -Parent)

$files = Get-ChildItem -Path . -Filter 'results*.json' | Sort-Object LastWriteTime
if ($files.Count -eq 0) { Write-Error "No results-*.json files found in $(Get-Location)"; exit 1 }

$entries = @()
foreach ($f in $files) {
    $raw = Get-Content $f.FullName -Raw
    try { $j = $raw | ConvertFrom-Json } catch { Write-Warning "Failed to parse $($f.Name)"; continue }
    # j is an array or object; try to extract model entry
    if ($j -is [System.Collections.IEnumerable]) { $me = $j[0] } else { $me = $j }
    $model = $me.model
    $available = $me.available -eq $true
    $tests = $me.tests
    # compute per-test scores
    $math = 0; $trans = 0; $summ = 0; $echo = 0; $latList = @(); $haveMath=$false; $haveTrans=$false; $haveSumm=$false; $haveEcho=$false
    foreach ($t in $tests) {
        if ($t.id -eq 'math_test') { if ($t.score -ne $null) { $math = [double]$t.score * 100; $haveMath=$true } }
        if ($t.id -eq 'translate_test') { if ($t.score -ne $null) { $trans = [double]$t.score * 100; $haveTrans=$true } }
        if ($t.id -eq 'summarize_test') { if ($t.score -ne $null) { $summ = [double]$t.score * 100; $haveSumm=$true } }
        if ($t.id -eq 'echo_test') { if ($t.score -ne $null) { $echo = [double]$t.score * 100; $haveEcho=$true } elseif ($t.success) { $echo = 100; $haveEcho=$true } }
        if ($t.elapsed_ms) { $latList += $t.elapsed_ms }
    }
    $meanLat = $null
    if ($latList.Count -gt 0) { $meanLat = [math]::Round(($latList | Measure-Object -Average).Average) }
    if ($meanLat -ne $null) { if ($meanLat -le 2000) { $latScore=100 } elseif ($meanLat -le 5000) { $latScore=80 } elseif ($meanLat -le 10000) { $latScore=50 } else { $latScore=20 } } else { $latScore = 0 }
    $availScore = ($available ? 100 : 0)
    $overall = 0.0
    $overall += ($math * 30/100)
    $overall += ($trans * 25/100)
    $overall += ($summ * 20/100)
    $overall += ($echo * 10/100)
    $overall += ($availScore * 5/100)
    $overall += ($latScore * 10/100)

    # parse temperature from filename if present (pattern -T0 or -T0_7)
    $temp = $null
    if ($f.Name -match '-T(\d+(_\d+)?)') { $tempRaw = $Matches[1]; $temp = $tempRaw -replace '_', '.' }

    $entries += [pscustomobject]@{
        file = $f.Name
        model = $model
        temperature = $temp
        math = [math]::Round($math,2)
        translate = [math]::Round($trans,2)
        summarize = [math]::Round($summ,2)
        echo = [math]::Round($echo,2)
        availability = $availScore
        latency_ms = $meanLat
        latency_score = $latScore
        overall = [math]::Round($overall,2)
    }
}

# Group by model and pick best temperature run (highest overall)
$grouped = $entries | Group-Object -Property model
$bestPerModel = @()
foreach ($g in $grouped) {
    $best = $g.Group | Sort-Object -Property overall -Descending | Select-Object -First 1
    $bestPerModel += $best
}

# Also rank all runs (model+temp) overall
$allRunsSorted = $entries | Sort-Object -Property overall -Descending

# Write outputs
$bestPerModel | ConvertTo-Json -Depth 5 | Out-File -FilePath .\batch_sweep_report.json -Encoding utf8
$csvPath = ".\batch_sweep_report.csv"
$bestPerModel | Select-Object model,temperature,overall,math,translate,summarize,echo,availability,latency_ms,latency_score | Export-Csv -Path $csvPath -NoTypeInformation -Encoding utf8

$txt = @()
$txt += "Batch Sweep Report - $(Get-Date -Format o)"
$txt += "Top run per model (best temperature)"
foreach ($b in $bestPerModel | Sort-Object -Property overall -Descending) {
    $txt += "Model: $($b.model) | Temp: $($b.temperature) | Overall: $($b.overall) | Math: $($b.math) | Translate: $($b.translate) | Summarize: $($b.summarize) | Echo: $($b.echo) | Lat_ms: $($b.latency_ms) | LatScore: $($b.latency_score)"
}
$txt += ""
$txt += "Top 5 runs (model+temp) overall:"
$i=0
foreach ($r in $allRunsSorted | Select-Object -First 5) { $i++; $txt += "$i. Model: $($r.model) | Temp: $($r.temperature) | Overall: $($r.overall)" }

$txt += ""; $txt += "Recommendation (top-3 model+temp):"
$top3 = $allRunsSorted | Select-Object -First 3
foreach ($r in $top3) { $txt += "- $($r.model) (temp=$($r.temperature)) — Overall=$($r.overall); Math=$($r.math), Translate=$($r.translate), Summarize=$($r.summarize), Echo=$($r.echo), Lat_ms=$($r.latency_ms)" }

$txt | Out-File -FilePath .\batch_sweep_report.txt -Encoding utf8
Write-Output "Wrote batch_sweep_report.json, .csv and .txt (best per-model and top runs)"

# Print top-3 to console for immediate visibility
Write-Output "Top 3 runs (model+temp):"
$k=1
foreach ($r in $top3) { Write-Output "$k) $($r.model)  temp=$($r.temperature)  overall=$($r.overall)"; $k++ }

# Exit
exit 0

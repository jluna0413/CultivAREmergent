# Aggregate stability runs (results files with -rN) into stats per model+temp
Set-Location -Path (Split-Path -Path $MyInvocation.MyCommand.Path -Parent)

$files = Get-ChildItem -Path . -Filter 'results*-r*.json' | Sort-Object Name
if ($files.Count -eq 0) { Write-Error "No stability result files found"; exit 1 }

$rows = @()
foreach ($f in $files) {
    $raw = Get-Content $f.FullName -Raw
    try { $j = $raw | ConvertFrom-Json } catch { Write-Warning "Failed to parse $($f.Name)"; continue }
    $me = if ($j -is [System.Collections.IEnumerable]) { $j[0] } else { $j }
    $model = $me.model
    # parse temp and repeat index from filename: results-{safe}-T{tempSafe}-r{n}.json or results-{safe}-Tbase-r{n}.json
    $temp = $null; $r = $null
    if ($f.Name -match '-T([^\-]+)-r(\d+)') { $temp = ($Matches[1] -replace '_','.') ; $r=[int]$Matches[2] }
    else { $temp = ''; $r = 0 }

    # compute overall score as aggregator did
    $math=0;$trans=0;$summ=0;$echo=0;$latlist=@();$avail=($me.available -eq $true)
    foreach ($t in $me.tests) {
        if ($t.id -eq 'math_test') { if ($t.score -ne $null) { $math = [double]$t.score *100 } }
        if ($t.id -eq 'translate_test') { if ($t.score -ne $null) { $trans = [double]$t.score *100 } }
        if ($t.id -eq 'summarize_test') { if ($t.score -ne $null) { $summ = [double]$t.score *100 } }
        if ($t.id -eq 'echo_test') { if ($t.score -ne $null) { $echo = [double]$t.score *100 } elseif ($t.success) { $echo=100 } }
        if ($t.elapsed_ms) { $latlist += $t.elapsed_ms }
    }
    $meanLat = $null; if ($latlist.Count -gt 0) { $meanLat = [math]::Round(($latlist | Measure-Object -Average).Average) }
    if ($meanLat -ne $null) { if ($meanLat -le 2000) { $latScore=100 } elseif ($meanLat -le 5000) { $latScore=80 } elseif ($meanLat -le 10000) { $latScore=50 } else { $latScore=20 } } else { $latScore=0 }
    $availScore = ($avail ? 100 : 0)
    $overall = 0.0; $overall += ($math * 30/100); $overall += ($trans * 25/100); $overall += ($summ * 20/100); $overall += ($echo * 10/100); $overall += ($availScore * 5/100); $overall += ($latScore * 10/100)

    $rows += [pscustomobject]@{file=$f.Name; model=$model; temp=$temp; repeat=$r; math=$math; translate=$trans; summarize=$summ; echo=$echo; availability=$availScore; latency_ms=$meanLat; latency_score=$latScore; overall=[math]::Round($overall,2)}
}

# Group by model+temp and compute mean/std
$grouped = $rows | Group-Object -Property @{Expression={$_.model+'/'+$_.temp}} 
$summary = @()
foreach ($g in $grouped) {
    $key = $g.Name
    $parts = $key -split '/'
    $model = $parts[0]; $temp = $parts[1]
    $vals = $g.Group
    $count = $vals.Count
    $meanOverall = [math]::Round(($vals | Measure-Object -Property overall -Average).Average,2)
    # compute standard deviation (population)
    $sumSquares = 0.0
    foreach ($v in $vals) { $diff = ($v.overall - $meanOverall); $sumSquares += ($diff * $diff) }
    if ($count -gt 0) { $stdOverall = [math]::Round([math]::Sqrt($sumSquares / $count),2) } else { $stdOverall = 0 }
    $meanMath = [math]::Round(($vals | Measure-Object math -Average).Average,2)
    $meanTrans = [math]::Round(($vals | Measure-Object translate -Average).Average,2)
    $meanSumm = [math]::Round(($vals | Measure-Object summarize -Average).Average,2)
    $meanEcho = [math]::Round(($vals | Measure-Object echo -Average).Average,2)
    $meanLat = [math]::Round(($vals | Where-Object { $_.latency_ms -ne $null } | Measure-Object latency_ms -Average).Average,0)

    $summary += [pscustomobject]@{model=$model; temp=$temp; runs=$count; mean_overall=$meanOverall; std_overall=$stdOverall; mean_math=$meanMath; mean_translate=$meanTrans; mean_summarize=$meanSumm; mean_echo=$meanEcho; mean_latency_ms=$meanLat}
}

$summary | Sort-Object mean_overall -Descending | ConvertTo-Json -Depth 5 | Out-File .\stability_report.json -Encoding utf8
$summary | Sort-Object mean_overall -Descending | Format-Table | Out-String | Out-File .\stability_report.txt -Encoding utf8

Write-Output "Wrote stability_report.json and stability_report.txt"
Write-Output "Top groups:"
$summary | Sort-Object mean_overall -Descending | Select-Object -First 5 | ForEach-Object { Write-Output "$($_.model) temp=$($_.temp) mean_overall=$($_.mean_overall) std_overall=$($_.std_overall) runs=$($_.runs)" }

# Run stability tests: repeat N times for selected model+temp combos and aggregate results
Set-Location -Path (Split-Path -Path $MyInvocation.MyCommand.Path -Parent)

$Endpoint = 'http://127.0.0.1:11436/v1'
$repeats = 3
$models = @(
    @{ model = 'gemma3:1b'; temp = 0.7 },
    @{ model = 'gemma3:270m'; temp = 0.0 },
    @{ model = 'cogito:3b-v1-preview-llama-q4_K_M'; temp = 0.0 }
)

$resultsFiles = @()

foreach ($m in $models) {
    for ($i = 1; $i -le $repeats; $i++) {
        $safe = ($m.model -replace '[:/\\]','_')
        $tempSafe = ($m.temp.ToString() -replace '\.','_')
        $out = "results-stability-$($safe)-T$($tempSafe)-run$i.json"
        Write-Host "Run $i/$repeats for $($m.model) (temp=$($m.temp)) -> $out"
        & .\run_eval.ps1 -Models @($m.model) -Endpoint $Endpoint -OutFile $out -Temperature $m.temp
        $resultsFiles += $out
        Start-Sleep -Milliseconds 400
    }
}

# Aggregate: compute per-model, per-test statistics across repeats
$summary = @()
foreach ($m in $models) {
    $safe = ($m.model -replace '[:/\\]','_')
    $tempSafe = ($m.temp.ToString() -replace '\.','_')
    $pattern = "results-stability-$safe-T$tempSafe-run*.json"
    $files = Get-ChildItem -Path . -Filter $pattern | Sort-Object Name
    if ($files.Count -eq 0) { Write-Warning "No files for $($m.model) temp $($m.temp)"; continue }

    $perTest = @{}
    $latencies = @()
    foreach ($f in $files) {
        try { $j = Get-Content $f.FullName -Raw | ConvertFrom-Json } catch { Write-Warning "Failed parse $($f.Name)"; continue }
        $entry = $j[0]
        foreach ($t in $entry.tests) {
            if (-not $perTest.ContainsKey($t.id)) { $perTest[$t.id] = @{scores = @(); success = 0; empty = 0; lat = @()} }
            $rec = $perTest[$t.id]
            if ($t.score -ne $null) { $rec.scores += [double]$t.score * 100 } else { if ($t.success) { $rec.empty += 0 } else { $rec.empty += 1 } }
            if ($t.success) { $rec.success += 1 }
            if ($t.elapsed_ms) { $rec.lat += $t.elapsed_ms; $latencies += $t.elapsed_ms }
        }
    }

    # Compute stats
    $testsSummary = @{}
    foreach ($k in $perTest.Keys) {
        $rec = $perTest[$k]
        $scores = $rec.scores
        $count = $scores.Count
        if ($count -gt 0) {
            $mean = [math]::Round(($scores | Measure-Object -Average).Average,2)
            $std = 0
            if ($count -gt 1) {
                $avg = ($scores | Measure-Object -Average).Average
                $sumSq = ($scores | ForEach-Object { ([double]$_ - $avg) * ([double]$_ - $avg) } | Measure-Object -Sum).Sum
                $std = [math]::Round([math]::Sqrt($sumSq / ($count - 1)),2)
            }
        } else { $mean = $null; $std = $null }
        $testsSummary[$k] = @{ mean = $mean; std = $std; success_runs = $rec.success; empty_count = $rec.empty; samples = $count }
    }

    $meanLat = $null
    $stdLat = $null
    if ($latencies.Count -gt 0) { $meanLat = [math]::Round(($latencies | Measure-Object -Average).Average); if ($latencies.Count -gt 1) { $avg = ($latencies | Measure-Object -Average).Average; $sumSq = ($latencies | ForEach-Object { ([double]$_ - $avg) * ([double]$_ - $avg) } | Measure-Object -Sum).Sum; $stdLat = [math]::Round([math]::Sqrt($sumSq / ($latencies.Count - 1))) } }

    $summary += [pscustomobject]@{
        model = $m.model
        temp = $m.temp
        runs = $files.Count
        per_test = $testsSummary
        latency_mean_ms = $meanLat
        latency_std_ms = $stdLat
    }
}

# Write report files
$summary | ConvertTo-Json -Depth 6 | Out-File -FilePath .\stability_report.json -Encoding utf8
$txt = @()
$txt += "Stability Report - $(Get-Date -Format o)"
foreach ($s in $summary) {
    $txt += "Model: $($s.model)  temp=$($s.temp)  runs=$($s.runs)  mean_latency_ms=$($s.latency_mean_ms)  latency_std_ms=$($s.latency_std_ms)"
    foreach ($k in $s.per_test.Keys) {
        $v = $s.per_test[$k]
        $txt += "  Test: $k | mean_score=$($v.mean) | std=$($v.std) | success_runs=$($v.success_runs) | empty_count=$($v.empty_count) | samples=$($v.samples)"
    }
}
$txt | Out-File -FilePath .\stability_report.txt -Encoding utf8

Write-Host "Wrote stability_report.json and stability_report.txt"

# Print short summary
Write-Host "Short summary:"
foreach ($s in $summary) { Write-Host "$($s.model) (temp=$($s.temp)) runs=$($s.runs) mean_latency_ms=$($s.latency_mean_ms)" }

exit 0

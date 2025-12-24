param(
    [string[]] $Models = @(
        'gemma3:270m',
        'gemma3:1b',
        'gemma3:4b-it-q4_K_M',
        'qwen3:0.6b',
        'qwen3-vl:2b-thinking-q4_K_M',
        'qwen3-vl:2b-instruct-q4_K_M',
        'cogito:3b-v1-preview-llama-q4_K_M',
        'granite4:micro-h'
    ),
    [string] $Endpoint = 'http://127.0.0.1:11436/v1',
    [int] $TimeoutSec = 300
)

if (-not (Test-Path '.\scores.log')) { New-Item -Path '.\scores.log' -ItemType File -Force | Out-Null }

$report = [ordered]@{
    run_time = (Get-Date).ToString('o')
    endpoint = $Endpoint
    models = @()
}

function Run-One([string]$model) {
    $safe = ($model -replace '[:/\\]','_')
    $outFile = "results-$($safe).json"
    Write-Output "Running eval for $model -> $outFile"
    # Use current working directory as script directory (interactive-friendly)
    $scriptDir = (Get-Location).Path
    $runEvalPath = Join-Path -Path $scriptDir -ChildPath 'run_eval.ps1'
    if (-not (Test-Path $runEvalPath)) { Write-Error "Could not find run_eval.ps1 at $runEvalPath"; return $null }
    & $runEvalPath -Models @($model) -Endpoint $Endpoint -OutFile $outFile -TimeoutSec $TimeoutSec | Out-Null

    # Find the last run_id for this model in scores.log
    $lines = Get-Content .\scores.log -ErrorAction SilentlyContinue | Where-Object { $_ -match '"model"' -or $_ -match '"run_id"' -or $_ -match '"test_id"' }
    # parse JSON objects from file; more robust: read all and ConvertFrom-Json by splitting blank lines
    $raw = (Get-Content .\scores.log -Raw)
    $objs = @()
    $parts = $raw -split "\r?\n\r?\n"
    foreach ($p in $parts) {
        $t = $p.Trim()
        if ($t -ne '') {
            try { $objs += $t | ConvertFrom-Json } catch { }
        }
    }
    $runs = $objs | Where-Object { $_.model -eq $model } | Select-Object -Property run_id -Unique
    if (-not $runs -or $runs.Count -eq 0) { Write-Warning "No score entries found for $model"; return $null }
    $runId = ($runs | Select-Object -Last 1).run_id
    $entries = $objs | Where-Object { $_.model -eq $model -and $_.run_id -eq $runId }
    return @{ run_id = $runId; entries = $entries }
}

function Score-Model($model,$entries) {
    # categories: Availability, Echo, Math, Translate, Summarize, Latency
    $avail = 0; $echo = 0; $math = 0; $translate = 0; $summ = 0; $latencies = @()
    foreach ($e in $entries) {
        if ($e.test_id -eq 'echo_test') {
            if ($e.score -ne $null) { $echo = [double]$e.score * 100 } elseif ($e.success) { $echo = 100 }
            if ($e.elapsed_ms) { $latencies += $e.elapsed_ms }
        }
        if ($e.test_id -eq 'math_test') {
            if ($e.score -ne $null) { $math = [double]$e.score * 100 } elseif ($e.success) { $math = 0 }
            if ($e.elapsed_ms) { $latencies += $e.elapsed_ms }
        }
        if ($e.test_id -eq 'translate_test') {
            if ($e.score -ne $null) { $translate = [double]$e.score * 100 }
            if ($e.elapsed_ms) { $latencies += $e.elapsed_ms }
        }
        if ($e.test_id -eq 'summarize_test') {
            if ($e.score -ne $null) { $summ = [double]$e.score * 100 } elseif ($e.success) { $summ = 100 }
            if ($e.elapsed_ms) { $latencies += $e.elapsed_ms }
        }
        if ($e.test_id -eq 'echo_test' -and $e.available -ne $null) { if ($e.available) { $avail = 100 } }
    }
    if ($latencies.Count -gt 0) { $meanLat = [math]::Round( ($latencies | Measure-Object -Average).Average ) } else { $meanLat = $null }

    # Latency scoring: <=2000ms =>100, <=5000ms => 80, <=10000ms =>50, >10000 =>20
    $latScore = 0
    if ($meanLat -ne $null) {
        if ($meanLat -le 2000) { $latScore = 100 } elseif ($meanLat -le 5000) { $latScore = 80 } elseif ($meanLat -le 10000) { $latScore = 50 } else { $latScore = 20 }
    }

    # Weights: Math 30, Translate 25, Summarize 20, Echo 10, Availability 5, Latency 10
    $weights = @{ math=30; translate=25; summarize=20; echo=10; avail=5; lat=10 }
    $overall = 0.0
    $overall += ($math * $weights.math / 100)
    $overall += ($translate * $weights.translate / 100)
    $overall += ($summ * $weights.summarize / 100)
    $overall += ($echo * $weights.echo / 100)
    $overall += ($avail * $weights.avail / 100)
    $overall += ($latScore * $weights.lat / 100)

    return [ordered]@{
        model = $model
        math = [math]::Round($math,2)
        translate = [math]::Round($translate,2)
        summarize = [math]::Round($summ,2)
        echo = [math]::Round($echo,2)
        availability = [math]::Round($avail,2)
        latency_ms = $meanLat
        latency_score = $latScore
        overall = [math]::Round($overall,2)
        run_id = ($entries | Select-Object -First 1).run_id
    }
}

$results = @()
foreach ($m in $Models) {
    $res = Run-One $m
    if ($res -eq $null) { Write-Warning "No results for $m"; continue }
    $sc = Score-Model $m $res.entries
    $results += $sc
}

$report.models = $results

$jsonOut = ConvertTo-Json $report -Depth 10
$jsonPath = 'batch_report.json'
$txtPath = 'batch_report.txt'
$jsonOut | Out-File -FilePath $jsonPath -Encoding utf8

# Create a human-readable report
$sb = New-Object System.Text.StringBuilder
$sb.AppendLine("Batch Eval Report - " + $report.run_time) | Out-Null
$sb.AppendLine("Endpoint: $($report.endpoint)") | Out-Null
$sb.AppendLine('') | Out-Null
$sb.AppendLine('Per-model scores (1-100):') | Out-Null
$sorted = $results | Sort-Object -Property overall -Descending
foreach ($r in $sorted) {
    $sb.AppendLine("- $($r.model): Overall=$($r.overall) Math=$($r.math) Translate=$($r.translate) Summarize=$($r.summarize) Echo=$($r.echo) Availability=$($r.availability) Latency(ms)=$($r.latency_ms) LatScore=$($r.latency_score)") | Out-Null
}
$sb.AppendLine('') | Out-Null
$sb.AppendLine('Top 3 models:') | Out-Null
$top3 = $sorted | Select-Object -First 3
$i=1
foreach ($t in $top3) { $sb.AppendLine("$i. $($t.model) - Overall: $($t.overall)"); $i++ }

$sb.AppendLine('') | Out-Null
$sb.AppendLine('Recommendation: Use the top 3 models in ensemble or task-specific routing. See README for integration notes.') | Out-Null

$sb.ToString() | Out-File -FilePath $txtPath -Encoding utf8

Write-Output "Wrote batch JSON report to $jsonPath and text report to $txtPath"

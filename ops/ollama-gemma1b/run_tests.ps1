<#
Runs a set of lightweight and heavier prompt-style tests against the isolated Ollama HTTP API
and writes results to `test_results.json` in this folder.

Usage: from this folder run `./run_tests.ps1` (PowerShell)
#>

Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Path)

function Post-Completion($model, $bodyHashtable, $timeoutSec){
    $json = $bodyHashtable | ConvertTo-Json -Compress
    $uri = 'http://127.0.0.1:11436/v1/completions'
    $stop = [System.Diagnostics.Stopwatch]::StartNew()
    try{
        $resp = Invoke-RestMethod -Uri $uri -Method POST -ContentType 'application/json' -Body $json -TimeoutSec $timeoutSec
        $stop.Stop()
        return @{ success = $true; elapsed_ms = $stop.ElapsedMilliseconds; response = $resp }
    } catch {
        $stop.Stop()
        return @{ success = $false; elapsed_ms = $stop.ElapsedMilliseconds; error = $_.Exception.Message }
    }
}

$tests = @()

# Lightweight smoke tests (fast)
$tests += @{ name = '270m_prompt_smoke'; model = 'gemma3:270m'; body = @{ model = 'gemma3:270m'; prompt = "Write a one-line confirmation: gemma3:270m is alive"; max_tokens = 32 }; timeout = 60 }
$tests += @{ name = '270m_prompt_question'; model = 'gemma3:270m'; body = @{ model = 'gemma3:270m'; prompt = "What is 2+2? Answer succinctly."; max_tokens = 16 }; timeout = 30 }

# Heavier functional tests against gemma3:1b
$tests += @{ name = '1b_summary_long'; model = 'gemma3:1b'; body = @{ model = 'gemma3:1b'; prompt = "Summarize the following paragraph in two sentences: 'Artificial intelligence research has grown rapidly...'"; max_tokens = 150 }; timeout = 180 }
$tests += @{ name = '1b_coding_prompt'; model = 'gemma3:1b'; body = @{ model = 'gemma3:1b'; prompt = "Provide a short Python function that reverses words in a sentence."; max_tokens = 120 }; timeout = 180 }

$results = @()

Write-Output "Running $($tests.Count) tests against http://127.0.0.1:11436/v1/completions"
foreach($t in $tests){
    Write-Output "-- Test: $($t.name) (model: $($t.model))"
    $res = Post-Completion -model $t.model -bodyHashtable $t.body -timeoutSec $t.timeout
    $entry = @{ name = $t.name; model = $t.model; elapsed_ms = $res.elapsed_ms; timestamp = (Get-Date).ToString('o') }
    if($res.success){
        $entry.response = $res.response
        Write-Output "  -> success in $($res.elapsed_ms) ms"
        if($res.response.choices -and $res.response.choices.Count -gt 0){
            $sample = $res.response.choices[0].text
            Write-Output "     sample: $sample"
        }
    } else {
        $entry.error = $res.error
        Write-Warning "  -> failed after $($res.elapsed_ms) ms: $($res.error)"
    }
    $results += $entry
}

$outFile = Join-Path -Path (Get-Location) -ChildPath 'test_results.json'
$results | ConvertTo-Json -Depth 6 | Set-Content -Path $outFile -Encoding UTF8

Write-Output "All tests complete. Results written to: $outFile"
Write-Output "Summary:"
$results | ForEach-Object { Write-Output ("{0} : {1} ms - {2}" -f $_.name, $_.elapsed_ms, ($_.response.choices[0].text -replace "\r|\n"," ")) }

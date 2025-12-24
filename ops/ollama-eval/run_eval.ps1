param(
    [string[]] $Models,
    [string] $Endpoint = $null,
    [string] $ConfigPath = "eval_config.json",
    [string] $OutFile = "results.json",
    [double] $Temperature = $null
)

if (-not (Get-Command Invoke-RestMethod -ErrorAction SilentlyContinue)) {
    Write-Error "Invoke-RestMethod not available in this environment."
    exit 1
}

if (-not (Test-Path $ConfigPath)) {
    Write-Error "Config file '$ConfigPath' not found."
    exit 1
}

$cfg = Get-Content $ConfigPath -Raw | ConvertFrom-Json
if ($Endpoint -eq $null) { $Endpoint = $cfg.Endpoint }
if (-not $Models) { $Models = $cfg.Models }
$tests = $cfg.Tests
$timeout = [int]($cfg.TimeoutSec -as [int])
if ($timeout -le 0) { $timeout = 120 }

# --- Helper functions for lightweight automatic metrics ---
function Normalize-Text([string]$s) {
    if (-not $s) { return "" }
    $s = $s -replace "[\p{P}\p{S}]"," "
    $s = $s.ToLowerInvariant()
    $s = $s -replace "\s+"," "
    return $s.Trim()
}

function Tokenize([string]$s) {
    $n = Normalize-Text $s
    if ($n -eq "") { return @() }
    return $n.Split(' ')
}

function Overlap-F1($pred, $gold) {
    $pt = Tokenize $pred
    $gt = Tokenize $gold
    if ($pt.Count -eq 0 -and $gt.Count -eq 0) { return @{f1=1.0;prec=1.0;rec=1.0} }
    if ($pt.Count -eq 0 -or $gt.Count -eq 0) { return @{f1=0.0;prec=0.0;rec=0.0} }
    $common = @{}
    foreach ($t in $gt) { if ($common.ContainsKey($t)) { $common[$t] += 1 } else { $common[$t] = 1 } }
    $match = 0
    foreach ($t in $pt) {
        if ($common.ContainsKey($t) -and $common[$t] -gt 0) { $match += 1; $common[$t] -= 1 }
    }
    $prec = [double]$match / [double]$pt.Count
    $rec = [double]$match / [double]$gt.Count
    $f1 = 0.0
    if (($prec + $rec) -gt 0) { $f1 = 2 * $prec * $rec / ($prec + $rec) }
    return @{f1 = [math]::Round($f1,4); prec = [math]::Round($prec,4); rec = [math]::Round($rec,4) }
}

function Unigram-Precision($pred, $gold) {
    $pt = Tokenize $pred
    $gt = Tokenize $gold
    if ($pt.Count -eq 0) { return 0.0 }
    $common = @{ }
    foreach ($t in $gt) { if ($common.ContainsKey($t)) { $common[$t] += 1 } else { $common[$t] = 1 } }
    $match = 0
    foreach ($t in $pt) { if ($common.ContainsKey($t) -and $common[$t] -gt 0) { $match += 1; $common[$t] -= 1 } }
    return [math]::Round(([double]$match / [double]$pt.Count),4)
}

function Evaluate-Math-FromPrompt([string]$prompt) {
    # crude: find simple expression like 'A + B', 'A - B', 'A * B', 'A / B'
    if (-not $prompt) { return $null }
    $m = [regex]::Match($prompt, '(\d+)\s*([\+\-\*\/])\s*(\d+)')
    if ($m.Success) {
        $a = [double]$m.Groups[1].Value
        $op = $m.Groups[2].Value
        $b = [double]$m.Groups[3].Value
        switch ($op) {
            '+' { return ([math]::Round($a + $b,4)).ToString() }
            '-' { return ([math]::Round($a - $b,4)).ToString() }
            '*' { return ([math]::Round($a * $b,4)).ToString() }
            '/' { if ($b -ne 0) { return ([math]::Round($a / $b,4)).ToString() } else { return $null } }
        }
    }
    return $null
}

function Extract-NumberPreferLast([string]$text) {
    if (-not $text) { return $null }
    # Prefer explicit phrasing like 'is 22', 'equals 22', '=> 22', '-> 22'
    $patterns = @("is\s+(-?\d+(?:\.\d+)?)",
                  "equals\s+(-?\d+(?:\.\d+)?)",
                  "=>\s*(-?\d+(?:\.\d+)?)",
                  "->\s*(-?\d+(?:\.\d+)?)",
                  "answer\s+(?:is\s+)?(-?\d+(?:\.\d+)?)")
    foreach ($pat in $patterns) {
        $m = [regex]::Match($text, $pat, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
        if ($m.Success) { return $m.Groups[1].Value }
    }
    # If no explicit phrasing, prefer the last number found in the text (handles '... is 22.' and trailing numbers)
    $all = [regex]::Matches($text, '(-?\d+(?:\.\d+)?)') | ForEach-Object { $_.Groups[1].Value }
    if ($all.Count -gt 0) { return $all[$all.Count - 1] }
    return $null
}

$results = @()

# Check models available on the server
try {
    $modelsResp = Invoke-RestMethod -Method Get -Uri ($Endpoint.TrimEnd('/') + '/models') -TimeoutSec 10 -ErrorAction Stop
} catch {
    Write-Warning "Could not query models endpoint at $Endpoint. Ensure the Ollama instance is running and the Endpoint is correct."
    $modelsResp = $null
}

$available = @()
if ($modelsResp -ne $null -and $modelsResp.data) {
    foreach ($m in $modelsResp.data) { $available += $m.id }
}

foreach ($model in $Models) {
    $modelEntry = [ordered]@{
        model = $model
        available = ($available -contains $model)
        tests = @()
    }

    if (-not $modelEntry.available) {
        Write-Warning "Model '$model' not listed by the server. You may need to pull it on the Ollama instance before running full eval."
    }

    foreach ($t in $tests) {
        $testEntry = [ordered]@{
            id = $t.id
            prompt = $t.prompt
            max_tokens = $t.max_tokens
            success = $false
            elapsed_ms = $null
            response_text = $null
            finish_reason = $null
            raw = $null
            error = $null
        }

        try {
            $sw = [System.Diagnostics.Stopwatch]::StartNew()

            # Try multiple payload shapes to accommodate Ollama runner differences.
            $payloads = @()
                $base1 = @{ model = $model; prompt = $t.prompt; max_tokens = $t.max_tokens }
                if ($Temperature -ne $null) { $base1['temperature'] = $Temperature }
                $payloads += $base1

                $base2 = @{ model = $model; messages = @(@{ role = 'user'; content = $t.prompt }); max_tokens = $t.max_tokens }
                if ($Temperature -ne $null) { $base2['temperature'] = $Temperature }
                $payloads += $base2

                $base3 = @{ model = $model; input = $t.prompt; max_tokens = $t.max_tokens }
                if ($Temperature -ne $null) { $base3['temperature'] = $Temperature }
                $payloads += $base3

            $resp = $null
            $testEntry.attempts = @()
            $lastError = $null

            foreach ($p in $payloads) {
                $json = $p | ConvertTo-Json -Depth 12
                try {
                    $req = Invoke-WebRequest -Method Post -Uri ($Endpoint.TrimEnd('/') + '/completions') -Body $json -ContentType 'application/json' -TimeoutSec $timeout -ErrorAction Stop
                    $sw.Stop()
                    $testEntry.elapsed_ms = [int]$sw.Elapsed.TotalMilliseconds
                    $status = $req.StatusCode
                    $content = $req.Content
                    $fmt = ($p.Keys -join ',')
                    $testEntry.attempts += @{format=$fmt; status=$status; body=($content -as [string])}
                    if ($status -ge 200 -and $status -lt 300) {
                        try { $resp = $content | ConvertFrom-Json } catch { $resp = $content }
                        $testEntry.attempt_format = $fmt
                        $testEntry.raw_http_status = $status
                        $testEntry.raw_http_body = $content
                        break
                    }
                } catch {
                    # capture HTTP response body if available for debugging
                    $bodyText = $null
                    try {
                        if ($_.Exception.Response -ne $null) {
                            $stream = $_.Exception.Response.GetResponseStream()
                            if ($stream -ne $null) {
                                $sr = New-Object System.IO.StreamReader($stream)
                                $bodyText = $sr.ReadToEnd()
                            }
                        }
                    } catch { }
                    $fmt = ($p.Keys -join ',')
                    $testEntry.attempts += @{format=$fmt; error=$_.Exception.Message; body=($bodyText -as [string])}
                    $lastError = $_.Exception.Message
                    continue
                }
            }

            if ($null -eq $resp) {
                $sw.Stop()
                $testEntry.elapsed_ms = [int]$sw.Elapsed.TotalMilliseconds
                if ($lastError) { $testEntry.error = $lastError } else { $testEntry.error = 'no_response' }
            }

            # Parse response: accept multiple Ollama response shapes
            try {
                $testEntry.raw = $resp | ConvertTo-Json -Depth 8

                # 1) Standard OpenAI-like: choices[0].text
                if ($resp.choices -and $resp.choices.Count -gt 0) {
                    $c = $resp.choices[0]
                    if ($c.text) { $testEntry.response_text = $c.text }
                    if ($c.finish_reason) { $testEntry.finish_reason = $c.finish_reason }
                }

                # 2) Direct text field
                if (-not $testEntry.response_text -and $resp.text) { $testEntry.response_text = $resp.text }

                # 3) 'output' field (Ollama variations). Try nested content structures.
                if (-not $testEntry.response_text -and $resp.output) {
                    if ($resp.output -is [System.Collections.IEnumerable]) {
                        foreach ($o in $resp.output) {
                            if ($o.content) {
                                foreach ($content in $o.content) {
                                    if ($content.text) { $testEntry.response_text = $content.text; break }
                                    if ($content.message) { $testEntry.response_text = $content.message; break }
                                    if ($content.data -and $content.data.text) { $testEntry.response_text = $content.data.text; break }
                                }
                                if ($testEntry.response_text) { break }
                            } elseif ($o.text) {
                                $testEntry.response_text = $o.text; break
                            }
                        }
                    } else {
                        if ($resp.output.text) { $testEntry.response_text = $resp.output.text }
                    }
                }

                # 4) Sometimes the response is an array (legacy or other versions). Try first element.
                if (-not $testEntry.response_text -and $resp -is [System.Collections.IEnumerable]) {
                    try {
                        $first = $resp[0]
                        if ($first -and $first.text) { $testEntry.response_text = $first.text }
                        elseif ($first -and $first.output) { $testEntry.response_text = (ConvertTo-Json $first.output -Depth 6) }
                    } catch { }
                }

                # 5) Fallback: stringify output field so we at least capture something
                if (-not $testEntry.response_text -and $resp.output) { $testEntry.response_text = ($resp.output | ConvertTo-Json -Depth 6) }

                    if ($testEntry.response_text -and $testEntry.response_text.Trim().Length -gt 0) {
                        $testEntry.success = $true
                    } else {
                        if ($testEntry.finish_reason -eq 'load') {
                            $testEntry.error = 'model_loading'
                        } else {
                            $testEntry.error = 'empty_response'
                        }
                    }
            } catch {
                $testEntry.error = 'parse_error: ' + $_.Exception.Message
            }

            # --- simple automatic metrics ---
            $testEntry.score = $null
            $testEntry.metric_details = $null
            try {
                if ($t.expected) {
                    $expected = $t.expected
                    if ($t.id -like '*math*') {
                        $calc = Evaluate-Math-FromPrompt $t.prompt
                        if ($calc -ne $null) {
                            $ok = $false
                            if ($testEntry.response_text) {
                                # extract first numeric from response
                                $respNum = Extract-NumberPreferLast $testEntry.response_text
                                if ($respNum) {
                                    try {
                                        $r = [double]$respNum
                                        $e = [double]$calc
                                        if ([math]::Abs($r - $e) -lt 0.0001) { $ok = $true }
                                    } catch {
                                        if ($respNum -eq $calc -or $respNum -eq $t.expected) { $ok = $true }
                                    }
                                }
                            }
                            $testEntry.score = ($ok ? 1 : 0)
                            $detected = $null
                            $numMatch2 = Extract-NumberPreferLast $testEntry.response_text
                            if ($numMatch2) { $detected = $numMatch2 }
                            $testEntry.metric_details = @{expected=$calc; detected=($detected -as [string]) }
                        }
                    } else {
                        # token-overlap F1 for translation / summaries
                        if ($testEntry.response_text) {
                            # For short expected phrases, prefer exact normalized match as a strong signal
                            $normPred = Normalize-Text $testEntry.response_text
                            $normExp = Normalize-Text $expected
                            $exactMatch = $false
                            $predTokens = Tokenize $testEntry.response_text
                            $expTokens = Tokenize $expected
                            if ($expTokens.Count -le 3) {
                                if ($normPred -eq $normExp -or $normPred -like "* $normExp *" -or $normPred -like "$normExp *" -or $normPred -like "* $normExp") {
                                    $exactMatch = $true
                                }
                            }
                            $ov = Overlap-F1 $testEntry.response_text $expected
                            $bp = Unigram-Precision $testEntry.response_text $expected
                            if ($exactMatch) {
                                $testEntry.score = 1.0
                            } else {
                                $testEntry.score = $ov.f1
                            }
                            $testEntry.metric_details = $ov
                            $testEntry.metric_details.Add('bleu_1', $bp)
                            $testEntry.metric_details.Add('exact_normalized_match', $exactMatch)
                        }
                    }
                } else {
                    # If no explicit expected answer but the test looks like math, try to auto-evaluate
                    if ($t.id -like '*math*') {
                        $calc = Evaluate-Math-FromPrompt $t.prompt
                        if ($calc -ne $null -and $testEntry.response_text) {
                                $numMatch = [regex]::Match($testEntry.response_text, '(-?\d+(?:\.\d+)?)')
                                $ok = $false
                                if ($numMatch.Success) {
                                    try {
                                        $r = [double]$numMatch.Groups[1].Value
                                        $e = [double]$calc
                                        if ([math]::Abs($r - $e) -lt 0.0001) { $ok = $true }
                                    } catch {
                                        if ($numMatch.Groups[1].Value -eq $calc) { $ok = $true }
                                    }
                                }
                                $testEntry.score = ($ok ? 1 : 0)
                                $detected = $null
                                if ($numMatch -and $numMatch.Success) { $detected = $numMatch.Groups[1].Value }
                                $testEntry.metric_details = @{expected=$calc; detected=($detected -as [string])}
                        }
                    }
                }
            } catch {
                $testEntry.metric_details = 'metric_error: ' + $_.Exception.Message
            }
        } catch {
            $sw.Stop()
            $testEntry.elapsed_ms = [int]$sw.Elapsed.TotalMilliseconds
            $testEntry.error = $_.Exception.Message
        }

        $modelEntry.tests += $testEntry

        # Small pause between tests to avoid hammering resources
        Start-Sleep -Milliseconds 400
    }

    $results += $modelEntry
}

# Write results to JSON file
# Write results to JSON file
$results | ConvertTo-Json -Depth 8 | Out-File -FilePath $OutFile -Encoding utf8
Write-Output "Wrote results to $OutFile"

# Also append per-test score entries to a JSONL scores log for easy comparison over time
$outParent = Split-Path -Path $OutFile -Parent
if (-not $outParent -or $outParent -eq '') { $outParent = (Get-Location).Path }
$logPath = Join-Path -Path $outParent -ChildPath 'scores.log'
$runId = [guid]::NewGuid().ToString()
$now = (Get-Date).ToString('o')
foreach ($m in $results) {
    foreach ($t in $m.tests) {
        $entry = [ordered]@{
            run_id = $runId
            timestamp = $now
            model = $m.model
            available = $m.available
            test_id = $t.id
            score = $t.score
            success = $t.success
            elapsed_ms = $t.elapsed_ms
            raw_status = $t.raw_http_status
            attempt_format = $t.attempt_format
            metric_details = $t.metric_details
            error = $t.error
        }
        $jsonLine = $entry | ConvertTo-Json -Depth 10
        Add-Content -Path $logPath -Value $jsonLine -Encoding utf8
    }
}
Write-Output "Appended per-test scores to $logPath"
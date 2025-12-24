# Stability run: repeat evaluation for selected model+temp combos
param(
    [int] $Repeats = 3,
    [string[]] $Models = @('gemma3:1b','gemma3:270m','cogito:3b-v1-preview-llama-q4_K_M'),
    [double[]] $Temps = @(0.7, 0.0, 0.0),
    [string] $Endpoint = 'http://127.0.0.1:11436/v1',
    [int] $TimeoutSec = 300
)

Set-Location -Path (Split-Path -Path $MyInvocation.MyCommand.Path -Parent)

if ($Models.Count -ne $Temps.Count) { Write-Error "Models and Temps arrays must be same length"; exit 1 }

for ($i = 0; $i -lt $Models.Count; $i++) {
    $model = $Models[$i]
    $temp = $Temps[$i]
    for ($r = 1; $r -le $Repeats; $r++) {
        $safe = ($model -replace '[:/\\]','_')
        $tempSafe = if ($temp -ne $null) { $temp.ToString().Replace('.','_') } else { 'base' }
        $out = "results-${safe}-T${tempSafe}-r${r}.json"
        Write-Host "[Stability] Run $r/$Repeats for $model (temp=$temp) -> $out"
        & .\run_eval.ps1 -Models @($model) -Endpoint $Endpoint -OutFile $out -Temperature $temp -TimeoutSec $TimeoutSec
        Start-Sleep -Milliseconds 500
    }
}

Write-Host "Stability runs complete."
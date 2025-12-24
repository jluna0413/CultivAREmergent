# Temperature sweep runner for evaluator
param()

Set-Location -Path (Split-Path -Path $MyInvocation.MyCommand.Path -Parent)

$models = @(
    "granite4:micro-h",
    "gemma3:270m",
    "gemma3:1b",
    "gemma3:4b-it-q4_K_M",
    "qwen3:0.6b",
    "qwen3-vl:2b-thinking-q4_K_M",
    "qwen3-vl:2b-instruct-q4_K_M",
    "cogito:3b-v1-preview-llama-q4_K_M"
)
$temps = @(0.0, 0.7)

foreach ($temp in $temps) {
    foreach ($m in $models) {
        $safe = ($m -replace '[:/\\]','_')
        $tempSafe = $temp.ToString().Replace('.','_')
        $out = "results-$($safe)-T$($tempSafe).json"
        Write-Host "Running model $m at temperature $temp -> $out"
        & .\run_eval.ps1 -Models @($m) -Endpoint 'http://127.0.0.1:11436/v1' -OutFile $out -Temperature $temp -TimeoutSec 300
    }
}

Write-Host "Temperature sweep complete."
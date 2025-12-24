Ollama Evaluation Framework

Lightweight evaluation harness for quickly comparing models with minimal resource usage.

Location: `ops/ollama-eval`

How it works:
- Uses PowerShell `run_eval.ps1` to run a short set of prompt-style checks against each model.
- Default endpoint: `http://127.0.0.1:11436/v1` (override with `-Endpoint`).
- Writes results to `results.json` in the same folder.

Notes:
- If the model is not present on the Ollama instance, the script will warn and provide guidance to pull the model.
- The harness is intentionally lightweight (small prompts, short max tokens) to keep resource usage low.

Usage (PowerShell / pwsh):
```
Set-Location -Path "a:\dev\CultivAREmergant\ops\ollama-eval"
./run_eval.ps1 -Models @('granite4:micro-h') -Endpoint 'http://127.0.0.1:11436/v1'
```

Output:
- `results.json` containing per-model/per-test timing and outputs.

Next steps:
- Add model pull automation where appropriate (careful with large models).
- Add automated quality metrics (BLEU/ROUGE/embedding similarity) if desired.

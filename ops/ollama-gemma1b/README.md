# Isolated Ollama instance for gemma3:1b

This folder contains a Docker Compose service and helper scripts to run an isolated Ollama server that serves `gemma3:1b` on host port `11436`. This is intended for agents or workflows that need a dedicated Ollama instance so they won't interfere with other Ollama-based agents.

Quick start (requires Docker Desktop):

1. Open PowerShell in this folder:

```powershell
cd ops/ollama-gemma1b
./start.ps1
```

2. Verify models available:

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:11436/v1/models' -Method GET | ConvertTo-Json -Depth 5
```

3. If you need to pull a different model, run:

```powershell
docker exec -it ollama-gemma1b ollama pull <model:id>
```

Stop and remove the container:

```powershell
./stop.ps1
```

Notes
- Data (models, config) are persisted under `ops/ollama-gemma1b/data` on the host. You can inspect or back it up.
- The Compose service maps host port `11436` to the container's internal Ollama HTTP port `11434` (note: Ollama listens on `11434` inside the container).

Troubleshooting
- If `Invoke-RestMethod` to `http://127.0.0.1:11436/v1/models` returns an error or the service appears `unhealthy`:
	- Check container status: `docker compose ps`.
	- Inspect container logs: `docker compose logs --tail 200`.
	- If a model pull failed with a `digest mismatch` error, remove the possibly-corrupted blobs and re-pull the model:
		```powershell
		# Stop the service, remove corrupted blob files, then restart and re-pull
		docker compose down
		# inspect blobs under ./data/models/blobs; remove files whose sha256 digest differs from the manifest
		# (example) Remove a problematic blob file and then restart/pull:
		Remove-Item .\data\models\blobs\sha256-<bad-digest>
		docker compose up -d
		docker compose exec -T ollama-gemma1b /usr/bin/ollama pull gemma3:1b
		```
	- If the HTTP models endpoint still doesn't respond but the container is `Up`, check which internal port Ollama is listening on (logs will show `Listening on [::]:11434`). If logs indicate a different internal port, update `docker-compose.yml` mapping and healthcheck accordingly.

Usage reminder
- Agents should use the MCP entry `task-master-ai-gemma1b` (set to `http://127.0.0.1:11436/v1` + `MODEL=gemma3:1b`) to target this instance.

Warm-up recommendation
- To get consistent prompt-style responses and avoid `finish_reason: "load"` during the first message-style call, use the prompt field for quick checks or warm the model after startup. The `start.ps1` script now includes an optional warm-up routine.

How to run with warm-up
- Default (no warm-up flag):
	```powershell
	./start.ps1
	```
- Pull & warm the default heavy model (`gemma3:1b`) and also pull the small `gemma3:270m` for quick warmups:
	```powershell
	./start.ps1 -Warmup270m
	```

Implementation note
- The warm-up sends a short `prompt`-style completion request to `http://127.0.0.1:11436/v1/completions` with a 120s timeout, which helps load model weights and improves the chance that subsequent message-style requests return generated text rather than `load`.

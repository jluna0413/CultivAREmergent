Handoff for gemini-cli — continue frontend/backend login debug

Summary

- Backend:
  - Restored FastAPI app at `A:\dev\CultivAREmergant\app\fastapi_app` (merged to `main`).
  - `create_app()` factory added; env guards `FASTAPI_SKIP_ROUTERS` and `FASTAPI_CREATE_AT_IMPORT`.
  - Sandbox copy at `A:\Experiment\CultivAR` with `run_dev_for_agent.ps1` (sets PYTHONPATH to repo).
  - Uvicorn sandbox normally runs at http://127.0.0.1:5002.
  - Some routers are currently skipped due to missing modules (e.g., ModuleNotFoundError: `app.models_async.auth`).

- Frontend:
  - Built Flutter web bundle at `A:\dev\CultivAREmergant\flutter_app\build\web`.
  - `main.dart.js` is the primary artifact to inspect for API endpoints.
  - Frontend served (quick static serve) on http://127.0.0.1:8080.

Problem

- Browser login returns: "Login Failed ApiException Login failed: null".
- Goal: determine the exact API endpoint the frontend calls for login, reproduce the request, capture backend response and uvicorn stack trace, and propose/fix root cause.

Files to inspect

- `A:\dev\CultivAREmergant\app\fastapi_app\__init__.py` (app factory)
- `A:\dev\CultivAREmergant\app\fastapi_app\main.py`
- `A:\dev\CultivAREmergant\app\fastapi_app\routers\*`
- `A:\dev\CultivAREmergant\flutter_app\build\web\main.dart.js`
- Sandbox run script: `A:\Experiment\CultivAR\run_dev_for_agent.ps1`
- Smoke test: `A:\dev\CultivAREmergant\tests\test_fastapi_import.py`

Immediate steps for gemini-cli (copy/paste-execute in PowerShell)

1) Extract candidate endpoints from the built JS:

powershell -NoProfile -Command "Get-Content -Raw 'A:\\dev\\CultivAREmergant\\flutter_app\\build\\web\\main.dart.js' | Select-String -Pattern 'https?://[^\"\'\s]+' -AllMatches | ForEach-Object { $_.Matches } | Sort-Object Value -Unique"

2) Search for /api, auth, login tokens:

powershell -NoProfile -Command "Get-Content -Raw 'A:\\dev\\CultivAREmergant\\flutter_app\\build\\web\\main.dart.js' | Select-String -Pattern '/api[\\w/\\.\\-]*|/auth[\\w/\\.\\-]*|api/login|login' -AllMatches | ForEach-Object { \"Line:$($_.LineNumber) -> $($_.Line.Trim())\" }"

3) Start backend (if not running) with required env:

Set-Item Env:SECRET_KEY 'dev-secret-for-local'
Set-Item Env:ALLOWED_HOSTS '127.0.0.1,localhost'
Set-Item Env:FASTAPI_SKIP_ROUTERS '0'
$env:PYTHONPATH='A:\\dev\\CultivAREmergant'
uvicorn app.fastapi_app:create_app --factory --reload --port 5002

4) Serve frontend (if not running):

python -m http.server 8080 --directory 'A:\\dev\\CultivAREmergant\\flutter_app\\build\\web'

5) Reproduce the login POST (replace path if main.dart.js indicates another endpoint):

$body = @{ email='admin@cultivar.com'; password='admin123' } | ConvertTo-Json
Invoke-RestMethod -Uri 'http://127.0.0.1:5002/api/login' -Method Post -Body $body -ContentType 'application/json' -Verbose

6) If you get an error from the backend: copy the uvicorn stdout/stderr where the server is running (it will show the traceback). If routers didn't register, check the uvicorn startup logs for ModuleNotFoundError and install dependencies from `requirements*.txt`.

Acceptance criteria for handoff task

- Exact login API path & host discovered (from `main.dart.js`)
- Reproduction of failing POST: response status and body
- Corresponding backend log/trace for the request
- Suggested next fix (config dependency or code patch) or a simple patch with tests if straightforward

Notes and assumptions

- The sandbox backend port is 5002. The frontend is served on 8080. Adjust ports if `main.dart.js` references a different host or port.
- The build `main.dart.js` is minified/compiled Dart JS, so string literals might be obfuscated; searching for 'Auth', 'Login', '/api' and http(s) URLs is the most reliable initial approach.
- Some routers depend on async models (`app.models_async.auth`) which are not present in the current environment; installing dependencies from `requirements*.txt` and setting `SECRET_KEY` and DB environment will be necessary for full router availability.

Contact & provenance

- Created by the local agent during recovery of the FastAPI app and early sandbox runs. The repository root is `A:\dev\CultivAREmergant`.
- Related todo entry: agent-managed todo list item ID 13 (status: in-progress).

--

If you want, the agent can also commit this file to a short-lived branch and push it. To add & push now from PowerShell:

```powershell
git checkout -b handoff/gemini-cli
git add HANDOFF_TO_GEMINI.md
git commit -m "chore: add handoff for gemini-cli to continue frontend/backend debug"
git push -u origin HEAD
```

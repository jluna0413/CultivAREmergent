- [ ] Implement unit tests for the cannabis API mapper
  - Task: Create unit tests for the cannabis API mapper
  - Status: Pending
  - Next Task: Create unit tests for the cannabis API mapper

## FastAPI Docker workflow (current default)

- Start the stack with:

  ```powershell
  docker compose -f docker-compose.fastapi.yml up --build
  ```

- This launches Uvicorn on <http://localhost:8000>; update `backend_test.py`'s `base_url`
  to `http://localhost:8000` (or whichever explicit host:port you are using) before running
  the smoke checks so the tests hit the FastAPI instance.

Note: FastAPI is now the default runtime. Flask is only available for legacy validation via
`docker-compose.dual.yml` and the dedicated `run_flask.py` script.